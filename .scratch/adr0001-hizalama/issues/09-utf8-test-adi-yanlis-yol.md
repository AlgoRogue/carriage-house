# 09: UTF-8 test adı yanlış yol (debt)

**Spec:** `.scratch/adr0001-hizalama/spec.md`

**What to build:**
`test_basari_utf8_okunamayan_*` (`tests/test_surucu.py`, `tests/test_surucu_adim.py`) bozuk dosya yazıp `SahteMotor(metin="")` çağırıyor. SP-1 sonrası boş metin yazmadan reddedildiği için UTF-8 okuma yolu çalışmıyor; ad/yorum okunamayan artefaktı ima ediyor. Gerçek bayt yolu `test_gecersiz_utf8_bytes_*`.

Ad/yorumu (veya gövdeyi) gerçek yolla hizala. Üretim davranışını değiştirme.

**Blocked by:** None (debt; H implement'ini bloklamaz)

**Status:** done

- [x] `test_basari_utf8_okunamayan_*` ya gerçek bayt yolunu ölçer ya da ad/yorum gerçek yolu yansıtır
- [x] UTF-8 okunamayan red `test_gecersiz_utf8_bytes_*` (veya eşdeğeri) ile durur
- [x] Üretim davranışı değişmez
- [x] `python3 -m unittest discover -s tests` ağsız yeşil

## Comments

- 2026-09-16: REVIEW-03 (ticket 03, engelleyici değil; Mysterious Name yargısı). Kaynak: `.scratch/adr0001-hizalama/REVIEW-03.md` ST-D2.
- 2026-09-16: uygulandı (Claude Code). `tests/test_surucu.py::test_basari_utf8_okunamayan_artefaktta_ilerlemez_motor_durumunda_kalir` artık `SahteMotor(metin=b"\xff\xfe\x00\x00")` ile gerçek bayt yolunu ölçüyor (önceden `metin=""` verip boş-metin kapısında dosyaya hiç dokunmadan dönüyordu, ad yanıltıcıydı). `tests/test_surucu_adim.py`'de aynı yanıltıcı test `test_basari_bos_metinde_eski_bozuk_dosyaya_dokunmadan_reddedilir_durum_korunur` adına ve yorumuna çekildi (gerçekte ölçtüğü şey budur); gerçek UTF-8-okunamaz red kanıtı zaten var olan `test_gecersiz_utf8_bytes_reddedilir_durum_korunur` ile duruyor (Debt 10 ile bytes kanalı belgelendi). Üretim davranışı değişmedi.
