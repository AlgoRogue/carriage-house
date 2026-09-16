"""Ticket 02: gerçek iskeletle, gerçek şablonla, tek geçişli Motor seam'i."""
import copy
import json
import tempfile
import unittest
from contextlib import ExitStack
from pathlib import Path
from unittest.mock import Mock, patch

from tests.surucu_yolu import KOK, PERSONEL
from sahte_motor import SahteMotor
from surucu_adim import SurucuAdim
from surucu_cekirdek import Surucu

# S4 (SEAMS.md, onaylı): motor durumu -> İş artefaktı dosya adı.
_ARTEFAKT_ADI = {"planlaniyor": "plan.md", "delege_hazirlaniyor": "paket.md"}


class SurucuAdimTesti(unittest.TestCase):
    def setUp(self):
        self.iskelet = json.loads(
            (KOK / "personel/CH-0001/aksiyon-iskeleti.json").read_text(encoding="utf-8"))
        self.sablon_kok = PERSONEL / "sablonlar"
        self.sablon_once = {
            yol.name: yol.read_bytes() for yol in self.sablon_kok.iterdir()}

    def tearDown(self):
        for yol in self.sablon_kok.iterdir():
            self.assertEqual(yol.read_bytes(), self.sablon_once[yol.name])

    def test_motor_durumlari_bir_kez_cagrilir_girdi_doldurulmus_sablondur(self):
        for durum, hedef in [("planlaniyor", "plan_hazir"),
                             ("delege_hazirlaniyor", "paket_hazir")]:
            for sinyal in ("basari", "hata"):
                with self.subTest(durum=durum, sinyal=sinyal):
                    metin = "içerik" if sinyal == "basari" else ""
                    motor = SahteMotor(sinyal, metin=metin)
                    hedef_durum = "hata" if sinyal == "hata" else hedef
                    cekirdek = Surucu(self.iskelet)
                    with tempfile.TemporaryDirectory() as gecici:
                        is_kok = Path(gecici)
                        with patch.object(Surucu, "gecis", wraps=cekirdek.gecis) as gecis:
                            sonuc = SurucuAdim(
                                self.iskelet, motor, is_id="IS-01", is_kok=is_kok,
                                sablon_kok=self.sablon_kok).adim(durum)
                        gecis.assert_called_once_with(durum, hedef_durum, sinyal)
                        self.assertTrue(sonuc.kabul)
                        self.assertEqual(sonuc.yeni_durum, hedef_durum)
                        self.assertEqual(len(motor.cagrilar), 1)

                        girdi = motor.cagrilar[0]["durum"]
                        # Girdi ≠ yalnız durum adı; doldurulmuş şablon adres taşır.
                        self.assertNotEqual(girdi, durum)
                        artefakt_yolu = is_kok / "IS-01" / _ARTEFAKT_ADI[durum]
                        self.assertIn(str(artefakt_yolu), girdi)

                        if sinyal == "basari":
                            self.assertEqual(
                                artefakt_yolu.read_text(encoding="utf-8"), "içerik")
                        else:
                            self.assertFalse(artefakt_yolu.exists())

    def test_delege_girdisinde_plan_yolu_var_plan_metni_yok(self):
        with tempfile.TemporaryDirectory() as gecici:
            is_kok = Path(gecici)
            plan_yolu = is_kok / "IS-02" / "plan.md"
            plan_yolu.parent.mkdir(parents=True)
            plan_yolu.write_text("gizli plan metni", encoding="utf-8")

            motor = SahteMotor(metin="paket içeriği")
            sonuc = SurucuAdim(self.iskelet, motor, is_id="IS-02", is_kok=is_kok,
                               sablon_kok=self.sablon_kok).adim("delege_hazirlaniyor")

            self.assertTrue(sonuc.kabul)
            girdi = motor.cagrilar[0]["durum"]
            self.assertIn(str(plan_yolu), girdi)
            self.assertIn(str(is_kok / "IS-02" / "paket.md"), girdi)
            self.assertNotIn("gizli plan metni", girdi)

    def test_basari_bos_artefaktta_reddedilir_durum_korunur(self):
        with tempfile.TemporaryDirectory() as gecici:
            is_kok = Path(gecici)
            motor = SahteMotor(metin="   ")

            sonuc = SurucuAdim(self.iskelet, motor, is_id="IS-03", is_kok=is_kok,
                               sablon_kok=self.sablon_kok).adim("planlaniyor")

            self.assertFalse(sonuc.kabul)
            self.assertEqual(sonuc.yeni_durum, "planlaniyor")
            self.assertFalse((is_kok / "IS-03" / "plan.md").exists())

    def test_basari_io_hatasinda_reddedilir_durum_korunur(self):
        with tempfile.TemporaryDirectory() as gecici:
            # is_kok dizin değil dosya yapılır (NotADirectoryError).
            is_dosya = Path(gecici) / "isler_dosyasi"
            is_dosya.write_text("dosya", encoding="utf-8")
            motor = SahteMotor(metin="plan içeriği")

            sonuc = SurucuAdim(self.iskelet, motor, is_id="IS-03B", is_kok=is_dosya,
                               sablon_kok=self.sablon_kok).adim("planlaniyor")

            self.assertFalse(sonuc.kabul)
            self.assertEqual(sonuc.yeni_durum, "planlaniyor")
            self.assertIn("İş artefaktı boş veya yazılamadı", sonuc.mesaj)

    def test_basari_utf8_okunamayan_artefaktta_reddedilir_durum_korunur(self):
        with tempfile.TemporaryDirectory() as gecici:
            is_kok = Path(gecici)
            plan_yolu = is_kok / "IS-03C" / "plan.md"
            plan_yolu.parent.mkdir(parents=True)
            plan_yolu.write_bytes(b"\xff\xfe\x00\x00")
            motor = SahteMotor(metin="")

            sonuc = SurucuAdim(self.iskelet, motor, is_id="IS-03C", is_kok=is_kok,
                               sablon_kok=self.sablon_kok).adim("planlaniyor")

            self.assertFalse(sonuc.kabul)
            self.assertEqual(sonuc.yeni_durum, "planlaniyor")
            self.assertIn("İş artefaktı boş veya yazılamadı", sonuc.mesaj)

    def test_motor_disinda_tek_adim_ve_sifir_cagri(self):
        with tempfile.TemporaryDirectory() as gecici:
            is_kok = Path(gecici)
            for durum, hedef in [("bos", "is_alindi"), ("is_alindi", "planlaniyor"),
                                 ("plan_hazir", "delege_hazirlaniyor"),
                                 ("paket_hazir", "park"), ("hata", "park"), ("park", "park")]:
                with self.subTest(durum=durum):
                    motor = SahteMotor()
                    sonuc = SurucuAdim(self.iskelet, motor, is_id="IS-04", is_kok=is_kok,
                                       sablon_kok=self.sablon_kok).adim(durum)
                    self.assertEqual(sonuc.yeni_durum, hedef)
                    self.assertEqual(sonuc.kabul, durum != "park")
                    self.assertEqual(motor.cagrilar, [])

    def test_sahte_motor_cagri_sirasini_ve_zamanini_kaydeder(self):
        saat = Mock(side_effect=[10.0, 12.5])
        motor = SahteMotor("hata", saat=saat)
        for durum in ("planlaniyor", "delege_hazirlaniyor"):
            sinyal, _metin = motor(durum)
            self.assertEqual(sinyal, "hata")
        self.assertEqual(motor.cagrilar, [
            {"durum": "planlaniyor", "zaman": 10.0},
            {"durum": "delege_hazirlaniyor", "zaman": 12.5}])
        self.assertEqual(SahteMotor().cagrilar, [])

    def test_hedefi_iskelet_belirler_her_callable_enjekte_edilebilir(self):
        for gecis in self.iskelet["gecisler"]:
            if gecis["from"] == "planlaniyor" and gecis["to"] == "plan_hazir":
                gecis["to"] = "paket_hazir"
        motor = Mock(return_value=("basari", "içerik"))
        with tempfile.TemporaryDirectory() as gecici:
            is_kok = Path(gecici)
            sonuc = SurucuAdim(self.iskelet, motor, is_id="IS-05", is_kok=is_kok,
                               sablon_kok=self.sablon_kok).adim("planlaniyor")
            self.assertEqual(sonuc.yeni_durum, "paket_hazir")
            self.assertTrue(sonuc.kabul)
            motor.assert_called_once()
            girdi = motor.call_args.args[0]
            self.assertNotEqual(girdi, "planlaniyor")
            self.assertIn(str(is_kok / "IS-05" / "plan.md"), girdi)

    def test_motor_disinda_kenar_secim_kurali(self):
        with tempfile.TemporaryDirectory() as gecici:
            is_kok = Path(gecici)
            self.iskelet["gecisler"].append({"from": "bos", "to": "hata"})
            self.assertEqual(
                SurucuAdim(self.iskelet, SahteMotor(), is_id="IS-06", is_kok=is_kok,
                          sablon_kok=self.sablon_kok).adim("bos").yeni_durum,
                "is_alindi")
            self.iskelet["gecisler"].append({"from": "bos", "to": "park"})
            sonuc = SurucuAdim(self.iskelet, SahteMotor(), is_id="IS-06", is_kok=is_kok,
                               sablon_kok=self.sablon_kok).adim("bos")
            self.assertFalse(sonuc.kabul)
            self.assertEqual(sonuc.yeni_durum, "bos")
            self.iskelet["gecisler"] = [{"from": "bos", "to": "hata"}]
            self.assertEqual(
                SurucuAdim(self.iskelet, SahteMotor(), is_id="IS-06", is_kok=is_kok,
                          sablon_kok=self.sablon_kok).adim("bos").yeni_durum,
                "hata")

    def test_gecersiz_sinyal_hedef_olarak_kullanilmaz(self):
        with tempfile.TemporaryDirectory() as gecici:
            is_kok = Path(gecici)
            with self.assertRaises(ValueError):
                SurucuAdim(self.iskelet, lambda girdi: ("park", ""), is_id="IS-07",
                          is_kok=is_kok, sablon_kok=self.sablon_kok).adim("planlaniyor")

    def test_belirsiz_motor_hedefi_ve_dilim_disi_hedef_reddedilir(self):
        with tempfile.TemporaryDirectory() as gecici:
            is_kok = Path(gecici)
            self.iskelet["gecisler"].append({"from": "planlaniyor", "to": "park"})
            motor = SahteMotor()
            sonuc = SurucuAdim(self.iskelet, motor, is_id="IS-08", is_kok=is_kok,
                               sablon_kok=self.sablon_kok).adim("planlaniyor")
            self.assertFalse(sonuc.kabul)
            self.assertEqual(sonuc.yeni_durum, "planlaniyor")
            self.assertEqual(len(motor.cagrilar), 1)
            sonuc = SurucuAdim(self.iskelet, motor, is_id="IS-08", is_kok=is_kok,
                               sablon_kok=self.sablon_kok, dilim={"bos"}).adim("bos")
            self.assertFalse(sonuc.kabul)
            self.assertEqual(sonuc.yeni_durum, "bos")

    def test_motor_durumunda_da_subprocess_ve_ag_acilmaz(self):
        once = copy.deepcopy(self.iskelet)
        with tempfile.TemporaryDirectory() as gecici:
            is_kok = Path(gecici)
            with ExitStack() as stack:
                for hedef in ("subprocess.Popen", "subprocess.run",
                             "os.system", "socket.socket"):
                    stack.enter_context(patch(hedef, side_effect=AssertionError(hedef)))
                surucu = SurucuAdim(self.iskelet, SahteMotor(metin="içerik"),
                                    is_id="IS-09", is_kok=is_kok, sablon_kok=self.sablon_kok)
                for durum in ("bos", "is_alindi", "planlaniyor", "plan_hazir",
                              "delege_hazirlaniyor", "paket_hazir", "park", "hata"):
                    surucu.adim(durum)
                self.assertEqual(surucu.adim("bos").yeni_durum, "is_alindi")
        self.assertEqual(self.iskelet, once)


if __name__ == "__main__":
    unittest.main()
