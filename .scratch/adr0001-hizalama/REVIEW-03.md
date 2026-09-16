# Ticket 03 + Debt 08 — TAM Spec ∥ Standards incelemesi (fix sonrası)

**Verdict: merge-ready**  
**Tarih:** 2026-09-16  
**Sabit nokta:** `d005e81c53e4f8f58d4f62abd426256c3d0663ba`  
**İncelenen HEAD:** `ee194aa252288d0c31f44aafd2107722d5ed3efa` (`758ae5b` + fix)  
**Diff:** `git diff d005e81...ee194aa`  
**Commitler:**
- `758ae5b ticket-03: Kapı reddi: basari ama kabul edilemez İş artefaktı (boş/yok/UTF-8/IO)`
- `ee194aa fix(ticket-03): REVIEW-03 düzeltmesi — SP-1, SP-2, SP-D1, ST-D1`

İki eksen ayrı, paralel ajanlarla incelendi; bulgular birleştirilip eksenler arasında sıralanmadı. Ana inceleme birincil seam üzerinden önceki REVIEW-03 senaryolarını ve sabit nokta karşılaştırmasını yeniden çalıştırdı. Kod değiştirilmedi; yalnız bu rapor üzerine yazıldı.

Uygulanan skill: `/workspace/mattpocock-skills/skills/engineering/code-review/SKILL.md`; companion `agents/openai.yaml` yalnız arayüz metadata'sı içeriyor. Yerel tracker `docs/agents/issue-tracker.md` uyarınca okundu. Gereksinim kaynakları: `issues/03-kapi-reddi-bos-artefakt.md`, birlikte ele alınan `issues/08-artefakt-io-hata-belge.md`, `spec.md` ve `SEAMS.md` (özellikle S1–S4). Standart kaynakları: `CLAUDE.md`, `ANAYASA.md`, `docs/agents/domain.md`, `CONTEXT.md`, ADR-0001–0005 ve skill'in Fowler smell baseline'ı.

Önceki REVIEW-03 (`758ae5b` vs `d005e81`) **needs-fix** demişti: SP-1 ve SP-2 engelleyici, SP-D1 ve ST-D1 debt. Bu tur o iddiaları `ee194aa` üzerinde doğruladı; dördü de kapanmış.

## Standards

**Eksen verdict'i: merge-ready. Engelleyici standart ihlali yok; önceki ST-D1 kapanmış.** Türkçe adlandırma, stdlib, ağsız `unittest`, personel altında kod konumlandırma, Python ve modüler monolit kuralları korunuyor. Yeni public seam, saf çekirdeğe I/O veya korunan insan dosyalarında değişiklik yok. Tooling'in denetlediği biçim konuları bulgu sayılmadı.

**ST-D1 — kapanmış (önceki olası Duplicated Code).** `758ae5b` içindeki iki `try` / `mkdir` / `write_*` / `except OSError` dalı `ee194aa` ile tek I/O sınırında birleşti (`personel/CH-0001/bin/surucu_adim.py`, `_artefakt_yaz`). Tür ayrımı yalnız `write_bytes` / `write_text` çağrısında; `except (OSError, UnicodeError)` ortak. Önceki incelemedeki yinelenen yazma-hata şekli yok.

**ST-D2 — Engelleyici olmayan debt adayı: olası Mysterious Name (yargı).** `tests/test_surucu.py` `test_basari_utf8_okunamayan_artefaktta_ilerlemez_motor_durumunda_kalir` ve `tests/test_surucu_adim.py` `test_basari_utf8_okunamayan_artefaktta_reddedilir_durum_korunur` bozuk dosya yazıp `SahteMotor(metin="")` çağırıyor. SP-1 sonrası boş metin yazmadan reddedildiği için UTF-8 okuma yolu çalışmıyor; ad/yorum okunamayan artefaktı ima ediyor. Gerçek bayt yolu `test_gecersiz_utf8_bytes_reddedilir_durum_korunur`. Bu, skill baseline'ından gelen bakım değerlendirmesidir; belgelenmiş zorunlu standart ihlali değildir.

Olumlu kapsam: `CLAUDE.md` Türkçe adlandırma / stdlib / ağsız unittest / kod `personel/CH-0001/bin/` altında. `ANAYASA.md` §5 insan dosyalarına dokunulmamış. S1 / ADR-0004: yeni public seam yok; `surucu_cekirdek` I/O'suz. Terimler `CONTEXT.md` ile uyumlu. `str | bytes` Primitive Obsession sayılmaz: dilim içerik şeması istemiyor.

## Spec

**Eksen verdict'i: merge-ready. Önceki SP-1 ve SP-2 `isi_ilerlet` birincil seam'inde `ee194aa`'da gerçekten düzelmiş; yeni spec regresyonu yok.**

**SP-1 (önceki engelleyici) — düzeldi.** Konum: `personel/CH-0001/bin/surucu_adim.py` `_artefakt_yaz`. Ticket 03 / S3: «`basari` + boş veya yok … geçiş yok, … `park` değil»; spec'te eski dosya yeniden kullanım sözleşmesi yok. SEAMS:140: «`basari` ise `metin`'i artefakt yoluna yazar»; boş/bozuk artefaktta ilerlemez. `758ae5b`'deki `elif yol.exists(): pass` kalkmış; boş/whitespace hemen `False`. Probe ve regresyon testleri: eski `plan.md`+`paket.md` + `SahteMotor(metin="")` → bitiş `planlaniyor`; eski paket + yeni plan + boş delege → `delege_hazirlaniyor`; whitespace eski dosyayı başarıya çevirmiyor.

**SP-2 (önceki engelleyici) — düzeldi.** Debt 08: «`mkdir`/`write_text` IO birincil seam'den kaçmaz». Spec:96/S3: «geçiş yok, döngü durur, durum Motor durumunda kalır.» `exists()` try dışında değil; mkdir/yaz/oku `(OSError, UnicodeError)` içinde. Probe: iş dizini `chmod(0)` + boş veya dolu metin PermissionError kaçırmıyor, bitiş `planlaniyor`. `NotADirectoryError` (`isler_kok` dosya) aynı şekilde tanımlı red.

**SP-D1 (d005e81'de de vardı) — düzeldi.** Motor `"\ud800"` artık `UnicodeEncodeError` kaçırmıyor; S3 reddi, bitiş `planlaniyor`. `except (OSError, UnicodeError)` kodlama hatasını tanımlı redde çeviriyor.

Engelleyici yeni açık yok.

**SP-D2 — Engelleyici olmayan debt adayı: bytes içerik kanalı (kapsam).** `_artefakt_yaz(..., metin: str | bytes)` + `write_bytes`. SEAMS S2: `motor(girdi: str) -> (Sinyal, metin)`; Sürücü `metin`'i İş artefaktı yazar. Bytes kanalı spec'te yok. Probe: geçerli UTF-8 bytes `bos`→`park`. Ticket 03'ün UTF-8 okunamayan reddi bu yolla kanıtlanıyor; mutlu yolu bozmuyor. Merge engeli değil.

**SP-D3 — Engelleyici olmayan debt adayı: encode başarısızlığında boş dosya kalıntısı.** Surrogate yazımı `write_text` dosyayı önce açtığı için boş `plan.md` bırakıyor; geçiş yine reddediliyor (S3). Spec silme istemiyor. Ayrıca birincil-seam «UTF-8 okunamayan» adlı test boş Motor ile decode'u ölçmüyor (ST-D2 ile aynı zayıf test); kapı yine yazım-sonrası `read_text` yapıyor ve geçersiz bytes reddi ayrı testte duruyor.

Olumlu kapsam: Ticket 03 / S3 / US 21–22: boş, yok, IO, delege boş → Motor durumunda durur, otomatik `hata` yok, `park` değil. US 23: `hata` artefakt kapısını açmaz. S4 / spec:131: varlık + UTF-8 + boş değil, şema yok (serbest Türkçe/emoji metin `park`). Debt 08 docstring + `NotADirectoryError`. Mutlu yol (02) duruyor. Yeni public seam yok (S1). İçerik şeması icat edilmemiş.

## Çalıştırılan testler ve karşılaştırma

Ortam: Python 3.13.5, Linux, uid 1000. Gerçek Motor/CLI veya ağ çağrısı kullanılmadı. Testlerin sahte koşucuları ve geçici dosyaları kullanıldı.

| Komut / çalışma bağlamı | Sonuç |
| --- | --- |
| `python3 -m unittest discover -s tests -p 'test_surucu*.py' -v` — çalışma ağacı | **51/51 geçti**; Sürücü, çekirdek, depo, adım ve kart/CLI bağlı giriş |
| `python3 -m unittest discover -s tests` — çalışma ağacı | **113 test, 1 failure**, yalnız bilinen Bekçi |
| Aynı discovery — `git archive d005e81` ile temiz geçici kopya | **95 test, 1 failure**, aynı Bekçi |
| Aynı discovery — `git archive 758ae5b` ile temiz geçici kopya | **101 test, 1 failure**, aynı Bekçi |
| Aynı discovery — `git archive ee194aa` ile temiz geçici kopya | **110 test, 1 failure**, aynı Bekçi |

Temiz kopyalarda tam commit içeriği test edildi; kullanıcı çalışma ağacındaki untracked hafıza testleri (`tests/test_hafiza_deposu.py`, 3 test) 113/110 farkını açıklıyor. `758ae5b` altı, `ee194aa` dokuz regresyon testi ekliyor. `test_kapi.py:29` dosya kapatma uyarıları önceden mevcut.

Bilinen kırmızı: `test_kit.BekciKatmanA.test_kosuda_anayasaya_dokunan_ajan_red`, `tests/test_kit.py:268`, `'tamam' != 'red'`. Sabit noktada da aynen oluştu. **Yeni regresyon değildir; verdict nedeni değildir.** Mevcut takip: `.scratch/suite-sagligi/issues/01-test-kit-bekci-kirmizi.md`.

### Birincil seam ek kanıtları

Aşağıdaki karşılaştırmada aynı `isi_ilerlet` ve geçici dosya düzeni üç `git archive` kopyasında çalıştırıldı. Çalışma ağacına kod/test yazılmadı.

| Senaryo | `d005e81` | `758ae5b` | `ee194aa` |
| --- | --- | --- | --- |
| Eski dolu plan + paket, Motor çıktısı boş | Normal red: `planlaniyor` | **Yanlış kabul: `park`** | Normal red: `planlaniyor` |
| Eski paket, yeni plan çıktısı, boş delege çıktısı | Normal red: `delege_hazirlaniyor` | **Yanlış kabul: `park`** | Normal red: `delege_hazirlaniyor` |
| İş dizini `chmod(0)`, Motor çıktısı boş | Normal red: `planlaniyor` | **`PermissionError`** | Normal red: `planlaniyor` |
| Motor çıktısı `"\ud800"` | `UnicodeEncodeError` | `UnicodeEncodeError` | Normal red: `planlaniyor` |

Hedefte ayrıca: whitespace + eski dosya → `planlaniyor`; `NotADirectoryError` (`isler_kok` dosya) → `planlaniyor`; `plan.md` dizin (`IsADirectoryError`) → `planlaniyor`; hedef dosya `chmod(0)` + dolu metin → `planlaniyor` (istisna kaçmaz); geçersiz UTF-8 bytes → `planlaniyor`; geçerli UTF-8 bytes ve şemasız Türkçe/emoji metin → `park`. Surrogate reddinde boş `plan.md` kalıntısı SP-D3; geçiş yine yok.

SP-1/SP-2 kapanışı artık commit'lenmiş `isi_ilerlet` regresyon testleriyle korunuyor (`test_eski_dolu_artefakt_varken_bos_motor_ciktisi_reddedilir_planlaniyor_kalir`, `test_eski_paket_varken_yeni_plan_ve_bos_delege_delege_durumunda_kalir`, `test_eski_artefakt_varken_whitespace_motor_ciktisi_reddedilir`, `test_is_dizini_chmod_0_permission_error_seamden_kacmaz_reddedilir`).

## Kapanış

Önceki REVIEW-03 kapanış koşulu (SP-1 ve SP-2'nin `isi_ilerlet` regresyon testleriyle korunması) `ee194aa`'da karşılanmış. Ticket 03 + Debt 08 birlikte **merge-ready**. ST-D2, SP-D2 ve SP-D3 engelleyici olmayan debt adaylarıdır; bu incelemede yeni ticket açılmadı. Bilinen Bekçi failure'ı ayrı takip edilmelidir.

**Eksen özeti:** Standards: 0 engelleyici + 1 debt (ST-D1 kapalı), en ağır bulgu bakım düzeyinde olası Mysterious Name (yanlış adlı UTF-8 testi); Spec: 0 engelleyici + 2 debt (SP-1/SP-2/SP-D1 kapalı), en ağır bulgu spec'te olmayan bytes içerik kanalı.
