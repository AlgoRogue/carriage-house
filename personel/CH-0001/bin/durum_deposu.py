"""Sürücünün durum kaydı; aksiyon iskeletine erişmez."""
import json
from dataclasses import dataclass
from pathlib import Path

from surucu_cekirdek import Sinyal


DURUM_YOLU = Path(__file__).resolve().parent.parent / "durum.json"


@dataclass(frozen=True)
class DurumKaydi:
    """Anlık durum, bağlı İş ve son Sinyal. Disk anahtarlarıyla aynı adlar."""
    durum: str
    is_id: str | None
    son_sinyal: Sinyal | None = None


class DurumDeposu:
    """Testlerde geçici bir dosya yolu verilebilir; diğer alanlar korunur."""

    def __init__(self, yol: str | Path = DURUM_YOLU):
        self.yol = Path(yol)

    def oku(self) -> dict:
        """Her çağrıda mevcut kaydı diskten oku; okuma hatalarını ilet."""
        return json.loads(self.yol.read_text(encoding="utf-8"))

    def yaz(self, kayit: DurumKaydi) -> None:
        """Sürücü alanlarını güncelle; kalan kayıt alanlarını koru."""
        belge = self.oku()
        belge.update(durum=kayit.durum, is_id=kayit.is_id,
                     son_sinyal=kayit.son_sinyal)
        self.yol.write_text(
            json.dumps(belge, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
