# grok — etkileşim katmanı görüşü
> tur: 2

Tez: uygulama ikinci bir sistem değil. `increment/evre.json` ve `increment/<id>/` zaten SoT; uygulama onları yansıtır ve insanın elini `kapi.py` / `kos.py`'ye uzatır. Kendi evre tutmaz, sonraki takımı kendisi başlatmaz, kapıyı tek dokunuşla geçirmez. Evre kilidi kalkmadan (döngü bir kez uçtan uca + Kapı 2) bu katman yazılmaz — `hedef.md` bitiş çizgisi, `kapsam-disi.md` yönetim uygulaması maddesi. Sevk'e o madde dururken verilen talep sözleşme değil, `kapsam-disi` duruşudur.

## 1. Ne

Göstermeli (tek ekran, tek aktif increment):

- `increment_id`, `evre`, `bekleyen_onay`, `talep`, kilitli motorlar (`insaat` / `bekci`), `kapsam_sapmasi`
- **sıradaki adım** — `kapi.py durum` içindeki eşlemenin aynısı, düz cümle: "şimdi Kapı 1" / "şimdi `kos.py sistem-insaat`" / "şimdi Kapı 2" / "açık increment yok, talep yaz"
- Taslak sözleşme (`sozlesme.json` + varsa `increment.md`) Kapı 1 öncesi; dondurulmuş kopya (`sozlesme.onayli.json`) sonrası — insan okumadan onay düğmesi yok
- Kapı 2: onaylı sözleşme + `teslim.json` + `bekci-raporu.json` (karar, her kriterin `kanit`'i, `ihlal`, `kapsam_sapmasi`) birlikte. **PASS yayın değildir**; "Yayınla" yalnız `karar=PASS` **ve** `evre=yayin-bekliyor` iken etkin
- `gecmis` (son olay yeter; tam liste açılır), ilgili takımın `son_sonuc` / `son_sebep`
- `fail` evresinde: FAIL gerekçesi + yalnız `red` (ve "sözleşmeyi düzelt" notu). Yamama, yeniden inşa, "düzeltip tekrar koş" sihirbazı yok
- Ham artefakt indirme/görüntüleme var; tarayıcıda JSON/kod/`evre.json` düzenleme yok

Yaptırmalı: `talep`, `onayla [--motor]`, `yayinla`, `red "<sebep>"`, ve **yalnız evrenin izin verdiği tek takım için** `kos.py <takim>`. Yanlış takım zaten `kos.py` `evre_kontrol` ile atlanır; uygulama takım seçici sunmaz. GET hiçbir zaman yazmaz.

Göstermemeli / yaptırmamalı:

- `.env`, anahtar, istem metni, motor CLI dökümü, canlı token/düşünce zinciri
- `sozlesme.onayli.json` düzenleme, `evre.json` yazma, `kararlar.md` / `ANAYASA.md` / `sema/` dokunma
- İkinci increment, kuyruk yöneticisi, takım sohbeti, `defter.md` duvarı
- Commit / push / tag, dış servise yazma
- Otomatik zincir: bir koşu bitince öteki takımı başlatmak
- "akıllı sonraki adım"ın kapıyı veya koşuyu sessizce basması
- Canlı log terminali birincil yüzey olarak — koşu kaydı linki yeter; insan log bakıcısına dönmesin

Uygulama `kapi.py durum`'un okunur hâlidir, dashboard değil. İnsan hâlâ "şimdi hangi takım?" diye soruyorsa yüzey yanlış kurulmuştur; evre zaten söylüyor.

## 2. Hangi teknoloji

**stdlib Python HTTP** (`http.server` veya ince bir `wsgiref` sarmalayıcı) + **sunucu-tarafı HTML** (üretilmiş sayfa) + `GET/POST`. Bağımlılık yok. SPA/PWA yok: istemci durum makinesi ikinci SoT olur; bekçi `komut` ile ölçemez.

Neden: ajanlar stdlib Python yazıyor; `tests/` ağsız `unittest`; `kapsam-disi.md` kalıcı madde para harcayan kurulumu dışarıda tutuyor. Flask/FastAPI/React/npm bir karardır ve bu katmanda gerekçesi yok. Native telefon uygulaması da yok: aynı HTML, telefon tarayıcısı.

Yerel önce: süreç **yalnız `127.0.0.1`**. Stdlib sunucu internete açılmaz. Uzak/telefon ayrı increment: özel ağ (Tailscale veya kimlik doğrulayan ters proxy) aynı loopback sürece bağlanır. TLS, oturum iptali, oran sınırı uygulamada elde yazılmaz — stdlib kazancını yer. Telegram tetiği bu katman değil.

Kimlik / yetki (iki ayrı soru):

- **"Kim?"** — uzak erişimde proxy'nin doğruladığı insan hesabı. Uygulama sahte `X-Forwarded-*` başlığına güvenmez; jeton `.env` üzerinden ajan ortamına veya koşu istemine girmez (ajan `.env` okur). Ortak cookie parolası "insan" sayılmaz.
- **"Dikkat etti mi?"** — `onayla` / `yayinla` / `red` tek tık değil: insan `increment_id`'yi (ve mevcut evreyi ekranda görerek) forma yazar; Kapı 2'de `karar=PASS` görünür. Rastgele bildirim dokunuşu kapı geçmez.
- Uygulama LLM çağırmaz, motor başlatmaz (`kapi.py` ile aynı kural). CSRF'siz POST ve GET ile mutasyon yok.

## 3. Nasıl etkileşim

Kapılar evreye göre **tek bir birincil düğme**:

| evre / bekleyen | düğme | zorunlu teyit |
|---|---|---|
| `bos` / `yayinlandi` / `red` | talep (tek cümle) | yok |
| `bekleyen_onay=sozlesme` | Kapı 1 onayla; `motor_adayi` gösterilir, `--motor` isteğe bağlı | `increment_id` + evre + sözleşmenin özeti ekranda |
| `sozlesme` / `insaat` / `bekci` | "bu takımı koştur" (takım evreden; seçici yok) | yok (evre zaten kilidi) |
| `yayin-bekliyor` | Kapı 2 yayinla | `increment_id` + evre + raporda `PASS` görünür |
| `fail` | red (sebep zorunlu) | `increment_id` + evre |
| her açık evre | red her zaman ikincil | sebep + `increment_id` + evre (hedef yanlışlıkla basılmasın) |

Eylemden hemen önce sunucu `evre.json`'u yeniden okur; eski sekmenin `increment_id`/evresi uyuşmuyorsa hiçbir şey yazmadan çatışma gösterir.

`kos.py` uygulamadan tetiklenir. Aksi hâlde insan yine makine başında 15 dakikalık koşuyu bekler; uzak etkileşimin anlamı kalmaz. Uyum: ANAYASA §4 "sürücü bir sonraki takımı kendisi başlatmaz; her koşu insanın elinden çıkar." Uygulama sürücü değildir, insanın elidir. Bir `POST /kos` **bir** `kos.py <takim>` başlatır; `takim` evreden türetilir, kullanıcı seçmez, keyfî argüman alınmaz; süreç bitince uygulama `evre.json`'u yeniden okur ve **durur**. Sonraki takım için ayrı basış gerekir. Uygulama `kos.py`'nin kuyruğuna ikinci iş koymaz, bitiş kancası yazmaz, `--zorla` sunmaz.

Koşu 15 dk sürebilir: HTTP isteği beklemez. `kos.py` alt süreç + `.kos.lock` (zaten var); tarayıcı kopması koşuyu öldürmez; sayfa `evre` / `son_sonuc` poll eder. Poll yazmaz. Otomatik yenileme eylem üretmez.

## 4. Determinizmle uyum

Okuma: her istekte `evre.json` ve **yalnız onun işaret ettiği** `increment/<id>/` dosyaları. Önbellek SoT değildir. Eksik, bozuk veya şemaya aykırı veri iyimser yorumlanmaz: ekran "tutarsız durum" gösterir, bütün yazma düğmeleri kapanır.

Yazma:

- Kapı mutasyonları `python3 bin/kapi.py …` **argv listesiyle, kabuksuz alt süreç**. Uygulama `kapi.py`'yi modül olarak import edip iç fonksiyonlara kaymaz — CLI ile web aynı giriş; kural değişince iki implementasyon ayrışmaz. Uygulama `evre_guncelle` çağırmaz, `sozlesme.onayli.json` kopyalamaz, `kararlar.md`'ye satır düşmez.
- Koşu `python3 bin/kos.py <takim>` alt süreç. Evre geçişini yine sürücü yapar (artefakt geçerliyse).
- Yazma istekleri sunucuda seri; UI ön kontrolü TOCTOU'ya yetmez. `kapi.py` zaten yanlış evrede çıkış 1 verir; uygulama o kodu ve mesajı basar, sonra SoT'u yeniden okur.

Uygulamanın kendi durumu: güvenlik oturumu / CSRF nonce, belki "koşu sürüyor mu" (PID / `.kos.lock`). Increment durumu, kuyruk, motor kilidi **yok**.

`kapi.py durum` ile `GET /durum` çelişirse dosya doğrudur, uygulama yanlıştır.

## 5. Sistemin kendisinin inşa edebilmesi

Bu yığın inşaat (codex/agy/grok) ve bekçi (`komut`/`dosya`) için en az sürtünme: tek dil, sıfır paket, mevcut `tests/` kalıbı (`sahte_kok` + `kapi.talep`). Bekçi `python3 -m unittest discover -s tests` ve `python3 -c "… urlopen('http://127.0.0.1:<port>/durum')"` (çıkış 0, JSON'da `evre`) ile ölçer. npm derlemesi, tarayıcı otomasyonu, Playwright, Docker, harici staging yok — ilk increment kabul kriteri olamaz.

Sözleşme dar tutulur: her increment bir görünür uç (`GET /durum` + salt-okur HTML, sonra yazma kapıları ayrı ayrı). Mantık "dosyaları oku → görünüm modeli → HTML/JSON" diye ayrılırsa bekçi hem saf fonksiyonu hem yerel portu ölçer. `sema/evre.schema.json` değişmez — uygulama yeni evre alanı icat etmez.

Motor önerisi: inşaat `codex` (dosya/şema/script, diff'e kilitli) veya kısa yüzey için `grok`. `claude` istisna; gerekçesiz seçilmez.

## 6. İlk increment

Önkoşul: increment 0 çizgisi geçmiş olmalı **ve** insan `kapsam-disi.md`'deki yönetim uygulaması maddesini silmiş olmalı. Aksi hâlde sevk durur; "uygulamayı yap" diye tek geniş sözleşme de kesilmez.

Talep: `python3 bin/uygulama.py` yalnız 127.0.0.1'de dinler; `GET /durum` JSON ve salt-okur HTML, `evre.json` ile aktif increment artefaktlarından evreyi, bekleyen onayı, sıradaki tek adımı ve dosya bağlantılarını gösterir; hiçbir yazma eylemi sunmaz.

Sonraki sıra (yol haritası değil):

1. `POST /talep` ve `POST /red` → `kapi.py`; red hedef `increment_id` + evre teyidi ister; GET yazmaz
2. Tam sözleşme incelemesi + motor seçimi + `increment_id` teyidi ile Kapı 1 (`kapi.py onayla`)
3. `POST /kos` yalnız evredeki takımı başlatır (bitişte durur) ve Kapı 2 (`yayinla`; PASS ≠ yayın)

Uzak bağ (proxy/Tailscale) ve CSRF bu yazma increment'lerinin dağıtım sınırıdır, ayrı ürün değildir. Telegram/zamanlayıcı açılmaz.

## 7. Riskler

Bu katman "sistemi yine insanın taşıması"na şuralarda döner:

- Uygulama SoT olursa (kendi DB'si, kendi evresi, `kapi.py`'yi taklit veya import ile ikinci kapı yolu) — insan iki gerçeği uzlaştırır
- "Kolaylık" diye otomatik zincir — Kapı 1/2 ve ANAYASA §4 fiilen kalkar; insan koşu bakıcısı olur
- Tek tık yayın / tek tık onay / ortak `.env` jetonu — kapı kalır ama karar kaybolur; ajanın okuyabildiği sır "insan" sayılır
- Canlı log, takım seçici, retry sihirbazı, SPA durum makinesi — insan yine "hangi takım, hangi dosya SoT" taşır
- Telegram/bot ilk yüzey — dış yazma + tetik; onay chate sıkışır, kanıt dosyada kalır
- Bağımlılık, internete açık stdlib, GET ile mutasyon — bekçi ölçemez veya kapı ajanın eline düşer

Yapılmamalı: `kapi.py`'yi yeniden yazmak veya üretimde import etmek, `kos.py`'yi bitişte zincirlemek, evreyi uygulamada önbellekleyip karar vermek, kapıyı jetonlu tek POST'a indirmek, yönetim uygulamasını işletme takımı veya zamanlayıcı ile aynı increment'te açmak, madde `kapsam-disi.md`'deyken sevk'e uygulama talebi vermek.

Başarı ölçütü `hedef.md`'deki en pahalı arızanın tersi: insan telefonda evreyi görür, sözleşmeyi/raporu okur, bir kapıya veya bir koşuya basar, durur. "Şimdi hangi takım?" sorusu ekranda cevaplıdır; insan sormaz.

## 2. turda değişen

Codex ile birleştiğim yerler gövdeye işlendi: salt-okur HTML ilk increment'e girdi (1. turda yalnız JSON vardı); PASS ≠ yayın ve Kapı 2'de üç artefakt birlikte; GET yazmaz; eylem öncesi evre yeniden okunur, eski sekme çatışması yazmaz; tarayıcı kopması `kos.py`'yi öldürmez; bozuk SoT "tutarsız durum" + yazma kapalı; üretim yolu `kapi.py` argv alt süreç (import değil); jeton `.env`/ajan ortamına girmez, uzak kimlik proxy'dedir; yazma sırası talep/red → Kapı 1 → kos+Kapı 2 diye ayrıldı.

agy'ye katılmadığım yerler duruyor, gerekçeyle: Vanilla SPA/PWA istemci durum makinesidir, sunucu-tarafı HTML kalır. `kapi.py`'yi modül import etmek ikinci kapı implementasyonudur; CLI tek giriş kalmalı. SSE 4. increment değil — poll yeter, eylem üretmez. Tek `ETKILESIM_TOKEN` çerezi "insan" kanıtı değil (ajan `.env` okur); teyit hâlâ `increment_id`+evre yazmaktır. agy `kapsam-disi` kilidini atladı; madde silinmeden ilk talep "durum sunucusu" olamaz.

Değişmeyen: uygulama sürücü değil insanın eli; takım seçici yok; `fail`'de yalnız red; otomatik zincir yok; evre kilidi kalkmadan yazılmaz.
