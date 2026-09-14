"""grok — xAI Grok CLI. json-schema, araç kısıtı (`--tools`), tur tavanı ve maliyet (`total_cost_usd`) destekler.

Çıktı alanları camelCase (grok 1.0.30 ile doğrulandı): `text`, `structuredOutput`, `stopReason`, `sessionId`,
`num_turns`, `total_cost_usd`. `cozumle` eski/alternatif adlara da toleranslıdır.
"""
import json

from ._ortak import bozuk, sonuc, yapisal_coz

YETENEK = {"maliyet_raporlar": True, "arac_kisiti": True, "json_sema": True, "tur_tavani": True}
METIN_ALANLARI = ("text", "result", "response", "content", "message", "output")
SEMA_KURALI = ("Son cevabın, araç çağırmadan ve açıklama eklemeden, verilen JSON şemasına uyan tek bir JSON "
               "nesnesi olmalıdır. Araç kullanımı bittikten sonra bu JSON'u yaz.")
# Takım dosyaları araçları Claude adıyla yazar; grok'un yerleşik adları farklı (oturum kayıtlarından doğrulandı).
ARAC_ESLEME = {"Read": ["read_file", "list_dir"], "Write": ["write"], "Edit": ["search_replace"],
               "Glob": ["list_dir"], "Grep": ["grep"], "Bash": ["run_terminal_command"],
               "WebSearch": ["search_tool"], "WebFetch": ["search_tool"]}


def araclari_cevir(araclar):
    """Claude araç adları → grok araç adları; bilinmeyen ad olduğu gibi geçer, tekrarlar atılır."""
    sonuc_ = []
    for ad in araclar or []:
        for g in ARAC_ESLEME.get(ad, [ad]):
            if g not in sonuc_:
                sonuc_.append(g)
    return sonuc_


def komut(istem, ayarlar):
    araclar = list(ayarlar.get("araclar") or [])
    komut_ = ["grok", "-p", istem, "--output-format", "json", "--permission-mode", "acceptEdits",
              "--always-approve", "--no-subagents", "--no-plan"]
    if araclar:
        komut_.extend(["--tools", ",".join(araclari_cevir(araclar))])
    if not any(a.lower().startswith("web") for a in araclar):
        komut_.append("--disable-web-search")
    if ayarlar.get("model"):
        komut_.extend(["-m", str(ayarlar["model"])])
    if ayarlar.get("effort"):
        komut_.extend(["--effort", str(ayarlar["effort"])])
    if ayarlar.get("maks_tur"):
        komut_.extend(["--max-turns", str(ayarlar["maks_tur"])])
    if ayarlar.get("json_sema"):
        komut_.extend(["--json-schema", json.dumps(ayarlar["json_sema"], ensure_ascii=False),
                       "--rules", SEMA_KURALI])
    return komut_


def _metin(veri):
    for alan in METIN_ALANLARI:
        deger = veri.get(alan)
        if isinstance(deger, str) and deger:
            return deger
        if isinstance(deger, (dict, list)) and deger:
            return json.dumps(deger, ensure_ascii=False)
    return ""


def cozumle(stdout):
    try:
        veri = json.loads(stdout or "")
    except ValueError:
        return bozuk(stdout, "grok")
    if not isinstance(veri, dict):
        return bozuk(stdout, "grok")
    metin = _metin(veri)
    hata = bool(veri.get("is_error") or veri.get("error")) or str(veri.get("status", "")).lower() in ("error", "failed")
    yapisal = veri.get("structuredOutput") or veri.get("structured_output")
    if not isinstance(yapisal, dict):
        yapisal = yapisal_coz(metin)
    return sonuc(hata=hata or not metin, maliyet=veri.get("total_cost_usd"),
                 tur=veri.get("num_turns") or veri.get("turns") or 1, metin=metin, yapisal=yapisal,
                 oturum=veri.get("sessionId") or veri.get("session_id"))
