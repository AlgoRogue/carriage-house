# Otomatik Sürücü — CH-0001 (Cengizhan)

Status: ready-for-agent

## Problem Statement

Parça 2b LOGIC prototipi (`personel/CH-0001/proto/index.html` + `personel/CH-0001/proto/CEVAP.md`)
Cengizhan'ın kilitli durum makinesinin ilk dilimini — `bos → is_alindi → planlaniyor → plan_hazir →
delege_hazirlaniyor → paket_hazir → park` — sapmadan yürüttüğünü, durumu yalnız Sürücü'nün yazdığını
ve Motor'un yalnız `planlaniyor`/`delege_hazirlaniyor` durumlarında kavramsal (hedef seçmeyen, yalnız
sinyal veren) kaldığını doğruladı. Claude bu prototipi ONAY etti (üç kozmetik düzeltmeyle).

Ama bu doğrulama; insan tıklamasıyla ilerleyen, taklit sinyali elle tetiklenen, durumu yalnız
sayfa belleğinde tutan, kalıcı hiçbir kayda dokunmayan bir HTML demosunda yaşıyor. Gerçek kayıtlar —
`personel/CH-0001/aksiyon-iskeleti.json` (durum makinesi tanımı) ve `personel/CH-0001/durum.json`
(anlık durum) — hâlâ elle yazılmış statik dosyalar. Onları okuyup yazan, insan müdahalesi olmadan
işi `bos`'tan `park`'a kadar götüren gerçek bir Sürücü kodu yok.

## Solution

Prototipteki `SurucuMakine` saf mantığını (geçerli geçişleri iskeletten okuma, Motor durumlarında
sinyal zorunluluğu, sonraki durumu yalnız kendisinin yazması) gerçek bir Sürücü modülüne taşı. Bu
modül:

- `personel/CH-0001/aksiyon-iskeleti.json`'u salt-okunur gerçeğin kaynağı olarak okur, değiştirmez.
- `personel/CH-0001/durum.json`'u okur ve yazar — Cengizhan'ın anlık durumunun tek kalıcı kaydı budur.
- İnsanın tek bir çağrısıyla (bir "işi ilerlet" girişiyle) durumu, insan tıklaması beklemeden,
  `bos`'tan `park`'a kadar otomatik ilerletir.
- Motor'u yalnız `planlaniyor` ve `delege_hazirlaniyor` durumlarında çağırır; Motor hedef seçmez,
  yalnız "çıktı geldi" / "hata" sinyali üretir — sonraki durumu iskeletten okuyup yazan yine Sürücü'dür.
- Bu dilimde gerçek CLI Motor yerine sahte bir motor (mevcut `tests/test_kit.py` içindeki
  `SahteMotor` desenine benzer bir sahte) kullanılır; gerçek motor bağlaması kapsam dışıdır.

Kısacası: prototipte doğrulanmış kararı, atılabilir HTML'den kalıcı, otomatik, gerçek dosyalara
dokunan bir Sürücü koduna kaldırmak — üretimin kendisini değil, bu ilk dilimin karar mantığını.

## User Stories

1. İnsan olarak, Cengizhan'ın işini tek bir çağrıyla başlatmak isterim; ardından hiçbir tıklama
   yapmadan durumun `park`'a kadar kendiliğinden ilerlediğini görmek isterim.
2. İnsan olarak, Sürücü çalıştıktan sonra `personel/CH-0001/durum.json`'u açtığımda son durumun
   `park` olduğunu ve iş kimliğinin doğru yazıldığını görmek isterim.
3. Geliştirici olarak, Sürücü'nün `personel/CH-0001/aksiyon-iskeleti.json`'daki geçiş listesini
   kaynak olarak kullandığını, bu dosyayı hiçbir koşulda değiştirmediğini bilmek isterim.
4. Geliştirici olarak, `bos → is_alindi` geçişinin "insan işi verdi" sinyaliyle tetiklendiğini,
   Motor çağrısı gerektirmediğini doğrulayabilmek isterim.
5. Geliştirici olarak, `is_alindi → planlaniyor` geçişinde Sürücü'nün Motor'u çağırdığını, ama
   hedefi Motor'un değil iskeletin belirlediğini test edebilmek isterim.
6. Geliştirici olarak, `planlaniyor` durumunda Motor "çıktı geldi" sinyali verdiğinde Sürücü'nün
   otomatik olarak `plan_hazir`'e geçtiğini görmek isterim.
7. Geliştirici olarak, `plan_hazir → delege_hazirlaniyor` geçişinin de insan müdahalesi olmadan,
   Sürücü tarafından tetiklendiğini doğrulayabilmek isterim.
8. Geliştirici olarak, `delege_hazirlaniyor` durumunda Motor'un yalnız sinyal ürettiğini, sonraki
   durumu (`paket_hazir`) yine Sürücü'nün iskeletten okuyup yazdığını test edebilmek isterim.
9. Geliştirici olarak, `paket_hazir → park` geçişinin ("atanacak usta yok") otomatik gerçekleştiğini
   ve bu ilk dilimde işin `park`'ta durduğunu doğrulayabilmek isterim.
10. Geliştirici olarak, Sürücü'nün iskelette tanımlı olmayan ya da mevcut durumdan geçerli olmayan
    bir hedefe geçişi reddettiğini; bu reddin durumu değiştirmediğini test edebilmek isterim.
11. Geliştirici olarak, Motor'un yalnız çağrıldığı iki durumda (`planlaniyor`, `delege_hazirlaniyor`)
    sinyal verebildiğini; başka bir durumda gelen Motor sinyalinin reddedildiğini doğrulayabilmek
    isterim.
12. Geliştirici olarak, `planlaniyor` ya da `delege_hazirlaniyor` durumunda Motor "hata" sinyali
    verdiğinde Sürücü'nün otomatik olarak `hata` durumuna geçtiğini görmek isterim.
13. Geliştirici olarak, `hata` durumundan Sürücü'nün otomatik olarak `park`'a düştüğünü ("yeniden
    denemeyi bekletir") ve bu ilk dilimde burada durduğunu doğrulayabilmek isterim.
14. Geliştirici olarak, uçtan uca mutlu yolda (`bos → … → park`) Sürücü'nün insan tıklaması olmadan
    tüm ara durumlardan tek bir çağrıyla geçtiğini bir test ile kanıtlayabilmek isterim.
15. Geliştirici olarak, uçtan uca hata yolunda (`… → planlaniyor → hata → park`) da aynı tek
    çağrının insan müdahalesi olmadan işi `park`'a düşürdüğünü bir test ile kanıtlayabilmek isterim.
16. Geliştirici olarak, Sürücü'yü test ederken gerçek bir CLI motor çalıştırmadan, mevcut
    `SahteMotor` desenine benzer bir sahte motoru geçirerek (subprocess yerine geçen) davranışı
    doğrulayabilmek isterim.
17. Geliştirici olarak, Sürücü'nün tek giriş fonksiyonunu çağırdığımda dönen sonucun; başlangıç
    durumu, bitiş durumu ve izlenen geçiş listesini (ya da en azından bitiş durumunu ve
    `durum.json`'a yazılan hâli) içerdiğini, böylece testin dış davranışı `durum.json` üzerinden
    doğrulayabildiğini isterim.
18. Geliştirici olarak, Sürücü'nün `personel/CH-0001/durum.json`'daki `is_id` ve `son_sinyal`
    alanlarını da güncel tuttuğunu, yalnız `durum` alanının değişmediğini doğrulayabilmek isterim.
19. Geliştirici olarak, Sürücü modülünün Kapı, defter, hafıza ya da usta atamasıyla hiçbir şekilde
    etkileşmediğini; bu kavramlara referans bile vermediğini kod incelemesiyle teyit edebilmek
    isterim.
20. Geliştirici olarak, `bin/dongu.py` ya da `bin/kos.py`'nin bu yeni Sürücü modülünü çağırmaya
    zorlanmadığını; CH-0001'in kendi bağımsız Sürücü'sünün mevcut çok-ajanlı orkestrasyondan ayrı
    durduğunu bilmek isterim.

## Implementation Decisions

Prototipten (`personel/CH-0001/proto/index.html`, `surucu-makine` script bloğu) ve
`personel/CH-0001/aksiyon-iskeleti.json`'dan taşınacak, doğrulanmış karar özeti (kaynak dosyaların
kendisi salt-okunur kalır, aşağıdaki yalnız mantığın özetidir):

- **Dilim kümesi**: `{bos, is_alindi, planlaniyor, plan_hazir, delege_hazirlaniyor, paket_hazir,
  park, hata}`. `usta_atandi`, `izleniyor`, `tamam` iskelette tanımlı ama bu dilimde etkin değil —
  Sürücü bu durumlara hiç geçmez.
- **Motor hedefleri iskeletten türetilir**: her `motor_cagrilan_durumlar` girişi
  (`planlaniyor`, `delege_hazirlaniyor`) için başarı hedefi, o durumdan çıkan ve `hata` olmayan
  geçişten okunur (`plan_hazir`, `paket_hazir`). Sürücü bu eşlemeyi kod içinde sabitlemez, iskeletten
  hesaplar.
- **Geçiş kuralı**: bir hedef, yalnız (a) o hedef iskelette geçerli bir `from`/`to` çifti olarak
  tanımlıysa VE (b) hedef dilim kümesindeyse VE (c) mevcut durum bir Motor durumuysa bunun için
  geçerli bir sinyal gelmişse uygulanır. Aksi hâlde geçiş reddedilir, durum değişmez.
  (`kural.sonraki_durumu_yalniz_surucu_yazar: true` — ajan/Motor kendi durumunu yazamaz.)
  Aynı reddetme mantığı, iskelette tanımlı olsa bile dilim kümesi dışındaki hedefler için de geçerlidir.
- **Sinyal sözlüğü**: yalnız iki girdi kavramsal olarak var — "Motor çıktısı geldi" (başarı hedefine
  geçer) ve "Motor hatası geldi" (`hata`'ya geçer). Motor durumu dışında gelen sinyal reddedilir.
- **Otomatik ilerleme**: prototip insan tıklamasıyla adım adım ilerliyordu; gerçek Sürücü bu adımları
  tek bir çağrı içinde, ara durumlarda insan girdisi beklemeden zincirler — `bos → park` (mutlu yol)
  ya da `bos → … → hata → park` (hata yolu) tek çağrıda tamamlanır.
- **Kalıcılık**: durum geçişleri bellekte değil, `personel/CH-0001/durum.json`'a yazılır; her geçişte
  bu dosya güncellenir (en azından son durumda; ara adımların da yazılıp yazılmayacağı uygulama
  ayrıntısıdır, dış davranış son hâl + varsa iz üzerinden doğrulanır).
- **Motor çağrısı bu dilimde sahte**: gerçek CLI/LLM motoru bağlanmaz; seam'de sahte motor (bkz.
  Testing Decisions) kullanılır. Prod motor bağlaması ayrı bir iştir.

## Testing Decisions

- **Birincil seam**: Sürücü'nün tek giriş fonksiyonu (mevcut `bin/kos.py` / `bin/dongu.py`
  testlerindeki desenle aynı — `tests/test_kit.py`'deki `SahteMotor`'un subprocess.run yerine
  geçmesi gibi, burada da gerçek Motor çağrısının yerine geçen bir sahte motor enjekte edilir).
  Testler bu fonksiyonu çağırır, iç durum makinesi sınıfını doğrudan import edip test etmez.
- **Dış davranış doğrulaması**: testler `personel/CH-0001/durum.json`'u (ve varsa ilgili kayıtlı
  sinyalleri) okuyarak doğrular — iç değişkenlere değil, dosyaya yazılan sonuca bakılır.
- **Kapsanacak senaryolar**:
  - Mutlu yol: tek çağrı, `bos` başlangıç → `park` bitiş, insan tıklaması/ara müdahale yok.
  - Motor yalnız doğru durumlarda çağrılır: `planlaniyor` ve `delege_hazirlaniyor` dışında sahte
    motorun hiç çağrılmadığı doğrulanır (motor bir seçici değil, yalnız sinyal kaynağıdır).
  - Yasadışı geçiş reddi: iskelette olmayan ya da dilim dışı bir hedefe zorlama denemesi durumu
    değiştirmez.
  - Motor hatası: `planlaniyor` ya da `delege_hazirlaniyor` sırasında sahte motor hata sinyali
    verdiğinde durum `hata`'ya, ardından otomatik olarak `park`'a düşer.
  - Sinyal/durum uyumsuzluğu reddi: Motor durumunda olmayan bir anda gelen sahte "çıktı/hata"
    sinyali reddedilir.
- **Test yeri**: mevcut `tests/` dizini ve `python3 -m unittest discover -s tests` akışına uyar;
  ağ çağrısı yok, gerçek motor çağrısı yok (repodaki genel kural).

## Out of Scope

- Kapı, defter, hafıza — bu ajan/dilim için hiçbiri kurulmaz.
- Gerçek usta ataması ve `park` sonrası durumlar (`usta_atandi`, `izleniyor`, `tamam`) — zorunlu
  teslimin parçası değil.
- Gerçek CLI Motor üretim bağlaması — bu dilimde yalnız sahte motor seam'de kullanılır.
- `bin/dongu.py`'nin tam çok-işli orkestrasyon yeniden yazımı — bu iş yalnız CH-0001'in kendi
  Sürücü'sünü kapsar, mevcut orkestrasyonu değiştirmez.
- `personel/CH-0001/aksiyon-iskeleti.json`'u değiştirmek — salt-okunur gerçeğin kaynağı olarak kalır.

## Further Notes

Bu spesifikasyonun birincil kaynağı `personel/CH-0001/proto/CEVAP.md` (Parça 2b LOGIC prototip
sonucu, Claude ONAY) ve `personel/CH-0001/proto/index.html` içindeki taşınabilir `surucu-makine`
saf modülüdür — mantığın doğrulanmış hâli oradadır, bu belge onu üretim moduna taşımanın kapsamını
tarif eder. Ek arka plan için `personel/CH-0001/README-aksiyon.md`, `personel/CH-0001/kurallar.md`
ve `personel/CH-0001/dosya.md` (Cengizhan'ın rol/kısıt tanımı) ve kök `CONTEXT.md`'deki Sürücü/Motor/
Sinyal/İş terim tanımları okunmalıdır.
