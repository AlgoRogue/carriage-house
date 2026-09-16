"""Tek geçişin geçici durum dosyasına kalıcılık sözleşmesi."""
import json
import shutil
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from tests.surucu_yolu import PERSONEL
from durum_deposu import DurumDeposu, DurumKaydi
from surucu_cekirdek import Sinyal, Surucu
from surucu_kalici_gecis import kalici_gecis


class SurucuDurumTesti(unittest.TestCase):
    def setUp(self):
        self.gecici = tempfile.TemporaryDirectory()
        self.addCleanup(self.gecici.cleanup)
        self.yol = Path(self.gecici.name) / "durum.json"
        shutil.copyfile(PERSONEL / "durum.json", self.yol)
        self.iskelet_yolu = PERSONEL / "aksiyon-iskeleti.json"
        self.iskelet_once = self.iskelet_yolu.read_bytes()
        self.prod_once = (PERSONEL / "durum.json").read_bytes()
        self.surucu = Surucu(json.loads(self.iskelet_once))
        self.depo = DurumDeposu(self.yol)

    def tearDown(self):
        self.assertEqual(self.iskelet_yolu.read_bytes(), self.iskelet_once)
        self.assertEqual((PERSONEL / "durum.json").read_bytes(), self.prod_once)

    def test_depo_okur_ve_yalniz_uc_alani_gunceller(self):
        once = json.loads(self.yol.read_text())
        self.assertEqual(self.depo.oku(), once)
        self.depo.yaz(DurumKaydi(
            durum="planlaniyor", is_id="IS-03", son_sinyal=None))
        beklenen = dict(once, durum="planlaniyor", is_id="IS-03", son_sinyal=None)
        self.assertEqual(DurumDeposu(self.yol).oku(), beklenen)

    def test_durum_kaydi_disk_formatini_degistirmeden_doner(self):
        once = json.loads(self.yol.read_text(encoding="utf-8"))
        kayit = DurumKaydi(
            durum="planlaniyor", is_id="IS-08", son_sinyal="basari")
        self.depo.yaz(kayit)
        belge = json.loads(self.yol.read_text(encoding="utf-8"))
        self.assertEqual(
            belge,
            dict(once, durum="planlaniyor", is_id="IS-08",
                 son_sinyal="basari"))
        okunan = self.depo.oku()
        self.assertEqual(okunan, belge)
        self.assertEqual(
            DurumKaydi(okunan["durum"], okunan["is_id"], okunan["son_sinyal"]),
            kayit)

    def test_kabul_tek_gecisi_ve_is_idyi_yazar(self):
        sonuc = kalici_gecis(
            self.depo, self.surucu,
            kayit=DurumKaydi(durum="is_alindi", is_id="IS-03"))
        self.assertTrue(sonuc.kabul)
        kayit = DurumDeposu(self.yol).oku()
        self.assertEqual(kayit["durum"], "is_alindi")
        self.assertEqual(kayit["is_id"], "IS-03")
        self.assertIsNone(kayit["son_sinyal"])

    def test_dosyayi_yeniden_okur_ve_sinyali_yazar(self):
        self.depo.yaz(DurumKaydi(durum="planlaniyor", is_id="ESKI"))
        sonuc = kalici_gecis(
            self.depo, self.surucu,
            kayit=DurumKaydi(durum="plan_hazir", is_id="YENI",
                             son_sinyal="basari"))
        self.assertTrue(sonuc.kabul)
        kayit = self.depo.oku()
        self.assertEqual((kayit["durum"], kayit["is_id"], kayit["son_sinyal"]),
                         ("plan_hazir", "YENI", "basari"))
        kalici_gecis(
            self.depo, self.surucu,
            kayit=DurumKaydi(durum="delege_hazirlaniyor", is_id=None))
        self.assertEqual(self.depo.oku()["durum"], "delege_hazirlaniyor")
        self.assertIsNone(self.depo.oku()["son_sinyal"])
        self.assertIsNone(self.depo.oku()["is_id"])

    def test_sinyal_enum_durum_jsona_onceki_dizgi_olarak_yazilir(self):
        for uye, dizgi in ((Sinyal.BASARI, "basari"),
                           (Sinyal.HATA, "hata")):
            with self.subTest(dizgi=dizgi):
                self.assertEqual(uye, dizgi)
                self.depo.yaz(DurumKaydi(
                    durum="planlaniyor", is_id="IS-07", son_sinyal=uye))
                kayit = json.loads(self.yol.read_text(encoding="utf-8"))
                self.assertEqual(kayit["son_sinyal"], dizgi)

    def test_red_dosyaya_hic_yazmaz(self):
        for mevcut, hedef, sinyal in [("bos", "park", None),
                                      ("planlaniyor", "plan_hazir", None),
                                      ("park", "usta_atandi", None)]:
            with self.subTest(mevcut=mevcut):
                self.depo.yaz(DurumKaydi(
                    durum=mevcut, is_id="ESKI", son_sinyal="onceki"))
                once = self.yol.read_bytes()
                with patch.object(self.depo, "yaz", wraps=self.depo.yaz) as yaz:
                    sonuc = kalici_gecis(
                        self.depo, self.surucu,
                        kayit=DurumKaydi(durum=hedef, is_id="YENI",
                                         son_sinyal=sinyal))
                    yaz.assert_not_called()
                self.assertFalse(sonuc.kabul)
                self.assertEqual(self.yol.read_bytes(), once)


if __name__ == "__main__":
    unittest.main()
