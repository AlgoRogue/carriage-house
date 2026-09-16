"""codex — OpenAI Codex CLI. JSONL olay akışı; şema dosyadan (`--output-schema`), araç kısıtı yok."""
import json

from ._ortak import bozuk, sonuc, yapisal_coz

YETENEK = {"maliyet_raporlar": False, "arac_kisiti": False, "json_sema": True, "tur_tavani": False}


def komut(istem, ayarlar):
    komut_ = ["codex", "exec", istem, "--json", "--dangerously-bypass-approvals-and-sandbox"]
    if ayarlar.get("model"):
        komut_.extend(["-m", str(ayarlar["model"])])
    # codex şemayı dosyadan okur; sürücü `sema_dosyasi`nı yazıp yolunu verir.
    if ayarlar.get("json_sema") and ayarlar.get("sema_dosyasi"):
        komut_.extend(["--output-schema", str(ayarlar["sema_dosyasi"])])
    return komut_


def cozumle(stdout):
    tur, metinler, hata, gordu, oturum = 0, [], False, False, None
    for satir in (stdout or "").splitlines():
        satir = satir.strip()
        if not satir:
            continue
        try:
            olay = json.loads(satir)
        except ValueError:
            continue
        if not isinstance(olay, dict):
            continue
        gordu = True
        tip = olay.get("type")
        if tip == "thread.started":
            oturum = olay.get("thread_id")
        elif tip == "turn.completed":
            tur += 1
        elif tip == "item.completed":
            oge = olay.get("item") or {}
            if oge.get("type") == "agent_message" and oge.get("text"):
                metinler.append(oge["text"])
        elif tip == "error":
            hata = True
    if not gordu:
        return bozuk(stdout, "codex")
    metin = "\n\n".join(metinler)
    # Şema verildiyse son ajan mesajı JSON'dur.
    return sonuc(hata=hata or not metinler, tur=tur or 1, metin=metin,
                 yapisal=yapisal_coz(metinler[-1]) if metinler else None, oturum=oturum)
