# Otomatik Motor bağlama - CH-0001 (Cengizhan)

Status: ready-for-agent

## Problem Statement

CH-0001 Sürücü'sü işi `bos`'tan `park`'a kadar tek çağrıda ilerletiyor. Motor seam'i `callable(durum) -> Sinyal` olarak kilitli; mevcut uçtan uca testler bu sözleşmeyi `SahteMotor` ile dolduruyor. Personel kartının arka yüzünde Motor zaten yazılı (`cli: claude`, `model: sonnet`). Şirketin Motor adaptörleri de duruyor: her CLI için `komut` + `cozumle`, kayıt `motor_al` ile çözülüyor.

Bu iki uç henüz birbirine bağlı değil. Sürücü karttaki Motor'u okumuyor. Adaptörün `hata` alanı Sürücü'nün `Sinyal` enum'una çevrilmiyor. Gerçek CLI henüz (ve bu dilimde unittest içinde olmayacak) çağrılmıyor; ama sahte koşucu ile "kart → adaptör sözleşmesi → Sinyal" yolu da yok. İnsan Cengizhan'ın kartındaki Motor'u değiştirdiğinde Sürücü'nün bunu kullanacağına dair bir bağ yok.

Önceki dilim bunu bilinçli olarak dışarıda bıraktı: "gerçek CLI Motor üretim bağlaması bu dilimde yok, yalnız sahte motor." Bu spesifikasyon o ertelenen bağı kurar. CLI'yi unittest'te çalıştırmaz.

## Solution

Kartı okuyan bir fabrika: Personel kartı arka yüzündeki `motor.cli` + `motor.model` ile kayıtlı adaptörü çözer ve Sürücü'nün beklediği `callable(durum) -> Sinyal` Motor'u döner.

Koşucu enjekte edilir. Testler CLI spawn etmez, ağ açmaz. Koşucu, adaptörün ürettiği komut listesini alır ve stdout (ve gerekirse çıkış kodu) döner; fabrika `cozumle` sonucundaki `hata` alanını `Sinyal`'e çevirir. Motor hedef seçmez, durum yazmaz.

Mevcut `isi_ilerlet(motor, ...)` imzası kalır. İsteğe bağlı, ince bir kart giriş noktası fabrika + `isi_ilerlet` çağrısını birleştirebilir; yeni bir durum makinesi açmaz.

`SahteMotor` durur. Mevcut e2e (mutlu yol ve hata yolu) sahte Motor ile geçmeye devam eder.

## User Stories

1. İnsan olarak, Cengizhan'ın Personel kartındaki Motor (`cli` + `model`) ile işin ilerleyeceğini bilmek isterim; her işte varsayılana dönülmesini istemem.
2. İnsan olarak, karttaki Motor'u değiştirdiğimde (ör. `cli` veya `model`) bir sonraki Sürücü çağrısının yeni değeri kullanmasını isterim.
3. İnsan olarak, Motor'un plan veya delege metnini "sonraki durum" sanmamasını; durumu yalnız Sürücü'nün yazmasını isterim.
4. Geliştirici olarak, kartı okuyan bir fabrikanın `callable(durum) -> Sinyal` döndürmesini isterim; böylece mevcut Sürücü girişini değiştirmeden gerçek adaptöre bağlanabilirim.
5. Geliştirici olarak, fabrikaya bir koşucu enjekte ederek unittest'te hiçbir CLI sürecinin açılmamasını isterim.
6. Geliştirici olarak, CH-0001 kartının (`claude` / `sonnet`) çözüldüğünü ve üretilen komutta bu `cli` ile `model`'in göründüğünü doğrulamak isterim.
7. Geliştirici olarak, kayıtlı dört Motor adının (`claude`, `agy`, `codex`, `grok`) her birinin kart `cli` değeri olarak çözülmesini isterim.
8. Geliştirici olarak, bilinmeyen bir `cli` verildiğinde koşucu çağrılmadan çözümlemenin başarısız olmasını isterim.
9. Geliştirici olarak, `arka_yuz.motor` eksik veya bozuksa (cli yok, motor nesnesi yok) çözümlemenin başarısız olmasını isterim.
10. Geliştirici olarak, adaptör `cozumle` çıktısında `hata: false` ise Sinyal'in `motor_ciktisi` olmasını isterim.
11. Geliştirici olarak, adaptör `hata: true` veya bozuk stdout ise Sinyal'in `motor_hatasi` olmasını isterim.
12. Geliştirici olarak, koşucu istisnasının (ör. OSError) da `motor_hatasi` Sinyali üretmesini; Sürücü döngüsünün patlamamasını isterim.
13. Geliştirici olarak, fabrika Motor'unu mevcut `isi_ilerlet`'e verince mutlu yolda işin `bos`'tan `park`'a gitmesini ve `durum.json`'un Sürücü tarafından yazılmasını isterim.
14. Geliştirici olarak, bu bağlı mutlu yolda koşucunun yalnız `planlaniyor` ve `delege_hazirlaniyor` için çağrıldığını görmek isterim.
15. Geliştirici olarak, hata stdout'unun `hata` durumuna, ardından `park`'a düştüğünü mevcut hata yolu gibi tek çağrıda görmek isterim.
16. Geliştirici olarak, Motor çıktısındaki `metin` / `yapisal` / `maliyet` alanlarının bu dilimde sonraki durumu belirlememesini isterim; yalnız `hata` Sinyal'e gider.
17. Geliştirici olarak, mevcut `SahteMotor` e2e testlerinin kırılmadan geçmesini isterim; SahteMotor silinmesin veya zorunlu kılınmasın.
18. Geliştirici olarak, `isi_ilerlet(motor, ...)` imzasının aynı kalmasını isterim; kart okuma fabrikada veya ince bir sarmalayıcıda kalsın.
19. Geliştirici olarak, isteğe bağlı ince bir kart girişinin (fabrika + `isi_ilerlet`) olmasını, yeni bir durum makinesi açmamasını isterim.
20. Geliştirici olarak, Personel kartı dosyasının bu dilimde yazılmamasını; fabrikanın kartı salt okumasını isterim.
21. Geliştirici olarak, aksiyon iskeletinin bu dilimde değişmemesini isterim.
22. Geliştirici olarak, şirket sürücüsünün (`kos` / `dongu`) bu bağa zorlanmamasını; CH-0001 Sürücü'sünün ayrı kalmasını isterim.
23. Geliştirici olarak, Kapı, defter, ajan hafızası, anlamsal eşleyici ve orkestrasyon kancasının bu dilimde kurulmamasını isterim.
24. Geliştirici olarak, karttaki skill listesinin bu dilimde okunup işe yansımamasını isterim; bağ yalnız Motor alanındadır.
25. Geliştirici olarak, TERS_MOTOR / bekçi eşlemesinin CH-0001 bağında kullanılmamasını isterim.
26. Geliştirici olarak, `.env` okunmamasını; anahtarın ekrana veya kayda dökülmemesini isterim.
27. Geliştirici olarak, ANAYASA tavanlarının (süre, USD, günlük koşu) bu dilimde CH-0001'e kopyalanmamasını isterim.
28. Geliştirici olarak, istem metninin yalnız durum adından türetilmesini; İş metni, hafıza veya skill yönlendirmesi eklenmemesini isterim.
29. Geliştirici olarak, koşucuya giden argv'nin testte kaydedilmesini (ilk token = cli, model karttan) isterim.
30. Geliştirici olarak, üretim kodunun personel-kapsamlı Sürücü yanında durmasını; şirket `bin/motorlar` kaydını sarmalayıp kopyalamamasını isterim.

## Implementation Decisions

Kilitli seam'ler (bu dilimde değişmez):

1. **Fabrika** Personel kartını okur, kayıtlı adaptörü çözer, `callable(durum) -> Sinyal` döner. Yeni ürün yüzeyi budur.
2. **Koşucu** fabrikaya enjekte edilir. Testler her zaman sahte koşucu verir; CLI spawn etmez. Koşucu komut listesi alır, stdout (ve gerekirse çıkış kodu) döner.
3. **Mevcut `isi_ilerlet(motor, ...)` kalır.** İsteğe bağlı ince kart girişi yalnızca fabrika + `isi_ilerlet` çağrısıdır; yeni makine değildir.

Mevcut Motor callable sözleşmesi (önceki dilimin kilitlediği, bu dilimin uyacağı şekil):

```
motor(durum: str) -> Sinyal   # motor_ciktisi | motor_hatasi
```

Personel kartı Motor alanı (CH-0001 kartından, şema değişmez):

```
arka_yuz.motor = { "cli": "<kayıtlı ad>", "model": "<adaptöre giden model>" }
```

CH-0001 bugün `cli: claude`, `model: sonnet`. Fabrika bu iki alanı okur; skill listesine bakmaz.

- Fabrika şirket Motor kaydını (`motor_al` / dört adaptör) kullanır. Yeni adaptör dosyası yazılmaz; mevcut `komut` / `cozumle` / `YETENEK` yüzü kopyalanmaz.
- `cli` çözümü kayıt anahtarıyladır (küçük harf, mevcut `motor_al` davranışı). Bilinmeyen ad koşucudan önce başarısız olur.
- `ayarlar.model` karttaki `model`'dir. Bu dilim bütçe, araç listesi, json-şema veya tur tavanı politikası icat etmez; adaptörün `.get()` ile yok saydığı diğer anahtarlar boş/None kalabilir.
- İstem, yalnız o anki durum adından türetilen deterministik kısa bir metindir. Plan/delege içeriği ürün değildir; `cozumle` sonucunun `metin` / `yapisal` / `maliyet` / `oturum` alanları Sinyal'e gitmez.
- Sinyal eşlemesi: `cozumle["hata"]` doğru veya stdout bozuk ise `motor_hatasi`; aksi halde `motor_ciktisi`. Koşucu istisnası (OSError benzeri) de `motor_hatasi`'dir; Sürücü döngüsü ValueError ile düşmez.
- Motor durum yazmaz. `durum.json`'u yalnız Sürücü yazar. Kart yazılmaz. İskelet yazılmaz.
- `SahteMotor` aynı callable sözleşmesinde kalır; fabrika onu silmez veya içine almaz. İki uygulama yan yana: test e2e'si SahteMotor, bağ testleri fabrika + sahte koşucu.
- Kod personel-kapsamlı Sürücü yanına konur. Şirket `kos` koşucusu (`_motor_kos`) takım/koşu kaydı/SIRKET_* ortamına bağlıdır; CH-0001 onu çağırmaz.
- Üretimde subprocess kullanan bir varsayılan koşucu bulunabilir. Unittest onu kullanmaz. PATH'te gerçek ikili arayan test yazılmaz. Varsayılan koşucu yazılırsa, kanıtı ancak sahte `subprocess.run` ile olabilir; tercih edilen kanıt enjekte koşucudur.
- `bin/kapi.py`, `bin/dongu.py`, şirket evre makinesi, TERS_MOTOR bu dilimde değişmez.

## Testing Decisions

- İyi test dış davranışı ölçer: verilen kart + enjekte koşucu için dönen Sinyal, koşucuya giden komut, ve (bağlı yolda) Sürücü'nün yazdığı durum kaydı. Fabrika iç yardımcı sınıfını birincil seam sanmaz.
- Birincil seam: `fabrika(kart, kosucu) -> motor`; ardından mevcut `isi_ilerlet(motor, ...)`. Testler iç durum makinesini yeniden birimlemez; o önceki dilimde kilitli.
- Koşucu sahte olur: argv'yi kaydeder, hazır stdout döner. `subprocess.Popen` / gerçek CLI / ağ yok.
- Önceki sanat:
  - Motor adaptör testleri: `komut` bayrakları ve sahte stdout `cozumle`; CLI yok.
  - CH-0001 Sürücü testleri: geçici `durum.json`, enjekte `SahteMotor`, `isi_ilerlet` e2e.
  - Şirket sürücü testleri: `subprocess.run` yerine SahteMotor. Bu dilim o deseni şirket koşucusuna bağlamak zorunda değil; CH-0001 koşucusu enjekte edilir.
- Kapsanacak senaryolar:
  - Çözümleme: CH-0001 kartı → `claude` + `sonnet`; komutun ilk token'ı cli; model karttan komutta.
  - Dört kayıtlı `cli`; bilinmeyen `cli` koşucudan önce hata.
  - Eksik/bozuk `arka_yuz.motor`.
  - Adaptör sözleşmesi: sahte başarı stdout → `motor_ciktisi`; `hata`/bozuk stdout → `motor_hatasi`.
  - Bağlı mutlu yol: fabrika motoru + `isi_ilerlet` → `park`; koşucu yalnız iki Motor durumunda.
  - Bağlı hata yolu: hata stdout → `hata` → `park`.
  - Gerileme: mevcut SahteMotor e2e aynı kalır.
  - Kart dosyası çağrı sonrası byte-eşit (yazılmamış).
- Test yeri: mevcut `tests/` ve `python3 -m unittest discover -s tests`. Ağ yok, gerçek motor yok.

## Out of Scope

- Kapı, defter, ajan hafızası, anlamsal eşleyici, orkestrasyon kancası.
- Usta ataması ve park sonrası durumlar (`usta_atandi`, `izleniyor`, `tamam`).
- Unittest içinde gerçek CLI çalıştırma; PATH'te `claude`/`agy`/`codex`/`grok` arama.
- Plan/delege ürünü, istem mühendisliği, skill yönlendirme, İş metnini Motor'a verme.
- Motor çıktısını kalıcı iş artefaktı olarak yazma (`metin`/`yapisal` saklama).
- Şirket sürücüsü, döngü, kapı, evre, TERS_MOTOR, koşu kaydı, maliyet tavanı.
- Adaptör modüllerinin `komut`/`cozumle` iç mantığını yeniden yazma (mevcut testler yeter).
- Aksiyon iskeletini veya Personel kartı şemasını değiştirme.
- `.env` okuma.
- SahteMotor'u kaldırma veya mevcut e2e'yi fabrikaya taşıma zorunluluğu.

## Further Notes

Kaynak: önceki dilim `.scratch/otomatik-surucu-ch0001/spec.md` Out of Scope maddesi ("Gerçek CLI Motor üretim bağlaması") ve CONTEXT.md'deki Motor / Sürücü / Sinyal / Personel kartı arka yüzü tanımları.

Yol haritası: kök `ROADMAP.md` adım 5. Bu dilim bitince sıradaki prototip adım 3 (Ajan hafızası). Kapı / defter / usta / park-sonrası bilinçli ertelenmiştir.

İskeletteki `bilincli_disi` hâlâ `motor_cagrisi` içerir. O kayıt durum makinesi tanımıdır, uygulama envanteri değildir. Bu dilim iskeleti güncellemez.
