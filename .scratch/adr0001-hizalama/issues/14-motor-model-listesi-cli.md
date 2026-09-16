# 14: Motor model listesi CLI'den (debt)

**Spec:** `.scratch/adr0001-hizalama/spec.md`

**What to build:**
Seçilen Motor cli'ye göre model listesini kurulu CLI'den çek (adaptör yüzü `modelleri_listele` / eşdeğeri). Kart düzenlemede cli→model seçimi bu listeye bağlanır.

Koşuda her `isi_ilerlet`'te canlı `models` çağrısı yok: seçim anı + önbellek. grok/agy: `models` alt komutu var. claude/codex keşif yarım — claude alias tablosu veya önbellek; codex headless yol sonra. Unittest ağsız. Sürücü bu yüzü bilmez.

H implement'ini bloklamaz.

**Blocked by:** None

**Status:** ready-for-agent

- [ ] Seçilen Motor cli'ye göre model listesi kurulu CLI'den çekilir (`modelleri_listele` veya eşdeğeri)
- [ ] Kart düzenlemede cli→model seçimi bu listeye bağlanır
- [ ] `isi_ilerlet` her çağrıda canlı models açmaz; seçim anı + önbellek
- [ ] grok/agy: `models` alt komutu; claude: alias tablosu veya önbellek; codex headless yol sonra
- [ ] Unittest ağsız yeşil; gerçek CLI/ağ açılmaz
- [ ] Sürücü adaptör yüzünü bilmez (kart/adaptör katmanı)

## Comments

- 2026-09-16: debt kuyruğa alındı. H 01–13 done; bu bilet frontier 4'ü değiştirmez.
