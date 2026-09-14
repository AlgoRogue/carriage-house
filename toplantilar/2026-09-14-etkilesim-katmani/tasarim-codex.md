# codex — etkileşim katmanı ön yüz tasarımı

## Tasarım ilkesi

Tek sayfa, mevcut dosya tabanlı evre makinesinin insan tarafından okunabilir yüzüdür.
Sayfa kendi durumunu üretmez; her yanıtta `increment/evre.json` ve aktif `increment/<id>/` artefaktlarını okur.
Gösterilen alanlar `bin/kapi.py durum` çıktısıyla aynı bilgi kümesidir: increment, evre, bekleyen onay,
motorlar, talep, kapsam sapması, dosyalar, son bekçi kararı, sıradaki adım ve son olay.
Bir anda yalnız bir birincil eylem vardır; red, açık evrelerde ayrı ve ikincil bir tehlike eylemidir.
Eksik, bozuk veya şemaya aykırı veri “tutarsız durum” olarak görünür ve bütün yazma eylemleri kapanır.

## Bilgi mimarisi ve blok sırası

1. `<header class="sayfa-basligi">`: “A Şirketi”, salt-okur/etkileşim modu ve son okuma zamanı.
2. `<main id="ana-icerik">` içinde `<section class="durum-ozeti">`: `increment_id`, evre rozeti ve bekleyen onay.
3. `<section class="siradaki-adim">`: insan dilinde tek yönlendirme, gerekiyorsa orijinal komut.
4. `<section class="increment-ozeti">`: talep, inşaat/bekçi motorları, son bekçi kararı ve son olay.
5. `<section class="kapi kapi-bir">`: yalnız sözleşme onayı bekleniyorsa tam Kapı 1 incelemesi.
6. `<section class="kapi kapi-iki">`: rapor varsa Kapı 2/FAIL incelemesi; PASS ve yayın ayrı durumlar.
7. `<section class="artefaktlar">`: aktif increment dosyalarının salt-okur bağlantıları.
8. `<details class="gecmis">`: eski olaylar; son olay yukarıda kalır, tam geçmiş ikincil yüzeydir.
9. `<footer class="kaynak-notu">`: doğruluk kaynağı yolları ve sayfanın otomatik eylem üretmediği notu.

## Evre görünümü ve tek birincil eylem

| Evre / koşul | Görünen ana mesaj | Tek birincil eylem |
|---|---|---|
| `bos` | Açık increment yok; alanlar `-`; son olay varsa gösterilir | “Yeni talep aç” |
| `sozlesme`, `bekleyen_onay=null` | Talep, henüz kilitlenmemiş motorlar, varsa artefaktlar | “`sistem-sevk`i koştur” |
| `sozlesme`, `bekleyen_onay=sozlesme` | Kapı 1, taslak sözleşme ve motor adayı | “Sözleşmeyi onayla” |
| `insaat` | Onaylı sözleşme, kilitli iki motor, inşaatın sırada olduğu | “`sistem-insaat`ı koştur” |
| `bekci` | Teslim ve onaylı sözleşme bağlantıları, denetimin sırada olduğu | “`sistem-bekci`yi koştur” |
| `yayin-bekliyor`, `bekleyen_onay=yayin` | PASS raporu, “Henüz yayınlanmadı” uyarısı ve Kapı 2 | “Yayınla” |
| `fail` | FAIL özeti, başarısız kriterler, ihlal ve kapsam sapması | “Gerekçeyle red” |
| `yayinlandi` | Kapalı increment, yayın olayı ve kayıt özeti | “Yeni talep aç” |
| `red` | Kapalı increment, red olayı/gerekçesi | “Yeni talep aç” |

`bekleyen_onay` evreden daha belirgin bir karar işaretidir: değer `sozlesme` ise Kapı 1,
değer `yayin` ise Kapı 2 başlığı ve teyit alanı sayfanın sıradaki-adım bölümüne bağlanır.
Geçersiz birleşimler (örneğin `evre=insaat`, `bekleyen_onay=yayin`) hata kartına dönüşür; eylem çizilmez.
Birincil eylemin yanında takım seçici yoktur; koşulacak takım evreden sunucuda türetilir.
İlk salt-okur dilimde düğme yerine komut ve “bu dilim eylem çalıştırmaz” etiketi gösterilir.

## Kapı 1 — sözleşme incelemesi

Kapı 1 başlığında `increment_id`, `evre=sozlesme`, “Sözleşme onayı bekliyor” ve `motor_adayi` birlikte görünür.
`increment.md` insan özeti önce, `sozlesme.json` alanları ardından okunur; ham dosya bağlantısı saklanmaz.
Sözleşme alanları şu sıradadır: `hedef_davranis`, `dokunulacak_yollar`, `yeni_dosyalar`,
`motor_adayi`, `kabul_kriterleri`, `durma_kosulu`, `kapsam_disi`, `yayin_anlami`.
Her kabul kriteri numaralı bir `<li class="kriter">` olur; açıklama üstte, `tip` rozeti ve `deger` kod satırı altta.
Boş yol/kapsam listeleri “Yok” diye açık yazılır; boş alan sayfanın bozulması gibi görünmez.
Motor seçimi yalnız izinli dört motoru sunar, sözleşmedeki aday ön seçilidir; bu takım seçici değildir.
Teyit alanı ayrı `<fieldset class="teyit-alani">` içinde hedef increment ve mevcut evreyi tekrar gösterir.
İnsan `increment_id` değerini yazar; onay düğmesi geri dönüşü “dondurulmuş kopya oluşturur” diye açıklar.
POST öncesi sunucu evreyi yeniden okur; eski sekme uyuşmazlığında hiçbir mutasyon yapmaz.

## Kapı 2 — bekçi raporu ve yayın kararı

Kapı 2, `sozlesme.onayli.json`, `teslim.json` ve `bekci-raporu.json` belgelerini tek inceleme akışında sunar.
Üst sonuç şeridinde bekçi motoru ve `karar` vardır; PASS yeşil, FAIL kırmızı sözcükle de yazılır.
Her `kriterler` girdisi kendi `<article class="kriter-sonucu">` bloğudur: açıklama, sonuç ve tam `kanit`.
Komut çıktısı veya dosya izi `<pre><code>` içinde kaydırılabilir gösterilir; yalnız renkle anlam verilmez.
`ihlal` listesinde her ihlalin kriteri ile kanıtı eşleşmiş görünür; boş liste “İhlal yok” der.
Raporun `kapsam_sapmasi` ile evrenin aynı alanı yan yana karşılaştırılır; fark varsa tutarsızlık uyarısı çıkar.
PASS şeridinin hemen altında ayrı yayın durumu bulunur: “Denetim geçti · henüz yayınlanmadı”.
Bu ayrımda bekçi kararı kanıt sonucu, Kapı 2 ise yalnız insanın vereceği yayın kararıdır.
“Yayınla” yalnız `evre=yayin-bekliyor`, `bekleyen_onay=yayin` ve `karar=PASS` birlikteyken etkinleşir.
Teyit alanı hedef `increment_id`, mevcut evre ve görülen PASS kararını tekrar eder; insan ID'yi yazar.
FAIL durumunda yayın kontrolü hiç sunulmaz; gerekçeli red tek birincil eylem olur.

## Sunucu-taraflı HTML yapısı

Belge iskeleti `<!doctype html>`, `<html lang="tr">`, anlamlı `<head>`, `<header>`, `<main>` ve `<footer>` kullanır.
Durum değerleri `<dl class="durum-listesi">`; koleksiyonlar `<ul>`/`<ol>`; bağımsız sonuçlar `<article>` olur.
Kapı ve sonraki-dilim açıklamaları `<section>` veya `<details>`; başlıkları hiyerarşik `h1`–`h3` sırasındadır.
Yazma uçları geldiğinde her eylem `method="post"` kullanan ayrı `<form class="eylem-formu">` olur.
Formlar gizli `increment_id` ve `evre` önkoşullarını taşır; görünür teyit girdisi bunların yerine geçmez.
Sunucu rota/alanları allowlist'ten üretir; dosya yolu ya da takım adı doğrudan kullanıcı girdisi olmaz.
Dinamik metin, öznitelik ve dosya adları bağlama uygun `html.escape(..., quote=True)` ile kaçışlanır.
Liste üreticileri küçük saf Python fonksiyonları döndürür; f-string yalnız kaçışlanmış parçalara uygulanır.
Sınıf adları Türkçe kebab-case'tir: `durum-ozeti`, `evre-rozeti`, `siradaki-adim`, `kapi-karti`,
`kriter-sonucu`, `kanit-kutusu`, `teyit-alani`, `ikincil-eylem`, `uyari-karti`, `artefakt-listesi`.
Erişilebilir isimler görünür etiketlerden gelir; renk tek durum göstergesi olmaz, odak çizgileri korunur.

## CSS ve yenileme davranışı

Tüm görünüm `<head>` içindeki tek `<style>` bloğundadır; harici font, ikon, CDN ve derleme adımı yoktur.
Yazı tipi `system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif`; kod yazısı sistem monospace'tir.
Renkler `:root` değişkenlerindedir; `@media (prefers-color-scheme: dark)` yalnız değişkenleri değiştirir.
Geniş ekranda özet alanları iki sütun olabilir; içerik en çok yaklaşık `72rem` genişler.
`@media (max-width: 42rem)` bütün gridleri tek sütuna indirir, dokunma hedeflerini tam genişlik yapar.
Uzun yol ve kanıtlar `overflow-wrap:anywhere`; `<pre>` yatay kaydırılır, sayfayı taşırmaz.
İlk dilimde JavaScript yoktur. Koşu yoklaması gerektiğinde yazmayan bir yenileme yeterliyse
`<meta http-equiv="refresh" content="10">` kullanılır; aksi kanıtlanmadıkça istemci polling kodu eklenmez.
`prefers-reduced-motion` gözetilir; tasarımın anlaşılması animasyona bağlı değildir.

## Increment dilimleri

1. Salt-okur: durum özeti, sıradaki adım, motorlar, talep, kapsam sapması, artefaktlar ve son olay.
2. Talep + red: tek cümle talep formu; açık increment'te ikincil, gerekçeli ve teyitli red POST'u.
3. Kapı 1: tam sözleşme alanları, motor seçimi, `increment_id`/evre teyidi ve `kapi.py onayla` POST'u.
4. Koş + Kapı 2: evreden türeyen tek `POST /kos`, koşu sonrası duran polling, kanıt görünümü ve yayın teyidi.
Her dilim önceki blokları korur; görünüm modeli aynı SoT okumasından genişler, ayrı bir istemci durumu doğmaz.

## Yapılmayacaklar

Takım seçici, motor sohbeti, prompt kutusu veya genel amaçlı terminal yapılmaz.
Canlı log birincil yüzey olmaz; gerekirse koşu kaydına ikincil salt-okur bağlantı verilir.
Uygulamanın kendi evresi, kuyruğu, veritabanı, artefakt kopyası veya “tamamlandı” bayrağı olmaz.
GET isteği talep açmaz, kapı geçmez, takım koşturmaz, red/yayın yapmaz; bütün mutasyonlar POST'tur.
Koşular otomatik zincirlenmez; bir insan basışı bir takımı başlatır ve bitince sistem durur.
Tarayıcıdan JSON, kod, SoT, sözleşme veya şema düzenlenmez; commit/push/tag ve `--zorla` sunulmaz.
