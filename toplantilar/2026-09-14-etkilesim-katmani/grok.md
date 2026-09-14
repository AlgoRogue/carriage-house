# grok — etkileşim katmanı görüşü
> tur: 1

Tez: uygulama ikinci bir sistem değil. `increment/evre.json` ve `increment/<id>/` zaten SoT; uygulama onları yansıtır ve insanın elini `kapi.py` / `kos.py`'ye uzatır. Kendi evre tutmaz, sonraki takımı kendisi başlatmaz, kapıyı tek dokunuşla geçirmez. Evre kilidi kalkmadan (döngü bir kez uçtan uca + Kapı 2) bu katman yazılmaz — `hedef.md` bitiş çizgisi, `kapsam-disi.md` yönetim uygulaması maddesi.

## 1. Ne

Göstermeli (tek ekran, tek aktif increment):

- `increment_id`, `evre`, `bekleyen_onay`, `talep`, kilitli motorlar (`insaat` / `bekci`), `kapsam_sapmasi`
- **sıradaki adım** — `kapi.py durum` içindeki eşlemenin aynısı, düz cümle: "şimdi Kapı 1" / "şimdi `kos.py sistem-insaat`" / "şimdi Kapı 2" / "açık increment yok, talep yaz"
- Taslak sözleşme (`sozlesme.json` + varsa `increment.md`) Kapı 1 öncesi; dondurulmuş kopya (`sozlesme.onayli.json`) sonrası — insan okumadan onay düğmesi yok
- `teslim.json`, `bekci-raporu.json` (karar, her kriterin `kanit`'i, `ihlal`) Kapı 2 öncesi — rapor okunmadan yayın düğmesi yok
- `gecmis` (son olay yeter; tam liste açılır), ilgili takımın `son_sonuc` / `son_sebep`
- `fail` evresinde: FAIL gerekçesi + yalnız `red` (ve "sözleşmeyi düzelt" notu). Yamama, yeniden inşa, "düzeltip tekrar koş" sihirbazı yok

Yaptırmalı: `talep`, `onayla [--motor]`, `yayinla`, `red "<sebep>"`, ve **yalnız evrenin izin verdiği tek takım için** `kos.py <takim>`. Yanlış takım zaten `kos.py` `evre_kontrol` ile atlanır; uygulama takım seçici sunmaz.

Göstermemeli / yaptırmamalı:

- `.env`, anahtar, istem metni, motor CLI dökümü
- `sozlesme.onayli.json` düzenleme, `evre.json` yazma, `kararlar.md` / `ANAYASA.md` / `sema/` dokunma
- İkinci increment, kuyruk yöneticisi, takım sohbeti, `defter.md` duvarı
- Commit / push / tag, dış servise yazma
- Otomatik zincir: bir koşu bitince öteki takımı başlatmak
- "akıllı sonraki adım"ın kapıyı veya koşuyu sessizce basması
- Canlı log terminali birincil yüzey olarak — koşu kaydı linki yeter; insan log bakıcısına dönmesin

Uygulama `kapi.py durum`'un okunur hâlidir, dashboard değil. İnsan hâlâ "şimdi hangi takım?" diye soruyorsa yüzey yanlış kurulmuştur; evre zaten söylüyor.

## 2. Hangi teknoloji

**stdlib Python HTTP** (`http.server` veya ince bir `wsgiref` sarmalayıcı) + sunucu-tarafı HTML (şablon dosyası veya üretilmiş sayfa) + `GET/POST` JSON. Bağımlılık yok.

Neden: ajanlar stdlib Python yazıyor; `tests/` ağsız `unittest`; `kapsam-disi.md` kalıcı madde para harcayan kurulumu dışarıda tutuyor. Flask/FastAPI/React/npm bir karardır ve bu katmanda gerekçesi yok — bekçinin ölçeceği yüzey büyür, inşaat sapması artar. Native telefon uygulaması da yok: aynı HTML, telefon tarayıcısı.

Yerel önce: varsayılan `127.0.0.1`. Uzak/telefon ayrı increment: özel ağ (Tailscale veya SSH tüneli) üzerinden aynı süreç. Telegram tetiği bu katman değil — `kapsam-disi.md`'de ayrı madde, dış servise yazma yasağına sürtünür, tetik otomatik zincire kayar.

Kimlik / yetki:

- Kapıya basan "gerçekten insan mı?" sorusunun cevabı OAuth değil, **onayın maliyeti**. `onayla` / `yayinla` / `red` tek tık değil: insan `increment_id`'yi (ve Kapı 2'de bekçi `karar=PASS` olduğunu) forma yazar. Rastgele bildirim dokunuşu kapı geçmez.
- `UYGULAMA_JETON` yalnız `.env`'de; her yazma isteğinde header veya form alanı. Jeton yoksa süreç yalnız localhost dinler.
- Uygulama LLM çağırmaz, motor başlatmaz (`kapi.py` ile aynı kural). Jeton çalınırsa zarar kapı teyidi + evre makinesinin reddi ile sınırlı kalır; yine de jeton log'a yazılmaz.

## 3. Nasıl etkileşim

Kapılar evreye göre **tek bir birincil düğme**:

| evre / bekleyen | düğme | zorunlu teyit |
|---|---|---|
| `bos` / `yayinlandi` / `red` | talep (tek cümle) | yok |
| `bekleyen_onay=sozlesme` | Kapı 1 onayla; `motor_adayi` gösterilir, `--motor` isteğe bağlı | `increment_id` + sözleşmenin özeti ekranda |
| `sozlesme` / `insaat` / `bekci` | "bu takımı koştur" | yok (evre zaten kilidi) |
| `yayin-bekliyor` | Kapı 2 yayinla | `increment_id` + raporda `PASS` görünür |
| `fail` | red (sebep zorunlu) | `increment_id` |
| her açık evre | red her zaman ikincil | sebep + `increment_id` |

`kos.py` uygulamadan tetiklenir. Aksi hâlde insan yine makine başında 15 dakikalık koşuyu bekler; uzak etkileşimin anlamı kalmaz. Uyum: ANAYASA §4 "sürücü bir sonraki takımı kendisi başlatmaz; her koşu insanın elinden çıkar." Uygulama sürücü değildir, insanın elidir. Kural şöyle bağlanır: bir `POST /kos` **bir** `kos.py <takim>` başlatır; `takim` evreden türetilir, kullanıcı seçmez; süreç bitince uygulama `evre.json`'u yeniden okur ve **durur**. Sonraki takım için ayrı basış gerekir. Uygulama `kos.py`'nin kuyruğuna ikinci iş koymaz, bitiş kancası yazmaz, `--zorla` sunmaz (o insan terminalinin kaçış vanasıdır).

Koşu 15 dk sürebilir: HTTP isteği beklemez. `kos.py` alt süreç + `.kos.lock` (zaten var); sayfa `evre` / `son_sonuc` poll eder. Poll yazmaz.

## 4. Determinizmle uyum

Okuma: her istekte `evre.json` ve `increment/<id>/` dosyaları. Önbellek SoT değildir; "son gördüğüm evre" yalnızca çizim kolaylığı, karar değil.

Yazma:

- Kapı mutasyonları `bin/kapi.py` (alt süreç veya aynı fonksiyonlar — `test_kapi.py` nasıl çağırıyorsa). Uygulama `evre_guncelle` çağırmaz, `sozlesme.onayli.json` kopyalamaz, `kararlar.md`'ye satır düşmez. `kapi.py` insanın dosyasıdır (ANAYASA §5); ajan dokunamaz, uygulama da onu yeniden yazmaz.
- Koşu `python3 bin/kos.py <takim>` alt süreç. Evre geçişini yine sürücü yapar (artefakt geçerliyse).

Uygulamanın kendi durumu: jeton oturumu, belki "koşu sürüyor mu" (PID / kilit dosyası var mı). Increment durumu, kuyruk, motor kilidi **yok**. İki yazar olursa (`uygulama` + `kapi.py`) evre makinesi yalan söyler; o an "sistemi yine insan taşır."

`kapi.py durum` ile `GET /durum` çelişirse dosya doğrudur, uygulama yanlıştır.

## 5. Sistemin kendisinin inşa edebilmesi

Bu yığın inşaat (codex/agy/grok) ve bekçi (`komut`/`dosya`) için en az sürtünme: tek dil, sıfır paket, mevcut `tests/` kalıbı (`sahte_kok` + `kapi.talep`). Bekçi `python3 -m unittest discover -s tests` ve `curl -s http://127.0.0.1:<port>/durum` (çıkış 0, JSON'da `evre` alanı) ile ölçer. npm derlemesi, tarayıcı otomasyonu, Docker, harici staging yok.

Sözleşme dar tutulur: her increment bir görünür uç (`GET /durum`, sonra bir POST kapısı, sonra `POST /kos`). Şablon + tek `bin/` girişi yeter. `sema/evre.schema.json` değişmez — uygulama yeni evre alanı icat etmez.

Motor önerisi: inşaat `codex` (dosya/şema/script, diff'e kilitli) veya kısa yüzey için `grok`. `claude` istisna; gerekçesiz seçilmez.

## 6. İlk increment

Talep: `python3 bin/uygulama.py` 127.0.0.1'de dinler; `GET /durum` `increment/evre.json`'dan id, evre, bekleyen_onay, motor, talep ve `kapi.py durum`'daki sıradaki komut eşlemesini JSON basar.

Sonraki sıra (yol haritası değil):

1. `POST /talep|/onayla|/yayinla|/red` → `kapi.py`; onayla/yayinla/red `increment_id` teyidi ister; yanlış evrede kapi'nin çıkış 1'i aynen döner
2. `POST /kos` yalnız evredeki takımı `kos.py` ile başlatır; bitişte evreyi okur, sonraki takımı başlatmaz
3. Jeton + localhost dışı bağ (telefon tarayıcısı); kapı teyidi durur, Telegram/zamanlayıcı açılmaz

Önkoşul: increment 0 çizgisi geçmiş olmalı. Aksi hâlde sevk `kapsam-disi` der, durur.

## 7. Riskler

Bu katman "sistemi yine insanın taşıması"na şuralarda döner:

- Uygulama SoT olursa (kendi DB'si, kendi evresi, `kapi.py`'yi taklit) — insan iki gerçeği uzlaştırır
- "Kolaylık" diye otomatik zincir — Kapı 1/2 ve ANAYASA §4 fiilen kalkar; insan koşu bakıcısı olur
- Tek tık yayın / tek tık onay — kapı kalır ama karar kaybolur; bildirim parmağı insan sayılır
- Canlı log, takım seçici, retry sihirbazı — insan yine "hangi takım, hangi dosya SoT, çıktıyı nereye yapıştırayım" taşır
- Telegram/bot ilk yüzey — dış yazma + tetik; onay bir chate sıkışır, kanıt dosyada kalır
- Bağımlılık ve SPA — her increment'de inşaat sapması, bekçi `komut` ile ölçemez, insan aracı taşır

Yapılmamalı: `kapi.py`'yi yeniden yazmak, `kos.py`'yi bitişte zincirlemek, evreyi uygulamada önbellekleyip karar vermek, kapıyı jetonlu tek POST'a indirmek, yönetim uygulamasını işletme takımı veya zamanlayıcı ile aynı increment'te açmak.

Başarı ölçütü `hedef.md`'deki en pahalı arızanın tersi: insan telefonda evreyi görür, sözleşmeyi/raporu okur, bir kapıya veya bir koşuya basar, durur. "Şimdi hangi takım?" sorusu ekranda cevaplıdır; insan sormaz.
