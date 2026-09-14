#!/usr/bin/env python3
"""Şirketin tek ayar dosyası — mesai, tavanlar, yollar, anahtarlar.

Bütün betikler buradan okur; hiçbir sayı ikinci bir yerde yazılmaz.
Anahtarlar repo kökündeki `.env` dosyasındadır (`.env.example` kopyası) ve git'e girmez.
"""
import json
import os
import re
from datetime import datetime, timedelta
from pathlib import Path

KOK = Path(__file__).resolve().parents[1]
TAKIMLAR = KOK / "takimlar"
INCREMENT = KOK / "increment"
ENV_DOSYASI = KOK / ".env"
MOTORLAR = ("claude", "agy", "codex", "grok")

# --- mesai — bugün uygulanmıyor (tetik insan); ileride zamanlayıcı increment'i için duruyor ----------
MESAI_BASLANGIC = 9   # dahil
MESAI_BITIS = 23      # hariç
MESAI_METNI = f"{MESAI_BASLANGIC:02d}:00-{MESAI_BITIS:02d}:00"

# --- tavanlar (ANAYASA 4) --------------------------------------------------
KOSU_BUTCESI_USD = 2.0          # tek koşunun para tavanı — yalnız maliyet raporlayan motorda (claude) uygulanır
KOSU_SURESI_SN = 15 * 60        # tek koşunun süre tavanı — her motorda
KOSU_TUR_TAVANI = 40            # tur tavanı — destekleyen motorda (grok)
GUNLUK_KOSU_TAVANI = 6          # takım başına gün — her motorda
GUNLUK_MALIYET_TAVANI_USD = 10.0  # tüm şirket, gün — raporlanan USD toplamı

ENV_SATIRI = re.compile(r"^\s*(?:export\s+)?([A-Za-z_][A-Za-z0-9_]*)\s*=\s*(.*?)\s*$")


def simdi_iso():
    return datetime.now().astimezone().isoformat(timespec="seconds")


# --- anahtarlar ------------------------------------------------------------

def env_yukle(yol=None):
    """`.env` dosyasını sözlük olarak okur; `export` ve tırnak toleranslı. Yoksa boş sözlük."""
    try:
        satirlar = Path(yol or ENV_DOSYASI).read_text(encoding="utf-8").splitlines()
    except OSError:
        return {}
    sonuc = {}
    for satir in satirlar:
        if satir.lstrip().startswith("#"):
            continue
        eslesme = ENV_SATIRI.match(satir)
        if eslesme:
            sonuc[eslesme.group(1)] = eslesme.group(2).strip("'\"")
    return sonuc


def ortam_yukle(yol=None):
    """`.env` içeriğini ortama ekler; zaten tanımlı değişkeni ezmez. Ortamın kopyasını döner."""
    for anahtar, deger in env_yukle(yol).items():
        os.environ.setdefault(anahtar, deger)
    return dict(os.environ)


def eksik_anahtarlar(gerekli, ortam=None):
    ortam = ortam if ortam is not None else os.environ
    return [a for a in gerekli if not ortam.get(a)]


# --- mesai -----------------------------------------------------------------

def mesaide_mi(simdi=None):
    an = simdi or datetime.now()
    return MESAI_BASLANGIC <= an.hour < MESAI_BITIS


def sonraki_mesai(simdi=None):
    an = simdi or datetime.now()
    aday = an.replace(hour=MESAI_BASLANGIC, minute=0, second=0, microsecond=0)
    return aday if aday > an else aday + timedelta(days=1)


# --- takim.md frontmatter --------------------------------------------------

def _deger(ham):
    ham = ham.strip()
    if ham.startswith("[") and ham.endswith("]"):
        ic = ham[1:-1].strip()
        return [p.strip().strip("'\"") for p in ic.split(",")] if ic else []
    return ham.strip("'\"")


def frontmatter(metin):
    """Basit YAML frontmatter: `anahtar: değer` ve `[a, b]` listeleri. (fm, gövde) döner."""
    if not metin.startswith("---"):
        return {}, metin
    parcalar = metin.split("---", 2)
    if len(parcalar) < 3:
        return {}, metin
    fm = {}
    for satir in parcalar[1].splitlines():
        if ":" not in satir or satir.lstrip().startswith("#"):
            continue
        anahtar, ham = satir.split(":", 1)
        fm[anahtar.strip()] = _deger(ham)
    return fm, parcalar[2].lstrip("\n")


def takim_bilgisi(takim, kok=None):
    """`takimlar/<takim>/takim.md` frontmatter'ı; dosya yoksa None."""
    yol = Path(kok or KOK) / "takimlar" / takim / "takim.md"
    if not yol.is_file():
        return None
    fm, _ = frontmatter(yol.read_text(encoding="utf-8"))
    return fm


# --- durum.json ------------------------------------------------------------

def durum_yolu(takim, kok=None):
    return Path(kok or KOK) / "takimlar" / takim / "durum.json"


def durum_oku(takim, kok=None):
    try:
        return json.loads(durum_yolu(takim, kok).read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}


def durum_guncelle(takim, yama, kok=None):
    """Yeni sözlük yazar (immutable birleştirme); yazılan durumu döner."""
    yol = durum_yolu(takim, kok)
    yeni = {**durum_oku(takim, kok), **yama}
    yol.parent.mkdir(parents=True, exist_ok=True)
    yol.write_text(json.dumps(yeni, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return yeni


# --- increment/evre.json (ANAYASA 2: tek aktif increment) -------------------

BOS_EVRE = {"increment_id": None, "evre": "bos", "bekleyen_onay": None,
            "motor": {"insaat": None, "bekci": None}, "talep": None, "kapsam_sapmasi": [], "gecmis": []}


def evre_yolu(kok=None):
    return Path(kok or KOK) / "increment" / "evre.json"


def evre_oku(kok=None):
    try:
        return {**BOS_EVRE, **json.loads(evre_yolu(kok).read_text(encoding="utf-8"))}
    except (OSError, ValueError):
        return dict(BOS_EVRE)


def evre_guncelle(yama, olay, kok=None):
    """Evreyi yamalar, geçmişe tarihli olay satırı ekler, yazar ve yeni evreyi döner."""
    eski = evre_oku(kok)
    yeni = {**eski, **yama, "gecmis": [*eski.get("gecmis", []), {"zaman": simdi_iso(), "olay": olay}]}
    yol = evre_yolu(kok)
    yol.parent.mkdir(parents=True, exist_ok=True)
    yol.write_text(json.dumps(yeni, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return yeni


def increment_klasoru(increment_id, kok=None):
    return Path(kok or KOK) / "increment" / str(increment_id)


if __name__ == "__main__":
    an = datetime.now().astimezone()
    durum = "içinde" if mesaide_mi(an) else "dışında"
    print(f"{an:%Y-%m-%d %H:%M} — mesai {durum} ({MESAI_METNI}), sonraki açılış {sonraki_mesai(an):%a %H:%M}")
    print(f"tavanlar: koşu {KOSU_BUTCESI_USD} USD / {KOSU_SURESI_SN // 60} dk / {KOSU_TUR_TAVANI} tur · "
          f"takım günde {GUNLUK_KOSU_TAVANI} koşu · şirket günde {GUNLUK_MALIYET_TAVANI_USD} USD")
    e = evre_oku()
    print(f"evre: {e['evre']} · increment: {e['increment_id'] or '-'} · bekleyen onay: {e['bekleyen_onay'] or '-'}"
          f" · .env: {'var' if ENV_DOSYASI.exists() else 'yok'}")
