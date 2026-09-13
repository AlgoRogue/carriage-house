#!/usr/bin/env python3
"""Telegram gelen kutusu — bota attığın linkleri okur (getUpdates, stdlib, bağımlılık yok).

Kullanım:
  python3 bin/telegram_oku.py --chat-id-bul   # bota bir mesaj at, sonra bunu koş, çıkanı .env'e yaz
  python3 bin/telegram_oku.py --son 5         # son mesajları bas (durum değişmez)
  python3 bin/telegram_oku.py --isle          # yeni mesajları takimlar/x-icerik/gelen/ altına yaz

Anahtarlar `.env`'de: TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID. Yalnızca kendi chat id'nden gelen
mesajlar işlenir — bot'a başkası yazarsa görmezden gelinir.

Offset: en son işlenen `update_id` `takimlar/x-icerik/durum.json` → `sayaclar.telegram_son_update`
alanında durur. Telegram bir güncellemeyi `offset` ile onaylandıktan sonra bir daha vermez;
bu yüzden `--son` offset'i ilerletmez, `--isle` ilerletir.
"""
import json
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import ayar  # noqa: E402

TAKIM = "x-icerik"
URL = re.compile(r"https?://\S+")


def _api(token, yontem, **parametreler):
    sorgu = urllib.parse.urlencode({k: v for k, v in parametreler.items() if v is not None})
    istek = urllib.request.Request(f"https://api.telegram.org/bot{token}/{yontem}?{sorgu}",
                                   headers={"User-Agent": "a-sirketi/1.0"})
    try:
        # long-poll: Telegram `timeout` saniye bekletir, sokete üstüne pay bırakılır
        with urllib.request.urlopen(istek, timeout=20 + int(parametreler.get("timeout") or 0)) as yanit:
            veri = json.loads(yanit.read().decode("utf-8"))
    except (urllib.error.URLError, TimeoutError, ValueError, OSError) as exc:
        print(f"telegram: ulaşılamadı — {type(exc).__name__}", file=sys.stderr)
        return []
    return veri.get("result", []) if veri.get("ok") else []


def guncellemeleri_cek(token, offset=None, bekleme=0):
    """`bekleme` saniye long-poll bekler (0 ise anında döner). `bin/telegram_dinle.py` 15 verir."""
    return _api(token, "getUpdates", offset=offset, timeout=bekleme, allowed_updates='["message"]')


def chat_idleri(guncellemeler):
    gorulen = []
    for g in guncellemeler:
        cid = (g.get("message") or {}).get("chat", {}).get("id")
        if cid is not None and cid not in gorulen:
            gorulen.append(cid)
    return gorulen


def _mesaj(g):
    m = g.get("message") or {}
    metin = m.get("text") or m.get("caption") or ""
    zaman = datetime.fromtimestamp(m.get("date", 0), tz=timezone.utc).astimezone()
    return {"update_id": g["update_id"], "zaman": zaman.isoformat(timespec="seconds"), "metin": metin,
            "linkler": [l.rstrip(".,)") for l in URL.findall(metin)], "not": URL.sub("", metin).strip()}


def mesajlari_ayikla(guncellemeler, chat_id):
    return [_mesaj(g) for g in guncellemeler
            if (g.get("message") or {}).get("chat", {}).get("id") == chat_id and "update_id" in g]


def isle(kok, guncellemeler, chat_id):
    """Yeni mesajları `gelen/` altına yazar, offset'i durum.json'a işler. Yazılan yolları döner."""
    durum = ayar.durum_oku(TAKIM, kok)
    son = int((durum.get("sayaclar") or {}).get("telegram_son_update", 0))
    gelen = Path(kok) / "takimlar" / TAKIM / "gelen"
    gelen.mkdir(parents=True, exist_ok=True)
    yazilan = []
    for mesaj in mesajlari_ayikla(guncellemeler, chat_id):
        if mesaj["update_id"] <= son:
            continue
        yol = gelen / f"{mesaj['zaman'][:10]}-{mesaj['update_id']}.json"
        yol.write_text(json.dumps(mesaj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        yazilan.append(yol)
        son = mesaj["update_id"]
    ayar.durum_guncelle(TAKIM, {"sayaclar": {**(durum.get("sayaclar") or {}),
                                             "telegram_son_update": son}}, kok)
    return yazilan


def main(argv):
    ayar.ortam_yukle()
    token = os.environ.get("TELEGRAM_BOT_TOKEN")
    if not token:
        print("TELEGRAM_BOT_TOKEN yok (.env)", file=sys.stderr)
        return 1
    if "--chat-id-bul" in argv:
        print(json.dumps({"chat_idleri": chat_idleri(guncellemeleri_cek(token))}))
        return 0
    ham_id = os.environ.get("TELEGRAM_CHAT_ID")
    if not ham_id:
        print("TELEGRAM_CHAT_ID yok (.env) — önce --chat-id-bul", file=sys.stderr)
        return 1
    chat_id = int(ham_id)
    if "--isle" in argv:
        son = int((ayar.durum_oku(TAKIM).get("sayaclar") or {}).get("telegram_son_update", 0))
        yazilan = isle(ayar.KOK, guncellemeleri_cek(token, offset=son + 1 if son else None), chat_id)
        print(json.dumps({"yeni": [y.name for y in yazilan]}, ensure_ascii=False))
        return 0
    adet = int(argv[argv.index("--son") + 1]) if "--son" in argv and len(argv) > argv.index("--son") + 1 else 5
    print(json.dumps(mesajlari_ayikla(guncellemeleri_cek(token), chat_id)[-adet:],
                     ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
