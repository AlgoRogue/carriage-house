"""Saf çekirdeğin tek geçişini durum dosyasına bağlar."""
from durum_deposu import DurumDeposu, DurumKaydi
from surucu_cekirdek import GecisSonucu, Surucu


def kalici_gecis(depo: DurumDeposu, surucu: Surucu, *,
                 kayit: DurumKaydi) -> GecisSonucu:
    """Açık hedefi bir kez dene; yalnız kabul edilen sonucu kaydet.

    ``kayit.durum`` denenen hedeftir. ``kayit.is_id`` yazılacak iş
    kimliğidir (None temizler). ``kayit.son_sinyal`` bu çağrının
    sinyalidir; yoksa None yazılır.
    İskelet çağıranın kurduğu Surucu içindedir; burada dosyası açılmaz.
    Motor çağrısı ve otomatik sonraki geçiş yoktur. Dosya hataları iletilir.
    """
    mevcut = depo.oku()
    sonuc = surucu.gecis(mevcut["durum"], kayit.durum, kayit.son_sinyal)
    if sonuc.kabul:
        depo.yaz(kayit)
    return sonuc
