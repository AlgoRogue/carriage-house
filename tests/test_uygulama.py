"""Salt-okur durum sayfası — sahte kök, port 0, loopback; ağ yok, motor yok."""
import hashlib
import json
import sys
import tempfile
import threading
import unittest
import urllib.error
import urllib.request
from pathlib import Path

KOK = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(KOK / "bin"))
import kapi  # noqa: E402
import uygulama  # noqa: E402

EVRE = {
    "increment_id": "inc-001",
    "evre": "insaat",
    "bekleyen_onay": None,
    "motor": {"insaat": "grok", "bekci": "claude"},
    "talep": "salt-okur sayfa",
    "kapsam_sapmasi": [],
    "gecmis": [{"zaman": "2026-09-15T00:00:00+03:00", "olay": "KAPI 1"}],
}


def sahte_kok(tmp, evre=None, dosyalar=None):
    kok = Path(tmp) / "kok"
    klasor = kok / "increment" / "inc-001"
    klasor.mkdir(parents=True)
    if evre is not None:
        (kok / "increment" / "evre.json").write_text(
            json.dumps(evre, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    for ad, icerik in (dosyalar or {}).items():
        (klasor / ad).write_text(icerik, encoding="utf-8")
    return kok


def agac_ozet(kok):
    ozet = {}
    for yol in sorted(Path(kok).rglob("*")):
        if yol.is_file():
            ozet[str(yol.relative_to(kok))] = hashlib.sha256(yol.read_bytes()).hexdigest()
    return ozet


def http_al(url, method="GET", data=None):
    istek = urllib.request.Request(url, data=data, method=method)
    return urllib.request.urlopen(istek, timeout=3)


class SunucuTemeli(unittest.TestCase):
    """Sahte kökte port 0'da sunucu; tearDown kapatır."""

    def ac(self, kok):
        self.httpd = uygulama.sunucu(kok, port=0)
        self.assertEqual(self.httpd.server_address[0], "127.0.0.1")
        self.port = self.httpd.server_address[1]
        self.taban = f"http://127.0.0.1:{self.port}"
        self.iplik = threading.Thread(target=self.httpd.serve_forever, daemon=True)
        self.iplik.start()

    def tearDown(self):
        if getattr(self, "httpd", None):
            self.httpd.shutdown()
            self.httpd.server_close()
        if getattr(self, "tmp", None):
            self.tmp.cleanup()


class SayfaVeArtefakt(SunucuTemeli):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.kok = sahte_kok(self.tmp.name, EVRE, {
            "sozlesme.onayli.json": '{"ok": true}\n',
            "not.txt": "merhaba\n",
        })
        self.once = agac_ozet(self.kok)
        self.ac(self.kok)

    def test_get_sayfa_alanlari_ve_baglantilar(self):
        with http_al(self.taban + "/") as yanit:
            govde = yanit.read().decode("utf-8")
            self.assertIn("text/html", yanit.headers.get_content_type())
        self.assertIn("<html", govde.lower())
        self.assertIn("inc-001", govde)
        self.assertIn("insaat", govde)
        self.assertIn("bekleyen onay", govde)
        self.assertIn("grok", govde)
        self.assertIn("claude", govde)
        self.assertIn("salt-okur sayfa", govde)
        adim = kapi.durum(self.kok)[1]
        self.assertIn("sıradaki:", adim)
        komut = [s for s in adim.splitlines() if s.startswith("sıradaki: ")][0][len("sıradaki: "):]
        self.assertIn(komut, govde)
        self.assertIn("python3 bin/kos.py sistem-insaat", govde)
        self.assertIn("/evre.json", govde)
        self.assertIn("/artefakt/sozlesme.onayli.json", govde)
        self.assertIn("/artefakt/not.txt", govde)

    def test_artefakt_icerik_evre_json_ve_yol_siniri(self):
        with http_al(self.taban + "/artefakt/not.txt") as yanit:
            self.assertEqual(yanit.headers.get_content_type(), "text/plain")
            self.assertEqual(yanit.read(), b"merhaba\n")
        with http_al(self.taban + "/evre.json") as yanit:
            self.assertEqual(yanit.headers.get_content_type(), "text/plain")
            self.assertEqual(yanit.read(), (self.kok / "increment" / "evre.json").read_bytes())
        for yol in ("/artefakt/%2e%2e", "/artefakt/..%2fnot.txt", "/artefakt/foo/bar",
                    "/artefakt/not.txt/../not.txt"):
            with self.assertRaises(urllib.error.HTTPError) as ctx:
                http_al(self.taban + yol)
            self.assertEqual(ctx.exception.code, 404, yol)
            ctx.exception.close()

    def test_yazma_yontemleri_405_ve_dosyalar_ayni(self):
        for method in ("POST", "PUT", "DELETE"):
            with self.assertRaises(urllib.error.HTTPError) as ctx:
                http_al(self.taban + "/", method=method, data=b"x")
            self.assertEqual(ctx.exception.code, 405, method)
            ctx.exception.close()
        self.assertEqual(agac_ozet(self.kok), self.once)


class BosEvre(SunucuTemeli):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.kok = sahte_kok(self.tmp.name, evre=None, dosyalar={})
        self.ac(self.kok)

    def test_eksik_evre_bos_baglanti_yok(self):
        with http_al(self.taban + "/") as yanit:
            govde = yanit.read().decode("utf-8")
        self.assertIn("evre: bos", govde)
        self.assertNotIn("/artefakt/", govde)
        self.assertNotIn("/evre.json", govde)
        with self.assertRaises(urllib.error.HTTPError) as ctx:
            http_al(self.taban + "/evre.json")
        self.assertEqual(ctx.exception.code, 404)
        ctx.exception.close()


if __name__ == "__main__":
    unittest.main()
