"""Motor adaptörleri — her CLI tek dosya, aynı üç yüz.

Her modül şunları verir:
  YETENEK  = {"maliyet_raporlar", "arac_kisiti", "json_sema", "tur_tavani"}  (bool)
  komut(istem, ayarlar) -> list[str]
      ayarlar: model, effort, araclar (list), butce_usd, json_sema (dict|None), sema_dosyasi (Path|None),
               maks_tur (int|None)
  cozumle(stdout) -> {"hata": bool, "maliyet": float, "tur": int, "metin": str, "yapisal": dict|None}

Sürücü (`bin/kos.py`) motoru adıyla alır; motorun ne olduğunu bilmez.
Bekçi motoru üreten motorun tersidir — tablo burada, kodda değil (ANAYASA §3).
"""
from . import agy, claude, codex, grok
from ._ortak import sonuc, yapisal_coz  # noqa: F401 — dışarıya da açık

MOTORLAR = {"claude": claude, "agy": agy, "codex": codex, "grok": grok}

# Üreten → denetleyen. claude üç motoru denetler; claude üretirse grok denetler (json-schema ile sıkı rapor).
TERS_MOTOR = {"codex": "claude", "agy": "claude", "grok": "claude", "claude": "grok"}


def motor_al(ad):
    """Adı bilinen motor modülü; bilinmeyen ad → KeyError (sürücü yakalar, koşuyu atlar)."""
    return MOTORLAR[str(ad).lower()]


def ters_motor(ad):
    return TERS_MOTOR[str(ad).lower()]
