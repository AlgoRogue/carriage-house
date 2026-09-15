"""Personel kapsamındaki Sürücü modüllerinin ortak test yolu."""
import sys
from pathlib import Path

KOK = Path(__file__).resolve().parents[1]
PERSONEL = KOK / "personel" / "CH-0001"
SURUCU_YOLU = str(PERSONEL / "bin")
if SURUCU_YOLU not in sys.path:
    sys.path.insert(0, SURUCU_YOLU)
