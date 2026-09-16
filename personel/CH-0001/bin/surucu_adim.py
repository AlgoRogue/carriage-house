"""Enjekte edilen Motor ile tek geçiş; kalıcılık ve otomatik döngü yok."""
from pathlib import Path

from surucu_cekirdek import GecisSonucu, ILK_DILIM, Sinyal, Surucu

# S4 (SEAMS.md, onaylı): motor durumu -> yazılan İş artefaktı dosya adı.
_ARTEFAKT_ADI = {"planlaniyor": "plan.md", "delege_hazirlaniyor": "paket.md"}
# delege_hazirlaniyor, planlaniyor'un yazdığı artefaktı okuma yönünü alır.
_OKUNAN_DURUM = {"delege_hazirlaniyor": "planlaniyor"}


class SurucuAdim:
    """``adim(mevcut_durum)`` bir GecisSonucu döndürür; durum çağıranda kalır.

    Motor, girdi alan ve ``(Sinyal, metin)`` döndüren bir callable'dır;
    girdi Sürücü'nün durum adına göre seçip doldurduğu Prompt şablonudur
    (yalnız yol/adres slotları; kimlik, skill, hafıza, Defter yok).
    ``metin`` içerik kanalıdır; ``basari`` sinyalinde İş artefaktı yoluna
    yazılır. Artefakt boş/yazılamazsa (veya dosya yoksa, UTF-8 okunamıyorsa,
    IO hatası alınırsa) geçiş reddedilir, durum Motor durumunda kalır
    (otomatik ``hata`` durumu açılmaz). Motor dışında etkin dilimdeki tek
    hata-dışı kenar, yoksa tek kenar seçilir. Kenar yoksa (ilk dilimde park
    gibi) veya seçim belirsizse durum korunarak red döner. Her çağrı en
    fazla bir geçiş uygular.

    ``metin`` üretimde her zaman ``str``dür (SEAMS.md S2). Artefakt yazıcısı
    ham ``bytes``'ı da olduğu gibi yazar; bu yalnız test seam'inin geçersiz
    UTF-8 red yolunu (SP-D2) kanıtlamasını sağlar, içerik şeması icat etmez.
    """

    def __init__(self, iskelet, motor, *, is_id=None, is_kok=None,
                sablon_kok=None, dilim=ILK_DILIM):
        self._dilim = frozenset(dilim)
        self._surucu = Surucu(iskelet, self._dilim)
        self._motor = motor
        self._is_id = is_id
        self._is_kok = Path(is_kok) if is_kok is not None else None
        self._sablon_kok = Path(sablon_kok) if sablon_kok is not None else None

    def adim(self, mevcut_durum: str) -> GecisSonucu:
        if mevcut_durum in self._surucu.motor_durumlari:
            girdi = self._sablon_doldur(mevcut_durum)
            sinyal, metin = self._motor(girdi)
            hedef = ("hata" if sinyal == Sinyal.HATA
                     else self._surucu.motor_basari_hedefi(mevcut_durum))
            if hedef is None:
                return GecisSonucu(False, mevcut_durum, "Motor başarı hedefi yok veya belirsiz.")
            sonuc = self._surucu.gecis(mevcut_durum, hedef, sinyal)
            if (sonuc.kabul and sonuc.sinyal == Sinyal.BASARI
                    and not self._artefakt_yaz(mevcut_durum, metin)):
                return GecisSonucu(
                    False, mevcut_durum,
                    "Motor başarı sinyali verdi ama İş artefaktı boş veya yazılamadı.")
            return sonuc

        hedef = self._surucu.tek_hata_disi_hedef(
            mevcut_durum, etkin_dilim=True, hata_yedegi=True)
        if hedef is None:
            return GecisSonucu(False, mevcut_durum, "Etkin dilimde tek geçiş yok veya belirsiz.")
        return self._surucu.gecis(mevcut_durum, hedef)

    def _artefakt_yolu(self, durum: str) -> Path:
        return self._is_kok / self._is_id / _ARTEFAKT_ADI[durum]

    def _sablon_doldur(self, durum: str) -> str:
        sablon = (self._sablon_kok / f"{durum}.md").read_text(encoding="utf-8")
        oku_durum = _OKUNAN_DURUM.get(durum)
        oku_yolu = self._artefakt_yolu(oku_durum) if oku_durum else ""
        return sablon.format(
            is_id=self._is_id, yaz_yolu=self._artefakt_yolu(durum), oku_yolu=oku_yolu)

    def _artefakt_yaz(self, durum: str, metin: str | bytes) -> bool:
        if not isinstance(metin, (str, bytes)) or not metin.strip():
            return False

        try:
            veri = metin if isinstance(metin, bytes) else metin.encode("utf-8")
        except UnicodeEncodeError:
            return False

        yol = self._artefakt_yolu(durum)
        try:
            yol.parent.mkdir(parents=True, exist_ok=True)
            yol.write_bytes(veri)

            if not yol.is_file():
                return False
            icerik = yol.read_text(encoding="utf-8")
            if not icerik.strip():
                return False
        except (OSError, UnicodeError):
            return False
        return True
