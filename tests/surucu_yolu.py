"""Personel kapsamındaki Sürücü modüllerinin ortak test yolu ve ortak test yardımcıları."""
import sys
from pathlib import Path

KOK = Path(__file__).resolve().parents[1]
PERSONEL = KOK / "personel" / "CH-0001"
SURUCU_YOLU = str(PERSONEL / "bin")
if SURUCU_YOLU not in sys.path:
    sys.path.insert(0, SURUCU_YOLU)


def dizin_bayt_haritasi(dizin):
    """Dizindeki dosyaların ad -> bayt içerik haritası."""
    return {yol.name: yol.read_bytes() for yol in Path(dizin).iterdir()}


def dizin_bayt_korumasini_dogrula(test, dizin, once):
    """``once`` ile şimdiki hâli tam eşleştirir; silinen dosyayı da yakalar
    (yalnız mevcut dosyaları dolaşmak silmeyi kaçırır)."""
    test.assertEqual(dizin_bayt_haritasi(dizin), once)


class HataKosucu:
    """Ortak stub: her çağrıda OSError fırlatır, çağrıları sırayla kaydeder."""

    def __init__(self, mesaj="cli yok"):
        self.cagrilar = []
        self._mesaj = mesaj

    def __call__(self, komut):
        self.cagrilar.append(list(komut))
        raise OSError(self._mesaj)
