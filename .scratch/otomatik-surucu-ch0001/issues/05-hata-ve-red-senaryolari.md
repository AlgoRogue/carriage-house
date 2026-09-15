# 05: Hata yolu zinciri ve reddedilen geçiş testleri

**What to build:**
04'teki tek giriş fonksiyonunu, sahte motorun `planlaniyor` ya da `delege_hazirlaniyor` sırasında
"hata" sinyali verdiği senaryoda test et: zincir otomatik olarak `hata`'ya, ardından (bu dilimde
tanımlı kural gereği: "Sürücü hatayı park'a düşürüp yeniden denemeyi bekletir") otomatik olarak
`park`'a düşmelidir — tek çağrı, insan müdahalesi yok.

Ayrıca, dosyaya-yansıyan davranış üzerinden şu red senaryolarını doğrula:
- İskelette tanımsız ya da dilim kümesi dışında bir hedefe zorlama denemesi durumu değiştirmez
  (`durum.json` aynı kalır).
- Motor durumunda olmayan bir anda gelen sahte "çıktı geldi"/"hata" sinyali reddedilir, durum
  değişmez.

Bu bilet yeni üretim mantığı eklemez — 01-04'te kurulan davranışı hata yolu ve red senaryolarıyla
uçtan uca kanıtlar.

**Blocked by:** 04

**Status:** done

- [x] Sahte motorun `planlaniyor` sırasında "hata" verdiği e2e senaryo: tek çağrı sonunda
      `durum.json` `park`'tadır (ara adım olarak `hata`'dan geçmiştir)
- [x] Sahte motorun `delege_hazirlaniyor` sırasında "hata" verdiği e2e senaryo aynı şekilde
      `park`'ta sonuçlanır
- [x] İskelette tanımsız bir hedefe (ör. var olmayan bir durum adı) zorlama denemesi `durum.json`'u
      değiştirmez
- [x] Dilim kümesi dışında ama iskelette tanımlı bir hedefe (`usta_atandi`, `izleniyor`, `tamam`)
      zorlama denemesi `durum.json`'u değiştirmez
- [x] Motor durumunda olmayan bir anda (ör. `bos` ya da `park`) gelen sahte "çıktı geldi"/"hata"
      sinyali reddedilir, `durum.json` değişmez
- [x] Tüm bu senaryolar `tests/` altında, `python3 -m unittest discover -s tests` ile ağ/gerçek
      motor çağrısı olmadan koşar

## Comments

- 2026-09-15: Planlama hatası testi önce hata'da durarak başarısız oldu; döngü
  park'a kadar ilerletilince geçti. Delege hatası ve dosyayı değiştirmeyen red
  senaryoları da doğrulandı.
- Doğrulama: `python3 -m unittest discover -s tests -p 'test_surucu*.py' -v`
  — 26 test geçti (5 yeni test metodu).
- Tam test kümesi: 80 test, 79 başarılı; kapsam dışındaki mevcut
  `test_kit.BekciKatmanA.test_kosuda_anayasaya_dokunan_ajan_red` başarısız.
  İlgili kod değiştirilmedi.
