# 13: HataKosucu stub tekrarı (debt)

**Spec:** `.scratch/adr0001-hizalama/spec.md`

**What to build:**
`tests/test_kart_motoru.py` iç-seam OSError stub'ı, `tests/test_surucu_motor.py` birincil-seam `HataKosucu` ile aynı şekil. SEAMS: iç OSError testi *olabilir*; birincil kanıt `isi_ilerlet`. İki katman kasıtlı; stub kopyası debt.

Ortak stub/yardımcı; iki test onu kullanır. Katmanları birleştirme. Üretim davranışını değiştirme.

**Blocked by:** None (debt; H implement'ini bloklamaz)

**Status:** done

- [x] `HataKosucu` (veya eşdeğer) tek ortak stub; `test_kart_motoru` ve `test_surucu_motor` onu kullanır
- [x] Birincil seam `isi_ilerlet` kanıtı durur; iç OSError katmanı silinmek zorunda değil
- [x] Üretim davranışı değişmez
- [x] `python3 -m unittest discover -s tests` ağsız yeşil

## Comments

- 2026-09-16: REVIEW-04 (ticket 04, engelleyici değil; Fowler Duplicated Code yargısı). Kaynak: `.scratch/adr0001-hizalama/REVIEW-04.md` ST-D2.
- 2026-09-16: uygulandı (Claude Code). `tests/surucu_yolu.py`'a ortak `HataKosucu` stub'ı eklendi (çağrıları kaydeder, her çağrıda `OSError` fırlatır). `tests/test_kart_motoru.py::test_kosucu_oserror_hata_sinyali_doner` (iç seam) ve `tests/test_surucu_motor.py::test_kosucu_oserror_motor_hatasi_olur_parkta_biter` (birincil seam, `isi_ilerlet`) artık kendi yerel sınıflarını değil bu ortak stub'ı kullanıyor; iki katman (iç OSError kanıtı + birincil `isi_ilerlet` kanıtı) ayrı testler olarak duruyor, birleştirilmedi. Üretim davranışı değişmedi.
