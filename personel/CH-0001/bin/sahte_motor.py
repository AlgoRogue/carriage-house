"""CLI çalıştırmadan hazır sinyal döndüren, bellek içi Motor."""
from time import monotonic

from surucu_cekirdek import Sinyal


class SahteMotor:
    """``motor(durum)`` sözleşmesi; çağrılar zaman sırasıyla kaydedilir.

    ``saat`` saniye döndüren bir callable'dır; varsayılan monoton saattir.
    Testler sabit bir saat enjekte edebilir. Hiçbir kayıt dosyaya yazılmaz.
    """

    def __init__(self, sinyal: Sinyal = Sinyal.MOTOR_CIKTISI, *, saat=monotonic):
        try:
            self.sinyal = Sinyal(sinyal)
        except ValueError:
            raise ValueError(
                "Sahte Motor sinyali motor_ciktisi veya motor_hatasi olmalı."
            ) from None
        self.saat = saat
        self.cagrilar = []

    def __call__(self, durum: str) -> Sinyal:
        self.cagrilar.append({"durum": durum, "zaman": self.saat()})
        return self.sinyal
