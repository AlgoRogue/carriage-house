# A Şirketi

Farklı yapay zekâ CLI'larını — **claude, agy, codex, grok** — yöneten deterministik bir üst katman.
Üç ajan (sözleşme kes · inşa et · ölç), dosya tabanlı durum. İnsan işi verir, sistem sonuna kadar götürür,
insan sonda **onaylar ya da revize eder**. Ajanlar bir içerik üretmez; **bu sistemin kendisini** bir increment
ileri götürür ve durur.

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
sen        python3 bin/dongu.py "sistemin sıradaki çalışan parçası: <tek davranış>" [--motor grok]
                    │  talep → evre: sozlesme
           sistem-sevk    (claude)          → sozlesme.json (şema zorlamalı, sürücü yazar)
           onayla         (otomatik)        → sozlesme.onayli.json, inşaat/bekçi motoru kilitlenir
           sistem-insaat  (sözleşme motoru) → kod + teslim.json; sürücü git farkını ölçer
           sistem-bekci   (ters motor)      → bekci-raporu.json PASS | FAIL
                    │  FAIL → yeniden (en fazla 2): inşaat raporu okuyup düzeltir
                    ▼  PASS → durur
sen        python3 bin/kapi.py yayinla            → kararlar.md satırı, git commit, evre kapanır
           python3 bin/kapi.py revize "<not>"     → sevk notu okuyup yeniden keser; dongu.py --devam
           python3 bin/kapi.py red "<sebep>"      → kapanır
```

Arada onay yok; karar sonda. `bin/kos.py` tek koşu yapar; zinciri `bin/dongu.py` (LLM'siz otomat) kurar.
Evreyi yalnız `kos.py` (artefakt geçerliyse), `dongu.py` ve `kapi.py` (sen) ilerletir; ajan evreyi yazamaz.

## Deterministik olan ne

- **Motor seçimi** takım dosyasında değil kuralda: `motor: claude` (sabit) · `sozlesme` (onayda kilitlenen) ·
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
python3 -m unittest discover -s tests     # ağ yok, para yok
python3 bin/kapi.py durum                 # evre: bos
python3 bin/kos.py sistem-sevk --kuru     # istemi ve evre kararını basar, motor çağırmaz
```
Ayrıntı ve ilk uçtan uca prova: [KURULUM.md](KURULUM.md).

## Komutlar

| Komut | Ne yapar |
|---|---|
| `bin/dongu.py "…" [--motor X] [--deneme N]` | **Ana komut** — işi açar, sevk→onay→inşaat→bekçi zincirini sonuna kadar götürür |
| `bin/dongu.py --devam` | Mevcut evreden sürdürür (revize sonrası, ya da kesilen döngü) |
| `bin/kapi.py yayinla` | İnsan onayı — `kararlar.md`'ye işler, **git commit**, evreyi kapatır |
| `bin/kapi.py revize "…"` | Notunla sözleşmeye döner; sevk yeniden keser |
| `bin/kapi.py yeniden` | FAIL sonrası aynı sözleşmeyle inşaata dön (dongu bunu otomatik yapar) |
| `bin/kapi.py red "…"` | Increment'i her evrede kapatır |
| `bin/kapi.py talep "…"` · `onayla` | Elle adım adım (dongu bunları kendisi yapar) |
| `bin/kapi.py durum` | Evre, bekleyen onay, motorlar, sıradaki komut |
| `bin/uygulama.py [--port 8765]` | Salt-okur durum sayfası; yalnız 127.0.0.1, `GET /` |
| `bin/kos.py <takim> [--kuru] [--zorla]` | Takımı bir kez koşturur; `--kuru` motor çağırmaz; `--zorla` günlük tavanı atlar |
| `bin/bekci.py --dogrudan <takim> [kosu]` | Katman A'yı elle çalıştırır |
| `bin/sema.py <şema> <dosya>` | JSON dosyasını dondurulmuş şemaya karşı doğrular |
| `bin/ayar.py` | Tavanlar, evre, `.env` var mı |

## Kapsam dışı (şimdilik)

İşletme takımları (kod geliştirme, inceleme, araştırma, planlama), zamanlayıcı, Telegram tetiği,
çoklu-motor karşılaştırma. Hepsi `kapsam-disi.md`'de tarihli; etkileşim katmanı (`bin/uygulama.py`, sırası
`hedef.md`'de) işler hâle gelmeden hiçbiri yazılmaz. Eski içerik şirketi `icerik-sirketi-v1` etiketinde.

## Lisans

MIT — [LICENSE](LICENSE).
