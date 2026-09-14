"""Adaptörlerin ortak parçaları — döngüsel import olmasın diye ayrı dosya."""
import json


def sonuc(hata=False, maliyet=0.0, tur=0, metin="", yapisal=None):
    return {"hata": bool(hata), "maliyet": float(maliyet or 0.0), "tur": int(tur or 0),
            "metin": str(metin or ""), "yapisal": yapisal}


def _nesne(parca):
    try:
        veri = json.loads(parca)
    except ValueError:
        return None
    return veri if isinstance(veri, dict) else None


def yapisal_coz(metin):
    """Metindeki JSON nesnesini çözer; yoksa None. Sıra: tüm metin → satır satır (sondan) → ilk { … son }.
    Şema zorlamalı motorlarda metin zaten JSON'dur; bazıları birden fazla satır basar."""
    if not metin:
        return None
    if (veri := _nesne(metin.strip())) is not None:
        return veri
    for satir in reversed(metin.splitlines()):
        if (veri := _nesne(satir.strip())) is not None:
            return veri
    basi, sonu = metin.find("{"), metin.rfind("}")
    if basi < 0 or sonu <= basi:
        return None
    return _nesne(metin[basi:sonu + 1])


def bozuk(stdout, motor):
    """Çıktı JSON değilse: hata, son 2000 karakter metin."""
    return sonuc(hata=True, metin=f"{motor} çıktısı çözümlenemedi: " + (stdout or "")[-2000:])
