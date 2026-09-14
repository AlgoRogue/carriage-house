"""İnsan kapıları — talep → onayla → (sahte teslim/rapor) → yayinla; yanlış evrede red. LLM yok."""
import json
import os
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

KOK = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(KOK / "bin"))
import ayar  # noqa: E402
import kapi  # noqa: E402
from test_sema import RAPOR, SOZLESME  # noqa: E402


def sahte_kok(tmp):
    kok = Path(tmp) / "kok"
    (kok / "takimlar" / "sistem-sevk" / "kosu").mkdir(parents=True)
    (kok / "takimlar" / "sistem-sevk" / "durum.json").write_text(
        json.dumps({"takim": "sistem-sevk", "kuyruk": [], "bekci": {}}), encoding="utf-8")
    shutil.copytree(KOK / "sema", kok / "sema")
    (kok / "kararlar.md").write_text("# Kararlar\n", encoding="utf-8")
    (kok / "increment").mkdir()
    return kok


class KapiAkisi(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.kok = sahte_kok(self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()

    def _taslak_yaz(self, veri=SOZLESME):
        id_ = ayar.evre_oku(self.kok)["increment_id"]
        klasor = ayar.increment_klasoru(id_, self.kok)
        (klasor / "sozlesme.json").write_text(json.dumps({**veri, "increment_id": id_}), encoding="utf-8")
        ayar.evre_guncelle({"bekleyen_onay": "sozlesme"}, "sahte sevk", self.kok)
        return id_, klasor

    def test_talep_evre_acar_ve_kuyruga_yazar(self):
        kod, mesaj = kapi.talep("kapi.py durum evreyi bassın", self.kok)
        self.assertEqual(kod, 0, mesaj)
        evre = ayar.evre_oku(self.kok)
        self.assertEqual((evre["increment_id"], evre["evre"], evre["bekleyen_onay"]), ("inc-001", "sozlesme", None))
        kuyruk = ayar.durum_oku("sistem-sevk", self.kok)["kuyruk"]
        self.assertEqual(kuyruk[0]["id"], "inc-001")
        self.assertTrue((self.kok / "increment" / "inc-001").is_dir())
        self.assertEqual(kapi.talep("ikinci", self.kok)[0], 1, "açık increment varken ikinci talep açılmaz")
        self.assertEqual(kapi.talep("   ", self.kok)[0], 1)

    def test_onayla_yalniz_bekleyen_sozlesmeyle(self):
        self.assertEqual(kapi.onayla(None, self.kok)[0], 1)
        kapi.talep("x", self.kok)
        self.assertEqual(kapi.onayla(None, self.kok)[0], 1, "taslak yokken onay yok")
        id_, klasor = self._taslak_yaz()
        kod, mesaj = kapi.onayla(None, self.kok)
        self.assertEqual(kod, 0, mesaj)
        evre = ayar.evre_oku(self.kok)
        self.assertEqual(evre["evre"], "insaat")
        self.assertEqual(evre["motor"], {"insaat": "codex", "bekci": "claude"})
        onayli = klasor / "sozlesme.onayli.json"
        self.assertTrue(onayli.exists())
        self.assertEqual(onayli.stat().st_mode & 0o777, 0o444)
        self.assertTrue(any("KAPI 1" in g["olay"] for g in evre["gecmis"]))

    def test_onayla_motor_secimi_ve_ters_bekci(self):
        kapi.talep("x", self.kok)
        self._taslak_yaz()
        kod, _ = kapi.onayla("claude", self.kok)
        self.assertEqual(kod, 0)
        self.assertEqual(ayar.evre_oku(self.kok)["motor"], {"insaat": "claude", "bekci": "grok"})

    def test_onayla_gecersiz_taslagi_reddeder(self):
        kapi.talep("x", self.kok)
        self._taslak_yaz({**SOZLESME, "motor_adayi": "gpt"})
        kod, mesaj = kapi.onayla(None, self.kok)
        self.assertEqual(kod, 1)
        self.assertIn("şemaya uymuyor", mesaj)
        self.assertEqual(ayar.evre_oku(self.kok)["evre"], "sozlesme")

    def test_yayinla_yalniz_pass_sonrasi(self):
        kapi.talep("x", self.kok)
        id_, klasor = self._taslak_yaz()
        kapi.onayla(None, self.kok)
        self.assertEqual(kapi.yayinla(self.kok)[0], 1, "insaat evresinde yayın yok")
        (klasor / "bekci-raporu.json").write_text(json.dumps({**RAPOR, "increment_id": id_}), encoding="utf-8")
        ayar.evre_guncelle({"evre": "yayin-bekliyor", "bekleyen_onay": "yayin"}, "sahte bekçi PASS", self.kok)
        kod, mesaj = kapi.yayinla(self.kok)
        self.assertEqual(kod, 0, mesaj)
        self.assertEqual(ayar.evre_oku(self.kok)["evre"], "yayinlandi")
        kararlar = (self.kok / "kararlar.md").read_text(encoding="utf-8")
        self.assertIn(id_, kararlar)
        self.assertIn(SOZLESME["yayin_anlami"], kararlar)
        self.assertEqual(ayar.durum_oku("sistem-sevk", self.kok)["kuyruk"][0]["durum"], "tamam")
        self.assertEqual(kapi.talep("sıradaki", self.kok)[0], 0, "yayından sonra yeni talep açılır")
        self.assertEqual(ayar.evre_oku(self.kok)["increment_id"], "inc-002")

    def test_yayinla_fail_raporunu_reddeder(self):
        kapi.talep("x", self.kok)
        id_, klasor = self._taslak_yaz()
        kapi.onayla(None, self.kok)
        (klasor / "bekci-raporu.json").write_text(json.dumps({**RAPOR, "increment_id": id_, "karar": "FAIL"}),
                                                   encoding="utf-8")
        ayar.evre_guncelle({"evre": "yayin-bekliyor", "bekleyen_onay": "yayin"}, "tutarsız", self.kok)
        self.assertEqual(kapi.yayinla(self.kok)[0], 1)

    def test_red_her_evrede_kapatir(self):
        self.assertEqual(kapi.red("boş", self.kok)[0], 1)
        kapi.talep("x", self.kok)
        kod, _ = kapi.red("yanlış increment", self.kok)
        self.assertEqual(kod, 0)
        evre = ayar.evre_oku(self.kok)
        self.assertEqual(evre["evre"], "red")
        self.assertEqual(ayar.durum_oku("sistem-sevk", self.kok)["son_red"]["sebep"], "yanlış increment")
        self.assertEqual(ayar.durum_oku("sistem-sevk", self.kok)["kuyruk"][0]["durum"], "red")

    def test_durum_siradaki_adimi_soyler(self):
        self.assertIn("kapi.py talep", kapi.durum(self.kok)[1])
        kapi.talep("x", self.kok)
        self.assertIn("kos.py sistem-sevk", kapi.durum(self.kok)[1])
        self._taslak_yaz()
        self.assertIn("kapi.py onayla", kapi.durum(self.kok)[1])
        kapi.onayla(None, self.kok)
        self.assertIn("kos.py sistem-insaat", kapi.durum(self.kok)[1])

    def test_evre_dosyasi_semaya_uyar(self):
        import sema
        kapi.talep("x", self.kok)
        self._taslak_yaz()
        kapi.onayla("grok", self.kok)
        veri = json.loads(ayar.evre_yolu(self.kok).read_text(encoding="utf-8"))
        self.assertEqual(sema.dogrula(sema.yukle("evre", KOK), veri), [])


if __name__ == "__main__":
    unittest.main()
