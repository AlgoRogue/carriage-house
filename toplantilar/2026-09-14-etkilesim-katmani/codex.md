# codex — etkileşim katmanı görüşü
> tur: 2

## 1. Ne

Uygulama bir “yönetim paneli” değil, mevcut dosya tabanlı makinenin insan yüzü olmalı.
Ana ekran tek bakışta aktif `increment_id`, `evre`, `bekleyen_onay`, kilitli motorlar, son olay,
mevcut artefaktlar ve insan dilinde “sıradaki tek adım”ı göstermeli.

Kapı 1 ekranı `increment.md` ile `sozlesme.json`u yan yana okunabilir sunmalı; hedef davranış,
dokunulacak/yeni yollar, her kabul kriteri, kapsam dışı, durma koşulu ve yayın anlamı saklanmamalı.
İnsan motor adayını görebilmeli, gerekirse izinli motorlardan birini seçebilmeli ve açık bir onayla
`sozlesme.onayli.json`un dondurulmasını istemeli.

Kapı 2 ekranı onaylı sözleşmeyi, `teslim.json`ı, `bekci-raporu.json`u, her kriterin PASS/FAIL sonucunu,
kanıtını ve kapsam sapmasını birlikte göstermeli. “Yayınla” yalnız rapor PASS ve evre
`yayin-bekliyor` iken etkin olmalı; PASS ile yayın aynı şeymiş gibi çizilmemeli.

Uygulama tek cümlelik talep açtırmalı ve açık increment'i gerekçeli `red` ile kapattırmalı.
Red, yanlışlıkla basılmaya karşı hedef increment'i ve mevcut evreyi tekrar gösteren ikinci bir
onay istemeli; yayın ve Kapı 1 de aynı kalıpta açık, geri dönüşü anlatan onaylar olmalı.

Ham artefaktları indirme/görüntüleme olmalı, fakat tarayıcıda JSON, kod, sözleşme ya da `evre.json`
düzenleme olmamalı. Genel amaçlı terminal, serbest komut, dosya yöneticisi, prompt kutusu, motor sohbeti,
git commit/push/tag, `--zorla`, şema/SoT düzenleme ve birden çok increment açma arayüzü olmamalı.
Maliyet ve koşu kaydı bilgi olarak gösterilebilir; bunlar evre veya kapı kararının yerine geçmemeli.

## 2. Hangi teknoloji

İlk tercih Python stdlib ile yazılmış küçük, sunucu-taraflı HTML üreten bir HTTP uygulaması ve az miktarda
vanilla CSS/JS'dir. Aynı Python sürümü, `pathlib`, `json`, `subprocess`, `html`, `http.server` gibi mevcut
araçlarla kurulabilir; npm derlemesi, SPA durum makinesi, veritabanı ve paket tedarik zinciri eklemez.
Stdlib HTTP sunucusu doğrudan internete açılmamalı; yalnız `127.0.0.1`e bağlanmalı.

Uygulama repo ve motorların bulunduğu sürekli açık makinede çalışmalı. Telefon erişimi, TLS ve kullanıcı
kimliği sağlayan özel ağ/kimlik doğrulayan ters proxy üzerinden gelmeli. Bu operasyonel bağımlılık bilinçli
bir karardır: TLS, cihaz/kullanıcı kimliği, oturum iptali ve oran sınırlamayı elde yazmak stdlib sadeliğinin
kazancını tersine çevirir. İnternete açık port ve uygulamanın kendi yazdığı parola sistemi önerilmez.

Kapı yetkisi yalnız allowlist'teki insan hesabına verilmeli; salt-okur erişim ayrı olabilir. Proxy yalnız
loopback arka uca doğrulanmış kimlik aktarmalı, uygulama sahte istemci başlığına güvenmemeli. Değiştiren tüm
POST'larda kısa ömürlü oturum, CSRF koruması, yeniden doğrulama ve ekranda görünen kimlik olmalı.
Kimlik sırrı repoya, `.env` üzerinden ajan ortamına veya koşu istemine girmemeli. “İnsan” olmanın teknik
karşılığı, ajanların sahip olmadığı bu oturumla imzalanmış ve CSRF-doğrulanmış bir insan isteğidir.
`increment_id`yi forma yeniden yazmak yararlı bir niyet teyididir, fakat kimlik doğrulama değildir; aynı
değeri dosyadan okuyabilen bir ajan veya ele geçirilmiş istemci de yazabilir. Benzer biçimde ortak bir
`.env` jetonu, süreçleri ve repoyu görebilen ajanlardan gerçekten ayrı tutulamıyorsa insan kapısını kanıtlamaz.

## 3. Nasıl etkileşim

Her evrede tek bir birincil eylem görünmeli: sevki çalıştır, sözleşmeyi onayla, inşaatı çalıştır, bekçiyi
çalıştır veya PASS'ı yayınla. Kapılar sıradan ikon değil, okunması gereken belge/kanıt ve sonuç etkisini
gösteren karar sayfaları olmalı. Eylemden hemen önce sunucu evreyi yeniden okumalı; eski sekmeden gelen
istek hedef `increment_id` ve evreyle uyuşmuyorsa hiçbir şey yapmadan çatışma göstermeli.

`kos.py <takim>` uygulamadan, yalnız sıradaki takım için açıkça etiketli tek seferlik bir insan düğmesiyle
tetiklenebilir. POST, kabuk kullanmadan sabit allowlist'ten tam bir komut başlatmalı; keyfî takım veya argüman
almamalı. Tarayıcı bağlantısı kesilse de koşu sunucuda tamamlanmalı; ekran dosyalardan yeniden okuyarak
sonucu göstermeli. Koşu sürerken ikinci tetik mevcut `.kos.lock` nedeniyle çoğaltılmamalı.

Bu, ANAYASA §4 ile uyumludur: her düğme yalnız bir takımı bir kez başlatır ve sonra sistem durur.
Sevkin bitişi inşaatı, inşaatın bitişi bekçiyi, PASS da yayını otomatik başlatmamalı. Otomatik yenileme
yalnız görüntüyü yeniler; eylem üretmez. Bildirim daha sonra “karar bekliyor” diyebilir, kapıya basamaz.

## 4. Determinizmle uyum

Alan durumu için uygulamanın veritabanı, kuyruğu, “tamamlandı” bayrağı veya ayrı evre makinesi olmamalı.
Her GET'te `increment/evre.json` ve yalnız onun işaret ettiği `increment/<id>/` artefaktları yeniden okunmalı;
buton görünürlüğü dahi bu anlık görüntüden türetilmeli. Eksik, bozuk veya şemaya aykırı veri iyimserce
yorumlanmamalı: ekran “tutarsız durum” göstermeli ve tüm yazma eylemlerini kapatmalı.

Talep, onay, yayın ve red için uygulama aynı işi yeniden yazmamalı; `bin/kapi.py`yi argüman listesiyle,
shell olmadan çağırmalı. Çıkış kodu ve mesaj kullanıcıya gösterilmeli, ardından sonuç yine SoT'tan okunmalı.
Böylece CLI ile web aynı kapı kurallarını kullanır; gelecekte kural değişince iki implementasyon ayrışmaz.

Uygulamada yalnız güvenlik oturumu, CSRF nonce'u ve çalışan HTTP isteği gibi geçici operasyonel durum
olabilir; bunlar iş akışının doğruluk kaynağı değildir. Erişim logu da gözlem kaydıdır, evre kanıtı değildir.
Yazma istekleri sunucuda seri yürütülmeli ve mümkün olan ilk increment'te `kapi.py` için beklenen
`increment_id`/evre kontrolü ile ortak kilit eklenmeli; yalnız UI ön kontrolüne güvenmek TOCTOU yarışı doğurur.

## 5. Sistemin kendisinin inşa edebilmesi

Sunucu-taraflı stdlib çözümü bu döngüye en az sürtünmeyle uyar: küçük Python dosyaları, şablon yerine test
edilebilir saf HTML üreticileri ve mevcut `unittest` yeterlidir. Geçici dizinde örnek `evre.json`/artefakt
fikstürleri kurulabilir; HTTP GET/POST, escaping, evreye göre eylemler ve sahte `kapi.py` çağrıları ağsız ve
motor çağrısız ölçülebilir. Kabul kriterleri `komut` ve `dosya` tipinde kalır.

Arayüz mantığı “dosyaları oku → görünüm modeli üret → HTML üret” diye ayrılırsa bekçi hem saf fonksiyonları
hem yerel ephemeral portta uçtan uca HTTP davranışını ölçebilir. Tarayıcı otomasyonu, Node veya gerçek kimlik
sağlayıcısı ilk increment'in kabul kriteri yapılmamalı; proxy sözleşmesi ayrı deployment testleriyle ölçülmeli.
Framework ancak rota, form ve güvenlik kodu büyüyüp stdlib çözümünden daha az toplam risk sunduğu ölçüldüğünde,
ayrı ve gerekçeli bir increment olarak eklenmeli.

## 6. İlk increment

Mevcut SoT'ta yönetim uygulaması evre kilidi altında kapsam dışıdır; önce kuruluş döngüsü uçtan uca
PASS+yayın görmeli, ardından insan ilgili maddeyi `kapsam-disi.md`den çıkarmalıdır. Sevke daha önce verilen
uygulama talebinin doğru sonucu sözleşme değil, `kapsam-disi` engelidir.

İlk talep: “Yerel salt-okur web ana sayfası, `increment/evre.json` ve aktif increment artefaktlarından evreyi,
bekleyen onayı, sıradaki tek insan/koşu adımını ve dosya bağlantılarını gösterir; hiçbir yazma eylemi sunmaz.”

Sonraki sıra önerim:

1. Özel ağ/ters proxy kimliğini doğrulayan dağıtım sınırı ile talep ve gerekçeli red POST'larını ekle.
2. Tam sözleşme incelemesi, motor seçimi ve yeniden doğrulamalı Kapı 1'i `bin/kapi.py onayla` üzerinden ekle.
3. Sıradaki tek takımı insan tetiğiyle çalıştırmayı, kanıt odaklı Kapı 2'yi ve `yayinla` eylemini ekle.

Her biri tek başına gözlenebilir davranış olmalı; “uygulamayı yap” diye tek, geniş sözleşmeye bağlanmamalı.

## 7. Riskler

En büyük risk, web yüzünün ikinci bir orkestratöre dönüşmesidir: kendi backlog'u, evresi, görev statüsü,
artefakt kopyası veya otomatik zinciri oluşursa insan iki sistem arasındaki farkı taşımaya başlar.
Ekrandaki cache “gerçek”, dosyalar “arka plan ayrıntısı” yapılmamalı; artefaktlar uygulama veritabanına
kopyalanmamalı. CLI ve web için ayrı kapı kuralları yazılmamalı.

İkinci risk, kolaylığın yetkiyi görünmez kılmasıdır. Tek tıkla yayın, kalıcı oturum, ortak parola, CSRF'siz POST,
internete açık stdlib sunucusu, URL üzerinden eylem, loglara sözleşme/anahtar sızması ve ajanların erişebildiği
kimlik bilgisi kapıları fiilen ajana bırakır. GET hiçbir zaman değişiklik yapmamalı.

Üçüncü risk, uygulamanın insana yine “hangi takımı şimdi koşturmalıyım?” dedirtmesidir. Arayüz sıradaki tek
geçerli eylemi dosyalardan türetmeli; ama onu kendisi başlatmamalı. Hata durumunda ham kanıt, red seçeneği ve
net toparlanma yolu göstermeli; insandan CLI çıktısı kopyalamasını, JSON düzeltmesini, süreç gözetmesini veya
bir motordan diğerine metin taşımasını istememeli.

Son olarak mobil görünüm yeni bir ürün yönetimi kapsamına şişirilmemeli. Sohbet, bildirim altyapısı, zengin
editör, çoklu kullanıcı rolleri, genel görev kuyruğu ve görsel diff ancak gerçek kullanım kanıtıyla ayrı
increment olabilir; ilk iş kapıların rengini güzelleştirmek değil, aynı deterministik kapıyı güvenle uzatmaktır.

## 2. turda değişen

Agy ve Grok'un dosyaları, stdlib Python, dosyaların SoT olması, `kapi.py`/`kos.py`nin alt süreç olarak
kullanılması, koşuların zincirlenmemesi ve ilk increment'in salt-okur olması konularındaki ortak zemini
güçlendirdi; bu ana önerileri değiştirmedim. Grok'un kapıda `increment_id` yazdırma fikrini niyet teyidi
olarak yararlı buldum ve bunun kimlik doğrulamanın yerine geçemeyeceğini 2. bölüme açıkça ekledim.

Agy'nin `.env` içindeki ortak jeton önerisine ve Grok'un “OAuth değil, onayın maliyeti” tezine katılmıyorum:
dosyayı okuyabilen ajan aynı jetonu kullanabilir, görünen kimliği tekrar yazmak da isteğin bir insandan
geldiğini ispatlamaz. Bu nedenle yetki sırrının ajan çalışma ortamının dışında tutulduğu özel ağ/kimlik
proxy'si, kısa ömürlü insan oturumu ve işlem anında yeniden doğrulama önerimi korudum. Agy'nin SPA/PWA ve SSE
önerisini de ilk dilimde gerekli görmedim; sunucu-taraflı HTML ve gerekirse polling daha küçük, ölçülebilir
bir yüzey bırakır. Grok'un koşu HTTP isteğini açık tutmama vurgusu zaten 3. bölümdeki sunucuda bağımsız
tamamlama yaklaşımıyla uyumluydu; ayrıca değişiklik gerektirmedi.
