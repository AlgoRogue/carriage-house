# 03: durum.json okuma/yazma ve dosya kalıcılığı

**What to build:**
`personel/CH-0001/durum.json`'u okuyan ve yazan bir katman: `durum`, `is_id`, `son_sinyal`
alanlarını günceller. `personel/CH-0001/aksiyon-iskeleti.json` bu bilette de dahil hiçbir koşulda
yazılmaz — yalnız salt-okunur okunur (testte içerik değişmediği doğrulanmalı).

Bu bilet, 01'deki saf geçiş fonksiyonunu tek bir geçiş için `durum.json`'a bağlar: geçiş öncesi
dosyadan mevcut durumu okur, geçiş uygulanırsa yeni `durum`/`is_id`/`son_sinyal` değerlerini yazar;
geçiş reddedilirse dosyaya dokunmaz. Henüz `bos`'tan `park`'a tam otomatik zincirleme yok (bkz. 04)
— bu bilet tek bir geçişin dosyaya doğru yazıldığını/yazılmadığını kanıtlar.

**Blocked by:** 01

**Status:** ready-for-agent

- [ ] `personel/CH-0001/durum.json` okunur ve (geçiş kabul edildiğinde) yazılır
- [ ] `personel/CH-0001/aksiyon-iskeleti.json` bu bilette hiç yazılmaz — test, dosya içeriğinin
      çağrı öncesi/sonrası birebir aynı kaldığını doğrular
- [ ] Kabul edilen bir geçişten sonra `durum.json`'daki `durum` alanı doğru yeni duruma güncellenir
- [ ] Kabul edilen bir geçişten sonra `is_id` ve `son_sinyal` alanları da güncellenir (yalnız
      `durum` değil)
- [ ] Reddedilen bir geçiş denemesinde `durum.json` hiç değişmez (dosya yazılmaz ya da içerik aynı
      kalır)
- [ ] Test, gerçek `personel/CH-0001/durum.json` yerine geçici/kopya bir dosya üzerinde çalışır
      (kalıcı prod dosyasını bozmaz)
