"""Tek giriş seam'i: geçici durum kaydı, geçici İş artefaktı kökü, SahteMotor."""
import json
import shutil
import tempfile
import unittest
from pathlib import Path

from tests.surucu_yolu import PERSONEL
from durum_deposu import DurumDeposu, DurumKaydi
from sahte_motor import SahteMotor
from surucu_cekirdek import BASARI, HATA, Surucu
from surucu_kalici_gecis import kalici_gecis
from surucu import isi_ilerlet


class SurucuMutluYolTesti(unittest.TestCase):
    def test_tek_cagri_isi_bostan_parka_kaydeder(self):
        with tempfile.TemporaryDirectory() as gecici:
            durum_yolu = Path(gecici) / "durum.json"
            isler_kok = Path(gecici) / "isler"
            shutil.copyfile(PERSONEL / "durum.json", durum_yolu)
            once = json.loads(durum_yolu.read_text(encoding="utf-8"))
            motor = SahteMotor(metin="plan içeriği")

            sonuc = isi_ilerlet(motor, is_id="IS-04", durum_yolu=durum_yolu,
                                isler_kok=isler_kok)

            self.assertEqual(sonuc.baslangic_durumu, "bos")
            self.assertEqual(sonuc.bitis_durumu, "park")
            self.assertEqual(sonuc.izlenen_yol, (
                "bos", "is_alindi", "planlaniyor", "plan_hazir",
                "delege_hazirlaniyor", "paket_hazir", "park"))
            self.assertEqual(
                json.loads(durum_yolu.read_text(encoding="utf-8")),
                dict(once, durum="park", is_id="IS-04", son_sinyal=None))

            # Motor'a giden girdi durum adının kendisi değil; doldurulmuş şablon.
            self.assertEqual(len(motor.cagrilar), 2)
            plan_girdisi = motor.cagrilar[0]["durum"]
            delege_girdisi = motor.cagrilar[1]["durum"]
            self.assertNotEqual(plan_girdisi, "planlaniyor")
            self.assertNotEqual(delege_girdisi, "delege_hazirlaniyor")
            self.assertIn(str(isler_kok / "IS-04" / "plan.md"), plan_girdisi)
            self.assertIn(str(isler_kok / "IS-04" / "plan.md"), delege_girdisi)
            self.assertIn(str(isler_kok / "IS-04" / "paket.md"), delege_girdisi)
            self.assertNotIn("plan içeriği", delege_girdisi)

            # İş artefaktı S2/S4: Sürücü metni artefakt olarak yazar.
            self.assertEqual(
                (isler_kok / "IS-04" / "plan.md").read_text(encoding="utf-8"),
                "plan içeriği")
            self.assertEqual(
                (isler_kok / "IS-04" / "paket.md").read_text(encoding="utf-8"),
                "plan içeriği")

    def test_kabul_edilebilir_serbest_metin_semasiz_bostan_parka_gider(self):
        with tempfile.TemporaryDirectory() as gecici:
            durum_yolu = Path(gecici) / "durum.json"
            isler_kok = Path(gecici) / "isler"
            shutil.copyfile(PERSONEL / "durum.json", durum_yolu)
            # Şema aramayan, serbest UTF-8 metin (Türkçe karakterler, özel simgeler)
            serbest_metin = "# Başlık: Özel Plan 🚀\n\n- Adım 1: Türkçe karakterler: çğışöü ÇĞİŞÖÜ\n"
            motor = SahteMotor(metin=serbest_metin)

            sonuc = isi_ilerlet(motor, is_id="IS-UTF8", durum_yolu=durum_yolu,
                                isler_kok=isler_kok)

            self.assertEqual(sonuc.baslangic_durumu, "bos")
            self.assertEqual(sonuc.bitis_durumu, "park")
            self.assertEqual(sonuc.izlenen_yol, (
                "bos", "is_alindi", "planlaniyor", "plan_hazir",
                "delege_hazirlaniyor", "paket_hazir", "park"))
            self.assertEqual(
                (isler_kok / "IS-UTF8" / "plan.md").read_text(encoding="utf-8"),
                serbest_metin)
            self.assertEqual(
                (isler_kok / "IS-UTF8" / "paket.md").read_text(encoding="utf-8"),
                serbest_metin)


class SurucuHataVeRedTesti(unittest.TestCase):
    def setUp(self):
        gecici = tempfile.TemporaryDirectory()
        self.addCleanup(gecici.cleanup)
        self.yol = Path(gecici.name) / "durum.json"
        self.isler_kok = Path(gecici.name) / "isler"
        shutil.copyfile(PERSONEL / "durum.json", self.yol)
        self.depo = DurumDeposu(self.yol)
        self.surucu = Surucu(json.loads(
            (PERSONEL / "aksiyon-iskeleti.json").read_text(encoding="utf-8")))

    def test_planlama_hatasi_tek_cagrida_hatadan_parka_kaydeder(self):
        once = self.depo.oku()

        sonuc = isi_ilerlet(SahteMotor(HATA), is_id="IS-05",
                            durum_yolu=self.yol, isler_kok=self.isler_kok)

        self.assertEqual(sonuc.izlenen_yol,
                         ("bos", "is_alindi", "planlaniyor", "hata", "park"))
        self.assertEqual(sonuc.bitis_durumu, "park")
        self.assertEqual(self.depo.oku(),
                         dict(once, durum="park", is_id="IS-05", son_sinyal=None))
        self.assertFalse((self.isler_kok / "IS-05").exists())

    def test_delege_hatasi_tek_cagrida_hatadan_parka_kaydeder(self):
        once = self.depo.oku()
        planlama = SahteMotor(metin="plan içeriği")
        delege = SahteMotor(HATA)

        def motor(girdi):
            return (delege if "paket.md" in girdi else planlama)(girdi)

        sonuc = isi_ilerlet(motor, is_id="IS-05", durum_yolu=self.yol,
                            isler_kok=self.isler_kok)

        self.assertEqual(sonuc.izlenen_yol, (
            "bos", "is_alindi", "planlaniyor", "plan_hazir",
            "delege_hazirlaniyor", "hata", "park"))
        self.assertEqual(sonuc.bitis_durumu, "park")
        self.assertEqual(self.depo.oku(),
                         dict(once, durum="park", is_id="IS-05", son_sinyal=None))

    def test_basari_bos_artefaktta_ilerlemez_motor_durumunda_kalir(self):
        once = self.depo.oku()

        sonuc = isi_ilerlet(SahteMotor(metin=""), is_id="IS-06",
                            durum_yolu=self.yol, isler_kok=self.isler_kok)

        self.assertEqual(sonuc.izlenen_yol, ("bos", "is_alindi", "planlaniyor"))
        self.assertEqual(sonuc.bitis_durumu, "planlaniyor")
        self.assertEqual(self.depo.oku(),
                         dict(once, durum="planlaniyor", is_id="IS-06", son_sinyal=None))
        self.assertFalse((self.isler_kok / "IS-06" / "plan.md").exists())

    def test_artefakt_io_hatasinda_ilerlemez_motor_durumunda_kalir(self):
        once = self.depo.oku()
        # isler_kok dizin değil dosya yapılır; mkdir NotADirectoryError verir (Debt 08 / SP-D1).
        isler_dosya = self.isler_kok.parent / "isler_dosyasi"
        isler_dosya.write_text("engelleyici dosya", encoding="utf-8")

        sonuc = isi_ilerlet(SahteMotor(metin="plan içeriği"), is_id="IS-08",
                            durum_yolu=self.yol, isler_kok=isler_dosya)

        self.assertEqual(sonuc.izlenen_yol, ("bos", "is_alindi", "planlaniyor"))
        self.assertEqual(sonuc.bitis_durumu, "planlaniyor")
        self.assertEqual(self.depo.oku(),
                         dict(once, durum="planlaniyor", is_id="IS-08", son_sinyal=None))

    def test_basari_utf8_okunamayan_artefaktta_ilerlemez_motor_durumunda_kalir(self):
        once = self.depo.oku()
        plan_yolu = self.isler_kok / "IS-09" / "plan.md"
        plan_yolu.parent.mkdir(parents=True)
        plan_yolu.write_bytes(b"\xff\xfe\x00\x00")

        # Motor basari sinyali verir ama metin boş olduğundan bozuk dosya kalır; UTF-8 okunamadığından reddedilir.
        sonuc = isi_ilerlet(SahteMotor(metin=""), is_id="IS-09",
                            durum_yolu=self.yol, isler_kok=self.isler_kok)

        self.assertEqual(sonuc.izlenen_yol, ("bos", "is_alindi", "planlaniyor"))
        self.assertEqual(sonuc.bitis_durumu, "planlaniyor")
        self.assertEqual(self.depo.oku(),
                         dict(once, durum="planlaniyor", is_id="IS-09", son_sinyal=None))
        # Bozuk dosya silinmez/değişmez ama geçiş kabul edilmez.
        self.assertEqual(plan_yolu.read_bytes(), b"\xff\xfe\x00\x00")

    def test_delege_basari_bos_artefaktta_ilerlemez_delege_durumunda_kalir(self):
        once = self.depo.oku()
        planlama = SahteMotor(metin="plan içeriği")
        delege = SahteMotor(metin="")

        def motor(girdi):
            return (delege if "paket.md" in girdi else planlama)(girdi)

        sonuc = isi_ilerlet(motor, is_id="IS-10", durum_yolu=self.yol,
                            isler_kok=self.isler_kok)

        self.assertEqual(sonuc.izlenen_yol, (
            "bos", "is_alindi", "planlaniyor", "plan_hazir", "delege_hazirlaniyor"))
        self.assertEqual(sonuc.bitis_durumu, "delege_hazirlaniyor")
        self.assertEqual(self.depo.oku(),
                         dict(once, durum="delege_hazirlaniyor", is_id="IS-10", son_sinyal=None))
        self.assertTrue((self.isler_kok / "IS-10" / "plan.md").exists())
        self.assertFalse((self.isler_kok / "IS-10" / "paket.md").exists())

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
            for sinyal in (BASARI, HATA):
                with self.subTest(mevcut=mevcut, sinyal=sinyal):
                    self.depo.yaz(DurumKaydi(
                        durum=mevcut, is_id="ESKI", son_sinyal="onceki"))
                    once = self.yol.read_bytes()

                    sinyal_uretilen, _metin = SahteMotor(sinyal)(mevcut)
                    sonuc = kalici_gecis(
                        self.depo, self.surucu,
                        kayit=DurumKaydi(
                            durum=hedef, is_id="IS-05",
                            son_sinyal=sinyal_uretilen))

                    self.assertFalse(sonuc.kabul)
                    self.assertEqual(sonuc.yeni_durum, mevcut)
                    self.assertEqual(self.yol.read_bytes(), once)


if __name__ == "__main__":
    unittest.main()
