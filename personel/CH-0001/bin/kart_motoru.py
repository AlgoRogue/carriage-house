"""Personel kartındaki Motor'u Sürücü callable'ına çevirir."""
import json
import sys
from pathlib import Path

from surucu_cekirdek import Sinyal

KOK = Path(__file__).resolve().parents[3]
_BIN = str(KOK / "bin")
if _BIN not in sys.path:
    sys.path.insert(0, _BIN)
import motorlar  # noqa: E402


def motor_uret(kart_yolu, kosucu):
    """Kartı okur, kayıtlı adaptörü çözer, callable(girdi) -> (Sinyal, metin) döner.

    Koşucu komut listesi alır ve stdout döner. Kart yazılmaz. ``metin``
    içerik kanalıdır; ``cozumle``'nin ``yapisal``/``maliyet``/``oturum``
    alanları sonraki durumu belirlemez.
    Bilinmeyen cli veya bozuk kart koşucudan önce ValueError yükseltir.
    """
    kart = _kart_oku(kart_yolu)
    cli, model = _motor_alanlari(kart)
    try:
        modul = motorlar.motor_al(cli)
    except KeyError:
        raise ValueError(f"Bilinmeyen Motor cli: {cli}") from None
    ayarlar = {"model": model}

    def motor(girdi: str) -> tuple[Sinyal, str]:
        komut = modul.komut(str(girdi), ayarlar)
        try:
            stdout = kosucu(komut)
        except OSError:
            return Sinyal.HATA, ""
        try:
            cozum = modul.cozumle(stdout)
        except (TypeError, ValueError):
            return Sinyal.HATA, ""
        if not isinstance(cozum, dict) or cozum.get("hata"):
            metin = cozum.get("metin", "") if isinstance(cozum, dict) else ""
            return Sinyal.HATA, metin
        return Sinyal.BASARI, cozum.get("metin", "")

    return motor


def karti_ilerlet(kart_yolu, kosucu, *, is_id, durum_yolu, isler_kok=None):
    """Fabrika Motorunu mevcut isi_ilerlet girişine verir; yeni makine açmaz."""
    from surucu import ISLER_KOK, isi_ilerlet
    return isi_ilerlet(
        motor_uret(kart_yolu, kosucu), is_id=is_id, durum_yolu=durum_yolu,
        isler_kok=ISLER_KOK if isler_kok is None else isler_kok)


def _kart_oku(kart_yolu):
    try:
        veri = json.loads(Path(kart_yolu).read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        raise ValueError(f"Personel kartı okunamadı: {exc}") from exc
    if not isinstance(veri, dict):
        raise ValueError("Personel kartı nesne değil.")
    return veri


def _motor_alanlari(kart):
    arka = kart.get("arka_yuz")
    if not isinstance(arka, dict):
        raise ValueError("Personel kartında arka_yuz yok veya bozuk.")
    motor = arka.get("motor")
    if not isinstance(motor, dict):
        raise ValueError("Personel kartında arka_yuz.motor yok veya bozuk.")
    cli = motor.get("cli")
    if not isinstance(cli, str) or not cli:
        raise ValueError("Personel kartında motor.cli yok veya bozuk.")
    return cli, motor.get("model")
