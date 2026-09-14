"""agy — Antigravity CLI. Maliyet raporlamaz, araç kısıtı yok; json-schema ve effort destekler."""
import json

from ._ortak import bozuk, sonuc, yapisal_coz

YETENEK = {"maliyet_raporlar": False, "arac_kisiti": False, "json_sema": True, "tur_tavani": False}


def komut(istem, ayarlar):
    komut_ = ["agy", "-p", istem, "--output-format", "json", "--mode", "accept-edits",
              "--dangerously-skip-permissions"]
    if ayarlar.get("model"):
        komut_.extend(["--model", str(ayarlar["model"])])
    if ayarlar.get("effort"):
        komut_.extend(["--effort", str(ayarlar["effort"])])
    if ayarlar.get("json_sema"):
        komut_.extend(["--json-schema", json.dumps(ayarlar["json_sema"], ensure_ascii=False)])
    return komut_


def cozumle(stdout):
    try:
        veri = json.loads(stdout or "")
    except ValueError:
        return bozuk(stdout, "agy")
    metin = veri.get("response") or ""
    if not isinstance(metin, str):
        metin = json.dumps(metin, ensure_ascii=False)
    # --json-schema verildiyse CLI `structured_output` alanını doldurur; yoksa metinden çözülür.
    yapisal = veri.get("structured_output")
    if not isinstance(yapisal, dict):
        yapisal = yapisal_coz(metin)
    return sonuc(hata=veri.get("status") != "SUCCESS", tur=veri.get("num_turns") or 1,
                 metin=metin, yapisal=yapisal)
