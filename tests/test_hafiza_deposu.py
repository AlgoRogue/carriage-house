"""CH-0001 Ajan hafızasının boş başlangıç ve ekleme sözleşmesi."""
import json
import shutil
import tempfile
import unittest
from pathlib import Path

from tests.surucu_yolu import PERSONEL
from hafiza_deposu import HafizaDeposu


class HafizaDeposuTesti(unittest.TestCase):
    def setUp(self):
        self.prod = PERSONEL / "hafiza.json"
        self.prod_once = self.prod.read_bytes()
        self.iskelet_once = (PERSONEL / "aksiyon-iskeleti.json").read_bytes()
        self.kart_once = (PERSONEL / "kart.json").read_bytes()
        self.durum_once = (PERSONEL / "durum.json").read_bytes()
        self.gecici = tempfile.TemporaryDirectory()
        self.addCleanup(self.gecici.cleanup)
        self.yol = Path(self.gecici.name) / "hafiza.json"
        shutil.copyfile(self.prod, self.yol)

    def tearDown(self):
        self.assertEqual((PERSONEL / "hafiza.json").read_bytes(), self.prod_once)
        self.assertEqual(
            (PERSONEL / "aksiyon-iskeleti.json").read_bytes(), self.iskelet_once)
        self.assertEqual((PERSONEL / "kart.json").read_bytes(), self.kart_once)
        self.assertEqual((PERSONEL / "durum.json").read_bytes(), self.durum_once)

    def test_bos_baslangic_oku_bos_liste_doner(self):
        self.assertEqual(HafizaDeposu().yol, PERSONEL / "hafiza.json")
        self.assertEqual(HafizaDeposu().oku(), [])
        self.assertEqual(HafizaDeposu(self.yol).oku(), [])

    def test_ekle_yeni_okuyucuda_kalir(self):
        HafizaDeposu(self.yol).ekle("öğle notu")
        kayitlar = HafizaDeposu(self.yol).oku()
        self.assertEqual(kayitlar, [{"metin": "öğle notu"}])
        belge = json.loads(self.yol.read_text(encoding="utf-8"))
        self.assertEqual(belge, {"kayitlar": [{"metin": "öğle notu"}]})

    def test_ikinci_ekleme_sirayi_korur(self):
        depo = HafizaDeposu(self.yol)
        depo.ekle("birinci")
        depo.ekle("ikinci")
        self.assertEqual(
            HafizaDeposu(self.yol).oku(),
            [{"metin": "birinci"}, {"metin": "ikinci"}],
        )


if __name__ == "__main__":
    unittest.main()
