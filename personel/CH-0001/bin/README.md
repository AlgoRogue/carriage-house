# CH-0001 Sürücü modülleri

Throwaway değil; canlı kod haritası. Kararlar: `docs/adr/0001` … `0004`.

```
                    isi_ilerlet (surucu.py)
                           |
                     SurucuAdim (surucu_adim.py)
                      /              \
              Surucu (cekirdek)    Motor callable
             (surucu_cekirdek.py)  (sahte_motor | ADR-0001 bag)
                      |
              (kalici_gecis / durum_deposu) ---- durum.json
```

| Dosya | Sorumluluk |
|---|---|
| `surucu_cekirdek.py` | Saf kurallar: geçiş, dilim, Sinyal |
| `surucu_adim.py` | Tek adım; Motor'u çağırır |
| `surucu.py` | `park`'a kadar döngü |
| `durum_deposu.py` | `durum.json` oku/yaz |
| `surucu_kalici_gecis.py` | Tek geçişi diske bağlar |
| `sahte_motor.py` | Test Motor'u |
| `kart_motoru.py` | **GEÇİCİ / HURDA ADAYI** - ADR-0001 uyumsuz; to-spec hizalamasında kesilir veya yeniden yazılır |
| `hafiza_deposu.py` | **GEÇİCİ / HURDA VEYA YENİDEN LIFT ADAYI** - prototype+ADR sonrası; to-spec'ten sonra gözden geçir |

Motor girdisi = ince prompt şablonu + CLI kalıcı yönlendirme; ayrıntı ADR-0001.

Bu harita to-spec hizalaması sonrası G3 gereği yeniden gözden geçirilir.
