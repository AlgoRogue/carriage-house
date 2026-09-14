#!/usr/bin/env python3
"""Şema doğrulayıcı — stdlib, bağımlılıksız. `sema/*.schema.json` dosyalarını okur ve uygular.

Desteklenen alt küme (dört CLI'nin `--json-schema` bayrağıyla ortak):
  type · properties · required · enum · items · additionalProperties:false · minItems · minLength

Kullanım:  python3 bin/sema.py <şema-adı|yol> <json-dosya>   → hatalar satır satır, çıkış 1; temizse "OK"
Kod:       sema.yukle("teslim") → dict · sema.dogrula(sema, veri) → [hata metni]
"""
import json
import sys
from pathlib import Path

KOK = Path(__file__).resolve().parents[1]
SEMA_KLASORU = KOK / "sema"
TIPLER = {"object": dict, "array": list, "string": str, "integer": int, "number": (int, float),
          "boolean": bool, "null": type(None)}


def yukle(ad, kok=None):
    """`teslim` → sema/teslim.schema.json; doğrudan yol da kabul eder."""
    yol = Path(ad)
    if not yol.is_file():
        yol = Path(kok or KOK) / "sema" / f"{ad}.schema.json"
    return json.loads(yol.read_text(encoding="utf-8"))


def _tip_uyar(deger, tip):
    if tip == "integer" and isinstance(deger, bool):
        return False
    if tip == "number" and isinstance(deger, bool):
        return False
    beklenen = TIPLER.get(tip)
    return beklenen is not None and isinstance(deger, beklenen)


def dogrula(sema, veri, yol="$"):
    """Hata listesi döner; boş liste = geçerli."""
    hatalar = []
    tip = sema.get("type")
    if isinstance(tip, list):
        if not any(_tip_uyar(veri, t) for t in tip):
            return [f"{yol}: tip {'|'.join(tip)} bekleniyordu"]
    elif tip and not _tip_uyar(veri, tip):
        return [f"{yol}: tip {tip} bekleniyordu, {type(veri).__name__} geldi"]
    if "enum" in sema and veri not in sema["enum"]:
        hatalar.append(f"{yol}: {veri!r} şu değerlerden biri olmalı: {sema['enum']}")
    if isinstance(veri, str) and len(veri) < sema.get("minLength", 0):
        hatalar.append(f"{yol}: en az {sema['minLength']} karakter olmalı")
    if isinstance(veri, dict):
        for alan in sema.get("required", []):
            if alan not in veri:
                hatalar.append(f"{yol}.{alan}: zorunlu alan eksik")
        ozellikler = sema.get("properties", {})
        for alan, deger in veri.items():
            if alan in ozellikler:
                hatalar.extend(dogrula(ozellikler[alan], deger, f"{yol}.{alan}"))
            elif sema.get("additionalProperties") is False:
                hatalar.append(f"{yol}.{alan}: şemada olmayan alan")
    if isinstance(veri, list):
        if len(veri) < sema.get("minItems", 0):
            hatalar.append(f"{yol}: en az {sema['minItems']} öğe olmalı")
        if "items" in sema:
            for i, oge in enumerate(veri):
                hatalar.extend(dogrula(sema["items"], oge, f"{yol}[{i}]"))
    return hatalar


def main(argv):
    if len(argv) < 2:
        print(__doc__)
        return 2
    try:
        sema = yukle(argv[0])
        veri = json.loads(Path(argv[1]).read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        print(f"okunamadı: {exc}")
        return 1
    hatalar = dogrula(sema, veri)
    print("\n".join(hatalar) if hatalar else "OK")
    return 1 if hatalar else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
