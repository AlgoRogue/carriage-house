"""CH-0001 için tek çağrıda park'a kadar ilerleten Sürücü girişi."""
import json
from dataclasses import dataclass
from pathlib import Path

from durum_deposu import DURUM_YOLU, DurumDeposu, DurumKaydi
from surucu_adim import SurucuAdim


PERSONEL_KOK = Path(__file__).resolve().parent.parent
ISKELET_YOLU = PERSONEL_KOK / "aksiyon-iskeleti.json"
SABLON_KOK = PERSONEL_KOK / "sablonlar"
ISLER_KOK = PERSONEL_KOK / "isler"


@dataclass(frozen=True)
class SurucuSonucu:
    baslangic_durumu: str
    bitis_durumu: str
    izlenen_yol: tuple[str, ...]


def isi_ilerlet(motor, *, is_id: str, durum_yolu: str | Path = DURUM_YOLU,
                isler_kok: str | Path = ISLER_KOK) -> SurucuSonucu:
    """İşi park'a kadar ilerlet; Motor durumlarında şablon doldurur, artefakt yazar.

    İskelet ve Prompt şablonları salt okunur; testler geçici durum dosyası
    ve İş artefaktı kökü enjekte eder (üretimde Personel kaydı altı).
    Her kabul edilen geçiş İş kimliği ve o geçişin Sinyali ile kaydedilir.
    Hata yolu da park'a kadar ilerler; reddedilen geçişte ilerleme durur
    (kabul edilemez artefakt dahil — S3, otomatik hata durumu açılmaz).
    """
    iskelet = json.loads(ISKELET_YOLU.read_text(encoding="utf-8"))
    adim = SurucuAdim(iskelet, motor, is_id=is_id, is_kok=Path(isler_kok),
                      sablon_kok=SABLON_KOK)
    depo = DurumDeposu(durum_yolu)
    durum = depo.oku()["durum"]
    yol = [durum]
    while durum != "park":
        sonuc = adim.adim(durum)
        if not sonuc.kabul:
            break
        durum = sonuc.yeni_durum
        depo.yaz(DurumKaydi(durum=durum, is_id=is_id,
                            son_sinyal=sonuc.sinyal))
        yol.append(durum)
    return SurucuSonucu(yol[0], durum, tuple(yol))
