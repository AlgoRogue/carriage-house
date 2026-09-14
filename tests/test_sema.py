"""Şema doğrulayıcı ve dört dondurulmuş şema — geçerli/geçersiz örnekler."""
import copy
import sys
import unittest
from pathlib import Path

KOK = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(KOK / "bin"))
import sema  # noqa: E402

SOZLESME = {
    "increment_id": "inc-001", "hedef_davranis": "kapi.py durum evreyi basar",
    "dokunulacak_yollar": ["bin/kapi.py"], "yeni_dosyalar": [], "motor_adayi": "codex",
    "kabul_kriterleri": [{"aciklama": "testler geçer",
                          "dogrulama": {"tip": "komut", "deger": "python3 -m unittest discover -s tests"}}],
    "durma_kosulu": "evre şeması belirsizse dur", "kapsam_disi": ["dağıtıcı"],
    "yayin_anlami": "kapi.py durum canlı komut olur",
}
TESLIM = {"increment_id": "inc-001", "motor": "codex", "diff_ozeti": "bin/kapi.py: durum komutu",
          "calistirilan_komutlar": ["python3 -m unittest discover -s tests"], "yapilmayanlar": [], "park_var": False}
RAPOR = {"increment_id": "inc-001", "motor": "claude", "karar": "PASS",
         "kriterler": [{"aciklama": "testler geçer", "sonuc": "PASS", "kanit": "unittest: OK (12 tests), çıkış 0"}],
         "ihlal": [], "kapsam_sapmasi": []}
EVRE = {"increment_id": "inc-001", "evre": "sozlesme", "bekleyen_onay": None,
        "motor": {"insaat": None, "bekci": None}, "talep": "x", "kapsam_sapmasi": [], "gecmis": []}


class DogrulayiciTesti(unittest.TestCase):
    def test_tip_enum_required_items(self):
        s = {"type": "object", "required": ["a"], "additionalProperties": False,
             "properties": {"a": {"type": "string", "enum": ["x", "y"]},
                            "b": {"type": "array", "minItems": 1, "items": {"type": "integer"}}}}
        self.assertEqual(sema.dogrula(s, {"a": "x", "b": [1]}), [])
        hatalar = sema.dogrula(s, {"a": "z", "b": [], "c": 1})
        self.assertTrue(any("enum" in h or "biri olmalı" in h for h in hatalar))
        self.assertTrue(any("en az 1" in h for h in hatalar))
        self.assertTrue(any("$.c" in h for h in hatalar))
        self.assertTrue(sema.dogrula(s, {"b": [True]}))  # a eksik, bool integer değil
        self.assertTrue(sema.dogrula(s, "nesne değil"))

    def test_null_ve_tip_listesi(self):
        s = {"type": ["string", "null"], "enum": [None, "a"]}
        self.assertEqual(sema.dogrula(s, None), [])
        self.assertEqual(sema.dogrula(s, "a"), [])
        self.assertTrue(sema.dogrula(s, 3))


class DondurulmusSemalar(unittest.TestCase):
    def _gecerli(self, ad, veri):
        self.assertEqual(sema.dogrula(sema.yukle(ad, KOK), veri), [])

    def _gecersiz(self, ad, veri):
        self.assertTrue(sema.dogrula(sema.yukle(ad, KOK), veri))

    def test_sozlesme(self):
        self._gecerli("increment-sozlesmesi", SOZLESME)
        for bozuk in ({**SOZLESME, "motor_adayi": "gpt"}, {**SOZLESME, "kabul_kriterleri": []},
                      {**SOZLESME, "hedef_davranis": "kısa"}, {**SOZLESME, "fazla": 1}):
            self._gecersiz("increment-sozlesmesi", bozuk)
        k = copy.deepcopy(SOZLESME)
        k["kabul_kriterleri"][0]["dogrulama"]["tip"] = "his"
        self._gecersiz("increment-sozlesmesi", k)

    def test_teslim(self):
        self._gecerli("teslim", TESLIM)
        self._gecersiz("teslim", {**TESLIM, "park_var": "hayır"})
        self._gecersiz("teslim", {k: v for k, v in TESLIM.items() if k != "diff_ozeti"})

    def test_rapor(self):
        self._gecerli("bekci-raporu", RAPOR)
        self._gecersiz("bekci-raporu", {**RAPOR, "karar": "belki"})
        self._gecersiz("bekci-raporu", {**RAPOR, "kriterler": []})
        k = copy.deepcopy(RAPOR)
        k["kriterler"][0]["kanit"] = ""
        self._gecersiz("bekci-raporu", k)

    def test_evre(self):
        self._gecerli("evre", EVRE)
        self._gecerli("evre", {**EVRE, "increment_id": None, "evre": "bos"})
        self._gecersiz("evre", {**EVRE, "evre": "uçuyor"})
        self._gecersiz("evre", {**EVRE, "bekleyen_onay": "hemen"})
        self._gecersiz("evre", {**EVRE, "motor": {"insaat": "gpt", "bekci": None}})


if __name__ == "__main__":
    unittest.main()
