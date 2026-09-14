# A Şirketi

Farklı yapay zekâ CLI'larını — **claude, agy, codex, grok** — yöneten deterministik bir üst katman.
Üç ajan (sözleşme kes · inşa et · ölç), iki insan kapısı, dosya tabanlı durum. Ajanlar bir içerik üretmez;
**bu sistemin kendisini** bir increment ileri götürür ve durur. Yayın düğmesi insanda.

> Sentezin kilit cümlesi: çekirdek kadro A Şirketi'ni *kullanan* üç bakanlık değildir; A Şirketi'ni
> *üreten* üç kilittir — sözleşme kes, bir increment inşa et, sözleşmeye karşı ölç, insan yayınlasın.

## Üç kilit

| Takım | Ne yapar | Motor | Çıktı (şema zorlamalı) |
|---|---|---|---|
| **sistem-sevk** | İnsanın tek cümlesini dondurulmuş increment sözleşmesine çevirir | `claude` | `increment/<id>/sozlesme.json` |
| **sistem-insaat** | Onaylı sözleşmeyi koda işler; ne fazla ne eksik | sözleşmeden (`codex` varsayılan; `agy`, `grok`, istisnai `claude`) | `teslim.json` (+ `park.md`) |
| **sistem-bekci** | Sözleşme kadar çalışıyor mu — kanıtla PASS/FAIL | üretenin tersi (`→ claude`; claude üretirse `→ grok`) | `bekci-raporu.json` |

Her takım `takimlar/<takim>/` altında aynı dört dosyayla yaşar: `takim.md` · `kurallar.md` · `defter.md` ·
`durum.json`. Okuma sırası her koşuda aynı: `ANAYASA.md` → `sirket/AJAN-KIMLIGI.md` → `hedef.md` →
`kararlar.md` → `kapsam-disi.md` → `kurallar.md` → `takim.md`.

## Döngü

```
sen        python3 bin/kapi.py talep "sistemin sıradaki çalışan parçası: <tek davranış>"
                    │  evre: sozlesme
           python3 bin/kos.py sistem-sevk         claude → sozlesme.json (şema zorlamalı, sürücü yazar)
                    │  bekleyen_onay: sozlesme
sen        python3 bin/kapi.py onayla [--motor grok]    ── KAPI 1: sozlesme.onayli.json (salt-okunur), motor kilidi
                    │  evre: insaat
           python3 bin/kos.py sistem-insaat       sözleşme motoru → kod + teslim.json; sürücü git farkını ölçer
                    │  evre: bekci (+ kapsam_sapmasi)
           python3 bin/kos.py sistem-bekci        ters motor → bekci-raporu.json PASS|FAIL
                    │  yayin-bekliyor | fail
sen        python3 bin/kapi.py yayinla                  ── KAPI 2: kararlar.md'ye satır, evre kapanır
```

Sürücü hiçbir koşuda bir sonraki takımı kendisi başlatmaz; her koşu senin elinden çıkar. Evreyi yalnız
`bin/kos.py` (artefakt geçerliyse) ve `bin/kapi.py` (sen) ilerletir; ajan evreyi yazamaz.

## Deterministik olan ne

- **Motor seçimi** takım dosyasında değil kuralda: `motor: claude` (sabit) · `sozlesme` (Kapı 1'de kilitlenen) ·
  `ters` (`bin/motorlar/TERS_MOTOR`). Aynı sözleşme her zaman aynı motora gider.
- **Yapısal çıktı** dört CLI'nin şema bayrağıyla zorlanır (`--json-schema` / `--output-schema`); dosyayı sürücü
  yazar, `bin/sema.py` doğrular. Ajanın "dosyayı doğru yere yazması"na güvenilmez.
- **Kapsam** koşu öncesi/sonrası `git status` farkıyla ölçülür: sevk ve bekçi kendi klasörü dışına yazarsa
  koşu `red`; inşaatın sapması bekçiye kanıt olarak gider ve tek başına FAIL sebebidir.
- **Bekçi katman A** LLM'siz: boş kayıt, gizli veri deseni, insanın dosyasına dokunma (mtime) → red.
- **Tavanlar** motor bağımsız: 15 dk/koşu, 6 koşu/gün/takım; USD tavanı yalnız maliyet raporlayan motorda
  (bugün claude) — raporlamayan motor kayda "motor raporlamıyor" notuyla girer, sıfır sayılmaz.

## Klasörler

```
ANAYASA.md · hedef.md · kararlar.md · kapsam-disi.md    insanın dosyaları (SoT) — ajan dokunamaz
sema/                 dondurulmuş JSON şemalar: increment-sozlesmesi · teslim · bekci-raporu · evre
increment/            evre.json (tek aktif increment) · <id>/ (sözleşme, onaylı kopya, teslim, rapor, park)
takimlar/<takim>/     takim.md · kurallar.md · defter.md · durum.json · kosu/
bin/                  kos.py (sürücü) · kapi.py (insan kapıları) · bekci.py (katman A) · sema.py · ayar.py
bin/motorlar/         claude.py · agy.py · codex.py · grok.py — her CLI tek dosya, aynı üç yüz
tests/                ağsız, motor çağrısız: python3 -m unittest discover -s tests
```

## Kurulum

```bash
git clone <repo> a-sirketi && cd a-sirketi
cp .env.example .env                      # motorlar kendi oturumunu kullanır; anahtar gerekmez
which claude agy codex grok               # dördü de yolda olmalı (en azından claude + bir tane daha)
python3 -m unittest discover -s tests     # 43 test, ağ yok, para yok
python3 bin/kapi.py durum                 # evre: bos
python3 bin/kos.py sistem-sevk --kuru     # istemi ve evre kararını basar, motor çağırmaz
```
Ayrıntı ve ilk uçtan uca prova: [KURULUM.md](KURULUM.md).

## Komutlar

| Komut | Ne yapar |
|---|---|
| `bin/kapi.py talep "…"` | Yeni increment açar (`inc-NNN`), evre `sozlesme` |
| `bin/kapi.py onayla [--motor X]` | Kapı 1 — taslağı dondurur, inşaat/bekçi motorunu kilitler |
| `bin/kapi.py yayinla` | Kapı 2 — PASS'ı `kararlar.md`'ye işler, evreyi kapatır |
| `bin/kapi.py red "…"` | Increment'i her evrede kapatır |
| `bin/kapi.py durum` | Evre, bekleyen onay, motorlar, sıradaki komut |
| `bin/uygulama.py [--port 8765]` | Salt-okur durum sayfası; yalnız 127.0.0.1, `GET /` |
| `bin/kos.py <takim> [--kuru] [--zorla]` | Takımı bir kez koşturur; `--kuru` motor çağırmaz; `--zorla` günlük tavanı atlar |
| `bin/bekci.py --dogrudan <takim> [kosu]` | Katman A'yı elle çalıştırır |
| `bin/sema.py <şema> <dosya>` | JSON dosyasını dondurulmuş şemaya karşı doğrular |
| `bin/ayar.py` | Tavanlar, evre, `.env` var mı |

## Kapsam dışı (şimdilik)

İşletme takımları (kod geliştirme, inceleme, araştırma, planlama), otomatik zincir, zamanlayıcı, Telegram
tetiği, yönetim uygulaması, çoklu-motor karşılaştırma. Hepsi `kapsam-disi.md`'de tarihli; döngü bir kez
uçtan uca işlemeden hiçbiri yazılmaz (ANAYASA §5, evre kilidi). Eski içerik şirketi `icerik-sirketi-v1`
etiketinde duruyor.

## Lisans

MIT — [LICENSE](LICENSE).
