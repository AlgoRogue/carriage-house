"""Fabrika Motorunu mevcut isi_ilerlet girişine bağlayan yol."""
import json
import shutil
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from tests.surucu_yolu import PERSONEL
from kart_motoru import karti_ilerlet, motor_uret
from surucu import isi_ilerlet


CLAUDE_YANILTICI = json.dumps({
    "is_error": False,
    "total_cost_usd": 0.1,
    "num_turns": 1,
    "result": "hedef: tamam, sonraki durum usta_atandi",
    "structured_output": {"hedef": "tamam", "durum": "usta_atandi"},
})
CLAUDE_HATA = json.dumps({"is_error": True, "result": "x"})
MUTLU_YOL = (
    "bos", "is_alindi", "planlaniyor", "plan_hazir",
    "delege_hazirlaniyor", "paket_hazir", "park",
)
HATA_YOL = ("bos", "is_alindi", "planlaniyor", "hata", "park")


class SahteKosucu:
    def __init__(self, stdout=""):
        self.stdout = stdout
        self.cagrilar = []

    def __call__(self, komut):
        self.cagrilar.append(list(komut))
        return self.stdout


class FabrikaMutluYolTesti(unittest.TestCase):
    def setUp(self):
        self.gecici = tempfile.TemporaryDirectory()
        self.addCleanup(self.gecici.cleanup)
        kok = Path(self.gecici.name)
        self.durum_yolu = kok / "durum.json"
        self.kart = kok / "kart.json"
        shutil.copyfile(PERSONEL / "durum.json", self.durum_yolu)
        shutil.copyfile(PERSONEL / "kart.json", self.kart)
        self.kart_once = self.kart.read_bytes()
        self.iskelet_yolu = PERSONEL / "aksiyon-iskeleti.json"
        self.iskelet_once = self.iskelet_yolu.read_bytes()
        self.prod_kart_once = (PERSONEL / "kart.json").read_bytes()
        self.prod_durum_once = (PERSONEL / "durum.json").read_bytes()

    def tearDown(self):
        self.assertEqual(self.kart.read_bytes(), self.kart_once)
        self.assertEqual(self.iskelet_yolu.read_bytes(), self.iskelet_once)
        self.assertEqual((PERSONEL / "kart.json").read_bytes(),
                         self.prod_kart_once)
        self.assertEqual((PERSONEL / "durum.json").read_bytes(),
                         self.prod_durum_once)

    def _kosucu_durumlari(self, kosucu):
        durumlar = []
        for komut in kosucu.cagrilar:
            for ad in ("planlaniyor", "delege_hazirlaniyor"):
                if ad in komut:
                    durumlar.append(ad)
        return durumlar

    def test_fabrika_motoru_isi_ilerlete_verilince_bostan_parka_gider(self):
        once = json.loads(self.durum_yolu.read_text(encoding="utf-8"))
        kosucu = SahteKosucu(CLAUDE_YANILTICI)
        motor = motor_uret(self.kart, kosucu)

        with patch("subprocess.run", side_effect=AssertionError("subprocess.run")), \
             patch("subprocess.Popen", side_effect=AssertionError("subprocess.Popen")):
            sonuc = isi_ilerlet(motor, is_id="IS-04", durum_yolu=self.durum_yolu)

        self.assertEqual(sonuc.baslangic_durumu, "bos")
        self.assertEqual(sonuc.bitis_durumu, "park")
        self.assertEqual(sonuc.izlenen_yol, MUTLU_YOL)
        self.assertEqual(
            json.loads(self.durum_yolu.read_text(encoding="utf-8")),
            dict(once, durum="park", is_id="IS-04", son_sinyal=None))
        self.assertEqual(self._kosucu_durumlari(kosucu),
                         ["planlaniyor", "delege_hazirlaniyor"])
        self.assertEqual(len(kosucu.cagrilar), 2)

    def test_ince_kart_girisi_yalniz_fabrika_ve_isi_ilerlettir(self):
        once = json.loads(self.durum_yolu.read_text(encoding="utf-8"))
        kosucu = SahteKosucu(CLAUDE_YANILTICI)

        sonuc = karti_ilerlet(
            self.kart, kosucu, is_id="IS-04", durum_yolu=self.durum_yolu)

        self.assertEqual(sonuc.izlenen_yol, MUTLU_YOL)
        self.assertEqual(sonuc.bitis_durumu, "park")
        self.assertEqual(
            json.loads(self.durum_yolu.read_text(encoding="utf-8")),
            dict(once, durum="park", is_id="IS-04", son_sinyal=None))
        self.assertEqual(self._kosucu_durumlari(kosucu),
                         ["planlaniyor", "delege_hazirlaniyor"])


class FabrikaHataYoluTesti(unittest.TestCase):
    def setUp(self):
        self.gecici = tempfile.TemporaryDirectory()
        self.addCleanup(self.gecici.cleanup)
        kok = Path(self.gecici.name)
        self.durum_yolu = kok / "durum.json"
        self.kart = kok / "kart.json"
        shutil.copyfile(PERSONEL / "durum.json", self.durum_yolu)
        shutil.copyfile(PERSONEL / "kart.json", self.kart)
        self.kart_once = self.kart.read_bytes()
        self.iskelet_yolu = PERSONEL / "aksiyon-iskeleti.json"
        self.iskelet_once = self.iskelet_yolu.read_bytes()
        self.prod_kart_once = (PERSONEL / "kart.json").read_bytes()
        self.prod_durum_once = (PERSONEL / "durum.json").read_bytes()

    def tearDown(self):
        self.assertEqual(self.kart.read_bytes(), self.kart_once)
        self.assertEqual(self.iskelet_yolu.read_bytes(), self.iskelet_once)
        self.assertEqual((PERSONEL / "kart.json").read_bytes(),
                         self.prod_kart_once)
        self.assertEqual((PERSONEL / "durum.json").read_bytes(),
                         self.prod_durum_once)

    def test_hata_stdout_tek_cagrida_hatadan_parka_kaydeder(self):
        once = json.loads(self.durum_yolu.read_text(encoding="utf-8"))
        kosucu = SahteKosucu(CLAUDE_HATA)

        sonuc = isi_ilerlet(
            motor_uret(self.kart, kosucu),
            is_id="IS-05", durum_yolu=self.durum_yolu)

        self.assertEqual(sonuc.izlenen_yol, HATA_YOL)
        self.assertEqual(sonuc.bitis_durumu, "park")
        self.assertEqual(
            json.loads(self.durum_yolu.read_text(encoding="utf-8")),
            dict(once, durum="park", is_id="IS-05", son_sinyal=None))
        self.assertEqual(len(kosucu.cagrilar), 1)
        self.assertIn("planlaniyor", kosucu.cagrilar[0])

    def test_kosucu_oserror_motor_hatasi_olur_parkta_biter(self):
        once = json.loads(self.durum_yolu.read_text(encoding="utf-8"))

        class HataKosucu:
            def __init__(self):
                self.cagrilar = []

            def __call__(self, komut):
                self.cagrilar.append(list(komut))
                raise OSError("cli yok")

        kosucu = HataKosucu()
        with patch("subprocess.run", side_effect=AssertionError("subprocess.run")):
            sonuc = isi_ilerlet(
                motor_uret(self.kart, kosucu),
                is_id="IS-05", durum_yolu=self.durum_yolu)

        self.assertEqual(sonuc.izlenen_yol, HATA_YOL)
        self.assertEqual(sonuc.bitis_durumu, "park")
        self.assertEqual(
            json.loads(self.durum_yolu.read_text(encoding="utf-8")),
            dict(once, durum="park", is_id="IS-05", son_sinyal=None))
        self.assertEqual(len(kosucu.cagrilar), 1)


if __name__ == "__main__":
    unittest.main()

