# ADR-0001 hizalama — seam önerisi

Status: onaylandı (2026-09-16)

İnsan S1–S5 önerilerini onayladı. Birincil seam `isi_ilerlet`; spec `.scratch/adr0001-hizalama/spec.md` (`ready-for-agent`).
G3: yayın sonrası ADR-0004 + `personel/CH-0001/bin/README.md` birlikte yeniden okunur.
Kelime hazinesi: **module**, **interface**, **depth**, **seam**, **adapter**, **leverage**, **locality**.

## Dilim (ne hizalanır)

ADR-0001 kilitli: Sürücü duruma göre ince **Prompt şablonu** seçer ve yalnız kendisi doldurur; kimlik her çağrıda yazılmaz; **Motor girdisi** "şu **İş artefaktı** yolunu oku / şu yola yaz"dır; kontrol yalnız kapalı **Sinyal** (`basari` / `hata`); `basari` ama kabul edilebilir artefakt yoksa Sürücü ilerletmez.

Bugünkü CH-0001 bunu yapmıyor. `kart_motoru` Personel kartından CLI'yi çözüp `callable(durum) -> Sinyal` üretiyor; `komut(str(durum), …)` ile **durum adını istem sayıyor**. `SurucuAdim` Motor'a yalnız durum adını veriyor. **İş artefaktı** yok. Prompt şablonu yok. Sinyal dizgileri `motor_ciktisi` / `motor_hatasi` (ADR ile uyumsuz).

ROADMAP adım H: bu uyumsuzluğu kesmek + hurda/kalan. Adım 3 ve 5 hizalama bitmeden done değil.

## Önerilen seam (tek birincil)

**Birincil seam = Sürücü module'ünün mevcut dış interface'i: `isi_ilerlet`.**

Yeni seam açılmaz. Mevcut en yüksek giriş durur; arkasına ADR-0001 derinliği konur.

Testler bu interface'i çağırır: enjekte Motor, geçici durum kaydı, geçici **İş** klasörü. Gözlenen sonuç: `durum.json`, `isler/<is_id>/` altındaki **İş artefaktı** dosyaları, Motor'a giden doldurulmuş **Motor girdisi**, bitiş durumu. İç sınıflar birincil test yüzeyi değildir.

`interface` burada imza değil: çağıranın bilmesi gereken her şey — otonomi (`park`'a kadar tek çağrı), şablonu Sürücü'nün doldurması, artefakt kapısı, Sinyal sözlüğü, Motor'un hedef seçmemesi.

### Neden bu yükseklik

- **Mevcut seam tercih.** `isi_ilerlet` zaten tek giriş; mutlu yol / hata yolu / kart bağı buradan kanıtlanıyor. Yeni bir ürün yüzeyi yok.
- **Mümkün olan en yüksek.** Prompt seçimi, doldurma, Motor çağrısı, artefakt yazma, kapı, geçiş ve `park` döngüsü bu interface'in arkasında. Bir alt katmanı (şablon yükleyici, artefakt deposu, `SurucuAdim`) birincil yapmak **depth**'i böler, **locality**'yi kaçırır.
- **Tek ürün seam'i.** İdeal sayı birdir. Aşağıdaki Motor slot'u ikinci bir ürün seam'i değil; bu module'ün zaten var olan iç adapter yuvasıdır.
- **Interface = test yüzeyi.** Çağıran da test de `isi_ilerlet`'ten geçer. Şablon doldurucunun birim testi, artefakt yardımcısının birim testi, `kart_motoru.motor("planlaniyor")` birincil kanıt sayılmaz.

### Bu module'ün interface'i (küçük kalır, depth artar)

Sürücü module'ü (`isi_ilerlet` + arkası) **deep** kalır: küçük interface, büyük davranış.

Çağıran öğrenir:

1. Motor callable enjekte edilir (CLI spawn etmez).
2. `is_id` ve durum kaydı yolu verilir; **İş artefaktı** kökü testte enjekte edilir (üretimde Personel kaydı dizini altı).
3. Tek çağrı `park`'a (veya reddedilip durmaya) kadar gider.
4. Dönüş: başlangıç, bitiş, izlenen yol.
5. Yan etki: durum kaydı + kabul edilmiş adımların **İş artefaktı** dosyaları.

Çağıran öğrenmez: şablon slot envanteri, `Surucu` / `SurucuAdim` iç kuralları, CLI argv, `cozumle` alanları, Ajan hafızası.

**Leverage:** bir doldurma + kapı uygulaması, hem SahteMotor e2e'sine hem kart/CLI bağlı yola hem insan çağrısına yeter.

**Locality:** ADR-0001 sapması (durum adını istem yapmak, artefaktsız `basari`) tek yerde düzeltilir; N çağıran ve M test dağılmaz.

## Mevcut iç seam — Motor adapter slot'u (yeni değil)

Sürücü module'ünün içinde zaten gerçek bir seam var: Motor callable. **İki adapter = gerçek seam** (codebase-design):

| Adapter | Rol |
|---|---|
| `SahteMotor` | Ağsız test: CLI yok, hazır Sinyal (+ içerik kanalı) |
| Kart/CLI (`kart_motoru` rolü) | Personel kartı `cli`+`model` → şirket `komut`/`cozumle` → Sinyal |

Bu slot **kalır**. Değişen, yuvadaki **interface**'tir — konum değil.

Bugün (uyumsuz):

```
motor(durum: str) -> Sinyal    # girdi = durum adı = istem
```

ADR-0001 sonrası (öneri):

```
motor(girdi: str) -> (Sinyal, metin)
```

- `girdi` = Sürücü'nün doldurduğu **Prompt şablonu** (durum adı değil).
- `Sinyal` = `basari` | `hata`. Motor metni Sinyal değildir.
- `metin` = içerik kanalı. Sürücü bunu **İş artefaktı** olarak yazar. Kontrol akışına girmez.
  Üretim Motor adaptörleri yalnız `str` döner; artefakt yazıcısı `bytes`'ı da ham yazar
  (Debt 10) — yalnız test seam'inin geçersiz UTF-8 red yolunu kanıtlaması için, içerik
  şeması değil.
- Motor şablon seçmez, doldurmaz, hedef seçmez, `durum.json` yazmaz, kimlik ezberlemez.

Kart/CLI adapter'ı şirket `bin/motorlar` kaydını kopyalamaz; `komut(doldurulmuş_girdi, ayarlar)` + `cozumle` + `hata`→Sinyal. Koşucu enjekte durur (unittest CLI açmaz).

Bu iç seam'in kendi testleri *olabilir* (dört `cli`, bozuk kart, koşucu `OSError`) ama birincil ürün kanıtı değildir. Birincil kanıt: aynı adapter `isi_ilerlet`'e verildiğinde artefakt + durum.

İç seam'i dış interface'e taşımak (fabrika = birincil) reddedilir: fabrika sığ kalır (kart oku, komut kur, stdout parse); ADR-0001 derinliği Sürücü'dedir.

## Silme testi

**Sürücü module'ü (`isi_ilerlet` arkası) silinirse:** şablon seçimi, yol doldurma, tek atım çağrı, artefakt yazma, `basari`+eksik dosya kapısı, iskelet geçişi ve `park` döngüsü her çağıranda yeniden belirir. Karmaşıklık yok olmaz; N yere yayılır. Module hakkını kazandı.

**Prompt şablonu yükleyicisi ayrı public module olursa:** silince kalan "dosya oku, slot değiştir"dir. Pass-through. Public seam değil; Sürücü implementation'ının içi.

**İş artefaktı deposu ayrı public module olursa:** silince kalan yol birleştirme + dosya yazmadır. Sürücü'den başka çağıran yok (Kapı/Defter/eşleyici yok). Public seam değil.

**Bugünkü `kart_motoru` gövdesi silinirse:** "durum adını `-p`'ye koy" kaybı ADR kazancıdır, kayıp değil. Fabrika *rolü* silinirse kart→CLI→Sinyal her çağıranda kopyalanır — rol kalır, gövde hurda.

**`HafizaDeposu` bu dilimde silinirse:** Motor girdisine zaten bağlı değil; erken lift grill'de yok sayıldı ama prototype + debt duruyor. Silmek hizalama değil, ayrı verdict. Bu dilimde silinmez, bağlanmaz.

## Reddedilen (daha alçak veya yanlış) seam'ler

| Aday | Neden değil |
|---|---|
| `SurucuAdim.adim` | Şablon + artefakt + kapı buraya sığar ama dış çağıran `isi_ilerlet`. Birincil yüzey yapmak testleri implementation'a kilitler. |
| `Surucu.gecis` (çekirdek) | I/O yok, ADR-0001 yok. Saf kural module'ü durur; birincil hizalama yüzeyi değil. |
| Yeni `PromptSablonu` module'ü | Sığ; tek adapter (disk dosyası). |
| Yeni `IsArtefaktiDeposu` public seam'i | Tek çağıran (Sürücü). İç yardımcı olabilir, dış seam değil. |
| `motor_uret` / `kart_motoru.motor(durum)` | Bugünkü yanlış interface. Bunu birincil tutmak uyumsuzluğu dondurur. |
| Koşu sürücüsü (`bin/kos.py` / `dongu.py`) | Yanlış module. Personel **Sürücü**sü değil. |
| CLI dosya aracı (Motor'un diske kendisinin yazması) | Üretim Claude için ikinci bir disk adapter'ı ister; unittest'te SahteMotor dosya yazardı. CONTEXT: Sürücü içerik çıktısını artefakt olarak yazar. İlk dilimde CLI yazma zorunlu değil. |

## Hurda / kalan

### Hurda (bu dilimde kesilir veya gövdesi yeniden yazılır)

- `kart_motoru` uygulaması: `komut(str(durum), …)` — ADR-0001'in adlandırdığı uyumsuzluk.
- Motor callable sözleşmesi "girdi = durum adı".
- Sinyal dizgileri `motor_ciktisi` / `motor_hatasi` → kilitli sözlük `basari` / `hata`. `durum.json` `son_sinyal` aynı sözlüğe döner. Durum adı `hata` ile Sinyal `hata` çakışması domain'de kilitli; yeni ad uydurulmaz.
- Test kanıtı `"planlaniyor" in komut` (durum adının istem olduğu varsayımı). Yeni kanıt: doldurulmuş şablon + artefakt yolu; girdi ≠ yalnız durum adı.
- `.scratch/otomatik-motor-ch0001/issues/05-test-sahte-kosucu-tekrari.md` — bu dilim test yüzeyini yeniden yazınca borç büyük ihtimalle düşer; ayrı kapatılır, üretim davranışı "dokunma" vaadi kalkar.

### Kalan (silinmez; bu dilimde bağlanmaz veya rolü durur)

- Motor adapter slot'u + iki adapter (SahteMotor, kart/CLI). SahteMotor silinmez; interface'i güncellenir.
- `motor_uret` / `karti_ilerlet` *rolü*: ince fabrika + `isi_ilerlet`. Yeni durum makinesi açılmaz.
- `surucu_cekirdek`, `durum_deposu`, `park`'a kadar otonomi, iskelet salt okunur.
- Şirket `bin/motorlar` `komut`/`cozumle` — kopyalanmaz.
- **Ajan hafızası** (`HafizaDeposu`, `hafiza.json`): bağlanmaz; Defter/eşleyici yok; erken lift yok sayılır. Silme = ayrı prototype verdict (ROADMAP adım 3).
- G8 `sys.path` borç: gerçek paket importu bu dilimde yok.
- Kapı, Defter, Anlamsal eşleyici, usta, park sonrası, orkestrasyon kancası, şirket `kos`/`dongu`/`kapi`.
- İş sözleşmesi (ADR-0005): `is.md` / increment sözleşmesi icat edilmez. İlk Motor adımı (`planlaniyor`) yazma yolu taşır; okunacak tamamlanmış artefakt yoksa slot boş/yok.
- Ayrı debt: hafıza `04-bos-metin-kayit-testi`, `suite-sagligi/01-test-kit-bekci-kirmizi`.

### Bu dilimde üretilir (hurda değil, eksik)

- Durum adına göre **Prompt şablonu** dosyaları (Personel kaydı; Q10 D kilitli). Henüz yok.
- `personel/<numara>/isler/<is_id>/` altında **İş artefaktı** (ADR kilitli yol). Dosya adları uygulama dilimi — öneri aşağıda.

## Davranış özeti (seam'in arkasında, onay sonrası spec'e)

1. Motor durumlarında Sürücü şablonu seçer, yolları doldurur, Motor'u tek atım çağırır.
2. `basari` ise `metin`'i artefakt yoluna yazar; dosya yok/boş/bozuksa Sinyal geçersiz, **ilerlemez** (durum aynı, döngü durur — otomatik `hata` durumu değil).
3. `hata` Sinyali iskeletteki `hata` durumuna, sonra `park`'a gider (mevcut hata yolu).
4. `planlaniyor` yazımı: plan artefaktı. `delege_hazirlaniyor` okur: plan; yazımı: delege paketi.
5. Kimlik, yasak, skill, Ajan hafızası, Defter şablona girmez.
6. Mevcut `SahteMotor` e2e'si yeni interface ile yeşil kalır; gerçek CLI unittest'te yok.

## Onaylanan kararlar (2026-09-16)

Seam onayının kendisi **S1**. S2–S5 spec'e kilitli uygulama kararlarıdır.

**S1 — Birincil seam.** Onay. `isi_ilerlet` dış interface; Motor callable mevcut iç seam (SahteMotor + kart/CLI); yeni public seam yok.

**S2 — Artefaktı kim yazar.** Onay. Sürücü, Motor'un `metin` kanalını **İş artefaktı** olarak yazar; CLI dosya aracı bu dilimde zorunlu değil.

**S3 — Kapı başarısızlığı.** Onay. `basari` + kabul edilemez artefakt → geçiş yok, döngü durur, durum Motor durumunda kalır.

**S4 — Artefakt adları.** Onay. `planlaniyor` → `plan.md`; `delege_hazirlaniyor` → `paket.md`; kök `isler/<is_id>/`. İçerik şeması yok (varlık + boş değil).

**S5 — Sinyal dizgileri.** Onay. Üretim ve `son_sinyal` `basari`/`hata` olur (`motor_ciktisi` hurda). Durum adı `hata` aynı kalır.

Yayın: `.scratch/adr0001-hizalama/spec.md` (`Status: ready-for-agent`). G3 hâlâ açık: ADR-0004 + `personel/CH-0001/bin/README.md` birlikte yeniden okunur.
