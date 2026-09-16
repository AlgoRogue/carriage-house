"""CLI çalıştırmadan hazır sinyal döndüren, bellek içi Motor."""
from time import monotonic

from surucu_cekirdek import Sinyal


class SahteMotor:
    """``motor(girdi) -> (Sinyal, metin)`` sözleşmesi; çağrılar zaman sırasıyla kaydedilir.

    ``saat`` saniye döndüren bir callable'dır; varsayılan monoton saattir.
    Testler sabit bir saat enjekte edebilir. ``metin`` içerik kanalıdır,
    Sinyal değildir. Hiçbir kayıt dosyaya yazılmaz.
    """

    def __init__(self, sinyal: Sinyal = Sinyal.BASARI, *, metin: str = "", saat=monotonic):
        try:
            self.sinyal = Sinyal(sinyal)
        except ValueError:
            raise ValueError(
                "Sahte Motor sinyali basari veya hata olmalı."
            ) from None
        self.metin = metin
        self.saat = saat
        self.cagrilar = []

    def __call__(self, girdi: str) -> tuple[Sinyal, str]:
        self.cagrilar.append({"durum": girdi, "zaman": self.saat()})
        return self.sinyal, self.metin
