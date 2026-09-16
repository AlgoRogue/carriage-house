"""Karttaki Motor'u Sürücü callable'ına çeviren fabrika."""
import json
import shutil
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from tests.surucu_yolu import HataKosucu, PERSONEL
from kart_motoru import motor_uret
from surucu_cekirdek import Sinyal


CLAUDE_BASARI = json.dumps({
    "is_error": False,
    "total_cost_usd": 0.1,
    "num_turns": 1,
    "result": "ok",
})
BASARI_STDOUT = {
    "claude": CLAUDE_BASARI,
    "agy": json.dumps({"status": "SUCCESS", "num_turns": 1, "response": "ok"}),
    "codex": "\n".join((
        json.dumps({"type": "thread.started", "thread_id": "t1"}),
        json.dumps({"type": "item.completed",
                    "item": {"type": "agent_message", "text": "ok"}}),
        json.dumps({"type": "turn.completed"}),
    )),
    "grok": json.dumps({"text": "ok", "num_turns": 1}),
}
HATA_STDOUT = {
    "claude": json.dumps({"is_error": True, "result": "x"}),
    "agy": json.dumps({"status": "ERROR", "response": ""}),
    "codex": json.dumps({"type": "error"}),
    "grok": json.dumps({"error": "kota"}),
}
BOZUK_STDOUT = "bu json değil"
KAYITLI_CLILER = ("claude", "agy", "codex", "grok")


class SahteKosucu:
    """Komut listesini kaydeder, hazır stdout döner. CLI açmaz."""

    def __init__(self, stdout=""):
        self.stdout = stdout
        self.cagrilar = []

    def __call__(self, komut):
        self.cagrilar.append(list(komut))
        return self.stdout


def kart_yaz(dizin, *, cli="claude", model="sonnet", skilller=None,
             motor="__varsayilan__", arka_yuz=True):
    yol = Path(dizin) / "kart.json"
    yol.parent.mkdir(parents=True, exist_ok=True)
    belge = {
        "personel_numarasi": "CH-0001",
        "on_yuz": {
            "tur": "ajan",
            "ad": "Cengizhan",
            "referans_gorsel": None,
            "birim": "İnşaat",
            "rol": "İnşaat mühendisi",
        },
    }
    if arka_yuz is True:
        if motor == "__varsayilan__":
            motor = {"cli": cli, "model": model}
        belge["arka_yuz"] = {
            "skilller": list(skilller) if skilller is not None else ["is-parcalama"],
            "motor": motor,
        }
    elif arka_yuz is not False:
        belge["arka_yuz"] = arka_yuz
    yol.write_text(json.dumps(belge, ensure_ascii=False, indent=2) + "\n",
                   encoding="utf-8")
    return yol


class KartMotoruFabrikaTesti(unittest.TestCase):
    def setUp(self):
        self.gecici = tempfile.TemporaryDirectory()
        self.addCleanup(self.gecici.cleanup)
        self.kart = Path(self.gecici.name) / "kart.json"
        shutil.copyfile(PERSONEL / "kart.json", self.kart)
        self.kart_once = self.kart.read_bytes()
        self.prod_kart_once = (PERSONEL / "kart.json").read_bytes()

    def tearDown(self):
        self.assertEqual(self.kart.read_bytes(), self.kart_once)
        self.assertEqual((PERSONEL / "kart.json").read_bytes(),
                         self.prod_kart_once)

    def test_claude_sonnet_basari_stdout_basari_verir(self):
        kosucu = SahteKosucu(CLAUDE_BASARI)
        with patch("subprocess.run", side_effect=AssertionError("subprocess.run")), \
             patch("subprocess.Popen", side_effect=AssertionError("subprocess.Popen")):
            motor = motor_uret(self.kart, kosucu)
            sinyal, metin = motor("planlaniyor")

        self.assertTrue(callable(motor))
        self.assertEqual(sinyal, Sinyal.BASARI)
        self.assertEqual(sinyal, "basari")
        self.assertEqual(metin, "ok")
        self.assertEqual(len(kosucu.cagrilar), 1)
        komut = kosucu.cagrilar[0]
        self.assertEqual(komut[0], "claude")
        self.assertIn("sonnet", komut)
        self.assertIn("planlaniyor", komut)


class KayitliMotorVeBozukKartTesti(unittest.TestCase):
    def setUp(self):
        self.gecici = tempfile.TemporaryDirectory()
        self.addCleanup(self.gecici.cleanup)
        self.dizin = Path(self.gecici.name)
        self.prod_kart_once = (PERSONEL / "kart.json").read_bytes()

    def tearDown(self):
        self.assertEqual((PERSONEL / "kart.json").read_bytes(),
                         self.prod_kart_once)

    def test_kayitli_cli_komutun_ilk_tokeni_ve_sinyal_eslemesi(self):
        for cli in KAYITLI_CLILER:
            with self.subTest(cli=cli, stdout="basari"):
                kosucu = SahteKosucu(BASARI_STDOUT[cli])
                kart = kart_yaz(self.dizin / cli / "basari",
                                cli=cli, model="deneme-model")
                motor = motor_uret(kart, kosucu)
                sinyal, _metin = motor("planlaniyor")
                self.assertEqual(sinyal, Sinyal.BASARI)
                self.assertEqual(kosucu.cagrilar[0][0], cli)
                self.assertIn("deneme-model", kosucu.cagrilar[0])
            with self.subTest(cli=cli, stdout="hata"):
                kosucu = SahteKosucu(HATA_STDOUT[cli])
                kart = kart_yaz(self.dizin / cli / "hata",
                                cli=cli, model="deneme-model")
                sinyal, _metin = motor_uret(kart, kosucu)("planlaniyor")
                self.assertEqual(sinyal, Sinyal.HATA)
            with self.subTest(cli=cli, stdout="bozuk"):
                kosucu = SahteKosucu(BOZUK_STDOUT)
                kart = kart_yaz(self.dizin / cli / "bozuk",
                                cli=cli, model="deneme-model")
                sinyal, _metin = motor_uret(kart, kosucu)("planlaniyor")
                self.assertEqual(sinyal, Sinyal.HATA)

    def test_bilinmeyen_cli_kosucu_cagrilmadan_basarisiz_olur(self):
        kosucu = SahteKosucu(CLAUDE_BASARI)
        kart = kart_yaz(self.dizin, cli="bilinmeyen", model="sonnet")
        with self.assertRaises(ValueError):
            motor_uret(kart, kosucu)
        self.assertEqual(kosucu.cagrilar, [])

    def test_eksik_veya_bozuk_motor_alani_kosucu_cagrilmadan_basarisiz_olur(self):
        vakalar = [
            ("arka_yuz_yok", dict(arka_yuz=False)),
            ("motor_yok", dict(arka_yuz={"skilller": []})),
            ("motor_none", dict(motor=None)),
            ("cli_yok", dict(motor={"model": "sonnet"})),
            ("cli_bos", dict(cli="", model="sonnet")),
        ]
        for ad, kwargs in vakalar:
            with self.subTest(ad=ad):
                kosucu = SahteKosucu(CLAUDE_BASARI)
                kart = kart_yaz(self.dizin / ad, **kwargs)
                with self.assertRaises(ValueError):
                    motor_uret(kart, kosucu)
                self.assertEqual(kosucu.cagrilar, [])

    def test_claude_araclari_salt_okuma_ile_sinirli(self):
        kosucu = SahteKosucu(CLAUDE_BASARI)
        kart = kart_yaz(self.dizin, cli="claude", model="sonnet")
        motor_uret(kart, kosucu)("planlaniyor")
        komut = kosucu.cagrilar[0]
        self.assertIn("--allowedTools", komut)
        araclar = komut[komut.index("--allowedTools") + 1]
        self.assertEqual(araclar, "Read")
        self.assertNotIn("Write", araclar.split(","))

    def test_skill_listesi_komuta_etki_etmez(self):
        kosucu = SahteKosucu(CLAUDE_BASARI)
        kart = kart_yaz(self.dizin, cli="claude", model="sonnet",
                        skilller=["olmayan-skill", "baska-skill"])
        motor_uret(kart, kosucu)("planlaniyor")
        komut = kosucu.cagrilar[0]
        self.assertEqual(komut[0], "claude")
        self.assertIn("sonnet", komut)
        self.assertNotIn("olmayan-skill", komut)
        self.assertNotIn("baska-skill", komut)

    def test_bos_liste_ve_json_dizi_attributeerror_kacmaz_hata_sinyali_doner(self):
        # Debt 05 / Ticket 04: Sahte koşucu [] veya "[]" döndüğünde
        # Claude/agy/codex cozumle'sinden AttributeError kaçmamalı; Sinyal.HATA dönmeli.
        for cli in KAYITLI_CLILER:
            for bozuk_cikti in ([], "[]"):
                with self.subTest(cli=cli, cikti=bozuk_cikti):
                    kosucu = SahteKosucu(bozuk_cikti)
                    kart = kart_yaz(self.dizin / cli / f"dizi_{type(bozuk_cikti).__name__}",
                                    cli=cli, model="deneme-model")
                    motor = motor_uret(kart, kosucu)
                    sinyal, _metin = motor("planlaniyor")
                    self.assertEqual(sinyal, Sinyal.HATA)

    def test_kosucu_oserror_hata_sinyali_doner(self):
        kart = kart_yaz(self.dizin / "oserror", cli="claude", model="sonnet")
        motor = motor_uret(kart, HataKosucu())
        sinyal, metin = motor("planlaniyor")
        self.assertEqual(sinyal, Sinyal.HATA)
        self.assertEqual(metin, "")


if __name__ == "__main__":
    unittest.main()
