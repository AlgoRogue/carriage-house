# agy — etkileşim katmanı görüşü
> tur: 1

## 1. Ne
Uygulama, insanı terminale bağımlı kılmadan sistemin evrelerini izleyen ve iki kilit insan kapısını yöneten yalın bir karar ve kontrol paneli olmalıdır. Görevi karmaşık bir analitik paneli olmak değil, döngüyü işletmektir.
- **Neyi göstermeli:**
  - **Evre ve durum:** `increment/evre.json` dosyasındaki `increment_id`, mevcut `evre` (`bos`, `sozlesme`, `insaat`, `bekci`, `yayin-bekliyor`, `fail`, `red`), bekleyen onay (`sozlesme`, `yayin`) ve kilitlenen motorlar (`insaat`, `bekci`).
  - **Sıradaki açık adım:** `bin/kapi.py durum` çıktısına paralel olarak sıradaki operasyonel eylemi net göstermeli (ör. "Sırada: `python3 bin/kos.py sistem-sevk`").
  - **Karar belgeleri:**
    - Kapı 1 öncesinde `increment/<id>/sozlesme.json` (ve `increment.md` insan özeti),
    - Kapı 2 öncesinde `increment/<id>/bekci-raporu.json` (kriterler, komut/dosya kanıtları, PASS/FAIL kararı, varsa `kapsam_sapmasi` ve `park.md`).
  - **İnsan eylemleri:**
    - Yeni talep açma (`bin/kapi.py talep "..."`),
    - Kapı 1 onayı (`bin/kapi.py onayla [--motor ...]`),
    - Kapı 2 yayını (`bin/kapi.py yayinla`),
    - Gerekçeli red (`bin/kapi.py red "..."`),
    - Sıradaki takımı koşturma tetiği (`bin/kos.py <takim>`).
- **Neyi göstermemeli / yaptırmamalı:**
  - Ajanların koşu sırasındaki ara token akışlarını veya ham LLM düşünce zincirlerini canlı yayınlamamalı; bu durum insanı bilişsel olarak yorar ve mikro-yöneticiye dönüştürür.
  - İnsanın korumalı dosyalarını (`ANAYASA.md`, `sema/*`, `kararlar.md`, `kapsam-disi.md`) web üzerinden doğrudan düzenletmemeli; dosya tabanlı SoT disiplini korunmalıdır.
  - Ajanlar adına karar vermemeli, sözleşme maddesi uydurmamalı, bekçi raporunu manipüle etmemelidir.
  - Otomatik ardışık zincirleme (insansız arka plan döngüsü) yapmamalıdır.

## 2. Hangi teknoloji
- **Seçim:** Python 3 standart kütüphanesi (`http.server`, `urllib`, `json`) ile çalışan yerel bir HTTP sunucusu ve saf HTML/CSS/JS (Vanilla) tek sayfa arayüzü (SPA/PWA).
- **Gerekçe:** Repodaki tüm CLI adaptörleri ve kural motorları stdlib Python ile çalışmaktadır. Harici bir web çatısı (FastAPI, Flask) veya Node/npm/React ekosistemi getirmek, bağımlılık yönetimini zorlaştırır, `sistem-insaat`ın hata yapma riskini artırır ve test maliyetini yükseltir. Standart kütüphane determinizmi ve taşınabilirliği en üst seviyede korur.
- **Canlı güncelleme:** WebSocket gibi harici kütüphane veya karmaşık protokoller yerine, tek yönlü ve stdlib ile kolayca sunulabilen Server-Sent Events (SSE) veya kısa aralıklı yoklama (polling) tercih edilmelidir.
- **Erişim (Uzak / Mobil):** Sunucu yerel makinede çalışır. Bilgisayar başında olmadan telefondan erişim için Tailscale (VPN/Mesh) veya güvenli yerel ağ bağlantısı kullanılır. Telegram tetiği veya harici bulut servisleri `kapsam-disi.md`'dedir ve dış servis bağımlılığı yaratır; yerel tünel/Tailscale bu kuralı ihlal etmeden mobil erişim sağlar.
- **Kimlik ve yetki:** `.env` dosyasında saklanan tek bir gizli oturum belirteci (`ETKILESIM_TOKEN`) kullanılır. Arayüz ilk açılışta bu token'ı ister ve başlıkta/çerezde saklar. Kapı işlemlerinde (POST istekleri) token doğrulanmadan hiçbir işlem yapılmaz (HTTP 401).

## 3. Nasıl etkileşim
- **Kapıların arayüzdeki görünümü:** Kapılar dekoratif değil, eylem kilitleridir.
  - **Kapı 1:** Taslak sözleşme `sozlesme.json` yapılandırılmış kartlar halinde gösterilir; `motor_adayi` açılır listeden seçilir veya değiştirilir; insan "Sözleşmeyi Dondur ve Onayla" düğmesine basar.
  - **Kapı 2:** Bekçi raporundaki kriterlerin kanıtları (çalıştırılan komutlar, dosya varlıkları) yeşil/kırmızı rozetlerle sunulur; insan raporu inceleyip "Canlıya Al / Yayınla" düğmesine basar.
- **Koşuların tetiklenmesi:**
  - Koşular arayüzdeki açık bir "Takımı Koştur" düğmesiyle insan tarafından tetiklenir.
  - Bu tetik arka planda `bin/kos.py <takim>` sürecini başlatır, işlem tamamlanana kadar arayüzde çalışma durumu gösterilir ve süreç bitince durur.
- **ANAYASA §4 ile uyum:** "Sürücü bir sonraki takımı kendisi başlatmaz; her koşu insanın elinden çıkar." Kural gereği uygulama bir otomatik ardışık dağıtıcı (daemon loop) olamaz. Koşu bittiğinde sistem durur, evre ilerlemesini kaydeder ve sıradaki adımı gösterir. İnsan yeni bir düğmeye basmadıkça sonraki takım asla koşmaz.

## 4. Determinizmle uyum
- **Tek Doğruluk Kaynağı (SoT):** Uygulama hiçbir harici veritabanı (SQLite, Redis vb.) veya bellek-içi durum (in-memory state) tutmaz. Tamamen "durumsuz" (stateless) bir mercektir. Her HTTP isteğinde doğrudan diskteki `increment/evre.json`, `increment/<id>/` klasöründeki dosyaları ve `kararlar.md`'yi okur. Birden fazla sekme açılsa dahi hepsi aynı disk durumunu yansıtır.
- **`bin/kapi.py` ile ilişki:** Uygulama kapı mantığını kendi içinde yeniden uygulamaz (`reinvent the wheel` yapmaz). `bin/kapi.py` betiğini Python modülü olarak import edip işlevlerini (`talep`, `onayla`, `yayinla`, `red`, `durum`) doğrudan çağırır veya CLI alt süreci (`subprocess`) olarak yürütür. Bu sayede şema doğrulaması, `chmod 0444` dosya kilidi ve `kararlar.md` yazımı tek merkezden deterministik olarak yürütülmeye devam eder.

## 5. Sistemin kendisinin inşa edebilmesi
- **İnşaat ve test kolaylığı:**
  - Python stdlib tabanlı HTTP sunucusu ve statik HTML/JS dosyası, `sistem-insaat`ın (özellikle `codex` ve `agy`) en yüksek doğrulukla kod yazabileceği alandır. Paket kurma, derleme veya harici bağımlılık hatası riski sıfırdır.
  - Bekçi için kabul kriterleri deterministik ve kolaydır:
    - Komut kriteri: `python3 -m unittest discover -s tests` (birim testler).
    - Komut kriteri: `python3 -c "import urllib.request; urllib.request.urlopen('http://localhost:8080/durum')"` (sağlık kontrolü).
    - Dosya kriteri: `bin/sunucu.py` veya `web/index.html` dosyasının varlığı.
  - Karmaşık frontend frameworkleri bekçinin kütüphane veya tarayıcı bağımlılığı (Playwright, Selenium vb.) olmadan test etmesini imkansızlaştırır; saf stdlib ise ağsız ve sıfır ek maliyetle anında doğrulanır.

## 6. İlk increment
- **İlk talep (Tek cümle):** "Sistemin `increment/evre.json` durumunu ve sıradaki adımı HTTP GET üzerinden JSON ve salt-okunur HTML sayfası olarak sunan stdlib tabanlı yerel durum sunucusu."
- **Sonraki increment sırası:**
  1. *2. Increment:* Web arayüzü üzerinden token doğrulamalı `talep`, `onayla` (Kapı 1), `yayinla` (Kapı 2) ve `red` kapı komutlarını çalıştıran POST uç noktaları.
  2. *3. Increment:* İlgili evredeki takımı tek tıkla arka planda koşturan (`bin/kos.py <takim>`), koşu kaydını gösteren ve tamamlandığında duran çalıştırma tetiği.
  3. *4. Increment:* Mobil cihazlara uyumlu duyarlı (responsive) kart görünümü, sözleşme ve bekçi raporu görsel fark/kanıt paneli, Server-Sent Events (SSE) ile dosya tabanlı canlı durum yenileme.

## 7. Riskler
- **Sistemin yeniden insanın taşımasına dönüşmesi:**
  - Arayüzün bir "sohbet / chat" penceresine dönüştürülmesi ve insanın her aşamada ajanla uzun metinlerle pazarlık yapmak zorunda kalması.
  - Bildirim kirliliği yaratarak her ara çıktı veya log için insanı uyarmak ve karar yorgunluğu oluşturmak.
  - Web üzerinden kontrolsüz dosya düzenleme izni verilerek deterministik evre ve sözleşme disiplininin kırılması.
  - Kapsam genişlemesi: Temel iki kapı döngüsü oturmadan tema seçimi, kullanıcı yönetimi, analitik panelleri gibi gereksiz detaylara boğulmak.
- **Ne yapılmamalı:**
  - Serbest sohbet arayüzü ve ham LLM akışı eklenmemelidir.
  - İnsansız otomatik tamamlama veya otomatik ardışık takım koşturma döngüsü yazılmamalıdır.
  - Uygulama içine diskteki dosyalardan bağımsız bir durum veya veritabanı katmanı konulmamalıdır.
  - Dış servislere bağımlı mesajlaşma botları (Telegram vb.) döngü temeli yapılmamalıdır.
