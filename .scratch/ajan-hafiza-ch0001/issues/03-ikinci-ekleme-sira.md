# 03: İkinci ekleme ilk kaydı silmez, sıra korunur

**Spec:** `.scratch/ajan-hafiza-ch0001/spec.md`

**What to build:**
Aynı Ajan hafızasına ikinci bir `metin` eklenir. Okuma iki kaydı da, ekleme sırasıyla, döner. İkinci yazma depoyu değiştirmez, sona ekler. Prototipin "yazılabilir" olduğu, tek kayıttan sonra da append-only kaldığı bu bilette görünür.

Sürücü, Motor ve orkestrasyon hâlâ bağlanmaz. Bu bilet depo API'sini onlara takmaz.

**Blocked by:** 02 (Tek kayıt ekle)

**Status:** done

- [x] İki `ekle` sonrası `oku()` iki kaydı ekleme sırasıyla döner (`metin` değerleri eşleşir)
- [x] İkinci yazma ilk kaydı silmez veya üzerine yazmaz
- [x] Yazma testi geçici yol kullanır; committed `hafiza.json` byte-eşit kalır
- [x] Unittest ağsızdır; `python3 -m unittest discover -s tests` ile keşfedilir
- [x] Bu dilim Sürücü / Motor / `isi_ilerlet` / `kos` / `dongu` / `kapi` bağını açmaz
- [x] Defter dosyası veya anlamsal eşleme fonksiyonu eklenmez

## Comments

- 2026-09-15: yayınlandı (to-tickets). Durum: ready-for-agent.
- 2026-09-15: İki `ekle` sırayı korur; ikinci yazma ilk kaydı silmez. Defter / eşleyici / Sürücü bağı yok. `python3 -m unittest tests.test_hafiza_deposu` 3/3 (`test_ikinci_ekleme_sirayi_korur`). Discover bu 3 testi yeşil bulur.
