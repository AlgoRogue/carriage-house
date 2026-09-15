# 04: Tek giriş fonksiyonu: bos → park mutlu yol otomatik zincirleme

**What to build:**
02'deki tek-adım Motor çağrısını ve 03'teki `durum.json` kalıcılığını birleştiren tek bir giriş
fonksiyonu (insanın "işi ilerlet" çağrısı). Bu fonksiyon, insan tıklaması/ara müdahale olmadan,
`bos`'tan başlayıp geçerli tüm ara durumlardan (`is_alindi → planlaniyor → plan_hazir →
delege_hazirlaniyor → paket_hazir`) `park`'a kadar otomatik olarak zincirler — tek çağrı.

Dönen sonuç en azından başlangıç durumunu ve bitiş durumunu içerir (izlenen tam geçiş listesini de
içermesi tercih edilir, ama zorunlu değil — dış davranış zaten `durum.json` üzerinden doğrulanabilir
olmalı). Bu bilet yalnız mutlu yolu kapsar; hata yolu ve reddedilen geçiş senaryoları 05'tedir.

**Blocked by:** 02, 03

**Status:** done

- [x] Tek bir fonksiyon çağrısı, `bos` başlangıçtan `park` bitişe kadar tüm ara durumları insan
      müdahalesi olmadan otomatik zincirler
- [x] Fonksiyonun dönüş değeri başlangıç durumu ve bitiş durumunu içerir (ideal olarak izlenen
      geçiş yolu da)
- [x] Zincir tamamlandıktan sonra `personel/CH-0001/durum.json`'daki `durum` alanı `park`'tır
- [x] Zincir tamamlandıktan sonra `durum.json`'daki `is_id` ve `son_sinyal` alanları doğru
      (son geçişe uygun) değerlerdedir
- [x] Zincir boyunca sahte motor yalnız `planlaniyor` ve `delege_hazirlaniyor` durumlarında
      çağrılır (uçtan uca e2e testle doğrulanır)
- [x] Bu uçtan uca mutlu yol senaryosu için `tests/` altında bir test vardır ve
      `python3 -m unittest discover -s tests` ile ağ/gerçek motor çağrısı olmadan koşar

## Comments

- 2026-09-15: `isi_ilerlet` tek giriş seam’inde red → green; `tests/test_surucu.py` tüm mutlu yol kabul ölçütlerini doğrular. Sürücü testleri: 21/21 geçti.
