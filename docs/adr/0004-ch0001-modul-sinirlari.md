# CH-0001 Sürücü modül sınırları

`personel/CH-0001/bin` içinde sorumluluklar ayrılır:

- `surucu_cekirdek`: saf geçiş/sinyal kuralları; I/O yok
- `surucu_adim`: tek geçiş; Motor callable çağrısı
- `surucu`: park'a kadar döngü (otonomi)
- `durum_deposu` / `surucu_kalici_gecis`: disk durumu
- `sahte_motor`: ağsız test Motor'u
- `kart_motoru`: **geçici / hurda adayı** (ADR-0001 ile uyumsuz; hizalama to-spec'inde ele alınır)
- `hafiza_deposu`: **geçici / hurda veya yeniden lift adayı** (grill'de yok sayıldı; prototype kararı + hizalama sonrası)

İnsan okunur harita: `personel/CH-0001/bin/README.md`.

**Gözden geçirme:** Hizalama **to-spec** yayımlandıktan sonra bu ADR + README birlikte yeniden okunur; kutular yanlışsa düzeltilir (G3 şartı).
