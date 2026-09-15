# CEVAP — Parça 2b Sürücü LOGIC prototipi

- Tarih: 2026-09-15
- Skill: mattpocock prototype / LOGIC
- Soru: Cengizhan'ın kilitli durum makinesi, ilk dilim bos → is_alindi → planlaniyor → plan_hazir → delege_hazirlaniyor → paket_hazir → park yolunu sapmadan koşturuyor mu; durumu yalnız Sürücü mü yazıyor ve Motor yalnızca planlaniyor/delege_hazirlaniyor'da kavramsal mı?
- Karar: EVET — ilk dilim sapmadan hissediliyor; iskeletle uyumlu.
- Önemli sınır: HTML'deki tıklamalar gerçek Sürücü değildir; demoda Sürücü temsilcisi + taklit Motor sinyalidir. Gerçek kurguda durum geçişleri insan tıklaması beklemez.
- Taşınacak karar: Saf SurucuMakine mantığı (yalnız Sürücü yazar; Motor sinyal verir, hedef seçmez; park ilk dilimin sonu) gerçek Sürücü modülüne lift edilecek. Throwaway HTML production değildir.
- Review: Claude ONAY (üç kozmetik düzeltme uygulandı).
- Bilinçli dışı (değişmedi): Kapı, defter, hafıza, gerçek CLI Motor, usta, production bin/surucu.py otomatik kuyruk — sonraki parçalar.
