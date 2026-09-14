#!/usr/bin/env python3
"""Kapı — insanın düğmeleri. LLM çağırmaz, motor başlatmaz; yalnız `increment/evre.json`'u ve
kapı dosyalarını yazar. Evreyi ilerleten iki şey vardır: bu betik (insan) ve `bin/kos.py`
(artefakt doğrulaması). Ajan evreyi yazamaz.

  python3 bin/kapi.py talep "<tek cümle>"        yeni increment aç (evre: sozlesme) → sırada sistem-sevk
  python3 bin/kapi.py onayla [--motor grok]      KAPI 1: taslak sözleşmeyi dondur (sozlesme.onayli.json,
                                                 salt-okunur), inşaat/bekçi motorunu kilitle → sistem-insaat
  python3 bin/kapi.py yayinla                    KAPI 2: PASS'ı SoT'a işle (kararlar.md), evreyi kapat
  python3 bin/kapi.py red "<sebep>"              increment'i her evrede kapat; sebep geçmişe düşer
  python3 bin/kapi.py durum                      evre, bekleyen onay, motorlar, son bekçi kararı

Çıkış: başarı 0, yanlış evre / eksik dosya 1.
"""
import json
import os
import re
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import ayar  # noqa: E402
import motorlar  # noqa: E402
import sema  # noqa: E402

KOK = ayar.KOK
SEVK = "sistem-sevk"
ID_DESENI = re.compile(r"^inc-(\d{3,})$")


def _yaz(mesaj):
    print(mesaj)


# --- yardımcılar -----------------------------------------------------------

def sonraki_id(kok=None):
    """increment/inc-NNN klasörlerinin en büyüğü + 1; hiç yoksa inc-001."""
    klasor = Path(kok or KOK) / "increment"
    sayilar = [int(m.group(1)) for p in klasor.glob("inc-*") if (m := ID_DESENI.match(p.name))]
    return f"inc-{(max(sayilar) + 1) if sayilar else 1:03d}"


def _sevk_kuyruguna(kok, id_, notu):
    durum = ayar.durum_oku(SEVK, kok)
    kuyruk = [o for o in (durum.get("kuyruk") or []) if isinstance(o, dict) and o.get("id") != id_]
    ayar.durum_guncelle(SEVK, {"kuyruk": [*kuyruk, {"id": id_, "durum": "bekliyor", "not": notu}]}, kok)


def _sevk_kuyrugunu_kapat(kok, id_, durum_adi):
    durum = ayar.durum_oku(SEVK, kok)
    kuyruk = [{**o, "durum": durum_adi} if isinstance(o, dict) and o.get("id") == id_ else o
              for o in (durum.get("kuyruk") or [])]
    ayar.durum_guncelle(SEVK, {"kuyruk": kuyruk}, kok)


def _kararlar_ekle(kok, satir):
    yol = Path(kok or KOK) / "kararlar.md"
    with open(yol, "a", encoding="utf-8") as dosya:
        dosya.write(satir.rstrip("\n") + "\n")


# --- komutlar --------------------------------------------------------------

def talep(cumle, kok=None):
    evre = ayar.evre_oku(kok)
    if evre["evre"] not in ("bos", "yayinlandi", "red"):
        return 1, f"açık increment var: {evre['increment_id']} ({evre['evre']}). Önce yayinla ya da red."
    cumle = (cumle or "").strip()
    if not cumle:
        return 1, "talep boş — tek cümle yaz."
    id_ = sonraki_id(kok)
    ayar.increment_klasoru(id_, kok).mkdir(parents=True, exist_ok=True)
    ayar.evre_guncelle({"increment_id": id_, "evre": "sozlesme", "bekleyen_onay": None,
                        "motor": {"insaat": None, "bekci": None}, "talep": cumle, "kapsam_sapmasi": []},
                       f"talep: {cumle}", kok)
    _sevk_kuyruguna(kok, id_, cumle)
    return 0, f"{id_} açıldı (evre: sozlesme). Sıradaki: python3 bin/kos.py sistem-sevk"


def onayla(motor=None, kok=None):
    """KAPI 1."""
    evre = ayar.evre_oku(kok)
    if evre["bekleyen_onay"] != "sozlesme":
        return 1, f"onaylanacak sözleşme yok (evre: {evre['evre']}, bekleyen: {evre['bekleyen_onay'] or '-'})."
    klasor = ayar.increment_klasoru(evre["increment_id"], kok)
    taslak = klasor / "sozlesme.json"
    try:
        veri = json.loads(taslak.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        return 1, f"taslak okunamadı: {exc}"
    hatalar = sema.dogrula(sema.yukle("increment-sozlesmesi", kok), veri)
    if hatalar:
        return 1, "taslak şemaya uymuyor:\n  " + "\n  ".join(hatalar)
    insaat = (motor or veri["motor_adayi"]).lower()
    if insaat not in motorlar.MOTORLAR:
        return 1, f"bilinmeyen motor: {insaat}"
    bekci = motorlar.ters_motor(insaat)
    onayli = klasor / "sozlesme.onayli.json"
    if onayli.exists():
        os.chmod(onayli, 0o644)
    shutil.copyfile(taslak, onayli)
    os.chmod(onayli, 0o444)  # dondurulmuş kopya — ajan yazamaz, insan chmod'suz düzeltemez
    ayar.evre_guncelle({"evre": "insaat", "bekleyen_onay": None, "motor": {"insaat": insaat, "bekci": bekci}},
                       f"KAPI 1: sözleşme donduruldu · inşaat={insaat} · bekçi={bekci}", kok)
    return 0, (f"KAPI 1 geçti. inşaat: {insaat} · bekçi: {bekci} · {onayli.relative_to(Path(kok or KOK))}\n"
               f"Sıradaki: python3 bin/kos.py sistem-insaat")


def yayinla(kok=None):
    """KAPI 2."""
    evre = ayar.evre_oku(kok)
    if evre["bekleyen_onay"] != "yayin" or evre["evre"] != "yayin-bekliyor":
        return 1, f"yayınlanacak PASS yok (evre: {evre['evre']}, bekleyen: {evre['bekleyen_onay'] or '-'})."
    id_ = evre["increment_id"]
    klasor = ayar.increment_klasoru(id_, kok)
    try:
        sozlesme = json.loads((klasor / "sozlesme.onayli.json").read_text(encoding="utf-8"))
        rapor = json.loads((klasor / "bekci-raporu.json").read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        return 1, f"kapı dosyası okunamadı: {exc}"
    if rapor.get("karar") != "PASS":
        return 1, "bekçi raporu PASS değil — yayın yok."
    _kararlar_ekle(kok, f"- {ayar.simdi_iso()[:10]} · {id_} · {sozlesme['hedef_davranis']} → "
                        f"{sozlesme['yayin_anlami']} (inşaat: {evre['motor']['insaat']}, "
                        f"bekçi: {evre['motor']['bekci']})")
    _sevk_kuyrugunu_kapat(kok, id_, "tamam")
    ayar.evre_guncelle({"evre": "yayinlandi", "bekleyen_onay": None}, "KAPI 2: yayınlandı", kok)
    return 0, f"KAPI 2 geçti. {id_} kararlar.md'ye işlendi. Yeni increment: python3 bin/kapi.py talep \"…\""


def red(sebep, kok=None):
    evre = ayar.evre_oku(kok)
    if evre["evre"] in ("bos", "yayinlandi", "red"):
        return 1, "açık increment yok."
    sebep = (sebep or "").strip() or "sebep yazılmadı"
    _sevk_kuyrugunu_kapat(kok, evre["increment_id"], "red")
    ayar.durum_guncelle(SEVK, {"son_red": {"increment_id": evre["increment_id"], "sebep": sebep,
                                            "zaman": ayar.simdi_iso()}}, kok)
    ayar.evre_guncelle({"evre": "red", "bekleyen_onay": None}, f"RED ({evre['evre']} evresinde): {sebep}", kok)
    return 0, f"{evre['increment_id']} kapatıldı (red). Sebep sevk'in durum.json'una düştü."


def durum(kok=None):
    evre = ayar.evre_oku(kok)
    satirlar = [f"increment: {evre['increment_id'] or '-'} · evre: {evre['evre']} · "
                f"bekleyen onay: {evre['bekleyen_onay'] or '-'}",
                f"motor: inşaat={evre['motor']['insaat'] or '-'} · bekçi={evre['motor']['bekci'] or '-'}",
                f"talep: {evre['talep'] or '-'}"]
    if evre.get("kapsam_sapmasi"):
        satirlar.append("kapsam sapması: " + ", ".join(evre["kapsam_sapmasi"]))
    if evre["increment_id"]:
        klasor = ayar.increment_klasoru(evre["increment_id"], kok)
        var = [p.name for p in sorted(klasor.glob("*")) if p.is_file()] if klasor.is_dir() else []
        satirlar.append("dosyalar: " + (", ".join(var) or "(yok)"))
        rapor = klasor / "bekci-raporu.json"
        if rapor.exists():
            try:
                satirlar.append("bekçi: " + json.loads(rapor.read_text(encoding="utf-8")).get("karar", "?"))
            except ValueError:
                satirlar.append("bekçi: rapor bozuk")
    sonraki = {"sozlesme": "python3 bin/kos.py sistem-sevk", "insaat": "python3 bin/kos.py sistem-insaat",
               "bekci": "python3 bin/kos.py sistem-bekci", "yayin-bekliyor": "python3 bin/kapi.py yayinla",
               "fail": "python3 bin/kapi.py red \"…\"  (ya da sözleşmeyi düzeltip yeniden onayla)"}
    if evre["bekleyen_onay"] == "sozlesme":
        satirlar.append("sıradaki: python3 bin/kapi.py onayla [--motor …]")
    elif evre["evre"] in sonraki:
        satirlar.append("sıradaki: " + sonraki[evre["evre"]])
    else:
        satirlar.append("sıradaki: python3 bin/kapi.py talep \"…\"")
    if evre["gecmis"]:
        son = evre["gecmis"][-1]
        satirlar.append(f"son olay: {son['zaman']} — {son['olay']}")
    return 0, "\n".join(satirlar)


def main(argv):
    if not argv:
        print(__doc__)
        return 2
    komut, gerisi = argv[0], argv[1:]
    if komut == "talep":
        kod, mesaj = talep(" ".join(gerisi))
    elif komut == "onayla":
        motor = gerisi[gerisi.index("--motor") + 1] if "--motor" in gerisi and len(gerisi) > gerisi.index("--motor") + 1 else None
        kod, mesaj = onayla(motor)
    elif komut == "yayinla":
        kod, mesaj = yayinla()
    elif komut == "red":
        kod, mesaj = red(" ".join(gerisi))
    elif komut == "durum":
        kod, mesaj = durum()
    else:
        print(__doc__)
        return 2
    _yaz(mesaj)
    return kod


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
