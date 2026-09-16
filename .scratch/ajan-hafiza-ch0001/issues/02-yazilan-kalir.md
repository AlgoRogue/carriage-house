# 02: Tek kayıt ekle: yazılan diskte kalır, yeni okuyucu döner

**Spec:** `.scratch/ajan-hafiza-ch0001/spec.md`

**What to build:**
Boş Ajan hafızasına bir `metin` eklenir. Süreç bittikten sonra (yeni bir `HafizaDeposu` örneği, aynı yol) `oku()` tam olarak o kaydı döner. Dış davranış hem API dönüşü hem dosya içeriğidir: `kayitlar` tek öğe, `metin` yazılan string.

Bu bilet yazma testlerini geçici dosyada koşar. Personel dizinindeki boş ürün dosyası boş kalır.

**Blocked by:** 01 (Boş başlangıç)

**Status:** done

- [x] `ekle(metin)` bir `{"metin": ...}` kaydı sona ekler ve dosyayı yazar
- [x] Aynı yolda yeni `HafizaDeposu` örneği `oku()` ile yazılan `metin`'i döner
- [x] Diskteki belge `kayitlar` içinde o tek kaydı taşır (bellek-içi sahte depo yeterli kanıt değildir)
- [x] Yazma testi geçici yol kullanır; committed `hafiza.json` çağrı öncesi/sonrası byte-eşittir
- [x] Unittest ağsızdır; `python3 -m unittest discover -s tests` ile keşfedilir
- [x] `HafizaDeposu` Sürücü / Motor / `isi_ilerlet` import etmez veya çağırmaz

## Comments

- 2026-09-15: yayınlandı (to-tickets). Durum: ready-for-agent.
- 2026-09-15: `ekle` geçici yolda yazar; yeni `HafizaDeposu` aynı `metin`'i döner, disk belgesi tek kaydı taşır. Ürün `hafiza.json` byte-eşit. `python3 -m unittest tests.test_hafiza_deposu` 3/3 (`test_ekle_yeni_okuyucuda_kalir`).
