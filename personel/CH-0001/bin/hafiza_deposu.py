"""CH-0001 Ajan hafızası; Sürücü ve Motor'a bağlanmaz."""
import json
from pathlib import Path


HAFIZA_YOLU = Path(__file__).resolve().parent.parent / "hafiza.json"


class HafizaDeposu:
    """Testlerde geçici bir dosya yolu verilebilir; ürün dosyası varsayılandır."""

    def __init__(self, yol: str | Path = HAFIZA_YOLU):
        self.yol = Path(yol)

    def oku(self) -> list:
        """kayitlar listesini her çağrıda diskten oku."""
        belge = json.loads(self.yol.read_text(encoding="utf-8"))
        return belge["kayitlar"]

    def ekle(self, metin: str) -> None:
        """Sona bir kayıt ekle ve dosyayı yaz; listeyi değiştirmez."""
        kayitlar = self.oku()
        kayitlar.append({"metin": metin})
        self.yol.write_text(
            json.dumps({"kayitlar": kayitlar}, ensure_ascii=False, indent=2)
            + "\n",
            encoding="utf-8",
        )
