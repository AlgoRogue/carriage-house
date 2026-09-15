# 01: Sürücü çekirdeği: iskelet-tabanlı geçiş fonksiyonu (saf mantık)

**What to build:**
`personel/CH-0001/aksiyon-iskeleti.json`'daki `gecisler` listesini ve bu dilimin dilim kümesini
(`{bos, is_alindi, planlaniyor, plan_hazir, delege_hazirlaniyor, paket_hazir, park, hata}`) girdi
alan, saf (dosya I/O'suz, bellek-içi) bir geçiş fonksiyonu/sınıf. `usta_atandi`, `izleniyor`, `tamam`
iskelette var ama bu dilimde etkin değil — fonksiyon bu durumlara hiç geçmemeli.

Fonksiyon, mevcut durum + hedef durum (ve varsa sinyal) alır, şu sırayla doğrular:
1. Hedef, iskelette geçerli bir `from`/`to` çifti mi?
2. Hedef, dilim kümesinde mi?
3. Mevcut durum bir Motor durumuysa (`planlaniyor`/`delege_hazirlaniyor`), geçerli bir sinyal geldi mi?

Üçü de sağlanmıyorsa geçiş reddedilir ve durum değişmez (hata fırlatma ya da açık red sonucu — uygulama
tercihi, ama sessizce yutmamalı). Motor hedefleri (`plan_hazir`, `paket_hazir`) kod içinde sabitlenmez;
`motor_cagrilan_durumlar` girişleri için o durumdan çıkan, `hata` olmayan geçişten iskeletten hesaplanır.

Bu bilet yalnız saf mantığı kapsar — dosya okuma/yazma, Motor çağrısı, tam zincirleme sonraki
biletlerde.

**Blocked by:** None (can start immediately)

**Status:** ready-for-agent

- [ ] Geçiş fonksiyonu/sınıfı hiçbir dosya okumaz/yazmaz; iskelet verisi ve dilim kümesi parametre/sabit olarak verilir
- [ ] Motor hedefleri (`planlaniyor`→`plan_hazir`, `delege_hazirlaniyor`→`paket_hazir`) iskeletten türetilir, kod içinde hardcode edilmez
- [ ] İskelette tanımsız bir `from`/`to` hedefi reddedilir, durum değişmez
- [ ] Dilim kümesi dışındaki bir hedef (iskelette tanımlı olsa bile, ör. `usta_atandi`) reddedilir, durum değişmez
- [ ] Motor durumunda (`planlaniyor`/`delege_hazirlaniyor`) geçerli sinyal olmadan hedefe geçiş reddedilir
- [ ] Motor durumu dışındaki bir anda gelen sinyal reddedilir
- [ ] Doğrudan unittest ile test edilebilir (dosya sistemi, subprocess veya ortam değişkeni gerektirmez)
