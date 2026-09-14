"""Adaptörlerin ortak parçaları — döngüsel import olmasın diye ayrı dosya."""
import json


def sonuc(hata=False, maliyet=0.0, tur=0, metin="", yapisal=None):
    return {"hata": bool(hata), "maliyet": float(maliyet or 0.0), "tur": int(tur or 0),
            "metin": str(metin or ""), "yapisal": yapisal}


def yapisal_coz(metin):
    """Metnin içindeki ilk JSON nesnesini çözer; yoksa None. Şema zorlamalı motorlarda metin zaten JSON'dur."""
    if not metin:
        return None
    basi, sonu = metin.find("{"), metin.rfind("}")
    if basi < 0 or sonu <= basi:
        return None
    try:
        veri = json.loads(metin[basi:sonu + 1])
    except ValueError:
        return None
    return veri if isinstance(veri, dict) else None


def bozuk(stdout, motor):
    """Çıktı JSON değilse: hata, son 2000 karakter metin."""
    return sonuc(hata=True, metin=f"{motor} çıktısı çözümlenemedi: " + (stdout or "")[-2000:])
