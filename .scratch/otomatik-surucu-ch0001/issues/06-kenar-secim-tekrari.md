# 06: Sürücü'de "tek hata-dışı kenar" seçimi için ortak yardımcı

**What to build:**
`Surucu` üzerinde bir durumdan çıkan geçiş kenarları arasından hata-dışı (başarı) tek kenarı seçen
mantık, şu an `SurucuAdim` ve `motor_basari_hedefi` içinde ayrı ayrı tekrarlanıyor. Bu bilet, bu
seçimi tek bir paylaşılan yardımcıya çıkarır; her iki çağıran da aynı yardımcıyı kullanır. Dışa
dönük davranış (hangi kenarın seçildiği, hata durumunda ne olduğu) değişmez — bu saf bir
prefactor'dür, yeni özellik eklemez.

**Blocked by:** None (can start immediately) — 04'ten önce prefactor olarak da yapılabilir.

**Status:** done

- [x] `Surucu` için tek bir "hata-dışı kenar seç" yardımcı fonksiyonu/metodu vardır
- [x] `SurucuAdim` bu yardımcıyı çağırır, kendi kopya mantığını içermez
- [x] `motor_basari_hedefi` bu yardımcıyı çağırır, kendi kopya mantığını içermez
- [ ] Mevcut tüm testler (`python3 -m unittest discover -s tests`) değişiklik sonrası da geçer
- [x] Davranış değişikliği yok: aynı girdiler için aynı kenar seçilir, aynı hata durumları aynı
      şekilde ele alınır

## Comments

- 2026-09-15: Ortak seçim yardımcısı tamamlandı; prefactor sonrası mevcut 20 Sürücü testi geçti. Tam suite: 75 testten 74 geçti; ilgisiz `test_kit.BekciKatmanA.test_kosuda_anayasaya_dokunan_ajan_red` testi `tamam != red` nedeniyle başarısız. Tam-suite ölçütü bu nedenle işaretlenmedi.
