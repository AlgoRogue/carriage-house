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

    def test_eski_dolu_artefakt_varken_bos_motor_ciktisi_reddedilir_planlaniyor_kalir(self):
        # SP-1 regresyon testi: eski dolu plan + paket varken boş Motor çıktısı park'a götürmemeli.
        once = self.depo.oku()
        is_dizini = self.isler_kok / "IS-11"
        is_dizini.mkdir(parents=True)
        (is_dizini / "plan.md").write_text("eski plan", encoding="utf-8")
        (is_dizini / "paket.md").write_text("eski paket", encoding="utf-8")

        sonuc = isi_ilerlet(SahteMotor(metin=""), is_id="IS-11",
                            durum_yolu=self.yol, isler_kok=self.isler_kok)

        self.assertEqual(sonuc.izlenen_yol, ("bos", "is_alindi", "planlaniyor"))
        self.assertEqual(sonuc.bitis_durumu, "planlaniyor")
        self.assertEqual(self.depo.oku(),
                         dict(once, durum="planlaniyor", is_id="IS-11", son_sinyal=None))

    def test_eski_paket_varken_yeni_plan_ve_bos_delege_delege_durumunda_kalir(self):
        # SP-1 regresyon testi: eski paket varken yeni plan geçerli ama boş delege çıktısı park'a değil delege_hazirlaniyor'da kalmalı.
        once = self.depo.oku()
        is_dizini = self.isler_kok / "IS-12"
        is_dizini.mkdir(parents=True)
        (is_dizini / "paket.md").write_text("eski paket", encoding="utf-8")

        planlama = SahteMotor(metin="yeni plan içeriği")
        delege = SahteMotor(metin="")

        def motor(girdi):
            return (delege if "paket.md" in girdi else planlama)(girdi)

        sonuc = isi_ilerlet(motor, is_id="IS-12", durum_yolu=self.yol,
                            isler_kok=self.isler_kok)

        self.assertEqual(sonuc.izlenen_yol, (
            "bos", "is_alindi", "planlaniyor", "plan_hazir", "delege_hazirlaniyor"))
        self.assertEqual(sonuc.bitis_durumu, "delege_hazirlaniyor")
        self.assertEqual(self.depo.oku(),
                         dict(once, durum="delege_hazirlaniyor", is_id="IS-12", son_sinyal=None))

    def test_eski_artefakt_varken_whitespace_motor_ciktisi_reddedilir(self):
        # SP-1 regresyon testi: whitespace çıktı eski dosyayı başarıya çevirmemeli.
        once = self.depo.oku()
        is_dizini = self.isler_kok / "IS-13"
        is_dizini.mkdir(parents=True)
        (is_dizini / "plan.md").write_text("eski plan", encoding="utf-8")

        sonuc = isi_ilerlet(SahteMotor(metin="   \n\t  "), is_id="IS-13",
                            durum_yolu=self.yol, isler_kok=self.isler_kok)

        self.assertEqual(sonuc.izlenen_yol, ("bos", "is_alindi", "planlaniyor"))
        self.assertEqual(sonuc.bitis_durumu, "planlaniyor")
        self.assertEqual(self.depo.oku(),
                         dict(once, durum="planlaniyor", is_id="IS-13", son_sinyal=None))

    def test_is_dizini_chmod_0_permission_error_seamden_kacmaz_reddedilir(self):
        # SP-2 regresyon testi: chmod(0) iş dizininde PermissionError seam'den kaçmamalı.
        once = self.depo.oku()

        # Hem boş metin hem içerikli metin için PermissionError yakalanmalı
        for is_id, metin in (("IS-14", ""), ("IS-14-B", "plan metni")):
            with self.subTest(metin=metin):
                shutil.copyfile(PERSONEL / "durum.json", self.yol)
                is_dizini = self.isler_kok / is_id
                is_dizini.mkdir(parents=True, exist_ok=True)
                is_dizini.chmod(0)
                try:
                    sonuc = isi_ilerlet(SahteMotor(metin=metin), is_id=is_id,
                                        durum_yolu=self.yol, isler_kok=self.isler_kok)
                    self.assertEqual(sonuc.bitis_durumu, "planlaniyor")
                    self.assertEqual(sonuc.izlenen_yol, ("bos", "is_alindi", "planlaniyor"))
                    self.assertEqual(self.depo.oku(),
                                     dict(once, durum="planlaniyor", is_id=is_id, son_sinyal=None))
                finally:
                    is_dizini.chmod(0o700)

    def test_utf8_kodlama_hatasi_surrogate_seamden_kacmaz_reddedilir(self):
        # SP-D1 regresyon testi: Motor "\ud800" döndürdüğünde UnicodeEncodeError kaçmamalı.
        once = self.depo.oku()

        sonuc = isi_ilerlet(SahteMotor(metin="\ud800"), is_id="IS-15",
                            durum_yolu=self.yol, isler_kok=self.isler_kok)

        self.assertEqual(sonuc.bitis_durumu, "planlaniyor")
        self.assertEqual(sonuc.izlenen_yol, ("bos", "is_alindi", "planlaniyor"))
        self.assertEqual(self.depo.oku(),
                         dict(once, durum="planlaniyor", is_id="IS-15", son_sinyal=None))

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

    def test_motor_hata_sinyalinde_dolu_metin_olsa_bile_artefakt_yazilmaz_kapi_acilmaz(self):
        # Ticket 04: Motor hata Sinyali verince metin dolu olsa bile İş artefaktı yazılmaz;
        # plan_hazir kapısı açılmaz, planlaniyor -> hata -> park tek çağrıda işler.
        once = self.depo.oku()
        motor = SahteMotor(sinyal=HATA, metin="# Sahte Başarılı Plan İçeriği\n")

        sonuc = isi_ilerlet(motor, is_id="IS-HATA-DOLU",
                            durum_yolu=self.yol, isler_kok=self.isler_kok)

        self.assertEqual(sonuc.izlenen_yol,
                         ("bos", "is_alindi", "planlaniyor", "hata", "park"))
        self.assertEqual(sonuc.bitis_durumu, "park")
        self.assertNotIn("plan_hazir", sonuc.izlenen_yol)
        self.assertEqual(self.depo.oku(),
                         dict(once, durum="park", is_id="IS-HATA-DOLU", son_sinyal=None))
        self.assertFalse((self.isler_kok / "IS-HATA-DOLU" / "plan.md").exists())

    def test_motor_hata_sinyalinde_eski_artefakt_olsa_bile_plan_hazir_acilmaz_hatadan_parka_gider(self):
        # Ticket 04: Önceden diskte eski dolu artefakt bulunsa dahi Motor hata Sinyali verince
        # plan_hazir açılmaz; hata -> park yoluna sapılır.
        once = self.depo.oku()
        plan_yolu = self.isler_kok / "IS-HATA-ESKI" / "plan.md"
        plan_yolu.parent.mkdir(parents=True)
        plan_yolu.write_text("önceden kalma plan", encoding="utf-8")

        motor = SahteMotor(sinyal=HATA, metin="hata açıklaması")

        sonuc = isi_ilerlet(motor, is_id="IS-HATA-ESKI",
                            durum_yolu=self.yol, isler_kok=self.isler_kok)

        self.assertEqual(sonuc.izlenen_yol,
                         ("bos", "is_alindi", "planlaniyor", "hata", "park"))
        self.assertEqual(sonuc.bitis_durumu, "park")
        self.assertNotIn("plan_hazir", sonuc.izlenen_yol)
        self.assertEqual(self.depo.oku(),
                         dict(once, durum="park", is_id="IS-HATA-ESKI", son_sinyal=None))

    def test_delege_motor_hata_sinyalinde_dolu_metin_olsa_bile_paket_hazir_acilmaz(self):
        # Ticket 04: delege adımında hata Sinyali verince paket_hazir açılmaz;
        # delege_hazirlaniyor -> hata -> park işler.
        once = self.depo.oku()
        planlama = SahteMotor(metin="plan içeriği")
        delege = SahteMotor(sinyal=HATA, metin="delege hatası")

        def motor(girdi):
            return (delege if "paket.md" in girdi else planlama)(girdi)

        sonuc = isi_ilerlet(motor, is_id="IS-DELEGE-HATA",
                            durum_yolu=self.yol, isler_kok=self.isler_kok)

        self.assertEqual(sonuc.izlenen_yol, (
            "bos", "is_alindi", "planlaniyor", "plan_hazir",
            "delege_hazirlaniyor", "hata", "park"))
        self.assertEqual(sonuc.bitis_durumu, "park")
        self.assertNotIn("paket_hazir", sonuc.izlenen_yol)
        self.assertEqual(self.depo.oku(),
                         dict(once, durum="park", is_id="IS-DELEGE-HATA", son_sinyal=None))
        # plan.md yazıldı (planlaniyor başarılıydı) ama paket.md yazılmadı
        self.assertTrue((self.isler_kok / "IS-DELEGE-HATA" / "plan.md").exists())
        self.assertFalse((self.isler_kok / "IS-DELEGE-HATA" / "paket.md").exists())

    def test_sinyal_hata_ile_03_kapi_reddi_farki(self):
        # Ticket 04 vs Ticket 03 ayrımı:
        # 04: Sinyal 'hata' -> hata durumu -> park'a kadar gider (bitiş = park).
        # 03: Sinyal 'basari' + kötü artefakt -> kapı reddi, döngü durur (bitiş = planlaniyor).
        once = self.depo.oku()

        # 04 yolu (hata sinyali):
        sonuc_04 = isi_ilerlet(SahteMotor(sinyal=HATA, metin=""), is_id="IS-KARSILASTIRMA-04",
                               durum_yolu=self.yol, isler_kok=self.isler_kok)
        self.assertEqual(sonuc_04.bitis_durumu, "park")
        self.assertEqual(sonuc_04.izlenen_yol,
                         ("bos", "is_alindi", "planlaniyor", "hata", "park"))

        # Sıfırla
        self.depo.yaz(DurumKaydi(durum="bos", is_id=None, son_sinyal=None))

        # 03 yolu (basari sinyali ama boş artefakt):
        sonuc_03 = isi_ilerlet(SahteMotor(sinyal=BASARI, metin=""), is_id="IS-KARSILASTIRMA-03",
                               durum_yolu=self.yol, isler_kok=self.isler_kok)
        self.assertEqual(sonuc_03.bitis_durumu, "planlaniyor")
        self.assertEqual(sonuc_03.izlenen_yol, ("bos", "is_alindi", "planlaniyor"))


if __name__ == "__main__":
    unittest.main()
