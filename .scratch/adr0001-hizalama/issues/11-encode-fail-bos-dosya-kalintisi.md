# 11: Encode fail boş dosya kalıntısı (debt)

**Spec:** `.scratch/adr0001-hizalama/spec.md`

**What to build:**
Surrogate yazımı (`"\ud800"`) `write_text` dosyayı önce açtığı için boş `plan.md` bırakıyor; geçiş yine reddediliyor (S3). Spec silme istemiyor. Kapı yazım-sonrası `read_text` ile yine red.

Ya encode fail'de boş kalıntıyı bırakma (temp+replace veya unlink) ya da kalıntının S3 reddiyle kabul olduğunu belge. Geçiş yine red; `park` değil.

**Blocked by:** None (debt; H implement'ini bloklamaz)

**Status:** done

- [x] Encode başarısızlığında ya boş `plan.md` kalıntısı yok ya da kalıntı belgelenmiş kabul (S3 red durur)
- [x] Geçiş yok, bitiş Motor durumu, `park` değil; otomatik `hata` yok
- [x] Üretim mutlu yolu değişmez
- [x] `python3 -m unittest discover -s tests` ağsız yeşil

## Comments

- 2026-09-16: REVIEW-03 (ticket 03, engelleyici değil). Kaynak: `.scratch/adr0001-hizalama/REVIEW-03.md` SP-D3.
- 2026-09-16: uygulandı (Claude Code). `SurucuAdim._artefakt_yaz`: `str` metin artık hedef dosyaya hiç dokunmadan önce `metin.encode("utf-8")` ile önceden kodlanıyor; `UnicodeEncodeError` (ör. `"\ud800"`) bu noktada yakalanıp reddediliyor, dolayısıyla `write_text`'in kısmi/boş dosya bırakma riski ortadan kalktı (kalıntı yok, belge değil). `mkdir`/`write_bytes` yalnız encode başarılı olduktan sonra çağrılıyor. Regresyon: `tests/test_surucu.py` ve `tests/test_surucu_adim.py`'deki surrogate testlerine `plan.md`'nin hiç oluşmadığını doğrulayan assert eklendi. Geçiş yok, bitiş Motor durumu, `park` yok; mutlu yol değişmedi.
