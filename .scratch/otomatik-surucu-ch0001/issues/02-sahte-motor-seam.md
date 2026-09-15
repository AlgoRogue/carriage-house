# 02: Sahte Motor seam'i ve tek-adım Sürücü çağrısı

**What to build:**
`tests/test_kit.py`'deki `SahteMotor` desenine benzer, enjekte edilebilir bir sahte motor (gerçek
CLI/subprocess çağrısının yerine geçer, hazır bir sinyal — "çıktı geldi" ya da "hata" — döner ve
kaç kez/ne zaman çağrıldığını kaydeder).

01'deki saf geçiş fonksiyonunu, bu sahte motorla birlikte kullanan tek-adım bir Sürücü çağrısı
yaz: mevcut durum bir Motor durumuysa (`planlaniyor`/`delege_hazirlaniyor`) motoru çağırır, dönen
sinyali geçiş fonksiyonuna verir; mevcut durum Motor durumu değilse (`bos`, `plan_hazir`,
`paket_hazir`, `park`, `hata`) motoru hiç çağırmadan iskeletteki tek geçerli geçişi uygular.

Bu bilet tek bir adım/geçiş için Motor çağırma kararını doğrular — `bos`'tan `park`'a tam otomatik
zincirleme henüz yok (bkz. 04).

**Blocked by:** 01

**Status:** ready-for-agent

- [ ] Sahte motor, gerçek subprocess/CLI çağrısı yapmadan enjekte edilebilir (test_kit.py'deki
      `SahteMotor` gibi çağrıları kaydeder)
- [ ] `planlaniyor` veya `delege_hazirlaniyor` durumunda tek adım çağrıldığında sahte motor tam
      olarak bir kez çağrılır
- [ ] `bos`, `plan_hazir`, `paket_hazir`, `park`, `hata` durumlarından herhangi birinde tek adım
      çağrıldığında sahte motor hiç çağrılmaz
- [ ] Sahte motorun "çıktı geldi" sinyali, 01'in geçiş fonksiyonu aracılığıyla doğru başarı hedefine
      (`plan_hazir` ya da `paket_hazir`) geçer; hedefi motor değil iskelet belirler
- [ ] Sahte motorun "hata" sinyali `hata` durumuna geçer
- [ ] Bu adımda hâlâ dosya I/O yok (durum bellekte tutulur); kalıcılık 03'te eklenir
