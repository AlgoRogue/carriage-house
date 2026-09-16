"""Sürücü çekirdeğinin saf, bellek içi geçiş sözleşmesi."""
import unittest

from tests import surucu_yolu
from surucu_cekirdek import Surucu


def aksiyon_iskeleti():
    return {
        "motor_cagrilan_durumlar": ["planlaniyor", "delege_hazirlaniyor"],
        "gecisler": [
            {"from": kaynak, "to": hedef}
            for kaynak, hedef in [
                ("bos", "is_alindi"), ("is_alindi", "planlaniyor"),
                ("planlaniyor", "plan_hazir"),
                ("plan_hazir", "delege_hazirlaniyor"),
                ("delege_hazirlaniyor", "paket_hazir"),
                ("paket_hazir", "park"), ("park", "usta_atandi"),
                ("usta_atandi", "izleniyor"), ("izleniyor", "tamam"),
                ("planlaniyor", "hata"), ("delege_hazirlaniyor", "hata"),
                ("izleniyor", "hata"), ("hata", "park"),
            ]
        ],
    }


class SurucuTesti(unittest.TestCase):
    def test_motor_disindaki_yasal_gecisler(self):
        surucu = Surucu(aksiyon_iskeleti())
        for mevcut, hedef in [("bos", "is_alindi"), ("is_alindi", "planlaniyor"),
                              ("plan_hazir", "delege_hazirlaniyor"),
                              ("paket_hazir", "park"), ("hata", "park")]:
            with self.subTest(mevcut=mevcut):
                sonuc = surucu.gecis(mevcut, hedef)
                self.assertTrue(sonuc.kabul)
                self.assertEqual(sonuc.yeni_durum, hedef)
                self.assertTrue(sonuc.mesaj)

    def test_iskelette_tanimsiz_cift_oncelikle_reddedilir(self):
        surucu = Surucu(aksiyon_iskeleti())
        for mevcut, hedef in [("bos", "park"), ("planlaniyor", "tamam"),
                              ("bilinmeyen", "is_alindi"), ("bos", "bos")]:
            with self.subTest(mevcut=mevcut, hedef=hedef):
                sonuc = surucu.gecis(mevcut, hedef, "bilinmeyen")
                self.assertFalse(sonuc.kabul)
                self.assertEqual(sonuc.yeni_durum, mevcut)
                self.assertIn("iskelet", sonuc.mesaj)

    def test_dilim_disindaki_hedef_sinyalden_once_reddedilir(self):
        for mevcut, hedef in [("park", "usta_atandi"), ("usta_atandi", "izleniyor"),
                              ("izleniyor", "tamam")]:
            with self.subTest(hedef=hedef):
                sonuc = Surucu(aksiyon_iskeleti()).gecis(mevcut, hedef, "basari")
                self.assertFalse(sonuc.kabul)
                self.assertEqual(sonuc.yeni_durum, mevcut)
                self.assertIn("dilim", sonuc.mesaj)
        for dilim in [set(), {"bos"}]:
            sonuc = Surucu(aksiyon_iskeleti(), dilim).gecis("bos", "is_alindi")
            self.assertFalse(sonuc.kabul)
            self.assertEqual(sonuc.yeni_durum, "bos")
        sonuc = Surucu(aksiyon_iskeleti(), {"planlaniyor"}).gecis(
            "planlaniyor", "plan_hazir")
        self.assertIn("dilim", sonuc.mesaj)

    def test_gecersiz_sinyal_erken_reddedilir(self):
        surucu = Surucu(aksiyon_iskeleti())
        for sinyal in ("", "bilinmeyen", "park"):
            with self.subTest(sinyal=sinyal):
                with self.assertRaises(ValueError):
                    surucu.gecis("planlaniyor", "plan_hazir", sinyal)

    def test_motor_gecisi_hedefle_uyumlu_sinyal_gerektirir(self):
        surucu = Surucu(aksiyon_iskeleti())
        for mevcut, basari_hedef in [("planlaniyor", "plan_hazir"),
                                     ("delege_hazirlaniyor", "paket_hazir")]:
            for hedef, dogru_sinyal in [(basari_hedef, "basari"), ("hata", "hata")]:
                for sinyal in [None, "basari", "hata"]:
                    with self.subTest(mevcut=mevcut, hedef=hedef, sinyal=sinyal):
                        sonuc = surucu.gecis(mevcut, hedef, sinyal)
                        kabul = sinyal == dogru_sinyal
                        self.assertEqual(sonuc.kabul, kabul)
                        self.assertEqual(sonuc.yeni_durum, hedef if kabul else mevcut)
                        self.assertTrue(sonuc.mesaj)

    def test_motor_disinda_gelen_her_sinyal_reddedilir(self):
        surucu = Surucu(aksiyon_iskeleti())
        for mevcut, hedef in [("bos", "is_alindi"), ("hata", "park"),
                              ("paket_hazir", "park")]:
            for sinyal in ["basari", "hata"]:
                with self.subTest(mevcut=mevcut, sinyal=sinyal):
                    sonuc = surucu.gecis(mevcut, hedef, sinyal)
                    self.assertFalse(sonuc.kabul)
                    self.assertEqual(sonuc.yeni_durum, mevcut)
                    self.assertIn("sinyal", sonuc.mesaj)

    def test_motor_hedefi_ve_motor_durumu_iskeletten_turetilir(self):
        iskelet = {
            "motor_cagrilan_durumlar": ["ozel_motor"],
            "gecisler": [{"from": "ozel_motor", "to": "hata"},
                         {"from": "ozel_motor", "to": "ozel_cikti"}],
        }
        surucu = Surucu(iskelet, {"ozel_motor", "ozel_cikti", "hata"})
        self.assertEqual(surucu.motor_basari_hedefi("ozel_motor"), "ozel_cikti")
        sonuc = surucu.gecis("ozel_motor", "ozel_cikti", "basari")
        self.assertTrue(sonuc.kabul)
        self.assertEqual(sonuc.yeni_durum, "ozel_cikti")
        self.assertFalse(surucu.gecis("ozel_motor", "ozel_cikti").kabul)
        self.assertIsNone(surucu.motor_basari_hedefi("bos"))

    def test_gecis_girdiyi_degistirmez_ve_onceki_cagriya_bagli_degil(self):
        iskelet = aksiyon_iskeleti()
        surucu = Surucu(iskelet)
        ilk = surucu.gecis("bos", "is_alindi")
        red = surucu.gecis("bos", "park")
        self.assertEqual(red.yeni_durum, "bos")
        self.assertEqual(surucu.gecis("bos", "is_alindi"), ilk)
        self.assertEqual(iskelet, aksiyon_iskeleti())

    def test_belirsiz_motor_basari_hedefi_secilmez(self):
        for hedefler in [[], ["plan_hazir", "park"]]:
            iskelet = {"motor_cagrilan_durumlar": ["planlaniyor"],
                       "gecisler": [{"from": "planlaniyor", "to": hedef}
                                    for hedef in ["hata", *hedefler]]}
            surucu = Surucu(iskelet)
            self.assertIsNone(surucu.motor_basari_hedefi("planlaniyor"))
            for hedef in hedefler:
                sonuc = surucu.gecis("planlaniyor", hedef, "basari")
                self.assertFalse(sonuc.kabul)
                self.assertEqual(sonuc.yeni_durum, "planlaniyor")
            self.assertTrue(surucu.gecis("planlaniyor", "hata", "hata").kabul)


if __name__ == "__main__":
    unittest.main()
