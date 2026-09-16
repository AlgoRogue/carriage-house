# 10: Bytes içerik kanalı (debt)

**Spec:** `.scratch/adr0001-hizalama/spec.md`

**What to build:**
`_artefakt_yaz(..., metin: str | bytes)` + `write_bytes`. SEAMS S2: `motor(girdi: str) -> (Sinyal, metin)`; Sürücü `metin`'i İş artefaktı yazar. Bytes kanalı spec'te yok. Ticket 03 UTF-8 okunamayan reddi bu yolla kanıtlanıyor; mutlu yolu bozmuyor.

Ya bytes kanalını spec/SEAMS ile hizala ya da üretimden kaldır (S2 yalnız str). İçerik şeması icat etme.

**Blocked by:** None (debt; H implement'ini bloklamaz)

**Status:** done

- [x] Üretim `metin` kanalı spec/SEAMS S2 ile aynı: ya bytes belgelenir ya da yalnız `str` kalır
- [x] UTF-8 okunamayan red kanıtı durur
- [x] Mutlu yol (02) kırılmaz; içerik şeması yok
- [x] `python3 -m unittest discover -s tests` ağsız yeşil

## Comments

- 2026-09-16: REVIEW-03 (ticket 03, engelleyici değil; kapsam). Kaynak: `.scratch/adr0001-hizalama/REVIEW-03.md` SP-D2.
- 2026-09-16: uygulandı (Claude Code). Karar: bytes kanalı üretimden kaldırılmadı, belgelendi (icat edilmiş içerik şeması değil — yalnız ham geçiş). `spec.md` ve `SEAMS.md`'nin S2 bölümlerine ve `SurucuAdim` docstring'ine: üretim Motor adaptörleri yalnız `str` döner; artefakt yazıcısı `bytes`'ı da olduğu gibi yazar, bu yalnız test seam'inin geçersiz UTF-8 red yolunu (SP-D2) kanıtlaması içindir. Mutlu yol (02, yalnız `str`) ve üretim davranışı değişmedi; ilgili red kanıtı `test_gecersiz_utf8_bytes_reddedilir_durum_korunur` duruyor.
