"""Ticket 02: gerçek iskeletle, dosyasız ve tek geçişli Motor seam'i."""
import copy
import json
import unittest
from contextlib import ExitStack
from unittest.mock import Mock, patch

from tests.surucu_yolu import KOK
from sahte_motor import SahteMotor
from surucu_adim import SurucuAdim
from surucu_cekirdek import Surucu


class SurucuAdimTesti(unittest.TestCase):
    def setUp(self):
        self.iskelet = json.loads(
            (KOK / "personel/CH-0001/aksiyon-iskeleti.json").read_text(encoding="utf-8"))

    def test_motor_durumlari_bir_kez_cagrilir_ve_sinyal_cekirdege_gider(self):
        for durum, hedef in [("planlaniyor", "plan_hazir"),
                             ("delege_hazirlaniyor", "paket_hazir")]:
            for sinyal in ("motor_ciktisi", "motor_hatasi"):
                with self.subTest(durum=durum, sinyal=sinyal):
                    motor = SahteMotor(sinyal)
                    hedef_durum = "hata" if sinyal == "motor_hatasi" else hedef
                    cekirdek = Surucu(self.iskelet)
                    with patch.object(Surucu, "gecis", wraps=cekirdek.gecis) as gecis:
                        sonuc = SurucuAdim(self.iskelet, motor).adim(durum)
                    gecis.assert_called_once_with(durum, hedef_durum, sinyal)
                    self.assertTrue(sonuc.kabul)
                    self.assertEqual(sonuc.yeni_durum, hedef_durum)
                    self.assertEqual(len(motor.cagrilar), 1)
                    self.assertEqual(motor.cagrilar[0]["durum"], durum)

    def test_motor_disinda_tek_adim_ve_sifir_cagri(self):
        for durum, hedef in [("bos", "is_alindi"), ("is_alindi", "planlaniyor"),
                             ("plan_hazir", "delege_hazirlaniyor"),
                             ("paket_hazir", "park"), ("hata", "park"), ("park", "park")]:
            with self.subTest(durum=durum):
                motor = SahteMotor()
                sonuc = SurucuAdim(self.iskelet, motor).adim(durum)
                self.assertEqual(sonuc.yeni_durum, hedef)
                self.assertEqual(sonuc.kabul, durum != "park")
                self.assertEqual(motor.cagrilar, [])

    def test_sahte_motor_cagri_sirasini_ve_zamanini_kaydeder(self):
        saat = Mock(side_effect=[10.0, 12.5])
        motor = SahteMotor("motor_hatasi", saat=saat)
        for durum in ("planlaniyor", "delege_hazirlaniyor"):
            self.assertEqual(motor(durum), "motor_hatasi")
        self.assertEqual(motor.cagrilar, [
            {"durum": "planlaniyor", "zaman": 10.0},
            {"durum": "delege_hazirlaniyor", "zaman": 12.5}])
        self.assertEqual(SahteMotor().cagrilar, [])

    def test_hedefi_iskelet_belirler_her_callable_enjekte_edilebilir(self):
        for gecis in self.iskelet["gecisler"]:
            if gecis["from"] == "planlaniyor" and gecis["to"] == "plan_hazir":
                gecis["to"] = "paket_hazir"
        motor = Mock(return_value="motor_ciktisi")
        sonuc = SurucuAdim(self.iskelet, motor).adim("planlaniyor")
        self.assertEqual(sonuc.yeni_durum, "paket_hazir")
        self.assertTrue(sonuc.kabul)
        motor.assert_called_once_with("planlaniyor")

    def test_motor_disinda_kenar_secim_kurali(self):
        self.iskelet["gecisler"].append({"from": "bos", "to": "hata"})
        self.assertEqual(SurucuAdim(self.iskelet, SahteMotor()).adim("bos").yeni_durum,
                         "is_alindi")
        self.iskelet["gecisler"].append({"from": "bos", "to": "park"})
        sonuc = SurucuAdim(self.iskelet, SahteMotor()).adim("bos")
        self.assertFalse(sonuc.kabul)
        self.assertEqual(sonuc.yeni_durum, "bos")
        self.iskelet["gecisler"] = [{"from": "bos", "to": "hata"}]
        self.assertEqual(SurucuAdim(self.iskelet, SahteMotor()).adim("bos").yeni_durum,
                         "hata")

    def test_gecersiz_sinyal_hedef_olarak_kullanilmaz(self):
        with self.assertRaises(ValueError):
            SurucuAdim(self.iskelet, lambda durum: "park").adim("planlaniyor")

    def test_belirsiz_motor_hedefi_ve_dilim_disi_hedef_reddedilir(self):
        self.iskelet["gecisler"].append({"from": "planlaniyor", "to": "park"})
        motor = SahteMotor()
        sonuc = SurucuAdim(self.iskelet, motor).adim("planlaniyor")
        self.assertFalse(sonuc.kabul)
        self.assertEqual(sonuc.yeni_durum, "planlaniyor")
        self.assertEqual(len(motor.cagrilar), 1)
        sonuc = SurucuAdim(self.iskelet, motor, dilim={"bos"}).adim("bos")
        self.assertFalse(sonuc.kabul)
        self.assertEqual(sonuc.yeni_durum, "bos")

    def test_dosya_io_subprocess_yok_girdiler_bellekte_kalir(self):
        once = copy.deepcopy(self.iskelet)
        with ExitStack() as stack:
            for hedef in ("builtins.open", "io.open", "os.open", "subprocess.Popen", "os.system"):
                stack.enter_context(patch(hedef, side_effect=AssertionError(hedef)))
            surucu = SurucuAdim(self.iskelet, SahteMotor())
            for durum in ("bos", "is_alindi", "planlaniyor", "plan_hazir",
                          "delege_hazirlaniyor", "paket_hazir", "park", "hata"):
                surucu.adim(durum)
            self.assertEqual(surucu.adim("bos").yeni_durum, "is_alindi")
        self.assertEqual(self.iskelet, once)


if __name__ == "__main__":
    unittest.main()
