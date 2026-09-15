"""Aksiyon iskeletini bellek içinde işleten saf Sürücü çekirdeği."""
from dataclasses import dataclass
from enum import StrEnum


class Sinyal(StrEnum):
    MOTOR_CIKTISI = "motor_ciktisi"
    MOTOR_HATASI = "motor_hatasi"


MOTOR_CIKTISI = Sinyal.MOTOR_CIKTISI
MOTOR_HATASI = Sinyal.MOTOR_HATASI


ILK_DILIM = frozenset({
    "bos", "is_alindi", "planlaniyor", "plan_hazir",
    "delege_hazirlaniyor", "paket_hazir", "park", "hata",
})


@dataclass(frozen=True)
class GecisSonucu:
    kabul: bool
    yeni_durum: str
    mesaj: str
    sinyal: Sinyal | None = None


class Surucu:
    """İskelet ve dilim verisini alır; anlık durum tutmaz, Motor çağırmaz.

    İskeletin ``gecisler`` ve ``motor_cagrilan_durumlar`` alanları gereklidir.
    Veriler kurulumda kopyalanır; çağıranın girdileri değiştirilmez.
    """
    def __init__(self, iskelet, dilim=ILK_DILIM):
        self._motor_durumlari = frozenset(iskelet["motor_cagrilan_durumlar"])
        self._dilim = frozenset(dilim)
        self._gecisler = frozenset((g["from"], g["to"]) for g in iskelet["gecisler"])

    @property
    def motor_durumlari(self) -> frozenset[str]:
        """İskelette Motor çağrılan durumların salt okunur kümesi."""
        return self._motor_durumlari

    @property
    def gecisler(self) -> frozenset[tuple[str, str]]:
        """İskeletteki (kaynak, hedef) çiftlerinin salt okunur kümesi."""
        return self._gecisler

    def motor_basari_hedefi(self, durum: str) -> str | None:
        """Motor durumunun tek hata-dışı hedefi; yoksa veya belirsizse None."""
        if durum not in self._motor_durumlari:
            return None
        return self.tek_hata_disi_hedef(durum)

    def tek_hata_disi_hedef(self, durum: str, *, etkin_dilim: bool = False,
                           hata_yedegi: bool = False) -> str | None:
        """Tek hata-dışı kenarı seç; istenirse dilime süz ve tek hataya izin ver."""
        hedefler = {
            hedef for kaynak, hedef in self._gecisler
            if kaynak == durum and (not etkin_dilim or hedef in self._dilim)
        }
        adaylar = hedefler - {"hata"}
        if hata_yedegi and not adaylar:
            adaylar = hedefler
        return next(iter(adaylar)) if len(adaylar) == 1 else None

    def gecis(self, mevcut_durum: str, hedef_durum: str,
              sinyal: Sinyal | None = None) -> GecisSonucu:
        """İskelet → dilim → sinyal sırasıyla tek geçişi doğrular.

        ``motor_ciktisi`` iskeletteki tek başarı hedefine, ``motor_hatasi``
        hata hedefine izin verir. Motor dışında sinyal yalnız None olabilir.
        Üye olmayan sinyal ValueError yükseltir. Red sonucunda yeni_durum
        mevcut_durum olarak kalır; kayıt yazılmaz.
        """
        if (mevcut_durum, hedef_durum) not in self._gecisler:
            return GecisSonucu(False, mevcut_durum, "Geçiş aksiyon iskeletinde tanımlı değil.")
        if hedef_durum not in self._dilim:
            return GecisSonucu(False, mevcut_durum, "Hedef etkin dilim dışında.")
        if sinyal is not None:
            try:
                sinyal = Sinyal(sinyal)
            except ValueError:
                raise ValueError(
                    "Sinyal motor_ciktisi veya motor_hatasi olmalı."
                ) from None
        if mevcut_durum in self._motor_durumlari:
            uygun = (
                sinyal == Sinyal.MOTOR_CIKTISI
                and self.motor_basari_hedefi(mevcut_durum) == hedef_durum
            ) or (sinyal == Sinyal.MOTOR_HATASI and hedef_durum == "hata")
            if not uygun:
                return GecisSonucu(False, mevcut_durum, "Motor sinyali eksik veya hedefle uyumsuz.")
        elif sinyal is not None:
            return GecisSonucu(False, mevcut_durum, "Bu durumda Motor beklenmiyor; sinyal reddedildi.")
        return GecisSonucu(True, hedef_durum, "Geçiş kabul edildi.", sinyal)
