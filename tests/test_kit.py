"""Sürücü (kos.py) ve bekçi katman A — sahte motor, sahte repo, git yok, para yok.

python3 -m unittest discover -s tests
"""
import io
import json
import os
import shutil
import sys
import tempfile
import time
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest import mock

KOK = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(KOK / "bin"))
import ayar  # noqa: E402
import bekci  # noqa: E402
import dongu  # noqa: E402
import kapi  # noqa: E402
import kos  # noqa: E402
from test_sema import RAPOR, SOZLESME, TESLIM  # noqa: E402

TAKIMLAR = ("sistem-sevk", "sistem-insaat", "sistem-bekci")


def sahte_kok(tmp):
    """Gerçek takım dosyalarının kopyası + şemalar + SoT; kosu/ boş."""
    kok = Path(tmp) / "kok"
    for ad in TAKIMLAR:
        hedef = kok / "takimlar" / ad
        shutil.copytree(KOK / "takimlar" / ad, hedef, ignore=shutil.ignore_patterns("kosu", ".bekci-deneme"))
        (hedef / "kosu").mkdir()
    shutil.copytree(KOK / "sema", kok / "sema")
    for ad in ("ANAYASA.md", "hedef.md", "kararlar.md", "kapsam-disi.md"):
        shutil.copy(KOK / ad, kok / ad)
    (kok / "sirket").mkdir()
    shutil.copy(KOK / "sirket" / "AJAN-KIMLIGI.md", kok / "sirket" / "AJAN-KIMLIGI.md")
    (kok / "bin").mkdir()
    shutil.copy(KOK / "bin" / "kapi.py", kok / "bin" / "kapi.py")
    (kok / "increment").mkdir()
    return kok


class SahteMotor:
    """subprocess.run yerine geçer: çağrılan motorun adını ve istemi kaydeder, hazır çıktıyı döner."""

    def __init__(self, yanit, kayit_yaz=True, dokun=None):
        self.yanit, self.kayit_yaz, self.dokun, self.cagrilar = yanit, kayit_yaz, dokun or [], []

    def __call__(self, komut, cwd=None, env=None, **_):
        self.cagrilar.append({"motor": komut[0], "istem": komut[2] if len(komut) > 2 else "", "env": env})
        if self.kayit_yaz:
            Path(env["SIRKET_KOSU"]).write_text("# Koşu\n\nokudum, ürettim.\n", encoding="utf-8")
        for yol in self.dokun:
            p = Path(cwd) / yol
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text("dokunuldu\n", encoding="utf-8")
        cikti = json.dumps({"is_error": False, "total_cost_usd": 0.1, "num_turns": 2,
                            "result": json.dumps(self.yanit, ensure_ascii=False)})
        return mock.Mock(stdout=cikti, stderr="", returncode=0)


class KosTemeli(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.kok = sahte_kok(self.tmp.name)
        self.yamalar = [mock.patch.object(kos, "KOK", self.kok), mock.patch.object(ayar, "KOK", self.kok),
                        mock.patch.object(bekci, "KOK", self.kok),
                        mock.patch.object(kos.agents_uret, "uret", lambda *a, **k: []),
                        mock.patch.dict(os.environ, {"VARSAYILAN_MOTOR": ""})]
        for y in self.yamalar:
            y.start()
        self.git_yollari = set()  # koşu SONRASI görülecek değişiklikler; ilk çağrı (öncesi) hep boş
        self.git_cagri = 0

        def sahte_git(kok=None):
            self.git_cagri += 1
            return set() if self.git_cagri == 1 else set(self.git_yollari)
        self.git_yamasi = mock.patch.object(kos, "git_degisenler", sahte_git)
        self.git_yamasi.start()

    def tearDown(self):
        self.git_yamasi.stop()
        for y in self.yamalar:
            y.stop()
        self.tmp.cleanup()

    def _kos(self, takim, motor, **kw):
        with mock.patch.object(kos.subprocess, "run", motor), redirect_stdout(io.StringIO()) as cikti:
            kos.kos(takim, **kw)
        return cikti.getvalue()

    def _talep_ve_onay(self, motor=None):
        kapi.talep("kapi.py durum evreyi bassın", self.kok)
        id_ = ayar.evre_oku(self.kok)["increment_id"]
        klasor = ayar.increment_klasoru(id_, self.kok)
        (klasor / "sozlesme.json").write_text(json.dumps({**SOZLESME, "increment_id": id_}), encoding="utf-8")
        ayar.evre_guncelle({"bekleyen_onay": "sozlesme"}, "sahte sevk", self.kok)
        self.assertEqual(kapi.onayla(motor, self.kok)[0], 0)
        return id_, klasor


class EvreVeMotor(KosTemeli):
    def test_yanlis_evrede_kosu_atlanir(self):
        m = SahteMotor({})
        cikti = self._kos("sistem-insaat", m)
        self.assertEqual(m.cagrilar, [], "motor çağrılmamalı")
        self.assertIn("atlandı", cikti)
        self.assertEqual(ayar.durum_oku("sistem-insaat", self.kok)["son_sonuc"], "atlandi")
        self.assertIn("evre uyuşmuyor", ayar.durum_oku("sistem-insaat", self.kok)["son_sebep"])

    def test_motor_belirle_uc_yol(self):
        evre = {"motor": {"insaat": "grok", "bekci": "claude"}}
        self.assertEqual(kos.motor_belirle({"motor": "claude"}, evre), "claude")
        self.assertEqual(kos.motor_belirle({"motor": "sozlesme"}, evre), "grok")
        self.assertEqual(kos.motor_belirle({"motor": "ters"}, evre), "claude")
        self.assertIsNone(kos.motor_belirle({"motor": "sozlesme"}, {"motor": {"insaat": None, "bekci": None}}))
        self.assertIsNone(kos.motor_belirle({"motor": "gpt"}, evre))
        self.assertEqual(kos.motor_belirle({}, evre), "claude")

    def test_kuru_kosu_hicbir_sey_yazmaz(self):
        kapi.talep("x", self.kok)
        m = SahteMotor({})
        cikti = self._kos("sistem-sevk", m, kuru=True)
        self.assertEqual(m.cagrilar, [])
        self.assertIn("KOŞAR", cikti)
        self.assertIn("increment-sozlesmesi", cikti)
        self.assertEqual(list((self.kok / "takimlar" / "sistem-sevk" / "kosu").iterdir()), [])

    def test_tavan_kontrolu(self):
        bugun = time.strftime("%Y-%m-%d")
        kosu = self.kok / "takimlar" / "sistem-sevk" / "kosu"
        for i in range(ayar.GUNLUK_KOSU_TAVANI):
            (kosu / f"{bugun}-{i:04d}.md").write_text("- maliyet: 0.5 USD\n", encoding="utf-8")
        self.assertIn("koşu tavanı", kos.tavan_kontrol(self.kok, "sistem-sevk"))
        self.assertIsNone(kos.tavan_kontrol(self.kok, "sistem-insaat"))
        (kosu / f"{bugun}-0000.md").write_text("- maliyet: 99 USD\n", encoding="utf-8")
        self.assertIn("maliyet tavanı", kos.tavan_kontrol(self.kok, "sistem-insaat"))


class Kapsam(unittest.TestCase):
    def test_izinli_ve_sapma(self):
        evre = {"increment_id": "inc-001"}
        soz = {"dokunulacak_yollar": ["bin/kapi.py"], "yeni_dosyalar": ["docs/yeni.md"]}
        izinli = kos.izinli_yollar("sistem-insaat", evre, soz)
        sonrasi = {"bin/kapi.py", "docs/yeni.md", "takimlar/sistem-insaat/defter.md",
                   "increment/inc-001/park.md", "ANAYASA.md", "bin/kos.py"}
        self.assertEqual(kos.kapsam_sapmasi({"bin/kos.py"}, sonrasi, izinli), ["ANAYASA.md"])
        izinli_sevk = kos.izinli_yollar("sistem-sevk", evre, soz)
        self.assertIn("bin/kapi.py", kos.kapsam_sapmasi(set(), sonrasi, izinli_sevk),
                      "sevk sözleşme yollarına bile yazamaz")


class UctanUca(KosTemeli):
    """talep → sevk → onayla → inşaat → bekçi → yayinla, sahte motorla."""

    def test_sevk_taslagi_surucu_yazar_ve_kapi1_bekler(self):
        kapi.talep("kapi.py durum evreyi bassın", self.kok)
        m = SahteMotor({**SOZLESME, "increment_id": "inc-001"})
        cikti = self._kos("sistem-sevk", m)
        self.assertEqual(m.cagrilar[0]["motor"], "claude")
        self.assertIn("sema/increment-sozlesmesi.schema.json", m.cagrilar[0]["istem"])
        self.assertEqual(m.cagrilar[0]["env"]["SIRKET_TAKIM"], "sistem-sevk")
        self.assertIn("tamam", cikti)
        taslak = json.loads((self.kok / "increment" / "inc-001" / "sozlesme.json").read_text(encoding="utf-8"))
        self.assertEqual(taslak["hedef_davranis"], SOZLESME["hedef_davranis"])
        self.assertEqual(ayar.evre_oku(self.kok)["bekleyen_onay"], "sozlesme")
        self.assertEqual(ayar.durum_oku("sistem-sevk", self.kok)["son_sonuc"], "tamam")

    def test_gecersiz_yapisal_evreyi_ilerletmez(self):
        kapi.talep("x", self.kok)
        m = SahteMotor({"increment_id": "inc-001", "hedef_davranis": "eksik alanlar"})
        self._kos("sistem-sevk", m)
        self.assertIsNone(ayar.evre_oku(self.kok)["bekleyen_onay"])
        self.assertEqual(ayar.durum_oku("sistem-sevk", self.kok)["son_sonuc"], "gecersiz")

    def test_yanlis_increment_id_gecersiz(self):
        kapi.talep("x", self.kok)
        self._kos("sistem-sevk", SahteMotor({**SOZLESME, "increment_id": "inc-999"}))
        self.assertIn("increment_id", ayar.durum_oku("sistem-sevk", self.kok)["son_sebep"])

    def test_insaat_sozlesme_motoruyla_kosar_ve_sapmayi_olcer(self):
        id_, klasor = self._talep_ve_onay("grok")
        m = SahteMotor({**TESLIM, "increment_id": id_, "motor": "grok"})
        self.git_yollari = {"bin/kapi.py", "bin/kos.py"}  # kos.py sözleşmede yok → sapma
        self._kos("sistem-insaat", m)
        self.assertEqual(m.cagrilar[0]["motor"], "grok")
        self.assertIn("sozlesme.onayli.json", m.cagrilar[0]["istem"])
        evre = ayar.evre_oku(self.kok)
        self.assertEqual(evre["evre"], "bekci")
        self.assertEqual(evre["kapsam_sapmasi"], ["bin/kos.py"])
        self.assertTrue((klasor / "teslim.json").exists())
        kayit = next((self.kok / "takimlar" / "sistem-insaat" / "kosu").glob("*.md")).read_text(encoding="utf-8")
        self.assertIn("kapsam sapması: bin/kos.py", kayit)
        self.assertNotIn("araç kısıtı", kayit)  # grok araç kısıtı destekler → uyarı satırı yok
        self.assertNotIn("motor raporlamıyor", kayit)  # grok maliyet raporlar (total_cost_usd)

    def test_sevk_kapsam_disina_yazarsa_red(self):
        kapi.talep("x", self.kok)
        self.git_yollari = {"bin/kos.py"}
        self._kos("sistem-sevk", SahteMotor({**SOZLESME, "increment_id": "inc-001"}))
        self.assertEqual(ayar.durum_oku("sistem-sevk", self.kok)["son_sonuc"], "red")
        self.assertIsNone(ayar.evre_oku(self.kok)["bekleyen_onay"])

    def test_bekci_ters_motorla_pass_ve_fail(self):
        id_, klasor = self._talep_ve_onay()  # codex → bekçi claude
        ayar.evre_guncelle({"evre": "bekci"}, "sahte inşaat", self.kok)
        m = SahteMotor({**RAPOR, "increment_id": id_, "motor": "claude"})
        self._kos("sistem-bekci", m)
        self.assertEqual(m.cagrilar[0]["motor"], "claude")
        evre = ayar.evre_oku(self.kok)
        self.assertEqual((evre["evre"], evre["bekleyen_onay"]), ("yayin-bekliyor", "yayin"))
        self.assertEqual(kapi.yayinla(self.kok)[0], 0)
        self.assertEqual(ayar.evre_oku(self.kok)["evre"], "yayinlandi")

    def test_bekci_fail(self):
        id_, _ = self._talep_ve_onay()
        ayar.evre_guncelle({"evre": "bekci"}, "sahte inşaat", self.kok)
        self._kos("sistem-bekci", SahteMotor({**RAPOR, "increment_id": id_, "motor": "claude", "karar": "FAIL"}))
        self.assertEqual(ayar.evre_oku(self.kok)["evre"], "fail")
        self.assertEqual(kapi.yayinla(self.kok)[0], 1)

    def test_bekci_raporunda_yanlis_motor_gecersiz(self):
        id_, _ = self._talep_ve_onay()
        ayar.evre_guncelle({"evre": "bekci"}, "sahte inşaat", self.kok)
        self._kos("sistem-bekci", SahteMotor({**RAPOR, "increment_id": id_, "motor": "codex"}))
        self.assertEqual(ayar.evre_oku(self.kok)["evre"], "bekci")
        self.assertIn("bekçi motoru", ayar.durum_oku("sistem-bekci", self.kok)["son_sebep"])

    def test_kayit_yazmayan_kosu_hata(self):
        kapi.talep("x", self.kok)
        self._kos("sistem-sevk", SahteMotor({**SOZLESME, "increment_id": "inc-001"}, kayit_yaz=False))
        self.assertEqual(ayar.durum_oku("sistem-sevk", self.kok)["son_sonuc"], "hata")
        kayit = next((self.kok / "takimlar" / "sistem-sevk" / "kosu").glob("*.md")).read_text(encoding="utf-8")
        self.assertIn("koşu kaydı yazmadı", kayit)


class BekciKatmanA(KosTemeli):
    def test_bos_kayit_ve_gizli_veri(self):
        kosu = self.kok / "takimlar" / "sistem-sevk" / "kosu" / "k.md"
        kosu.write_text("", encoding="utf-8")
        self.assertEqual(bekci.karar_ver(self.kok, kosu)["karar"], "red")
        kosu.write_text("anahtar sk-ant-abcdefgh12345\n", encoding="utf-8")
        k = bekci.karar_ver(self.kok, kosu)
        self.assertEqual(k["karar"], "red")
        self.assertIn("gizli veri", k["gerekce"])
        kosu.write_text("temiz kayıt\n", encoding="utf-8")
        self.assertEqual(bekci.karar_ver(self.kok, kosu)["karar"], "kabul")

    def test_korunan_dosyaya_dokunma(self):
        kosu = self.kok / "takimlar" / "sistem-sevk" / "kosu" / "k.md"
        kosu.write_text("temiz\n", encoding="utf-8")
        baslangic = time.time()
        self.assertEqual(bekci.karar_ver(self.kok, kosu, baslangic)["karar"], "kabul")
        time.sleep(0.01)
        (self.kok / "ANAYASA.md").write_text("# değişti\n", encoding="utf-8")
        k = bekci.karar_ver(self.kok, kosu, baslangic)
        self.assertEqual(k["karar"], "red")
        self.assertIn("ANAYASA.md", k["gerekce"])

    def test_kosuda_anayasaya_dokunan_ajan_red(self):
        kapi.talep("x", self.kok)
        m = SahteMotor({**SOZLESME, "increment_id": "inc-001"}, dokun=["kararlar.md"])
        self._kos("sistem-sevk", m)
        self.assertEqual(ayar.durum_oku("sistem-sevk", self.kok)["son_sonuc"], "red")
        self.assertIn("kararlar.md", ayar.durum_oku("sistem-sevk", self.kok)["bekci"]["gerekce"])

    def test_hook_engelleme_en_fazla_iki(self):
        kosu = self.kok / "takimlar" / "sistem-sevk" / "kosu" / "k.md"
        kosu.write_text("", encoding="utf-8")
        self.assertTrue(bekci.engelle_mi(self.kok, "sistem-sevk", kosu))
        self.assertFalse(bekci.engelle_mi(self.kok, "sistem-sevk", kosu), "ikinci red'de bırakır")


if __name__ == "__main__":
    unittest.main()


class SiraliMotor:
    """Ardışık koşulara sırayla farklı yanıt verir (sevk → inşaat → bekçi …)."""

    def __init__(self, yanitlar):
        self.yanitlar, self.cagrilar = list(yanitlar), []

    def __call__(self, komut, cwd=None, env=None, **_):
        self.cagrilar.append((env["SIRKET_TAKIM"], komut[0]))
        yanit = self.yanitlar.pop(0) if self.yanitlar else {}
        Path(env["SIRKET_KOSU"]).write_text("# Koşu\n\nokudum, ürettim.\n", encoding="utf-8")
        metin = json.dumps(yanit, ensure_ascii=False)
        if komut[0] == "codex":  # her motor kendi biçiminde cevap verir
            cikti = "\n".join(json.dumps(o) for o in [
                {"type": "thread.started", "thread_id": "t1"},
                {"type": "item.completed", "item": {"type": "agent_message", "text": metin}},
                {"type": "turn.completed"}])
        elif komut[0] == "agy":
            cikti = json.dumps({"status": "SUCCESS", "num_turns": 1, "response": metin, "structured_output": yanit})
        else:  # claude ve grok
            cikti = json.dumps({"is_error": False, "total_cost_usd": 0.1, "num_turns": 1, "result": metin, "text": metin})
        return mock.Mock(stdout=cikti, stderr="", returncode=0)


class Dongu(KosTemeli):
    def _dongu(self, motor, **kw):
        with mock.patch.object(kos.subprocess, "run", motor), redirect_stdout(io.StringIO()) as cikti:
            kod = dongu.dongu(kok=self.kok, **kw)
        return kod, cikti.getvalue()

    def test_talepten_pass_a_kadar_tek_komut(self):
        m = SiraliMotor([{**SOZLESME, "increment_id": "inc-001"},
                         {**TESLIM, "increment_id": "inc-001", "motor": "codex"},
                         {**RAPOR, "increment_id": "inc-001", "motor": "claude"}])
        kod, cikti = self._dongu(m, talep="kapi.py durum evreyi bassın")
        self.assertEqual(kod, 0, cikti)
        self.assertEqual([c[0] for c in m.cagrilar], ["sistem-sevk", "sistem-insaat", "sistem-bekci"])
        self.assertEqual([c[1] for c in m.cagrilar], ["claude", "codex", "claude"])
        evre = ayar.evre_oku(self.kok)
        self.assertEqual((evre["evre"], evre["bekleyen_onay"]), ("yayin-bekliyor", "yayin"))
        self.assertIn("İNSAN KARARI", cikti)
        self.assertEqual(kapi.yayinla(self.kok)[0], 0)

    def test_fail_sonrasi_yeniden_dener_sonra_durur(self):
        fail = {**RAPOR, "increment_id": "inc-001", "motor": "claude", "karar": "FAIL"}
        teslim = {**TESLIM, "increment_id": "inc-001", "motor": "codex"}
        m = SiraliMotor([{**SOZLESME, "increment_id": "inc-001"}, teslim, fail, teslim, fail, teslim,
                         {**RAPOR, "increment_id": "inc-001", "motor": "claude"}])
        kod, cikti = self._dongu(m, talep="x", maks_deneme=2)
        self.assertEqual(kod, 0, cikti)
        self.assertEqual(ayar.evre_oku(self.kok)["deneme"], 2)
        self.assertEqual(sum(1 for c in m.cagrilar if c[0] == "sistem-insaat"), 3)

    def test_deneme_tavaninda_insana_birakir(self):
        fail = {**RAPOR, "increment_id": "inc-001", "motor": "claude", "karar": "FAIL"}
        teslim = {**TESLIM, "increment_id": "inc-001", "motor": "codex"}
        m = SiraliMotor([{**SOZLESME, "increment_id": "inc-001"}, teslim, fail, teslim, fail])
        kod, cikti = self._dongu(m, talep="x", maks_deneme=1)
        self.assertEqual(kod, 1)
        self.assertEqual(ayar.evre_oku(self.kok)["evre"], "fail")
        self.assertIn("İNSAN KARARI", cikti)
        self.assertEqual(kapi.revize("daralt", self.kok)[0], 0)
        self.assertEqual(ayar.evre_oku(self.kok)["evre"], "sozlesme")

    def test_sevk_sozlesme_uretmezse_durur(self):
        m = SiraliMotor([{"increment_id": "inc-001", "hedef_davranis": "eksik"}])
        kod, cikti = self._dongu(m, talep="x")
        self.assertEqual(kod, 1)
        self.assertEqual(len(m.cagrilar), 1)
        self.assertIn("sevk sözleşme üretmedi", cikti)

    def test_insaat_istemi_fail_raporunu_gosterir(self):
        kapi.talep("x", self.kok)
        evre = ayar.evre_guncelle({"evre": "insaat", "deneme": 1, "motor": {"insaat": "codex", "bekci": "claude"}}, "t", self.kok)
        fm = ayar.takim_bilgisi("sistem-insaat", self.kok)
        metin = kos.istem("sistem-insaat", fm, self.kok / "k.md", "z", evre, self.kok)
        self.assertIn("2. deneme", metin)
        self.assertIn("bekci-raporu.json", metin)
        evre = ayar.evre_guncelle({"evre": "sozlesme", "revizyon": [{"zaman": "t", "not": "CSS de olsun"}]}, "r", self.kok)
        metin = kos.istem("sistem-sevk", ayar.takim_bilgisi("sistem-sevk", self.kok), self.kok / "k.md", "z", evre, self.kok)
        self.assertIn("REVİZE NOTU", metin)
        self.assertIn("CSS de olsun", metin)
