"""claude — Claude Code CLI. Maliyet raporlar, araç kısıtı ve json-schema destekler."""
import json

from ._ortak import bozuk, sonuc, yapisal_coz

YETENEK = {"maliyet_raporlar": True, "arac_kisiti": True, "json_sema": True, "tur_tavani": False}
VARSAYILAN_MODEL = "sonnet"


def komut(istem, ayarlar):
    komut_ = ["claude", "-p", istem, "--output-format", "json",
              "--model", str(ayarlar.get("model") or VARSAYILAN_MODEL),
              "--max-budget-usd", str(ayarlar.get("butce_usd")),
              "--allowedTools", ",".join(ayarlar.get("araclar") or []),
              "--permission-mode", "acceptEdits"]
    if ayarlar.get("json_sema"):
        komut_.extend(["--json-schema", json.dumps(ayarlar["json_sema"], ensure_ascii=False)])
    return komut_


def cozumle(stdout):
    try:
        veri = json.loads(stdout or "")
    except ValueError:
        return bozuk(stdout, "claude")
    metin = veri.get("result") or ""
    # --json-schema verildiyse yapısal çıktı `structured_output` alanında gelir; yoksa metinden çözülür.
    yapisal = veri.get("structured_output")
    if not isinstance(yapisal, dict):
        yapisal = yapisal_coz(metin if isinstance(metin, str) else json.dumps(metin))
    return sonuc(hata=veri.get("is_error"), maliyet=veri.get("total_cost_usd"), tur=veri.get("num_turns"),
                 metin=metin if isinstance(metin, str) else json.dumps(metin, ensure_ascii=False),
                 yapisal=yapisal)
