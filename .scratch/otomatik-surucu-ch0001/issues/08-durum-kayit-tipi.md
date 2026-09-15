# 08: Data Clumps - durum/is_id/son_sinyal için küçük bir değer tipi

**What to build:**
`durum`, `is_id`, `son_sinyal` (ve `kalici_gecis` parametreleri) şu an ilgili fonksiyonlar arasında
ayrı ayrı, birlikte taşınan bir grup olarak dolaşıyor (Data Clumps kokusu). Bu bilet bu alanları tek
bir küçük değer tipinde (ör. dataclass/namedtuple) toplar; bu tip fonksiyon imzalarında ve
`kalici_gecis` çağrılarında kullanılır. Dışa dönük davranış ve kalıcı `durum.json` formatı değişmez.
Bu saf bir iç yapı düzenlemesidir.

**Blocked by:** 04 (mutlu yol giriş noktası kurulduktan sonra yapılmalı)

**Status:** done

- [x] `durum`, `is_id`, `son_sinyal` alanlarını bir arada tutan tek bir küçük değer tipi vardır
- [x] İlgili fonksiyon imzaları (`kalici_gecis` dahil) bu üç ayrı parametre yerine yeni değer tipini
      kullanır
- [x] `durum.json`'a yazılan/okunan alanların isim ve şekli önceki ile aynı kalır. Kalıcı veri
      formatı bozulmaz
- [x] Mevcut tüm testler (`python3 -m unittest discover -s tests`) değişiklik sonrası da geçer

## Comments

- 2026-09-15: `DurumKaydi` (frozen dataclass: `durum`, `is_id`, `son_sinyal`) eklendi; `DurumDeposu.yaz`, `kalici_gecis` ve `isi_ilerlet` yazma çağrıları bu tipi kullanır. Disk anahtarları aynı. `python3 -m unittest discover -s tests -p 'test_surucu*.py'` → 28 test, OK.
