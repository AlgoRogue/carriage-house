# Hedef — A Şirketi ne için var

> SoT. İnsanındır; ajan okur, değiştirmez. Sözleşme bu dosyayla çelişemez.

## Amaç
Farklı yapay zekâ CLI'larını (claude, agy, codex, grok) **tek bir deterministik üst katmandan** yönetmek.
Yük icra değil: belirsiz fikri tek doğrulanabilir adıma indirmek, kararı dondurmak, kapsamı kilitlemek,
yayın düğmesini insanda tutmak. Dört motora da ödeme yapılıyor; boşta kalan kapasite sözleşmeye bağlı
motor seçimiyle doldurulur — rastgele değil, Kapı 1'de kilitlenerek.

## En pahalı arıza
İlerleme kaybı ve "sistemi yine insanın taşıması". İnsan hâlâ şunları taşıyorsa sistem yanlış kurulmuştur:
- "Şimdi hangi takımı kuruyoruz?"
- "Bu dosya SoT mi?"
- "Sıradaki increment ne, hangisi kapsam dışı?"
- "Çıktıyı diğer CLI'ye ben mi yapıştırayım?"

## Kadro (üç kilit, üç bakanlık değil)
| Takım | Varoluş amacı | Motor |
|---|---|---|
| `sistem-sevk` | Bir sonraki çalışan increment'i dondurulmuş sözleşmeye çevirir; evreyi ve SoT'u korur | claude |
| `sistem-insaat` | Onaylı sözleşmeyi koda işler; başka ürün yazmaz | sözleşmeden (codex varsayılan; agy, grok, istisnai claude) |
| `sistem-bekci` | Increment'in sözleşme kadar çalıştığını PASS/FAIL eder; yamamaz | üretenin tersi |

İnsan: sistemin amacı, increment seçimi, Kapı 1 (sözleşme), Kapı 2 (yayın).

## Bitiş çizgisi (increment 0'ın kabul kriteri)
`kapi.py talep → kos.py sistem-sevk → kapi.py onayla → kos.py sistem-insaat → kos.py sistem-bekci → kapi.py yayinla`
zinciri **bir kez uçtan uca** işler: sözleşme şemaya uyar, inşaat sözleşme dışına çıkmaz, bekçi kanıtla PASS
verir, `kararlar.md`'ye satır düşer. Bu çizgi geçilmeden işletme takımı, otomatik zincir, zamanlayıcı ve
yönetim uygulaması yazılmaz (bkz. `kapsam-disi.md`).

## Sonrası (kadro tanımı değil, increment konusu) — sıra önemli

**1. Etkileşim katmanı — önce bu.** İnsan sistemle terminalden değil bir uygulamadan etkileşir; uygulamayı
sistemin kendisi inşa eder. Çerçeve `toplantilar/2026-09-14-etkilesim-katmani/` toplantısında (agy, codex,
grok) kilitlendi:
- Uygulama ikinci bir sistem değil, `evre.json` + `increment/<id>/` artefaktlarının **insan yüzü**dür. Kendi
  durumu, kuyruğu, evresi yoktur; her istekte dosyaları okur. Kapı mutasyonları `bin/kapi.py` alt süreç,
  koşu `bin/kos.py <takim>` alt süreç; takım evreden türer, insan seçmez. Bir basış = bir koşu, bitince durur.
- stdlib Python (`http.server`) + sunucu tarafı HTML + polling; bağımlılık yok. Önce `127.0.0.1`; uzak erişim
  ve kimlik ayrı increment.
- Kalıcı sınırlar: LLM çağırmaz, sohbet yüzeyi yok, takım seçici yok, otomatik zincir yok, dosya/SoT düzenleme
  yok, commit/push yok, GET yazmaz.
- Increment sırası: (1) salt-okur durum sayfası → (2) `talep` + `red` → (3) Kapı 1 (`onayla`, motor seçimi,
  teyit) → (4) `POST /kos` + Kapı 2 → (5) uzak erişim + kimlik.

**2. Sonra.** İşletme takımları (`is_tipi`: kod geliştirme, kod inceleme, araştırma/yazı, planlama), otomatik
zincir, kuyruk/dosya tetiği, Telegram tetiği, zamanlanmış sabah/akşam koşusu, aynı işi birden fazla motora
verip karşılaştırma. Etkileşim katmanı işler hâle gelmeden bunlara bakılmaz. Her biri `sistem-sevk`in
keseceği ayrı bir increment'tir.
