# ADR-0001 hizalama + hurda/kalan — CH-0001 Sürücü

Status: ready-for-agent

Seam S1–S5 insan onaylı (2026-09-16). Kaynak: `SEAMS.md`. Bu belge uygulama sözleşmesidir.

## Problem Statement

Cengizhan'ın Sürücü'sü işi `bos`'tan `park`'a tek çağrıda götürüyor ve Personel kartındaki Motor'u bir fabrikadan çözüyor. Bu, ADR-0001'in tarif ettiği sürüş değil.

ADR-0001: Sürücü duruma göre ince bir Prompt şablonu seçer ve yalnız kendisi doldurur; kimlik ve yasaklar her çağrıda yazılmaz (Personel kaydı + CLI kalıcı yönlendirme). Şablon bu adımı "şu İş artefaktı yolunu oku / şu yola yaz"a indirger. Kontrol kapalı Sinyal sözlüğüdür (`basari` / `hata`); Motor metni Sinyal değildir. İçerik `isler/<is_id>/` altında İş artefaktı olur. `basari` ama kabul edilebilir artefakt yoksa Sürücü ilerletmez.

Bugün Motor callable'ı durum adını alır; kart fabrikası o adı CLI istemi yapar. Prompt şablonu yoktur. İş artefaktı yoktur. Sinyal dizgileri `motor_ciktisi` / `motor_hatasi`'dir. Ajan hafızası Sürücü'ye bağlı değildir (doğru) ama erken lift ROADMAP'te "done" gibi duruyordu; grill onu yok saydı.

İnsan, karttaki Motor'un iş üreteceğini sanır. Üretilen şey bir durum adı yankısı ve bir Sinyal'dir; sonraki adımın okuyacağı plan veya delege paketi diskte yoktur. Adım 3 ve 5 bu yüzden done değildir.

## Solution

Mevcut Sürücü girişini (`isi_ilerlet`) derinleştir: Motor durumlarında şablonu seç, doldur, Motor'u doldurulmuş Motor girdisi ile tek atım çağır, içerik kanalını İş artefaktı olarak yaz, kapıyı tut, sonra iskelet geçişini uygula. `park`'a kadar otonomi durur; kapı reddinde otonomi o Motor durumunda durur.

Motor adapter slot'u durur (SahteMotor + kart/CLI). Slot'un interface'i değişir: girdi doldurulmuş şablondur, çıkış Sinyal + içerik kanalıdır. Kart/CLI adapter'ının "durum adı = istem" gövdesi hurdadır; fabrika rolü ADR-0001'e göre yeniden yazılır.

Ajan hafızası, Defter, eşleyici, Kapı, usta, park sonrası ve şirket Koşu sürücüsü bağlanmaz. Hafıza dosyası silinmez.

## User Stories

1. İnsan olarak, Cengizhan bir işi `park`'a götürdüğünde diskte o işe ait plan ve delege paketi artefaktlarını görmek isterim; yalnız `durum.json` yetmez.
2. İnsan olarak, Motor'un serbest metninin sonraki durum sanılmamasını isterim; durumu yalnız Sürücü yazar.
3. İnsan olarak, `basari` deyip dosya bırakmayan bir Motor adımının işi ileri götürmemesini isterim.
4. İnsan olarak, Cengizhan'ın kimliğinin her Motor çağrısında yeniden anlatılmamasını isterim; kimlik Personel kaydı ve CLI zeminindedir.
5. İnsan olarak, karttaki Motor (`cli` + `model`) değişince bir sonraki çağrının yeni çifti kullanmasını isterim.
6. İnsan olarak, Ajan hafızasının bu dilimde Motor'a karışmamasını isterim; boş erken lift gerçeği gibi davranmasın.
7. Geliştirici olarak, birincil kanıtın `isi_ilerlet` olduğunu isterim; iç şablon yükleyiciyi veya artefakt yardımcısını birincil seam sanmam.
8. Geliştirici olarak, `isi_ilerlet`'e SahteMotor verince mutlu yolda `bos` → `park` gitmesini ve iki Motor durumunda artefakt yazılmasını isterim.
9. Geliştirici olarak, `planlaniyor` adımının plan artefaktını `isler/<is_id>/plan.md` olarak yazmasını isterim.
10. Geliştirici olarak, `delege_hazirlaniyor` adımının plan artefaktı yolunu okuma yönü, `isler/<is_id>/paket.md` yolunu yazma yönü olarak şablona doldurmasını isterim.
11. Geliştirici olarak, Prompt şablonunun durum adına göre ayrı dosya olmasını isterim; tek global şablon olmasın.
12. Geliştirici olarak, şablonu yalnız Sürücü'nün doldurmasını isterim; Motor ve fabrika slot doldurmasın.
13. Geliştirici olarak, şablona yapıştırılan şeyin artefakt metni değil yol/adres olmasını isterim.
14. Geliştirici olarak, Motor callable'ına giden metnin yalnız durum adı olmamasını isterim; doldurulmuş şablon olsun.
15. Geliştirici olarak, SahteMotor'un çağrı kaydında girdi olarak bu doldurulmuş metni görmek isterim.
16. Geliştirici olarak, kart/CLI adapter'ında koşucuya giden komutun `-p` yükünün doldurulmuş şablon olmasını, durum adının kendisinin olmasını istemem.
17. Geliştirici olarak, Sinyal sözlüğünün `basari` / `hata` olmasını isterim; `motor_ciktisi` / `motor_hatasi` üretimde kalmasın.
18. Geliştirici olarak, durum kaydındaki `son_sinyal`'in yeni sözlükle yazılmasını isterim.
19. Geliştirici olarak, durum adı `hata` ile Sinyal `hata`'nın ayrı kavramlar olarak kalmasını isterim; ikisini birleştirmem.
20. Geliştirici olarak, Motor `hata` Sinyali verince mevcut hata yolunun (`planlaniyor` → `hata` → `park`) tek çağrıda işlemesini isterim.
21. Geliştirici olarak, `basari` + boş veya yok artefaktta geçişin reddedilmesini ve döngünün durmasını isterim; iş sessizce `park`'a kaçmasın.
22. Geliştirici olarak, bu kapı reddinde durumun Motor durumunda kalmasını isterim (otomatik `hata` durumu değil; S3 kilitli).
23. Geliştirici olarak, Motor `hata` verdiğinde artefakt kapısının başarı yolunu açmamasını isterim.
24. Geliştirici olarak, `cozumle` çıktısındaki `metin` dışındaki `yapisal` / `maliyet` / `oturum` alanlarının sonraki durumu belirlememesini isterim.
25. Geliştirici olarak, Sürücü'nün Motor'u duruma göre tek atım çağırmasını isterim; unittest'in CLI içinde çok tur simüle etmemesini isterim.
26. Geliştirici olarak, Motor'un yalnız `planlaniyor` ve `delege_hazirlaniyor`'da çağrılmasını isterim.
27. Geliştirici olarak, `bos` → `is_alindi` → `planlaniyor` geçişlerinde Motor çağrılmamasını isterim.
28. Geliştirici olarak, `plan_hazir` → `delege_hazirlaniyor` ve `paket_hazir` → `park` geçişlerinde de Motor çağrılmamasını isterim.
29. Geliştirici olarak, iskeletin salt okunur kalmasını isterim.
30. Geliştirici olarak, Personel kartının bu dilimde yazılmamasını isterim.
31. Geliştirici olarak, testlerin ürün durum kaydına ve ürün kart dosyasına dokunmamasını isterim.
32. Geliştirici olarak, İş artefaktı yazımının testte enjekte kökte olmasını; Personel kaydı dizinini kirletmemesini isterim.
33. Geliştirici olarak, Prompt şablonu dosyalarının iskelet gibi salt okunur kanıtını (byte-eşit) isterim.
34. Geliştirici olarak, `isi_ilerlet(motor, …)` adının ve "Motor enjekte" şeklinin kalmasını isterim; yeni durum makinesi açılmasın.
35. Geliştirici olarak, isteğe bağlı ince kart girişinin (fabrika + `isi_ilerlet`) durmasını, gövdesinin yeni Motor interface'ini kullanmasını isterim.
36. Geliştirici olarak, SahteMotor'un silinmemesini; yeni interface'i karşılamasını isterim.
37. Geliştirici olarak, kayıtlı dört Motor `cli` değerinin (`claude`, `agy`, `codex`, `grok`) fabrikada çözülmesini isterim.
38. Geliştirici olarak, bilinmeyen `cli`'nin koşucudan önce başarısız olmasını isterim.
39. Geliştirici olarak, bozuk veya eksik `arka_yuz.motor` alanında koşucudan önce başarısız olunmasını isterim.
40. Geliştirici olarak, koşucu `OSError`'unun `hata` Sinyali olmasını ve Sürücü döngüsünün patlamamasını isterim.
41. Geliştirici olarak, skill listesinin komuta ve şablona girmemesini isterim.
42. Geliştirici olarak, şirket `komut`/`cozumle` adaptörlerinin kopyalanmamasını; CH-0001'in onları sarmalamasını isterim.
43. Geliştirici olarak, unittest'in `subprocess` açmamasını, ağ açmamasını, PATH'te CLI aramamasını isterim.
44. Geliştirici olarak, şirket Koşu sürücüsü ve Kapı betiklerinin bu dilimde değişmemesini isterim.
45. Geliştirici olarak, TERS_MOTOR / bekçi eşlemesinin CH-0001 bağında kullanılmamasını isterim.
46. Geliştirici olarak, `.env` okunmamasını isterim.
47. Geliştirici olarak, Kapı, Defter, Anlamsal eşleyici, usta ataması ve park sonrası durumların kurulmamasını isterim.
48. Geliştirici olarak, Ajan hafızası deposunun import edilmemesini ve Motor girdisine katılmamasını isterim; dosyanın da silinmemesini isterim.
49. Geliştirici olarak, ADR-0005 iş sözleşmesinin icat edilmemesini isterim; `planlaniyor`'da okunacak tamamlanmış artefakt yoksa şablon yalnız yazma yolu taşısın.
50. Geliştirici olarak, `usta_atandi` / `izleniyor` / `tamam`'a geçilmemesini isterim.
51. Geliştirici olarak, yasadışı iskelet geçişinin durumu değiştirmemesini isterim (çekirdek kuralı durur).
52. Geliştirici olarak, çekirdek kural module'ünün saf kalmasını; şablon ve dosya I/O'sunun oraya girmemesini isterim.
53. Geliştirici olarak, G3 sonrası insan okumasında personel Sürücü README ve ADR-0004 kutularının kart/CLI hurda notunu güncellemesini isterim (yayın sonrası; bu spec o dosyaları yazmaz).
54. Geliştirici olarak, test kanıtının "durum adı komutta geçiyor" olmamasını isterim; artefakt yolu şablonda, girdi durum adından ibaret değil.
55. Geliştirici olarak, `python3 -m unittest discover -s tests` ile ağsız yeşil kalmasını isterim.
56. İnsan olarak, bu dilim bitince ROADMAP adım H'nin kapanmaya aday olmasını; 3 ve 5'in hâlâ prototype/bağ kararına bağlı kalmasını isterim — sessiz done yok.
57. Geliştirici olarak, Motor durumlarında Sürücü'nün aynı callable'ı iki kez (plan, delege) doldurulmuş ayrı girdilerle çağırmasını isterim.
58. Geliştirici olarak, ikinci Motor çağrısının birinci artefakt yolunu şablonda görmesini isterim; metin yapıştırılmasın.
59. Geliştirici olarak, kabul edilmiş artefaktın UTF-8 metin dosyası olmasını; bu dilimde JSON şema doğrulaması icat edilmemesini isterim.
60. Geliştirici olarak, üretim kodunun personel-kapsamlı Sürücü yanında durmasını; şirket evre makinesine taşınmamasını isterim.

## Implementation Decisions

### Kilitli seam (S1–S5)

İnsan 2026-09-16'da onayladı. Uygulama bunları değiştirmez.

- **S1 — Birincil seam:** Sürücü module'ünün dış interface'i (`isi_ilerlet`). Yeni public seam yok. Test yüzeyi bu interface'tir. Motor callable mevcut iç seam olarak kalır (SahteMotor + kart/CLI).
- **S2 — Kim yazar:** Sürücü, Motor'un `metin` kanalını İş artefaktı yoluna yazar. CLI'nin kendisinin dosya yazması bu dilimde zorunlu değil; araç listesi politikası icat edilmez.
- **S3 — Kapı başarısızlığı:** `basari` + kabul edilemez artefakt → geçiş yok, döngü durur, durum Motor durumunda kalır. Otomatik `hata` durumu yok.
- **S4 — Artefakt adları:** `planlaniyor` → `plan.md`; `delege_hazirlaniyor` → `paket.md`; kök `isler/<is_id>/` (Personel kaydı dizini altında). İçerik şeması yok (varlık + boş değil).
- **S5 — Sinyal:** üretim ve `son_sinyal` `basari` / `hata` olur. `motor_ciktisi` / `motor_hatasi` hurda. Durum adı `hata` aynı kalır.

### Module ve interface

- **Birincil seam = `isi_ilerlet`.** Yeni ürün yüzeyi yok. Mevcut en yüksek giriş durur; arkasına ADR-0001 derinliği konur.
- Çağıran öğrenir: Motor callable enjekte edilir; `is_id` ve durum kaydı yolu verilir; İş artefaktı kökü testte enjekte edilir (üretimde Personel kaydı dizini altı); tek çağrı `park`'a veya kapı reddinde durmaya kadar gider; dönüş başlangıç, bitiş, izlenen yol; yan etki durum kaydı + kabul edilmiş adımların İş artefaktı dosyaları.
- Çağıran öğrenmez: şablon slot envanteri, iç adım sınıflarının kuralları, CLI argv, `cozumle` alanları, Ajan hafızası.
- **Depth:** şablon seçimi, doldurma, Motor çağrısı, artefakt yazma, kapı, geçiş ve `park` döngüsü Sürücü module'ünün implementation'ındadır. Prompt yükleyici ve artefakt yol birleştirme public module değildir (silme testi: pass-through).
- **Leverage:** bir doldurma + kapı uygulaması SahteMotor e2e'sine, kart/CLI bağlı yola ve insan çağrısına yeter.
- **Locality:** ADR-0001 sapması (durum adını istem yapmak, artefaktsız `basari`) tek yerde düzeltilir.

### İç seam — Motor adapter slot'u

Konum değişmez; yuvadaki interface değişir. İki adapter = gerçek seam. Şekil (onaylı seam belgesinden):

```
motor(girdi: str) -> (Sinyal, metin)
```

- `girdi` = Sürücü'nün doldurduğu Prompt şablonu (durum adı değil).
- `Sinyal` = `basari` | `hata`. Motor metni Sinyal değildir.
- `metin` = içerik kanalı. Sürücü bunu İş artefaktı olarak yazar. Kontrol akışına girmez.
  Üretim Motor adaptörleri yalnız `str` döner. Artefakt yazıcısı `bytes`'ı da ham olarak
  yazar (Debt 10, ticket `.scratch/adr0001-hizalama/issues/10-bytes-icerik-kanali.md`);
  bu yalnız test seam'inin geçersiz UTF-8 red yolunu kanıtlaması içindir, içerik şeması
  icat edilmez, mutlu yolu (yalnız `str`) değiştirmez.
- Motor şablon seçmez, doldurmaz, hedef seçmez, durum kaydı yazmaz, kimlik ezberlemez.
- `cozumle["hata"]` veya bozuk stdout veya koşucu `OSError` → `hata`; aksi `basari`.
- Kart/CLI adapter'ı şirket Motor kaydını kopyalamaz; `komut(doldurulmuş_girdi, ayarlar)` + `cozumle` + `hata`→Sinyal. Koşucu enjekte durur.
- İç seam'in kendi testleri olabilir (dört `cli`, bozuk kart, koşucu `OSError`) ama birincil ürün kanıtı değildir. Birincil kanıt: aynı adapter `isi_ilerlet`'e verildiğinde artefakt + durum.
- Fabrikayı birincil yapmak reddedilir: fabrika sığ kalır; ADR-0001 derinliği Sürücü'dedir.

### Prompt şablonu ve İş artefaktı

- Prompt şablonu Personel kaydı altında, durum adına göre ayrı dosyalar. Slot'lar yol/adres; kimlik, skill, hafıza, Defter yok.
- İlk Motor adımında (`planlaniyor`) okunacak tamamlanmış artefakt yoksa yalnız yazma yolu doldurulur (`isler/<is_id>/plan.md`).
- İkinci Motor adımında (`delege_hazirlaniyor`) okuma: `plan.md` yolu; yazma: `paket.md` yolu. Plan metni şablona yapıştırılmaz.
- Kabul: dosya var, UTF-8 okunur, boş değil. İçerik şeması yok.
- Kapı fail → S3. Motor `hata` → mevcut iskelet hata yolu (`hata` durumu, sonra `park`); başarı kapısı açılmaz.

### Fabrika, hurda, kalan

- Fabrika rolü kalır: kart salt okunur; `cli`+`model` şirket kaydından çözülür; koşucu enjekte; bilinmeyen `cli` koşucudan önce hata. `ayarlar.model` karttandır. İnce kart girişi yalnız fabrika + `isi_ilerlet`.
- **Hurda:** durum adını istem sayan fabrika gövdesi; eski Motor callable sözleşmesi (`callable(durum) -> Sinyal`); eski Sinyal dizgileri; "durum adı komutta" test kanıtı.
- **Kalan:** SahteMotor (interface güncellenir); çekirdek saf kurallar (Sinyal dizgileri yeni sözlüğe çekilir; I/O girmez); durum deposu; şirket Motor adaptörleri; Ajan hafızası (bağsız, silinmez); G8 path hack; Kapı/Defter/eşleyici/usta/orkestrasyon.
- **Bu dilimde üretilir:** durum adına göre Prompt şablonu dosyaları; `isler/<is_id>/plan.md` ve `paket.md`.
- **Dil ve şekil:** ADR-0002 Python; ADR-0003 modüler monolit (yeni process yok). CH-0001 personel-kapsamlı `bin` durur.
- İskelet ve dilim kümesi önceki Sürücü diliminde kilitli; bu dilim iskeleti değiştirmez, park sonrası durumlara geçmez.

## Testing Decisions

- İyi test dış davranışı ölçer: `isi_ilerlet` sonrası durum kaydı, İş artefaktı dosyaları, Motor'a giden girdi, çağrı sayısı. İç sınıf, iç yardımcı ve şablon doldurma fonksiyonu birincil yüzey değildir. Interface test yüzeyidir.
- **Birincil seam:** `isi_ilerlet`. Motor enjekte (SahteMotor veya fabrika + sahte koşucu).
- **İç seam kanıtı (ikincil):** fabrika hâlâ kart/cli/koşucu eşlemesini kanıtlar; "durum adı komutta" kanıtı geçersizdir. Yeni kanıt: doldurulmuş girdi, artefakt yolu, girdi ≠ yalnız durum adı.
- **Önceki sanat:** Sürücü e2e (SahteMotor + geçici durum kaydı + `isi_ilerlet`); kart/CLI testleri (sahte koşucu, kart kopyası). Aynı düzen; beklenen girdi ve artefakt iddiaları değişir. Çekirdek testleri saf kural olarak kalır; Sinyal dizgileri yeni sözlüğe çekilir.
- **Kapsanacak senaryolar:**
  - Mutlu yol: tek çağrı, `bos` → `park`, iki Motor çağrısı, iki kabul edilebilir artefakt (`plan.md`, `paket.md`).
  - Motor girdisi doldurulmuş şablon; durum adı tek başına istem değil; delege adımında plan yolu var, plan metni yok.
  - `basari` + boş/yok artefakt: durum ileri gitmez, `park` olmaz, durum Motor durumunda kalır.
  - `hata` stdout / koşucu `OSError`: `hata` → `park`; sahte başarı metni durum seçmez.
  - Kart çözümü: CH-0001 `claude`/`sonnet`; dört kayıtlı `cli`; bilinmeyen `cli`; bozuk kart; skill etkisiz; kart byte-eşit.
  - Gerileme: SahteMotor e2e yeni interface ile yeşil; iskelet byte-eşit; ürün durum/kart byte-eşit; hafıza okunmaz.
- **Test yeri:** `tests/`, `python3 -m unittest discover -s tests`. Ağ yok, gerçek Motor yok.
- "Motor'a yalnız durum adı ver" iddiaları birincil olmaktan çıkar; depth Sürücü interface'ine taşındı (replace, don't layer).

## Out of Scope

- Kapı, Defter, Anlamsal eşleyici, Orkestrasyon kancası, usta ataması, park sonrası durumlar.
- Ajan hafızasını Motor girdisine bağlamak veya hafıza deposunu silmek.
- İş sözleşmesi / increment sözleşmesi (ADR-0005).
- Unittest içinde gerçek CLI; PATH'te ikili arama; CLI'nin araçla diske yazması.
- Prompt şablonuna kimlik, skill, yasak, Defter veya hafıza parçası gömmek.
- Artefakt içerik şeması, kalite bekçisi, `yeniden` Sinyali.
- Şirket Koşu sürücüsü / döngü / Kapı / evre / TERS_MOTOR / maliyet tavanı kopyası.
- Şirket Motor `komut`/`cozumle` iç mantığını yeniden yazmak.
- Aksiyon iskeleti veya Personel kartı şeması değişikliği.
- G8 gerçek paket importu.
- UI; başka personel numarasına taşıma.
- `test_kit` kırmızısı ve hafıza debt 04 (ayrı ticket).
- G3 (ADR-0004 + personel Sürücü README birlikte yeniden okuma) — yayın sonrası ayrı adım; bu spec o dosyaları yazmaz.

## Further Notes

Kaynak: `docs/adr/0001-surucu-motoru-nasil-surer.md` (kilit), 0002–0005, `CONTEXT.md` (Sürücü, Motor, Motor girdisi, Prompt şablonu, İş artefaktı, Sinyal), `ROADMAP.md` adım H, personel Sürücü README, ADR-0004 hurda notu, `.scratch/otomatik-surucu-ch0001/spec.md` ve `.scratch/otomatik-motor-ch0001/spec.md` (erken lift; bu dilim onları supersede eder).

Seam belgesi: `.scratch/adr0001-hizalama/SEAMS.md` (S1–S5 onaylı).

G3: bu spec yayınlandıktan sonra ADR-0004 + `personel/CH-0001/bin/README.md` birlikte yeniden okunur; kutular yanlışsa düzeltilir. Uygulama ajanı o okumayı bu spec'in işi sanmaz.

Tracker: `.scratch/adr0001-hizalama/` — bu turda issue dosyası açılmaz.
