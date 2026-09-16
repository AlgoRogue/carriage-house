#!/usr/bin/env python3
"""Canlı Motor dumanı — ürün durum/kart/şablon kirletmez. Unittest değil."""
from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
import tempfile
import time
from datetime import datetime, timezone
from pathlib import Path

KOK = Path(__file__).resolve().parents[2]
PERSONEL = KOK / "personel" / "CH-0001"
BIN = PERSONEL / "bin"
SCRATCH = Path(__file__).resolve().parent

sys.path.insert(0, str(BIN))
from kart_motoru import karti_ilerlet  # noqa: E402


class GercekKosucu:
    """Komutu subprocess ile çalıştırır; çağrıları ve ham stdout'u kaydeder."""

    def __init__(self, log_dir: Path, timeout_s: int = 600):
        self.log_dir = log_dir
        self.timeout_s = timeout_s
        self.cagrilar: list[dict] = []
        log_dir.mkdir(parents=True, exist_ok=True)

    def __call__(self, komut):
        n = len(self.cagrilar) + 1
        t0 = time.monotonic()
        kayit = {
            "sira": n,
            "argv0": komut[0] if komut else "",
            "komut_ozet": list(komut[:6]) + (["…"] if len(komut) > 6 else []),
            "p_yuku_uzunluk": len(komut[2]) if len(komut) > 2 else 0,
            "baslangic": datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds"),
        }
        print(f"\n=== Motor çağrısı {n} ===", flush=True)
        print("argv:", " ".join(str(x) for x in komut[:8]),
              ("…" if len(komut) > 8 else ""), flush=True)
        try:
            sonuc = subprocess.run(
                list(komut),
                cwd=str(KOK),
                capture_output=True,
                text=True,
                timeout=self.timeout_s,
            )
            kayit["returncode"] = sonuc.returncode
            kayit["sure_s"] = round(time.monotonic() - t0, 1)
            kayit["stdout_len"] = len(sonuc.stdout or "")
            kayit["stderr_len"] = len(sonuc.stderr or "")
            (self.log_dir / f"cagri-{n}-stdout.txt").write_text(
                sonuc.stdout or "", encoding="utf-8")
            (self.log_dir / f"cagri-{n}-stderr.txt").write_text(
                sonuc.stderr or "", encoding="utf-8")
            (self.log_dir / f"cagri-{n}-p.txt").write_text(
                komut[2] if len(komut) > 2 else "", encoding="utf-8")
            print(f"returncode={sonuc.returncode} sure={kayit['sure_s']}s "
                  f"stdout={kayit['stdout_len']}B", flush=True)
            if sonuc.returncode != 0:
                print("stderr başı:", (sonuc.stderr or "")[:400], flush=True)
            self.cagrilar.append(kayit)
            return sonuc.stdout or ""
        except OSError as exc:
            kayit["oserror"] = str(exc)
            kayit["sure_s"] = round(time.monotonic() - t0, 1)
            self.cagrilar.append(kayit)
            raise
        except subprocess.TimeoutExpired as exc:
            kayit["timeout"] = True
            kayit["sure_s"] = round(time.monotonic() - t0, 1)
            self.cagrilar.append(kayit)
            raise OSError(f"Motor zaman aşımı ({self.timeout_s}s)") from exc


def main() -> int:
    ap = argparse.ArgumentParser(description="Canlı Motor dumanı")
    ap.add_argument("--cli", default="claude")
    ap.add_argument("--model", default=None,
                    help="Kart model alanı; boşsa CLI varsayılanına bırak (None)")
    ap.add_argument("--is-id", default=None)
    ap.add_argument("--timeout", type=int, default=600)
    args = ap.parse_args()

    cli = args.cli
    model = args.model
    is_id = args.is_id or f"DUMAN-{cli.upper()}"
    log_dir = SCRATCH / f"duman-logs-{cli}"
    rapor = SCRATCH / f"DUMAN-SONUC-{cli}.md"

    prod_kart = PERSONEL / "kart.json"
    prod_durum = PERSONEL / "durum.json"
    prod_iskelet = PERSONEL / "aksiyon-iskeleti.json"
    sablon_kok = PERSONEL / "sablonlar"
    kart_once = prod_kart.read_bytes()
    durum_once = prod_durum.read_bytes()
    iskelet_once = prod_iskelet.read_bytes()
    sablon_once = {p.name: p.read_bytes()
                   for p in sorted(sablon_kok.iterdir()) if p.is_file()}

    if shutil.which(cli) is None:
        print(f"PATH'te {cli} yok — duman iptal.", flush=True)
        return 2

    gecici = tempfile.mkdtemp(prefix=f"duman-{cli}-")
    kok = Path(gecici)
    durum_yolu = kok / "durum.json"
    isler_kok = kok / "isler"
    kart_yolu = kok / "kart.json"
    shutil.copyfile(prod_durum, durum_yolu)
    kart = json.loads(prod_kart.read_text(encoding="utf-8"))
    motor = kart.setdefault("arka_yuz", {}).setdefault("motor", {})
    motor["cli"] = cli
    if model is None:
        motor.pop("model", None)
    else:
        motor["model"] = model
    kart_yolu.write_text(json.dumps(kart, ensure_ascii=False, indent=2) + "\n",
                         encoding="utf-8")

    durum = json.loads(durum_yolu.read_text(encoding="utf-8"))
    if durum.get("durum") != "bos":
        durum = {
            "personel_numarasi": "CH-0001",
            "durum": "bos",
            "is_id": None,
            "son_sinyal": None,
            "not": "duman kopyası",
        }
        durum_yolu.write_text(json.dumps(durum, ensure_ascii=False, indent=2) + "\n",
                              encoding="utf-8")

    if log_dir.exists():
        shutil.rmtree(log_dir)
    kosucu = GercekKosucu(log_dir, timeout_s=args.timeout)

    print(f"cli={cli} model={model!r} is_id={is_id}", flush=True)
    print(f"geçici kök: {kok}", flush=True)
    print(f"kart motor: {motor}", flush=True)
    t0 = time.monotonic()
    try:
        sonuc = karti_ilerlet(
            kart_yolu, kosucu, is_id=is_id, durum_yolu=str(durum_yolu),
            isler_kok=isler_kok)
        hata = None
    except Exception as exc:  # noqa: BLE001 — duman raporu
        sonuc = None
        hata = f"{type(exc).__name__}: {exc}"
        print("İSTİSNA:", hata, flush=True)
    sure = round(time.monotonic() - t0, 1)

    durum_son = json.loads(durum_yolu.read_text(encoding="utf-8"))
    plan = isler_kok / is_id / "plan.md"
    paket = isler_kok / is_id / "paket.md"
    plan_metin = plan.read_text(encoding="utf-8") if plan.is_file() else None
    paket_metin = paket.read_text(encoding="utf-8") if paket.is_file() else None

    koruma = {
        "kart": prod_kart.read_bytes() == kart_once,
        "durum": prod_durum.read_bytes() == durum_once,
        "iskelet": prod_iskelet.read_bytes() == iskelet_once,
        "sablonlar": all(
            (sablon_kok / ad).read_bytes() == bayt
            for ad, bayt in sablon_once.items()
        ) and set(p.name for p in sablon_kok.iterdir() if p.is_file()) == set(sablon_once),
    }

    mutlu = (
        sonuc is not None
        and sonuc.baslangic_durumu == "bos"
        and sonuc.bitis_durumu == "park"
        and list(sonuc.izlenen_yol) == [
            "bos", "is_alindi", "planlaniyor", "plan_hazir",
            "delege_hazirlaniyor", "paket_hazir", "park",
        ]
        and plan_metin is not None and plan_metin.strip() != ""
        and paket_metin is not None and paket_metin.strip() != ""
        and len(kosucu.cagrilar) == 2
        and all(koruma.values())
    )

    # Takılma teşhisi
    takilma = []
    if hata:
        takilma.append(f"istisna: {hata}")
    if sonuc is not None and sonuc.bitis_durumu != "park":
        takilma.append(
            f"bitiş={sonuc.bitis_durumu} yol={' → '.join(sonuc.izlenen_yol)}")
    if len(kosucu.cagrilar) != 2:
        takilma.append(f"motor çağrı sayısı={len(kosucu.cagrilar)} (beklenen 2)")
    for c in kosucu.cagrilar:
        if c.get("returncode") not in (0, None):
            takilma.append(f"çağrı #{c['sira']} rc={c.get('returncode')}")
        if c.get("oserror"):
            takilma.append(f"çağrı #{c['sira']} OSError={c['oserror']}")
        if c.get("timeout"):
            takilma.append(f"çağrı #{c['sira']} TIMEOUT")
    if plan_metin is None or not str(plan_metin).strip():
        takilma.append("plan.md yok/boş")
    if paket_metin is None or not str(paket_metin).strip():
        takilma.append("paket.md yok/boş")
    if not all(koruma.values()):
        takilma.append("ürün koruması bozuldu: "
                       + ", ".join(k for k, v in koruma.items() if not v))

    satirlar = [
        f"# Canlı Motor dumanı — {cli}",
        "",
        f"**Zaman:** {datetime.now(timezone.utc).astimezone().isoformat(timespec='seconds')}",
        f"**Süre:** {sure}s",
        f"**cli / model:** `{cli}` / `{model}`",
        f"**is_id:** `{is_id}`",
        f"**Geçici kök:** `{kok}`",
        f"**Mutlu yol:** {'EVET' if mutlu else 'HAYIR'}",
        f"**Takılma:** {('yok' if mutlu else '; '.join(takilma) or 'bilinmiyor')}",
        "",
        "## Sürücü sonucu",
        "",
    ]
    if sonuc is None:
        satirlar.append(f"- İstisna: `{hata}`")
    else:
        satirlar.extend([
            f"- başlangıç: `{sonuc.baslangic_durumu}`",
            f"- bitiş: `{sonuc.bitis_durumu}`",
            f"- yol: `{' → '.join(sonuc.izlenen_yol)}`",
        ])
    satirlar.extend([
        "",
        "## Geçici durum.json (ürün değil)",
        "",
        "```json",
        json.dumps(durum_son, ensure_ascii=False, indent=2),
        "```",
        "",
        "## Motor çağrıları",
        "",
        f"Sayı: **{len(kosucu.cagrilar)}** (beklenen 2)",
        "",
    ])
    for c in kosucu.cagrilar:
        satirlar.append(
            f"- #{c['sira']}: argv0=`{c.get('argv0')}` sure={c.get('sure_s')}s "
            f"rc={c.get('returncode')} stdout={c.get('stdout_len')}B "
            f"p_len={c.get('p_yuku_uzunluk')}"
            + (f" OSError={c['oserror']}" if "oserror" in c else "")
            + (" TIMEOUT" if c.get("timeout") else ""))
    satirlar.extend([
        "",
        "## Artefaktlar",
        "",
        f"- `plan.md`: {'var, ' + str(len(plan_metin)) + ' karakter' if plan_metin is not None else 'YOK'}",
        f"- `paket.md`: {'var, ' + str(len(paket_metin)) + ' karakter' if paket_metin is not None else 'YOK'}",
        "",
    ])
    if plan_metin is not None:
        satirlar.extend(["### plan.md (ilk 800 karakter)", "", "```",
                         plan_metin[:800], "```", ""])
    if paket_metin is not None:
        satirlar.extend(["### paket.md (ilk 800 karakter)", "", "```",
                         paket_metin[:800], "```", ""])
    satirlar.extend([
        "## Ürün koruması (byte-eşit)",
        "",
        *[f"- {k}: {'OK' if v else 'BOZULDU'}" for k, v in koruma.items()],
        "",
        "## Loglar",
        "",
        f"`{log_dir}`",
        "",
        "## Not",
        "",
        "Acceptance unittest değil. Codex bu turda yok (kota).",
    ])
    rapor.write_text("\n".join(satirlar) + "\n", encoding="utf-8")
    print("\n==== ÖZET ====", flush=True)
    print(f"cli={cli} mutlu_yol={mutlu} bitis={getattr(sonuc, 'bitis_durumu', None)} "
          f"cagri={len(kosucu.cagrilar)} sure={sure}s", flush=True)
    if not mutlu:
        print("takilma:", "; ".join(takilma) or "?", flush=True)
    print(f"rapor: {rapor}", flush=True)
    return 0 if mutlu else 1


if __name__ == "__main__":
    raise SystemExit(main())
