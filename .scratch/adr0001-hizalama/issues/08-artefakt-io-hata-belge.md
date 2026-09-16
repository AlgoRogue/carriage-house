# 08: Artefakt IO hata belge (debt)

**Spec:** `.scratch/adr0001-hizalama/spec.md`

**What to build:**
`surucu_adim` docstring (ve ticket 02 uygulama notu) “Artefakt boş/yazılamazsa geçiş reddedilir” diyor; `mkdir`/`write_text` IO istisnaları yakalanmıyor. Birincil seam'de `isler_kok` konumuna dizin yerine dosya koyup dolu içerikle `isi_ilerlet` çağrılınca `NotADirectoryError` kaçıyor; kalıcı durum `planlaniyor` kalıyor.

Kabul edilemez artefaktın tam reddi Ticket 03 işi. 03 yapılırken uygulama ve belge birlikte hizalanmalı: ya IO yakalanıp geçiş reddedilir (durum Motor durumunda kalır, `park` değil) ya da docstring daraltılır. UTF-8/IO reddi 02'de tamamlanmış sayılmamalı.

**Blocked by:** 03 Kapı: `basari` ama kabul edilemez İş artefaktı (03 ile birlikte; 03 yapılırken hizalanıp kapatılabilir)

**Status:** done
 
- [x] Docstring / 03 davranışı hizalı: yazılamayan artefakt ya reddedilir ya da belge daraltılır
- [x] `mkdir`/`write_text` IO birincil seam'den kaçmaz (`NotADirectoryError` kanıtı)
- [x] Red halinde geçiş yok, bitiş Motor durumu, `park` değil; otomatik `hata` yok
- [x] Mutlu yol (02) kırılmaz
- [x] 03 ile aynı frontier; 03 yapılırken birleştirilip kapatılabilir
 
 ## Comments
 
 - 2026-09-16: Codex REVIEW-02 (ticket 02, engelleyici değil). Ticket 03 ile hizala. Kaynak: `.scratch/adr0001-hizalama/REVIEW-02.md` SP-D1.
- 2026-09-16: Ticket 03 ile birlikte tamamlandı ve kapatıldı. IO istisnaları (NotADirectoryError vb.) ve UTF-8 çözümleme hataları yakalanıp geçiş reddedildi; docstring güncellendi.
