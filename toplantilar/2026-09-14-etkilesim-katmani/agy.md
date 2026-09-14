# agy — etkileşim katmanı görüşü
> tur: 2

## 1. Ne
Uygulama, insanı terminale bağımlı kılmadan sistemin evrelerini izleyen ve iki kilit insan kapısını yöneten yalın bir karar ve kontrol yüzeyi olmalıdır. Görevi karmaşık bir dashboard değil, döngüyü işletmektir.
- **Neyi göstermeli:**
  - **Evre ve durum:** `increment/evre.json` dosyasındaki `increment_id`, mevcut `evre` (`bos`, `sozlesme`, `insaat`, `bekci`, `yayin-bekliyor`, `fail`, `red`), bekleyen onay (`sozlesme`, `yayin`) ve kilitlenen motorlar (`insaat`, `bekci`).
  - **Sıradaki açık adım:** `bin/kapi.py durum` çıktısına paralel olarak sıradaki operasyonel eylemi net göstermeli (ör. "Sırada: `python3 bin/kos.py sistem-sevk`").
  - **Karar belgeleri ve kanıtlar:**
    - Kapı 1 öncesinde `increment/<id>/sozlesme.json` ve `increment.md` insan özeti,
    - Kapı 2 öncesinde `increment/<id>/bekci-raporu.json` (kriterler, komut/dosya kanıtları, PASS/FAIL kararı, varsa `kapsam_sapmasi` ve `park.md`), `teslim.json`.
  - **İnsan eylemleri:**
    - Yeni talep açma (`bin/kapi.py talep "..."`),
    - Kapı 1 onayı (`bin/kapi.py onayla [--motor ...]`),
    - Kapı 2 yayını (`bin/kapi.py yayinla`),
    - Gerekçeli red (`bin/kapi.py red "..."`),
    - Yalnızca evrenin izin verdiği sıradaki takımı koşturma tetiği (`bin/kos.py <takim>`).
- **Neyi göstermemeli / yaptırmamalı:**
  - Ajanların koşu sırasındaki ara token akışlarını veya ham LLM düşünce zincirlerini canlı yayınlamamalı; insanı log bakıcısına veya mikro-yöneticiye dönüştürmemelidir.
  - İnsanın korumalı dosyalarını (`ANAYASA.md`, `sema/*`, `kararlar.md`, `kapsam-disi.md`) doğrudan düzenletmemeli; dosya tabanlı SoT disiplini korunmalıdır.
  - Ajanlar adına karar vermemeli, sözleşme maddesi uydurmamalı, bekçi raporunu manipüle etmemelidir.
  - Otomatik ardışık zincirleme (insansız arka plan döngüsü) veya kontrolsüz serbest terminal çalıştırmamalıdır.

## 2. Hangi teknoloji
- **Seçim:** Python 3 standart kütüphanesi (`http.server`, `urllib`, `json`) ile sunucu-taraflı üretilen minimal HTML (SSR) ve az miktarda saf CSS/JS.
- **Gerekçe:** Repodaki adaptörler ve motorlar stdlib Python ile çalışmaktadır. Harici bir web framework'ü (FastAPI, Flask) veya Node/npm/React ekosistemi bağımlılık riski yaratır ve `sistem-insaat`ın hata yapma yüzeyini genişletir. Stdlib determinizmi, taşınabilirliği ve test edilebilirliği en üst düzeyde korur. İlk turdaki SPA/PWA ve SSE önerisi yerine, inşaat ve bekçi sürtünmesini en aza indiren sunucu-taraflı HTML ve sade yoklama (polling) esas alınmalıdır.
- **Erişim ve Dağıtım (Uzak / Mobil):** Sunucu süreç seviyesinde yalnız `127.0.0.1`e bağlanmalıdır; internete doğrudan açık port açılmamalıdır. Bilgisayar başında olmadan erişim için Tailscale (VPN/Mesh) veya yerel kimlik doğrulayan bir ters proxy kullanılır. Telegram tetiği veya bulut botları `kapsam-disi.md`'dedir ve dış servis bağımlılığı yaratır.
- **Kimlik ve yetki:** Kimlik sırrı asla `.env` üzerinden ajanların erişebileceği çalışma ortamına konulmamalıdır. Kimlik doğrulaması, ajan ortamından yalıtılmış ters proxy/özel ağ oturumu ve CSRF korumalı kısa ömürlü oturum belirteçleri ile sağlanmalıdır. Ayrıca kritik kapı eylemlerinde (onay/yayın/red) insanın ekrandaki `increment_id`yi teyit etmesi zorunlu kılınarak rastgele dokunuşlar önlenir.

## 3. Nasıl etkileşim
- **Kapıların arayüzdeki görünümü:** Kapılar sıradan ikonlar değil, eylem kilitleridir.
  - **Kapı 1:** Taslak sözleşme `sozlesme.json` ve `increment.md` okunabilir sunulur; `motor_adayi` gösterilir; insan teyidiyle `bin/kapi.py onayla` çağrılır.
  - **Kapı 2:** Bekçi raporundaki kriterlerin kanıtları (`komut`/`dosya`) açıkça listelenir; yalnızca rapor PASS ve evre `yayin-bekliyor` iken yayın butonu aktif olur.
- **Koşuların tetiklenmesi:**
  - Koşular arayüzdeki açık ve tek bir "Takımı Koştur" düğmesiyle insan tarafından tetiklenir. Takım seçimi sunulmaz, evreden türetilir.
  - Koşular uzun sürebileceğinden HTTP bağlantısı bloke edilmez; `subprocess.Popen` ile arka planda çalıştırılır, arayüz `.kos.lock` ve evre durumunu yoklayarak (polling) sonucu yansıtır.
- **ANAYASA §4 ile uyum:** "Sürücü bir sonraki takımı kendisi başlatmaz; her koşu insanın elinden çıkar." Kuralı gereği uygulama otomatik ardışık dağıtıcı olamaz. Bir tetik yalnızca bir takımı bir kez başlatır; koşu bittiğinde sistem durur, evre güncellenir ve arayüz sıradaki adımı göstererek yeni bir insan dokunuşu bekler.

## 4. Determinizmle uyum
- **Tek Doğruluk Kaynağı (SoT):** Uygulama veritabanı (SQLite, Redis vb.), kuyruk veya bellek-içi bağımsız durum tutmaz. Her GET isteğinde diski (`increment/evre.json`, `increment/<id>/` artefaktları) anlık okur. Uygulama durumu değil, diskteki evre makinesini yansıtan salt bir mercektir.
- **`bin/kapi.py` ile ilişki:** Uygulama kapı mantığını ve evre kurallarını kendi içinde yeniden yazmaz. `bin/kapi.py`yi kabuksuz (`shell=False`) CLI alt süreci (`subprocess`) olarak argüman listesiyle çağırır. Şema doğrulaması, `chmod 0444` dosya kilidi ve `kararlar.md` yazımı tek merkezden deterministik olarak yürütülür; çıkış kodu ve mesaj kullanıcıya iletilir.

## 5. Sistemin kendisinin inşa edebilmesi
- **İnşaat ve test kolaylığı:**
  - Python stdlib tabanlı HTTP sunucusu ve saf HTML üretimi, `sistem-insaat`ın (codex, agy, grok) en güvenilir ve hatasız kod ürettiği alandır. Paket yükleme, derleme veya harici bağımlılık arızası riski yoktur.
  - Bekçi için kabul kriterleri deterministik ve yerel kalır:
    - Komut kriteri: `python3 -m unittest discover -s tests` (birim testler, sahte disk fikstürleri).
    - Komut kriteri: `python3 -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:<port>/durum')"` (sağlık kontrolü).
    - Dosya kriteri: `bin/sunucu.py` veya `web/index.html` gibi doğrudan artefaktlar.
  - Tarayıcı otomasyonu (Playwright vb.) gerektirmeyen bu yapı, bekçinin ağsız ortamda `komut` ve `dosya` kurallarıyla doğrulanmasını sağlar.

## 6. İlk increment
- **Önkoşul:** Kuruluş döngüsü uçtan uca tamamlanıp PASS ve Kapı 2 yayını görmeli, ardından insan `kapsam-disi.md`deki yönetim uygulaması maddesini bilinçli olarak kaldırmalıdır (evre kilidi kalkmadan bu katman açılamaz).
- **İlk talep (Tek cümle):** "Sistemin `increment/evre.json` durumunu ve sıradaki tek adımı 127.0.0.1 üzerinde HTTP GET ile JSON ve salt-okunur HTML sayfası olarak sunan stdlib tabanlı yerel durum sunucusu."
- **Sonraki increment sırası:**
  1. *2. Increment:* Ajan ortamından yalıtılmış oturum doğrulaması ile `talep`, `onayla` (Kapı 1), `yayinla` (Kapı 2) ve `red` kapı komutlarını `subprocess` üzerinden çalıştıran POST uç noktaları.
  2. *3. Increment:* İlgili evredeki takımı tek tıkla arka planda başlatan (`bin/kos.py <takim>`), kilit/koşu durumunu yansıtan ve bitince duran çalıştırma tetiği.
  3. *4. Increment:* Mobil cihazlara uyumlu duyarlı (responsive) kart görünümü, sözleşme/bekçi raporu kanıt paneli ve form içi `increment_id` niyet teyidi.

## 7. Riskler
- **Sistemin yeniden insanın taşımasına dönüşmesi:**
  - Arayüzün serbest sohbet, prompt kutusu veya ham log akışına boğulup insanı mikro-yöneticiye dönüştürmesi.
  - Kolaylık adına koşuların otomatik zincirlenmesi veya tek tıkla incelemesiz yayın yapılması (karar mekanizmasının buharlaşması).
  - Uygulamanın kendi durumunu/veritabanını tutarak `evre.json` ile ayrışması ve insanın iki gerçeği uzlaştırmak zorunda kalması.
  - CLI ile web arayüzü arasına ayrı iş kuralları sokulması.
- **Ne yapılmamalı:**
  - Serbest terminal veya motor sohbet penceresi açılmamalıdır.
  - İnsansız otomatik takım koşturma döngüsü yazılmamalıdır.
  - Uygulama içine diskten bağımsız veritabanı veya kuyruk katmanı konulmamalıdır.
  - Dış servislere bağımlı mesajlaşma botları (Telegram vb.) çekirdek süreç yapılmamalıdır.

## 2. turda değişen

Codex ve Grok'un katkıları doğrultusunda şu kritik değişiklikleri yaptım:

1. **Kimlik ve Yetki Güvenliği (2. bölüm):** 1. turdaki `.env` içinde `ETKILESIM_TOKEN` tutma önerimi geri çektim. Codex'in haklı olarak işaret ettiği gibi, repoya veya süreç ortamına erişebilen ajanlar bu jetonu okuyabilir ve insan taklidi yapabilir. Yetki sırrının ajan çalışma ortamından yalıtıldığı ters proxy/özel ağ oturumu ve CSRF koruması modelini benimsedim.
2. **"Onayın Maliyeti" vs Kimlik Doğrulama:** Grok'un formda `increment_id` ve PASS kararı yazdırma teyidini niyet teyidi (yanlışlıkla basmayı önleme) olarak değerli bulup benimsedim; ancak Grok'un "bu mekanizma kimlik doğrulaması yerine geçer" tezine katılmıyorum. Ajanlar da metin üretebilir ve diskteki ID'yi okuyabilir; dolayısıyla bu teyit kimlik doğrulamanın alternatifi değil, ancak proxy/oturum katmanının üstüne konan ikincil bir emniyet kilididir.
3. **SPA/PWA ve SSE yerine Sunucu-Taraflı HTML (SSR) (2. ve 5. bölüm):** 1. turdaki tek sayfa uygulaması (SPA/PWA) ve SSE ısrarından vazgeçtim. Codex ve Grok'un vurguladığı üzere, sunucu-taraflı HTML ve sade yoklama (polling) modeli; `sistem-insaat`ın en az sürtünmeyle kod yazmasını ve `sistem-bekci`nin stdlib `urllib` ile ağsız ortamda testi kolayca tamamlamasını sağlar.
4. **Önkoşul ve Kapsam Disiplini (6. bölüm):** Codex ve Grok'un hatırlattığı üzere, `kapsam-disi.md`deki yönetim uygulaması maddesi ve evre kilidi kaldırılmadan bu increment başlatılamaz. Kuruluş döngüsünün uçtan uca PASS+yayın görmesi zorunluluğunu 6. bölüme önkoşul olarak ekledim.
5. **Alt Süreç Yalıtımı ve Asenkron Koşu (3. ve 4. bölüm):** `kapi.py`yi Python modülü olarak import etme seçeneğini çıkarıp, süreç yalıtımı ve argüman kontrolü için doğrudan kabuksuz `subprocess` çağırma çizgisine sabitledim. Grok'un 15 dakikalık koşu uyarısı gereğince, `kos.py` tetiklendiğinde HTTP isteğinin asılı kalmayıp arka plan süreci ve kilit dosyasıyla çalışacağı netleştirildi.
