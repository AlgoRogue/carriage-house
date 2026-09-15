"""CH-0001 için tek çağrıda park'a kadar ilerleten Sürücü girişi."""
import json
from dataclasses import dataclass
from pathlib import Path

from durum_deposu import DURUM_YOLU, DurumDeposu, DurumKaydi
from surucu_adim import SurucuAdim


ISKELET_YOLU = Path(__file__).resolve().parent.parent / "aksiyon-iskeleti.json"


@dataclass(frozen=True)
class SurucuSonucu:
    baslangic_durumu: str
    bitis_durumu: str
    izlenen_yol: tuple[str, ...]


def isi_ilerlet(motor, *, is_id: str, durum_yolu: str | Path = DURUM_YOLU
                ) -> SurucuSonucu:
    """İşi park'a kadar ilerlet; Motor callable'ı yalnız Sinyal üretir.

    İskelet salt okunur; testler geçici durum dosyası enjekte eder.
    Her kabul edilen geçiş İş kimliği ve o geçişin Sinyali ile kaydedilir.
    Hata yolu da park'a kadar ilerler; reddedilen geçişte ilerleme durur.
    """
    iskelet = json.loads(ISKELET_YOLU.read_text(encoding="utf-8"))
    adim = SurucuAdim(iskelet, motor)
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
