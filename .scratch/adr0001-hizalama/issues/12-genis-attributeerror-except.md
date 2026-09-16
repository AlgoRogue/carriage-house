# 12: Geniş AttributeError except (debt)

**Spec:** `.scratch/adr0001-hizalama/spec.md`

**What to build:**
`personel/CH-0001/bin/kart_motoru.py` içinde `except (TypeError, ValueError, AttributeError)` yalnız `modul.cozumle(stdout)` çevresinde. Fowler: gerçek adapter bug'ını gizleyebilir. Ticket 04 / Debt 05 / spec: bozuk stdout, `cozumle` hatası → `hata` Sinyali; döngü patlamaz. `Exception` değil; yer doğru. Spec ezer.

Daraltma yalnız `"[]"` → `hata` yolunu bozmadan; yoksa yakalamanın kasıtlı olduğu belgelenir.

**Blocked by:** None (debt; H implement'ini bloklamaz)

**Status:** done

- [x] `AttributeError` ya dar (`"[]"` / `.get` yolu durur) ya da spec gerekçesiyle belgelenmiş
- [x] Bozuk stdout → `hata` Sinyali; Sürücü döngüsü düşmez
- [x] `Exception` yakalanmaz; unittest CLI/ağ açmaz
- [x] `python3 -m unittest discover -s tests` ağsız yeşil

## Comments

- 2026-09-16: REVIEW-04 (ticket 04, engelleyici değil; Fowler yargı, spec ezer). Kaynak: `.scratch/adr0001-hizalama/REVIEW-04.md` ST-D1.
- 2026-09-16: uygulandı (Claude Code). Kök neden düzeltildi: `bin/motorlar/claude.py` ve `agy.py`'nin `cozumle()`'si artık `json.loads` sonucu dict değilse (`"[]"` gibi dizi/skaler) `.get()` çağırmadan önce `bozuk(...)` ile erken dönüyor; `codex.py`'nin JSONL döngüsü dict olmayan satırları `continue` ile atlıyor (grok.py zaten bu koruma vardı). Bu sayede `kart_motoru.py`'deki `except (TypeError, ValueError, AttributeError)` → `except (TypeError, ValueError)`'a daraltıldı; `AttributeError` artık hiç yakalanmıyor çünkü kaynağında önleniyor, böylece gerçek bir adapter bug'ı (`Exception` değil, dar tip demeti) gizlenmiyor. `"[]"` / `[]` → `hata` yolu bozulmadı (mevcut `test_kart_motoru`/`test_surucu_motor` testleri + yeni `tests/test_motorlar.py::OrtakTesti::test_json_dizi_non_dict_cozumle_attributeerror_kacmadan_hata_doner` dört motor için de doğruluyor). Ağsız/CLI'sız.
