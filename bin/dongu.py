#!/usr/bin/env python3
"""Döngü — bir işi sonuna kadar götüren otomat. İnsan adına çalışır; ara onay istemez.

  python3 bin/dongu.py "<tek cümle iş>" [--motor grok] [--deneme 2] [--zorla]
  python3 bin/dongu.py --devam [--motor grok] [--deneme 2] [--zorla]      mevcut evreden sürdür

Zincir: talep → sevk (sözleşme) → onayla (otomatik) → inşaat → bekçi → PASS ise DUR (insan: yayinla | revize)
                                                     └─ FAIL ise yeniden (en fazla --deneme kez) ─┘
Her adım yine `bin/kos.py`'nin tek koşusudur; evreyi artefakt doğrulaması ilerletir. Bu betik yalnız
"sıradaki komut ne?" sorusuna bakıp onu çalıştırır. LLM çağırmaz; motorları kos.py başlatır.

Durma sebepleri (çıkış 1): sevk sözleşme üretmedi (kapsam-dışı / hata), koşu hata/red/geçersiz, deneme tavanı,
adım tavanı. Başarı (çıkış 0): evre `yayin-bekliyor` — karar insanın.
"""
import fcntl
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import ayar  # noqa: E402
import kapi  # noqa: E402
import kos  # noqa: E402

KOK = ayar.KOK
MAKS_ADIM = 12
VARSAYILAN_DENEME = 2


def _son(takim, kok=None):
    d = ayar.durum_oku(takim, kok)
    return d.get("son_sonuc"), d.get("son_sebep")


def adim(motor=None, maks_deneme=VARSAYILAN_DENEME, zorla=False, kok=None):
    """Evreye bakar, tek adım atar. (devam_mi, mesaj) döner."""
    evre = ayar.evre_oku(kok)
    e, bekleyen = evre["evre"], evre.get("bekleyen_onay")
    if e in ("bos", "yayinlandi", "red"):
        return False, "açık iş yok — python3 bin/dongu.py \"<iş>\""
    if e == "sozlesme" and bekleyen is None:
        kos.kos("sistem-sevk", zorla=zorla)
        sonuc, sebep = _son("sistem-sevk", kok)
        if sonuc != "tamam":
            return False, f"sevk sözleşme üretmedi ({sonuc}): {sebep or 'koşu kaydına bak'}"
        return True, "sözleşme kesildi"
    if e == "sozlesme" and bekleyen == "sozlesme":
        kod, mesaj = kapi.onayla(motor, kok)
        return (kod == 0), mesaj.splitlines()[0]
    if e == "insaat":
        kos.kos("sistem-insaat", zorla=zorla)
        sonuc, sebep = _son("sistem-insaat", kok)
        if sonuc != "tamam":
            return False, f"inşaat bitmedi ({sonuc}): {sebep or 'koşu kaydına bak'}"
        return True, "inşaat teslim etti"
    if e == "bekci":
        kos.kos("sistem-bekci", zorla=zorla)
        sonuc, sebep = _son("sistem-bekci", kok)
        if sonuc != "tamam":
            return False, f"bekçi rapor üretmedi ({sonuc}): {sebep or 'koşu kaydına bak'}"
        return True, "bekçi karar verdi"
    if e == "fail":
        deneme = int(evre.get("deneme") or 0)
        if deneme >= maks_deneme:
            return False, f"bekçi {deneme + 1} denemede de FAIL — İNSAN KARARI: kapi.py revize \"…\" | yeniden | red"
        kod, mesaj = kapi.yeniden(kok)
        return (kod == 0), mesaj
    if e == "yayin-bekliyor":
        return False, "PASS — İNSAN KARARI: python3 bin/kapi.py yayinla | python3 bin/kapi.py revize \"…\""
    return False, f"bilinmeyen evre: {e}"


def dongu(talep=None, motor=None, maks_deneme=VARSAYILAN_DENEME, zorla=False, kok=None):
    if talep:
        kod, mesaj = kapi.talep(talep, kok)
        print(mesaj)
        if kod != 0:
            return 1
    for _ in range(MAKS_ADIM):
        devam, mesaj = adim(motor, maks_deneme, zorla, kok)
        print(f"→ {mesaj}")
        if not devam:
            break
    else:
        print("→ adım tavanı; döngü durdu")
    evre = ayar.evre_oku(kok)
    print(kapi.durum(kok)[1])
    return 0 if evre["evre"] == "yayin-bekliyor" else 1


def main(argv):
    if not argv:
        print(__doc__)
        return 2
    motor = argv[argv.index("--motor") + 1] if "--motor" in argv and len(argv) > argv.index("--motor") + 1 else None
    deneme = int(argv[argv.index("--deneme") + 1]) if "--deneme" in argv and len(argv) > argv.index("--deneme") + 1 else VARSAYILAN_DENEME
    zorla = "--zorla" in argv
    devam = "--devam" in argv
    atla = {"--motor", "--deneme", "--devam", "--zorla", str(motor), str(deneme)}
    talep = " ".join(a for a in argv if a not in atla).strip() if not devam else None
    if not devam and not talep:
        print(__doc__)
        return 2
    with open(KOK / ".kos.lock", "w") as kilit:  # kos.py ile aynı kilit — aynı anda iki koşu olmasın
        fcntl.flock(kilit, fcntl.LOCK_EX)
        try:
            return dongu(talep, motor, deneme, zorla)
        finally:
            fcntl.flock(kilit, fcntl.LOCK_UN)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
