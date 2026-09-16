# HAFIZA-CEVAP · Ajan hafızası LOGIC prototipi

- Tarih: 2026-09-16
- Skill: mattpocock prototype / LOGIC (UI.md değil)
- Demo: `personel/CH-0001/proto/hafiza-demo.html` (çift tık; kurulum yok)
- Soru: Boş ama yazılabilir Ajan hafızası, sırayla eklenen düz metin kayıtları olarak hissediliyor mu? Defter ve anlamsal eşleyici olmadan bu şekil yeterli mi, yoksa kayıt alanları/şekli eksik mi?

## Önerilen varsayılan karar: EVET

Kâğıtta bu dilim için şekil yeterli: tek ajana ait depo, boş `kayitlar` listesi, sona eklenen `{ "metin": "<düz metin>" }`. Defter sıcak yüzdür, hafızanın kendisi değildir; anlamsal eşleyici adım 4'te bu metin listesine bakacak. Zaman, kayıt kimliği, etiket, İş numarası ve gömülü vektör bu dilimde yok diye şekil bozuk sayılmaz; spec onları bilinçli erteledi. Boş başlangıç ve yalnız-sona-ekleme, "boş ama yazılabilir" iddiasını karşılar.

Bu EVET, insanın tıklamasının yerine geçmez. Aşağıdaki bekleyen karar onaylanmadan üretim lift'i kapanmış sayılmaz.

## Bekleyen karar (insan tıklayınca teyit)

Demo tamdır; AFK ise sonra açılıp dört sekme ve serbest deneme tıklanabilir. İnsan şunları onaylasın veya tersine çevirsin:

1. İki düz metin notu (öğle, sonra akşam) Ajan hafızası gibi duruyor mu, yoksa koşu kaydı / günlük gibi mi?
2. Zaman, kayıt kimliği, etiket veya İş numarası olmadan kayıtlar bu dilimde ayrılabiliyor mu? Yoksa eksik alan deponun kendisinde mi durmalı?
3. Boş metnin (`""`) yine kayıt sayılması dürüst mü, yoksa delik gibi mi?
4. Defter üretilmeden depo "hafıza" gibi duruyor mu, yoksa ajanın okuyacağı sıcak yüz olmadan kör mü? (Kör ise cevap KISMI olur; Defter hâlâ ayrı adım, ama şekil "yeterli" olmaktan çıkar.)
5. Anlamsal arama tuşunun reddi rahatsız ediyor mu, yoksa adım 4'e bırakmak doğru mu?
6. "Yeni okuyucu" (bellekte paylaşılan belge) kalıcılık hissini veriyor mu? Asıl disk yazımı prototipin bağı olmamalı; ürün dosyası ayrı karar.

Tıklama sonrası 1 veya 4 hayır ise kararı KISMI yapın. 2'de bir alanın bu dilimde zorunlu olduğu söylenirse HAYIR (şekli büyüt). Aksi hâlde önerilen EVET durur.

## Taşınacak (karar EVET ise)

Saf `HafizaDeposu` yüzeyi, demoda `id="hafiza-deposu"` script bloğundadır. Taşınacak karar:

- Belge: `{ "kayitlar": [] }`
- Kayıt: `{ "metin": "<düz unicode metin>" }` (başka alan yok)
- `oku()` listeyi döner; boş başlangıç `[]`
- `ekle(metin)` sona bir kayıt ekler; ikinci yazma birinciyi ezmez
- Boş metin de kayıttır
- Depo CH-0001 Personel kaydı dizinine aittir; Defter ve anlamsal eşleyici API'si yoktur
- HTML kabuğu üretime girmez

## Ertelenen (bilinçli dışı)

- Defter (sıcak yüz, projeksiyon, context derleme)
- Anlamsal eşleyici (benzerlik, gömülü vektör, stokastik ada)
- Orkestrasyon hafızası
- Kayıt alanları: zaman, kimlik, etiket, `is_id`, gömülü vektör
- Silme, düzenleme, arama
- Sürücü / Motor / Kapı / usta / `kos` / `dongu` / `kapi` bağı
- Gerçek disk kalıcılığı bu demoda yok (LOGIC kural 3: bellek içi). Ürün dosyası ayrı.

## Erken üretim lift'i (silmeyin)

Aşağıdakiler prototip skill'i atlanarak gece yazılmış üretim-benzeri lift'tir. Bu oturum onları silmedi. Prototip kararı (insan tıklaması + yukarıdaki bekleyen maddeler) gelene kadar beklerler:

- `personel/CH-0001/hafiza.json`
- `personel/CH-0001/bin/hafiza_deposu.py`
- `tests/test_hafiza_deposu.py`
- `.scratch/ajan-hafiza-ch0001/issues/04-bos-metin-kayit-testi.md` (boş metin test borcu)

EVET kapanırsa bu dosyaların şekli demo ile örtüşür; lift sonradan meşrulaşır, yeniden yazılmaz. HAYIR veya KISMI olursa bu dosyalar üretim sayılmaz; şekil değişir, sonra yeniden lift.

## Bu oturumun sınırı

Commit, push, tag yok. `to-spec` / implement yok. Test eklenmedi, test koşulmadı. ROADMAP ve spec dokunulmadı. Karar henüz `kararlar.md`'ye işlenmedi.
