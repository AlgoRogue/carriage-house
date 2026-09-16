# Ticket 01 — Spec ∥ Standards review

**Verdict: merge-ready (yalnız ticket 01).**

İncelenen commit: `148052b9caedf6053133d3f6b085fe6d60208164`; parent: `f744eb0292ec28e9fcdc1c0a1c2838dee45b5e85`.
Diff: `git diff f744eb0...148052b`. HEAD incelenen commit ile aynı. Code-review skill’i ve companion metadata okundu; iki eksen bağımsız alt ajanlarla incelendi. Kod veya test değiştirilmedi.

Kaynaklar: ticket 01, `spec.md` (yalnız 01 kapsamı), `SEAMS.md` S1–S5; `CLAUDE.md`, `ANAYASA.md`, domain belgeleri ve ADR-0004/personel Sürücü README. Çalışma alanındaki önceden mevcut değişiklikler commit’e mal edilmedi.

## Spec — pass

- `surucu_cekirdek.py:6–12,85–94` kapalı Sinyal sözlüğünü `basari`/`hata` yapıyor. Üretim Python kodunda eski sinyal dizgileri kalmamış. `son_sinyal` yeni değerlerle yazılıyor; Motor dışı geçişlerde mevcut `None` davranışı korunuyor. İskeletin `hata` durumu ayrı kavram olarak duruyor.
- `sahte_motor.py:14–28` ve `kart_motoru.py:31–44`, `motor(girdi) -> (Sinyal, metin)` interface’ini karşılıyor. `surucu_adim.py:23` içerik kanalını ayırıyor; metin sonraki durumu seçmiyor.
- `isi_ilerlet(motor, …)` ve Motor enjeksiyonu korunmuş. Yeni durum makinesi veya ürün seam’i yok; ince kart girişi belgelenmiş fabrika + `isi_ilerlet` rolünde. Çekirdek saf kalmış.
- Ticket’ın “girdi … geçici olarak durum adı kalabilir” izni uygulanmış. Prompt doldurma, İş artefaktı ve başarı kapısı eklenmemiş; S2–S4 henüz bu ticket’ın acceptance’ı değil. Mevcut hata yolunu yeni sözlükle çalıştırmak 04’ün artefakt kapısı davranışını erkenden kurmak anlamına gelmiyor. 02–04 kapsamına taşma saptanmadı.

**Engelleyici Spec bulgusu: 0.**

## Standards — pass

Türkçe domain adları, stdlib/unittest, personel-kapsamlı yerleşim, saf çekirdek ve şirket `motorlar` kaydının yeniden kullanımı korunmuş. Birincil seam `isi_ilerlet`; iki adapter mevcut iç seam’i kullanıyor. `karti_ilerlet` delegasyonu belgelenmiş rol olduğundan Middle Man sayılmadı. G8 import borcu kapsam dışında.

**Engelleyici olmayan Fowler notu — olası Duplicated Code:** `tests/test_kart_motoru.py:43–52` ve `tests/test_surucu_motor.py:29–36` aynı `SahteKosucu` mantığını yineliyor: `self.cagrilar.append(list(komut)); return self.stdout`. Ortak test yardımcısı locality sağlayabilir. Bu bir yargı; sert standart ihlali değil. SEAMS zaten `05-test-sahte-kosucu-tekrari` borcunu anıyor; yeni regresyon veya merge engeli sayılmadı.

**Engelleyici Standards bulgusu: 0; engelleyici olmayan smell: 1.**

## Doğrulama ve kapsam sınırları

- İlgili altı test modülü: **38/38 geçti** (`test_kart_motoru`, `test_surucu`, `test_surucu_adim`, `test_surucu_cekirdek`, `test_surucu_durum`, `test_surucu_motor`).
- `python3 -m unittest discover -s tests`: **95 test, 1 bilinen failure**. Commit’te izlenen test dosyalarıyla ayrıca **92 test, aynı tek failure** doğrulandı. Fark çalışma alanındaki commit dışı testlerden geliyor.
- Tek failure: `test_kit.BekciKatmanA.test_kosuda_anayasaya_dokunan_ajan_red`, beklenen `red`, gerçekleşen `tamam`. Kullanıcının belirttiği önceden kırmızı Bekçi borcudur; **yeni regresyon sayılmadı**.
- **04’e not:** Sahte koşucu `[]` stdout verdiğinde Claude/agy/codex çözümleyicilerinden `AttributeError` kaçıyor; `kart_motoru.py:37–40` yalnız `TypeError`/`ValueError` yakalıyor. Ağsız doğrulandı. Ticket 04’ün “bozuk stdout, cozumle hatası … Sürücü döngüsü patlamaz” işi kapsamında ele alınmalı; 01’in ertelenmiş acceptance’ı olarak kullanılmadı.
- **CLI entegrasyon sınırı:** `kart_motoru.py:29–32` yalnız model ayarı verdiğinde mevcut Claude komut üreticisi `--max-budget-usd None` oluşturuyor; argv sahte koşucuyla doğrulandı. Gerçek CLI çalıştırılmadı, kabul/red davranışı doğrulanmadı. Önceki Motor spec’i model dışı ayarların boş/None kalmasına izin veriyor; güncel spec şirket maliyet tavanı kopyasını dışlıyor. Bu nedenle ANAYASA tavanını CH-0001’e dayatan bir standart ihlali veya bu prefactor için merge engeli sayılmadı. Gerçek CLI uyumluluğu bu testlerin kanıtladığı bir sonuç değildir.

## Net verdict — merge-ready

- Ticket 01’in sözlük ve callable prefactor acceptance’ı karşılanıyor.
- İki eksende de zorunlu düzeltme yok; tekrarlı test adapter’ı engelleyici olmayan mevcut borç.
- Bilinen Bekçi kırmızısı hariç yeni test regresyonu yok. Bu verdict 02–04’ün tamamlandığı veya gerçek CLI entegrasyonunun doğrulandığı anlamına gelmez.

**Eksen özeti:** Spec: 0 bulgu; Standards: 1 engelleyici olmayan Duplicated Code notu, 0 sert ihlal.
