"""Enjekte edilen Motor ile tek geçiş; kalıcılık ve otomatik döngü yok."""
from surucu_cekirdek import GecisSonucu, ILK_DILIM, Sinyal, Surucu


class SurucuAdim:
    """``adim(mevcut_durum)`` bir GecisSonucu döndürür; durum çağıranda kalır.

    Motor, girdi alan ve ``(Sinyal, metin)`` döndüren bir callable'dır; bu
    dilimde girdi geçici olarak durum adıdır. ``metin`` içerik kanalıdır,
    henüz artefakt olarak yazılmaz. Motor dışında etkin dilimdeki tek
    hata-dışı kenar, yoksa tek kenar seçilir. Kenar yoksa (ilk dilimde
    park gibi) veya seçim belirsizse durum korunarak red döner. Her çağrı
    en fazla bir geçiş uygular.
    """

    def __init__(self, iskelet, motor, dilim=ILK_DILIM):
        self._dilim = frozenset(dilim)
        self._surucu = Surucu(iskelet, self._dilim)
        self._motor = motor

    def adim(self, mevcut_durum: str) -> GecisSonucu:
        if mevcut_durum in self._surucu.motor_durumlari:
            sinyal, _metin = self._motor(mevcut_durum)
            hedef = ("hata" if sinyal == Sinyal.HATA
                     else self._surucu.motor_basari_hedefi(mevcut_durum))
            if hedef is None:
                return GecisSonucu(False, mevcut_durum, "Motor başarı hedefi yok veya belirsiz.")
            return self._surucu.gecis(mevcut_durum, hedef, sinyal)

        hedef = self._surucu.tek_hata_disi_hedef(
            mevcut_durum, etkin_dilim=True, hata_yedegi=True)
        if hedef is None:
            return GecisSonucu(False, mevcut_durum, "Etkin dilimde tek geçiş yok veya belirsiz.")
        return self._surucu.gecis(mevcut_durum, hedef)
