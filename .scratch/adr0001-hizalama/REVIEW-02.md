# REVIEW-02 — Tam Spec ∥ Standards incelemesi

**Verdict: merge-ready** — yalnız Ticket 02 kapsamı için. Engelleyici bulgu yok; aşağıdaki iki engelleyici olmayan bulgu debt adayıdır. Bu rapor önceki dar REVIEW-02'nin yerini alır. Tüm hizalama spec'inin tamamlandığı anlamına gelmez; 03/04 açık kalır.

- Tarih: 2026-09-16.
- Sabit nokta: `148052b9caedf6053133d3f6b085fe6d60208164`.
- İncelenen / HEAD: `d005e81c53e4f8f58d4f62abd426256c3d0663ba`.
- Diff: `git diff 148052b...d005e81` (9 dosya, +330/−104).
- Commit: `d005e81 ticket-02: Sürücü şablon doldurur, İş artefaktı yazar (mutlu yol)`.
- Sözleşme: `issues/02-sablon-artefakt-mutlu-yol.md`, `spec.md` içindeki 02 kapsamı, `SEAMS.md` S1–S5. 03/04 ticket'ları kapsam ayrımı için okundu.
- Yöntem: `/workspace/mattpocock-skills/skills/engineering/code-review/SKILL.md` uygulandı; companion `agents/openai.yaml` okundu (yalnız arayüz metadatası). Spec ve Standards bağımsız, paralel alt ajanlarda incelendi; aşağıda eksenler ayrı tutuldu.
- Repo kaynakları: `CLAUDE.md`, `ANAYASA.md`, SoT dosyaları, `CONTEXT.md`, `docs/agents/{domain,issue-tracker}.md`, ADR-0001–0005, personel kuralları ve Sürücü README. Çalışma ağacındaki mevcut izlenmeyen ADR/spec belgeleri kullanıcı tarafından verilen bağlam olarak okundu; kod karşılaştırmasına dahil edilmedi. G3 belge güncellemesi ve G8 import borcu bu ticket'a yüklenmedi.

## Standards

**Sonuç: engelleyici belgelenmiş standart ihlali yok.**

**ST-D1 — Engelleyici değil; debt adayı: possible Duplicated Code.** Bu bir Fowler sezgisidir, zorunlu kural ihlali değildir. `tests/test_surucu_adim.py:23–29` ile `tests/test_surucu_motor.py:57–59,70–71` aynı şablon değişmezliği kontrolünü tekrarlar:

```python
self.sablon_once = {
    yol.name: yol.read_bytes() for yol in self.sablon_kok.iterdir()}
# ...
for yol in self.sablon_kok.iterdir():
    self.assertEqual(yol.read_bytes(), self.sablon_once[yol.name])
```

Koruma kuralı değiştiğinde iki sınıf birlikte güncellenmek zorunda. Ayrıca iki kopya da yalnız test sonunda mevcut dosyaları dolaştığından silinen şablonu denetlemez. Ortak bir test yardımcısında önce/sonra dosya adı→bayt haritalarını karşılaştırmak hem tekrarı hem kanıt boşluğunu kaldırabilir. Ürünün şablon sildiği gösterilmedi; merge engeli değildir.

`CLAUDE.md` Türkçe adlandırma/stdlib/personel kapsamı, `ANAYASA.md` insan dosyası sınırı, domain dili ve ADR sorumluluklarıyla yeni çatışma saptanmadı. Saf çekirdek I/O almıyor; ayrı servis, public şablon/depo module'ü veya şirket Motor adaptörü kopyası eklenmemiş.

Fowler taraması: Duplicated Code yukarıda. Mysterious Name, Feature Envy, Data Clumps, Primitive Obsession, Repeated Switches, Shotgun Surgery, Divergent Change, Speculative Generality, Message Chains ve Refused Bequest için yeterince güçlü yeni bulgu yok. Middle Man adayı `karti_ilerlet`, repo sözleşmesinin açıkça koruduğu ince giriş olduğundan bastırıldı. Repo kuralları baseline'a üstün tutuldu; tooling tarafından denetlenen biçim konuları bulgu yapılmadı.

## Spec

**Sonuç: Ticket 02 için engelleyici eksik, yanlış uygulama veya kapsam genişlemesi yok.**

**SP-D1 — Engelleyici değil; debt adayı: uygulanandan geniş hata yönetimi iddiası.** `personel/CH-0001/bin/surucu_adim.py:19–20`, “Artefakt boş/yazılamazsa geçiş reddedilir” diyor; Ticket 02 uygulama notu da bunu yineliyor. Ancak aynı dosyada `71–72` üzerindeki `mkdir/write_text` istisnaları yakalanmıyor. Birincil seam'de geçici `isler_kok` konumuna dizin yerine dosya koyup dolu içerikle `isi_ilerlet` çağrıldığında sonuç yerine `NotADirectoryError` kaçıyor; kalıcı durum `planlaniyor` kalıyor.

Spec S3: “geçiş yok, döngü durur, durum Motor durumunda kalır.” Kabul edilemez artefaktın tam reddi açıkça Ticket 03'ün işi; 02 mutlu yolunu engellemez. Açıklamaların tamamlanmış davranışı abartması debt adayıdır; 03'te uygulama ve belge birlikte hizalanmalı. UTF-8/IO reddi tamamlanmış sayılmamalı.

02 kapsamındaki kanıtlar:

- `tests/test_surucu.py:18`: birincil `isi_ilerlet` üzerinden tek çağrıda `bos → park`, iki Motor çağrısı, iki UTF-8 artefakt ve doldurulmuş yollar; ikinci istemde plan metni yok.
- `tests/test_surucu_motor.py:73`: fabrika Motor'u aynı girişe bağlı; koşucunun CLI `-p` yükünde doldurulmuş yollar, diskte içerik. İnce kart girişi ayrıca sınanıyor.
- `surucu_adim.py:60–65`: durum başına ayrı şablon seçimi/doldurma Sürücü içinde. İlk şablonda yalnız yazma yolu; ikincide plan okuma ve paket yazma yolları. Kimlik, skill, hafıza ve Defter gömülmüyor.
- S1: `isi_ilerlet` birincil seam; yeni public module yok. S2: içerik kanalını Sürücü yazıyor. S4: `isler/<is_id>/{plan,paket}.md`. S5: mevcut `basari`/`hata` sözlüğü korunuyor. S3'ün basit boş içerik reddi mevcut; tam kapı matrisi 03'e ait.
- Testlerde artefakt kökü geçici dizine enjekte. Ürün durum/kart/iskelet/şablon bayt kontrolleri mevcut; şablon silinmesi kanıtının sınırlılığı ST-D1'de. Hafıza importu/silmesi, şirket `kos/dongu/kapi` değişikliği veya park sonrası akış eklenmemiş.

## Çalıştırılan doğrulamalar

| Ortam / komut | Sonuç |
|---|---|
| Çalışma ağacı: `python3 -m unittest discover -s tests -p 'test_surucu*.py'` | 36 test, OK |
| Çalışma ağacı: `python3 -m unittest tests.test_kart_motoru` | 5 test, OK |
| Çalışma ağacı: `python3 -m unittest discover -s tests` | 98 test, 97 geçti; yalnız bilinen Bekçi kırmızısı |
| `d005e81` temiz `git archive` kopyası: `python3 -m unittest discover -s tests` | 95 test, 94 geçti; aynı tek Bekçi kırmızısı |
| `148052b` temiz `git archive` kopyası: `python3 -m unittest discover -s tests -p 'test_kit.py'` | 23 test, 22 geçti; aynı Bekçi kırmızısı |
| Geçici dizinde dolu içerik + dosya olan artefakt köküyle `isi_ilerlet` | `NotADirectoryError`; kalıcı durum `planlaniyor` — SP-D1 doğrulandı |

Bilinen kırmızı: `test_kit.BekciKatmanA.test_kosuda_anayasaya_dokunan_ajan_red`, `AssertionError: 'tamam' != 'red'`. Sabit noktada da yeniden üretildi; yeni regresyon değildir. Çalışma ağacındaki 3 ek test izlenmeyen `test_hafiza_deposu.py` dosyasından gelir; commit'e ait test sayısı ayrıca temiz arşivde doğrulandı. `test_kapi.py:29` ResourceWarning çıktıları diff dışında ve verdict'e yeni bulgu olarak eklenmedi.

Başlangıçta baseline testini tek modül adıyla çağırma denemesi `test_sema` import yolu nedeniyle yüklenemedi; yukarıdaki discovery komutuyla yeniden çalıştırıldı. Bu ilk çağrı ürün hatası olarak değerlendirilmedi.

Testler gerçek Motor/ağ çağrısı olmadan çalıştırıldı. Kod değiştirilmedi; yalnız bu rapor yeniden yazıldı. Debt adayları burada kaydedildi, ayrı ticket açılmadı. 04/05'teki bozuk stdout ve 06'daki bütçe argv borçları bu diff'in yeni regresyonu sayılmadı.

**Eksen özeti:** Standards: 1 engelleyici olmayan bulgu; en önemli konu tekrarlanan ve silinmeyi kaçıran şablon test koruması. Spec: 1 engelleyici olmayan bulgu; en önemli konu Ticket 03 davranışının açıklamalarda erken tamamlanmış gösterilmesi. Her iki eksende engelleyici: 0.
