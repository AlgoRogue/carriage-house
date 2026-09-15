#!/usr/bin/env python3
"""Bekçi katman A — her koşuyu LLM'siz denetleyen sert kontrol (ANAYASA 3, 5). Stop hook + doğrudan mod.

Üç kontrol, üçü de deterministik:
  1. Koşu kaydı boş mu → red.
  2. Koşu kaydında gizli veri deseni (API anahtarı, token, e-posta) var mı → red.
  3. İnsanın dosyalarına koşu sırasında dokunulmuş mu (mtime > koşu başlangıcı) → red.
     İnsanın dosyaları: ANAYASA.md · hedef.md · kararlar.md · kapsam-disi.md · sema/ · takimlar/*/kurallar.md ·
     increment/*/sozlesme.onayli.json · bin/kapi.py · bin/dongu.py

Katman B (sözleşmeye karşı PASS/FAIL, LLM, ters motor) bir takımdır: `takimlar/sistem-bekci`.

Modlar:
  Stop hook (stdin JSON): takım, koşu dosyası ve başlangıç `SIRKET_TAKIM` / `SIRKET_KOSU` /
      `SIRKET_KOSU_BASLANGIC` ortamından okunur. red → {"decision":"block","reason":...} (en fazla 2 kez).
  `--dogrudan <takim> [kosu]`: hook dışından denetle, kararı JSON bas.

Sözleşme: her zaman çıkış 0 — bekçi oturumu düşürmez.
"""
import json
import os
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import ayar  # noqa: E402

KOK = ayar.KOK
MAKS_RED = 2

ON_KONTROL = {
    "e-posta adresi": re.compile(r"[\w.+-]+@[\w-]+\.[\w.-]+"),
    "OpenAI anahtarı": re.compile(r"\bsk-[A-Za-z0-9_-]{6,}"),
    "Anthropic anahtarı": re.compile(r"\bsk-ant-[A-Za-z0-9_-]{6,}"),
    "xAI anahtarı": re.compile(r"\bxai-[A-Za-z0-9]{6,}"),
    "Google anahtarı": re.compile(r"\bAIza[0-9A-Za-z_-]{6,}"),
    "GitHub token": re.compile(r"\bgh[pousr]_[A-Za-z0-9]{6,}"),
    "Telegram bot token": re.compile(r"\b\d{8,}:[A-Za-z0-9_-]{20,}"),
}
# İnsanın dosyaları — glob desenleri (ANAYASA §5)
KORUNAN = ["ANAYASA.md", "hedef.md", "kararlar.md", "kapsam-disi.md", "sema/*.json",
           "takimlar/*/kurallar.md", "increment/*/sozlesme.onayli.json", "bin/kapi.py", "bin/dongu.py"]


def _oku(yol, varsayilan=""):
    try:
        return Path(yol).read_text(encoding="utf-8")
    except OSError:
        return varsayilan


def on_kontrol(metin):
    """LLM'siz gizli-veri kontrolü. İhlal adları listesi döner; boş liste = temiz."""
    return [ad for ad, desen in ON_KONTROL.items() if desen.search(metin or "")]


def korunan_dokunulan(kok, baslangic):
    """Koşu başlangıcından sonra değişmiş korunan dosyalar (repo köküne göre yol)."""
    if not baslangic:
        return []
    kok = Path(kok)
    dokunulan = []
    for desen in KORUNAN:
        for yol in kok.glob(desen):
            try:
                if yol.is_file() and yol.stat().st_mtime > float(baslangic):
                    dokunulan.append(str(yol.relative_to(kok)))
            except OSError:
                continue
    return sorted(dokunulan)


def karar_ver(kok, kosu, baslangic=None):
    """Katman A kararı: {karar: kabul|red, gerekce, ihlal_edilen_kural}."""
    metin = _oku(kosu)
    if not metin.strip():
        return {"karar": "red", "gerekce": "koşu kaydı boş — ajan SIRKET_KOSU dosyasını yazmadı",
                "ihlal_edilen_kural": "koşu kaydı"}
    if ihlaller := on_kontrol(metin):
        return {"karar": "red", "gerekce": "gizli veri: " + ", ".join(ihlaller) + " koşu kaydında geçiyor",
                "ihlal_edilen_kural": "gizli veri"}
    if dokunulan := korunan_dokunulan(kok, baslangic):
        return {"karar": "red", "gerekce": "insanın dosyasına dokunuldu: " + ", ".join(dokunulan),
                "ihlal_edilen_kural": "ANAYASA §5"}
    return {"karar": "kabul", "gerekce": "katman A temiz: kayıt dolu, gizli veri yok, korunan dosya değişmedi",
            "ihlal_edilen_kural": None}


def _kaydet(kok, takim, kosu, karar):
    """Kararı koşu kaydının altına, durum.json'a ve bekçi telemetrisine yazar."""
    durum = ayar.durum_oku(takim, kok)
    onceki = dict(durum.get("bekci") or {})
    red = int(onceki.get("red_sayisi_7g", 0)) + (1 if karar["karar"] == "red" else 0)
    ayar.durum_guncelle(takim, {"bekci": {**onceki, "son_karar": karar["karar"], "gerekce": karar["gerekce"],
                                          "red_sayisi_7g": red, "zaman": ayar.simdi_iso()}}, kok)
    with open(kosu, "a", encoding="utf-8") as dosya:
        dosya.write(f"\n\n## Bekçi\n- karar: **{karar['karar']}**\n- gerekçe: {karar['gerekce']}\n"
                    f"- ihlal edilen kural: {karar.get('ihlal_edilen_kural') or '-'}\n")
    telemetri = Path(kok) / "takimlar" / "bekci-telemetri.jsonl"
    with open(telemetri, "a", encoding="utf-8") as dosya:
        dosya.write(json.dumps({"zaman": ayar.simdi_iso(), "takim": takim, "kosu": Path(kosu).name, **karar},
                               ensure_ascii=False) + "\n")


def denetle(kok, takim, kosu, baslangic=None):
    """Bir koşu kaydını denetler, kararı kaydeder ve döner."""
    karar = karar_ver(kok, kosu, baslangic)
    _kaydet(Path(kok), takim, kosu, karar)
    return karar


def _deneme_sayaci(kosu):
    return Path(kosu).parent / ".bekci-deneme"


def engelle_mi(kok, takim, kosu, baslangic=None):
    """Stop hook kararı: red ise ve deneme hakkı kaldıysa True (ajanı düzeltmeye gönder)."""
    karar = denetle(kok, takim, kosu, baslangic)
    sayac = _deneme_sayaci(kosu)
    if karar["karar"] != "red":
        sayac.unlink(missing_ok=True)
        return False
    deneme = int(_oku(sayac, "0").strip() or 0) + 1
    sayac.write_text(str(deneme), encoding="utf-8")
    if deneme >= MAKS_RED:
        sayac.unlink(missing_ok=True)
        return False
    return True


def _son_kosu(kok, takim):
    kosular = sorted((Path(kok) / "takimlar" / takim / "kosu").glob("*.md"))
    return kosular[-1] if kosular else None


def _hook():
    try:
        veri = json.load(sys.stdin)
    except ValueError:
        veri = {}
    takim = os.environ.get("SIRKET_TAKIM")
    if not takim:
        return 0  # şirket koşusu değil — karışma
    kosu = os.environ.get("SIRKET_KOSU") or _son_kosu(KOK, takim)
    if not kosu:
        return 0
    baslangic = os.environ.get("SIRKET_KOSU_BASLANGIC")
    if veri.get("stop_hook_active"):  # ikinci durma: engelleme, ama son kararı yeniden ver
        denetle(KOK, takim, kosu, baslangic)
        _deneme_sayaci(kosu).unlink(missing_ok=True)
        return 0
    if engelle_mi(KOK, takim, kosu, baslangic):
        gerekce = (ayar.durum_oku(takim).get("bekci") or {}).get("gerekce", "")
        print(json.dumps({"decision": "block",
                          "reason": f"🛑 BEKÇİ RED: {gerekce}\nKoşu kaydını ({kosu}) düzelt, sonra bitir."},
                         ensure_ascii=False))
    return 0


def main(argv):
    if argv and argv[0] == "--dogrudan" and len(argv) > 1:
        takim = argv[1]
        kosu = Path(argv[2]) if len(argv) > 2 else _son_kosu(KOK, takim)
        if not kosu:
            print(json.dumps({"karar": "atlandi", "gerekce": "koşu dosyası yok"}, ensure_ascii=False))
            return 0
        print(json.dumps(denetle(KOK, takim, kosu), ensure_ascii=False))
        return 0
    return _hook()


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
