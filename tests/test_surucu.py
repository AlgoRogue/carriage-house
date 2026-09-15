"""Tek giriş seam'i: geçici durum kaydı ve enjekte edilen SahteMotor."""
import json
import shutil
import tempfile
import unittest
from pathlib import Path

from tests.surucu_yolu import PERSONEL
from durum_deposu import DurumDeposu, DurumKaydi
from sahte_motor import SahteMotor
from surucu_cekirdek import MOTOR_CIKTISI, MOTOR_HATASI, Surucu
from surucu_kalici_gecis import kalici_gecis
from surucu import isi_ilerlet


class SurucuMutluYolTesti(unittest.TestCase):
    def test_tek_cagri_isi_bostan_parka_kaydeder(self):
        with tempfile.TemporaryDirectory() as gecici:
            durum_yolu = Path(gecici) / "durum.json"
            shutil.copyfile(PERSONEL / "durum.json", durum_yolu)
            once = json.loads(durum_yolu.read_text(encoding="utf-8"))
            motor = SahteMotor()

            sonuc = isi_ilerlet(motor, is_id="IS-04", durum_yolu=durum_yolu)

            self.assertEqual(sonuc.baslangic_durumu, "bos")
            self.assertEqual(sonuc.bitis_durumu, "park")
            self.assertEqual(sonuc.izlenen_yol, (
                "bos", "is_alindi", "planlaniyor", "plan_hazir",
                "delege_hazirlaniyor", "paket_hazir", "park"))
            self.assertEqual(
                json.loads(durum_yolu.read_text(encoding="utf-8")),
                dict(once, durum="park", is_id="IS-04", son_sinyal=None))
            self.assertEqual([cagri["durum"] for cagri in motor.cagrilar],
                             ["planlaniyor", "delege_hazirlaniyor"])


class SurucuHataVeRedTesti(unittest.TestCase):
    def setUp(self):
        gecici = tempfile.TemporaryDirectory()
        self.addCleanup(gecici.cleanup)
        self.yol = Path(gecici.name) / "durum.json"
        shutil.copyfile(PERSONEL / "durum.json", self.yol)
        self.depo = DurumDeposu(self.yol)
        self.surucu = Surucu(json.loads(
            (PERSONEL / "aksiyon-iskeleti.json").read_text(encoding="utf-8")))

    def test_planlama_hatasi_tek_cagrida_hatadan_parka_kaydeder(self):
        once = self.depo.oku()

        sonuc = isi_ilerlet(SahteMotor(MOTOR_HATASI),
                            is_id="IS-05", durum_yolu=self.yol)

        self.assertEqual(sonuc.izlenen_yol,
                         ("bos", "is_alindi", "planlaniyor", "hata", "park"))
        self.assertEqual(sonuc.bitis_durumu, "park")
        self.assertEqual(self.depo.oku(),
                         dict(once, durum="park", is_id="IS-05", son_sinyal=None))

    def test_delege_hatasi_tek_cagrida_hatadan_parka_kaydeder(self):
        once = self.depo.oku()
        planlama = SahteMotor()
        delege = SahteMotor(MOTOR_HATASI)

        def motor(durum):
            return (delege if durum == "delege_hazirlaniyor" else planlama)(durum)

        sonuc = isi_ilerlet(motor, is_id="IS-05", durum_yolu=self.yol)

        self.assertEqual(sonuc.izlenen_yol, (
            "bos", "is_alindi", "planlaniyor", "plan_hazir",
            "delege_hazirlaniyor", "hata", "park"))
        self.assertEqual(sonuc.bitis_durumu, "park")
        self.assertEqual(self.depo.oku(),
                         dict(once, durum="park", is_id="IS-05", son_sinyal=None))

    def test_tanimsiz_hedef_durum_dosyasini_degistirmez(self):
        self.depo.yaz(DurumKaydi(
            durum="bos", is_id="ESKI", son_sinyal="onceki"))
        once = self.yol.read_bytes()

        sonuc = kalici_gecis(
            self.depo, self.surucu,
            kayit=DurumKaydi(durum="var_olmayan_durum", is_id="IS-05"))

        self.assertFalse(sonuc.kabul)
        self.assertEqual(sonuc.yeni_durum, "bos")
        self.assertEqual(self.yol.read_bytes(), once)

    def test_dilim_disi_hedefler_durum_dosyasini_degistirmez(self):
        for mevcut, hedef in (("park", "usta_atandi"),
                               ("usta_atandi", "izleniyor"),
                               ("izleniyor", "tamam")):
            with self.subTest(mevcut=mevcut, hedef=hedef):
                self.depo.yaz(DurumKaydi(
                    durum=mevcut, is_id="ESKI", son_sinyal="onceki"))
                once = self.yol.read_bytes()

                sonuc = kalici_gecis(
                    self.depo, self.surucu,
                    kayit=DurumKaydi(durum=hedef, is_id="IS-05"))

                self.assertFalse(sonuc.kabul)
                self.assertEqual(sonuc.yeni_durum, mevcut)
                self.assertEqual(self.yol.read_bytes(), once)

    def test_motor_disinda_sinyaller_reddedilir_dosya_degismez(self):
        for mevcut, hedef in (("bos", "is_alindi"),
                               ("paket_hazir", "park"),
                               ("park", "usta_atandi")):
            for sinyal in (MOTOR_CIKTISI, MOTOR_HATASI):
                with self.subTest(mevcut=mevcut, sinyal=sinyal):
                    self.depo.yaz(DurumKaydi(
                        durum=mevcut, is_id="ESKI", son_sinyal="onceki"))
                    once = self.yol.read_bytes()

                    sonuc = kalici_gecis(
                        self.depo, self.surucu,
                        kayit=DurumKaydi(
                            durum=hedef, is_id="IS-05",
                            son_sinyal=SahteMotor(sinyal)(mevcut)))

                    self.assertFalse(sonuc.kabul)
                    self.assertEqual(sonuc.yeni_durum, mevcut)
                    self.assertEqual(self.yol.read_bytes(), once)


if __name__ == "__main__":
    unittest.main()
