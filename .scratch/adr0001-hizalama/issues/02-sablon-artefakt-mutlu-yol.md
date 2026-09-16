# 02: Mutlu yol: Prompt şablonu, İş artefaktı, park

**Spec:** `.scratch/adr0001-hizalama/spec.md`

**What to build:**
İnsan `isi_ilerlet`'i bir kez çağırınca iş `bos`'tan `park`'a gider ve diskte o işe ait `isler/<is_id>/plan.md` ile `isler/<is_id>/paket.md` durur. Sürücü module'ü duruma göre Prompt şablonunu seçer, yalnız kendisi doldurur (slot = yol/adres, metin yapıştırılmaz) ve doldurulmuş Motor girdisi ile Motor'u tek atım çağırır. İçerik kanalını Sürücü yazar (S2). Kimlik, skill, yasak, Defter, Ajan hafızası şablona girmez.

Birincil seam `isi_ilerlet` kalır; yeni public module yok (Prompt yükleyici ve artefakt yardımcısı public seam değildir — silme testi: pass-through). Aynı doldurma hem SahteMotor e2e'sine hem kart/CLI bağlı yola yeter (**leverage**). **Depth** Sürücü implementation'ındadır: şablon, doldurma, Motor çağrısı, artefakt yazma, geçiş, `park` döngüsü.

**Blocked by:** 01 Prefactor: Sinyal sözlüğü ve Motor callable şekli

**Status:** done

- [x] Tek çağrı, iki Motor çağrısı (`planlaniyor`, `delege_hazirlaniyor`); diğer geçişlerde Motor yok
- [x] `planlaniyor` yazımı: `plan.md`. Okunacak tamamlanmış artefakt yoksa yalnız yazma yolu
- [x] `delege_hazirlaniyor` okuma: `plan.md` yolu; yazma: `paket.md` yolu; plan metni şablonda yok
- [x] SahteMotor çağrı kaydında girdi doldurulmuş şablon; girdi ≠ yalnız durum adı
- [x] Kart/CLI yolunda koşucunun `-p` yükü doldurulmuş şablon; "durum adı komutta" birincil kanıt değil
- [x] İş artefaktı kökü testte enjekte; ürün Personel kaydı, kart, iskelet, şablon dosyaları byte-eşit
- [x] `HafizaDeposu` import edilmez; `hafiza.json` silinmez; şirket `kos` / `dongu` / `kapi` değişmez
- [x] `python3 -m unittest discover -s tests` ağsız yeşil

## Comments

- 2026-09-16: yayınlandı (to-tickets adım 5). Durum: ready-for-agent. 01 bitince frontier.
- 2026-09-16: 01 done; asıl frontier. REVIEW-01 debt 05/06 ürün sırasını bloklamaz.
- 2026-09-16: uygulandı (Claude Code). `SurucuAdim` artık motor durumlarında `personel/CH-0001/sablonlar/<durum>.md`
  şablonunu okuyup yalnız yol/adres slotlarını (`is_id`, `yaz_yolu`, `delege_hazirlaniyor` için `oku_yolu`) doldurur;
  bu doldurulmuş metin Motor'a girdi olur. `basari` sinyalinde `metin` `isler/<is_id>/{plan,paket}.md`'ye yazılır;
  boş/yazılamayan artefaktta geçiş reddedilir, durum Motor durumunda kalır (S3, otomatik `hata` yok). `isi_ilerlet`
  ve `karti_ilerlet` yeni `isler_kok` parametresi alır (üretim varsayılanı Personel kaydı altı `isler/`, testler
  geçici dizin enjekte eder). `kart_motoru.motor_uret` değişmedi — zaten jenerik `girdi` alıyordu, doldurulmuş
  şablon otomatik CLI `-p` yüküne taşındı. `test_surucu*.py` yeni sözleşmeye güncellendi (dosya IO/subprocess
  ayrımı netleşti: şablon+artefakt IO'ya izin var, subprocess/ağ hâlâ yasak). `python3 -m unittest discover -s tests`
  yeşil; tek istisna önceden kırmızı `test_kit.BekciKatmanA.test_kosuda_anayasaya_dokunan_ajan_red` (Out of Scope,
  dokunulmadı).
