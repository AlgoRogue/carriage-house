#!/usr/bin/env python3
"""Salt-okur durum sayfası — evre.json ve aktif increment artefaktlarının insan yüzü.

  python3 bin/uygulama.py [--port 8765]

Yalnız 127.0.0.1'de dinler. Her GET dosyaları yeniden okur; GET dışı 405; hiçbir istek yazmaz.
"""
import html
import json
import sys
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from urllib.parse import unquote, urlparse

sys.path.insert(0, str(Path(__file__).resolve().parent))
import ayar  # noqa: E402
import kapi  # noqa: E402

HOST = "127.0.0.1"
VARSAYILAN_PORT = 8765


class LoopbackSunucu(HTTPServer):
    allow_reuse_address = True


def siradaki_adim(kok):
    """`bin/kapi.py durum` ile aynı komut metni — çıktının `sıradaki:` satırı."""
    _, metin = kapi.durum(kok)
    for satir in metin.splitlines():
        if satir.startswith("sıradaki: "):
            return satir[len("sıradaki: "):]
    return ""


def _artefaktlar(kok, evre):
    """Aktif increment klasöründeki dosya adları; `/` veya `..` içerenler elenir."""
    id_ = evre.get("increment_id")
    if not id_:
        return []
    klasor = ayar.increment_klasoru(id_, kok)
    if not klasor.is_dir():
        return []
    adlar = []
    for yol in sorted(klasor.iterdir()):
        if yol.is_file() and "/" not in yol.name and ".." not in yol.name:
            adlar.append(yol.name)
    return adlar


def _bekci_karar(kok, evre):
    id_ = evre.get("increment_id")
    if not id_:
        return None
    rapor = ayar.increment_klasoru(id_, kok) / "bekci-raporu.json"
    if not rapor.is_file():
        return None
    try:
        return json.loads(rapor.read_text(encoding="utf-8")).get("karar", "?")
    except ValueError:
        return "rapor bozuk"


def sayfa_html(kok):
    """Her istekte evre.json + aktif klasörden üretilen salt-okur HTML."""
    evre_yolu = Path(kok) / "increment" / "evre.json"
    evre = ayar.evre_oku(kok)
    kac = html.escape
    id_ = evre.get("increment_id") or "-"
    evre_adi = evre.get("evre") or "bos"
    onay = evre.get("bekleyen_onay") or "-"
    motor = evre.get("motor") or {}
    insaat = motor.get("insaat") or "-"
    bekci = motor.get("bekci") or "-"
    talep = evre.get("talep") or "-"
    adim = siradaki_adim(kok)
    karar = _bekci_karar(kok, evre)
    bekci_satir = f"<p>bekçi kararı: {kac(karar)}</p>\n" if karar is not None else ""

    baglantilar = []
    if evre_yolu.is_file():
        baglantilar.append('<li><a href="/evre.json">evre.json</a></li>')
        for ad in _artefaktlar(kok, evre):
            href = "/artefakt/" + ad
            baglantilar.append(f'<li><a href="{kac(href)}">{kac(ad)}</a></li>')
    liste = ("<ul>\n" + "\n".join(baglantilar) + "\n</ul>") if baglantilar else "<p>bağlantı yok</p>"

    return (
        "<!DOCTYPE html>\n<html lang=\"tr\">\n<head>\n"
        "<meta charset=\"utf-8\">\n<title>A Şirketi</title>\n</head>\n<body>\n"
        "<h1>A Şirketi</h1>\n"
        f"<p>increment: {kac(id_)}</p>\n"
        f"<p>evre: {kac(evre_adi)}</p>\n"
        f"<p>bekleyen onay: {kac(onay)}</p>\n"
        f"<p>motorlar: inşaat={kac(insaat)} · bekçi={kac(bekci)}</p>\n"
        f"<p>talep: {kac(talep)}</p>\n"
        f"<p>sıradaki adım: {kac(adim)}</p>\n"
        f"{bekci_satir}"
        "<h2>artefakt bağlantıları</h2>\n"
        f"{liste}\n"
        "</body>\n</html>\n"
    )


def artefakt_yolu(kok, ad):
    """Aktif klasördeki düz dosya adı. `/` veya `..` içeren / eksik / kaçış → None (404)."""
    if not ad or "/" in ad or ".." in ad or ad != Path(ad).name:
        return None
    evre = ayar.evre_oku(kok)
    id_ = evre.get("increment_id")
    if not id_:
        return None
    klasor = ayar.increment_klasoru(id_, kok)
    yol = klasor / ad
    try:
        if yol.is_file() and yol.resolve().parent == klasor.resolve():
            return yol
    except OSError:
        return None
    return None


def isleyici(kok):
    kok = Path(kok)

    class Isleyici(BaseHTTPRequestHandler):
        def log_message(self, fmt, *args):
            pass

        def _gonder(self, kod, tur, govde):
            self.send_response(kod)
            self.send_header("Content-Type", tur)
            self.send_header("Content-Length", str(len(govde)))
            self.end_headers()
            self.wfile.write(govde)

        def _yasak(self):
            self.send_error(HTTPStatus.METHOD_NOT_ALLOWED)

        def __getattr__(self, ad):
            if ad.startswith("do_"):
                return self._yasak
            raise AttributeError(ad)

        def do_GET(self):
            yol = unquote(urlparse(self.path).path)
            if yol == "/":
                self._gonder(200, "text/html; charset=utf-8", sayfa_html(kok).encode("utf-8"))
                return
            if yol == "/evre.json":
                dosya = kok / "increment" / "evre.json"
                if not dosya.is_file():
                    self.send_error(HTTPStatus.NOT_FOUND)
                    return
                self._gonder(200, "text/plain; charset=utf-8", dosya.read_bytes())
                return
            if yol.startswith("/artefakt/"):
                hedef = artefakt_yolu(kok, yol[len("/artefakt/"):])
                if hedef is None:
                    self.send_error(HTTPStatus.NOT_FOUND)
                    return
                self._gonder(200, "text/plain; charset=utf-8", hedef.read_bytes())
                return
            self.send_error(HTTPStatus.NOT_FOUND)

    return Isleyici


def sunucu(kok, port=VARSAYILAN_PORT):
    """127.0.0.1'de dinleyen sunucu. port=0 OS seçer (test). Bind adresi seçeneği yok."""
    return LoopbackSunucu((HOST, port), isleyici(kok))


def main(argv=None):
    argv = list(sys.argv[1:] if argv is None else argv)
    port = VARSAYILAN_PORT
    i = 0
    while i < len(argv):
        if argv[i] == "--port" and i + 1 < len(argv):
            try:
                port = int(argv[i + 1])
            except ValueError:
                print("kullanım: python3 bin/uygulama.py [--port 8765]", file=sys.stderr)
                return 2
            i += 2
        else:
            print("kullanım: python3 bin/uygulama.py [--port 8765]", file=sys.stderr)
            return 2
    httpd = sunucu(ayar.KOK, port=port)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        httpd.server_close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
