# Debt 06/07/09–13 — TAM Spec ∥ Standards incelemesi

**Verdict: merge-ready**  
**Tarih:** 2026-09-16  
**Sabit nokta:** `e5d8e9338a751de726c9d8fde2afc33b77ebd311` (ticket-04 merge-ready)  
**İncelenen HEAD:** `e69a5a8fdd36dad812968dd42505360b07d73a2f`  
**Diff:** `git diff e5d8e93...e69a5a8`  
**Commitler:**
- `e69a5a8 debt: Ticket 06/07/09-13 kapatıldı — argv, tekrar, isim, bytes, kalıntı, except`

İki eksen ayrı, paralel ajanlarla incelendi; bulgular birleştirilip eksenler arasında sıralanmadı. Kod değiştirilmedi; yalnız bu rapor yazıldı. Çalışma ağacındaki `CONTEXT.md` değişikliği, untracked hafıza testleri ve diğer `.scratch/` log/CLI dosyaları bu commit’e mal edilmedi.

Uygulanan skill: `/workspace/mattpocock-skills/skills/engineering/code-review/SKILL.md`; companion `agents/openai.yaml` yalnız arayüz metadata'sı içeriyor. Yerel tracker `docs/agents/issue-tracker.md` uyarınca okundu. Gereksinim kaynakları: `issues/{06,07,09,10,11,12,13}-*.md`, `spec.md`, `SEAMS.md` (S2 bytes kanalı) ve `DEBT.md`. Standart kaynakları: `CLAUDE.md`, `ANAYASA.md`, `docs/agents/domain.md`, `CONTEXT.md`, ADR-0001–0005, codebase-design sözlüğü (module / interface / depth / seam / adapter / leverage / locality) ve skill'in Fowler smell baseline'ı.

H implement 01–04 zaten merge-ready; bu dilim debt. `spec.md` / `SEAMS.md` üç-nokta diff’te yeni dosya görünür çünkü `e5d8e93`’te henüz commit’li değillerdi; üretim davranışı scratch belgelerinin ilk commit’inden değil, motor/Sürücü/test hunk’larından okundu.

## Standards

**Eksen verdict'i: merge-ready. Engelleyici standart ihlali yok; bu dilimde yeni numaralı ST-D yok.** Türkçe adlandırma, stdlib, ağsız `unittest`, personel altında kod konumlandırma, Python ve modüler monolit kuralları korunuyor. Yeni public seam, saf çekirdeğe I/O veya korunan insan dosyalarında değişiklik yok. Tooling'in denetlediği biçim konuları bulgu sayılmadı. Biletler 06/12 şirket `komut`/`cozumle` “yeniden yazma” yasağını bu debt için ezer; 07/13 ortak test yardımcısını ister; 10 bytes belgesini speculative generality saymaz.

**Yargı kokusu (numaralanmadı; mevcut iz):** `SahteKosucu` hâlâ `tests/test_kart_motoru.py` ve `tests/test_surucu_motor.py` içinde kopya. Bu dilim yalnız `HataKosucu`’yu ortaklaştırdı (bilet 13). Kötüleşmedi. Mevcut takip: `.scratch/otomatik-motor-ch0001/issues/05-test-sahte-kosucu-tekrari.md`.

**Yargı kokusu (numaralanmadı):** `claude` / `agy` `cozumle` dict koruması aynı iki satır (`if not isinstance(veri, dict): return bozuk(...)`). grok zaten vardı; codex JSONL’de `continue`. Ticket 12 kaynağa düzeltmeyi istedi; ortak `json_nesne` çıkarmak biletin ötesidir. Adapter locality (dört CLI = iç Motor seam) repo baskın.

Shotgun Surgery değil: yedi debt tek commit’te kasıtlı dilim; her hunk kendi biletine bağlanıyor.

Olumlu kapsam: S1 — birincil interface `isi_ilerlet`; yeni public seam yok; `_sablon_doldur` / `_artefakt_yaz` public module değil. Depth / leverage: encode + kapı `SurucuAdim`’de; SahteMotor ve kart/CLI aynı yazıcıyı kullanır. 07/13: `tests/surucu_yolu.py` `dizin_bayt_haritasi` / `dizin_bayt_korumasini_dogrula` / `HataKosucu` — silme tam sözlükle yakalanır; iç OSError katmanı durur. 10: `str | bytes` spec/SEAMS S2 + docstring; içerik şeması yok. 11: `encode` diskten önce. 12: `except (TypeError, ValueError)`; `AttributeError` kaynakta kesildi. 06: `butce_usd is not None` — diğer motorların opsiyonel bayrak locality’si. CLAUDE.md Türkçe / stdlib / unittest / ağ yok / personel `bin`. ANAYASA §5 insan dosyası yok; ADR-0002/0003; ADR-0004 çekirdek I/O’suz; ADR-0005 iş sözleşmesi yok. CONTEXT terimleri duruyor.

## Spec

**Eksen verdict'i: merge-ready. Engelleyici veya yeni SP-D yok.** Yedi debt acceptance’ı kod + ağsız unittest ile duruyor; 01–04 regresyonu yok.

**(a) Eksik/kısmi:** yok.  
**(b) Kapsam şişmesi:** yok. Spec Out of Scope «Şirket Motor `komut`/`cozumle` iç mantığını yeniden yazmak» ticket 06 ve 12 ile ezilir; adapter değişimi creep değil.  
**(c) Yanlış uygulama:** yok. Encode fail’de `plan.md` yok; `"[]"` artık `cozumle` kaynağında `bozuk`; `kart_motoru` yalnız `TypeError`/`ValueError`.

**Ticket kanıtı**

- **06** «Yalnız model ayarında argv’de `--max-budget-usd None` yok»: `bin/motorlar/claude.py` `butce_usd is not None` iken bayrak ekler. `tests/test_motorlar.py::ClaudeTesti::test_butce_verilmezse_max_budget_usd_argvde_yok`. `butce_usd: 2` mevcut testte durur; `0` bayrağı korur (None ile karışmaz). CLI/ağ yok.
- **07** «tek ortak yardımcı… silinen şablon da kaçmaz»: `dizin_bayt_haritasi` tam `ad → bayt`; `SurucuAdimTesti` + `FabrikaMutluYolTesti` `dizin_bayt_korumasini_dogrula`. Yalnız kalan dosyayı dolaşmak yok. Üretim şablon/artefakt davranışı değişmedi.
- **09** «ya gerçek bayt yolunu ölçer ya da ad/yorum…»: `tests/test_surucu.py::test_basari_utf8_okunamayan_*` artık `SahteMotor(metin=b"\xff\xfe\x00\x00")` (birincil `isi_ilerlet`). `test_surucu_adim` yanıltıcı ad `test_basari_bos_metinde_eski_bozuk_dosyaya_dokunmadan_reddedilir_durum_korunur` oldu; gerçek UTF-8 red `test_gecersiz_utf8_bytes_reddedilir_durum_korunur` duruyor.
- **10** «ya bytes belgelenir ya da yalnız `str`»: belge seçildi. `spec.md` / `SEAMS.md` S2 + `SurucuAdim` docstring: üretim adaptörleri `str`; yazıcı ham `bytes` (yalnız test seam’inin geçersiz UTF-8 red yolu). `_artefakt_yaz(str | bytes)` + `write_bytes`. `motor_uret` hâlâ `tuple[Sinyal, str]`. Mutlu yol (02) yalnız `str`. İçerik şeması yok.
- **11** «boş `plan.md` kalıntısı yok… `park` değil»: `str.encode("utf-8")` `mkdir`/`write_bytes` öncesi; `UnicodeEncodeError` → red. Surrogate testleri (`test_surucu`, `test_surucu_adim`) `plan.md` yok, bitiş `planlaniyor`. Otomatik `hata` yok.
- **12** «`AttributeError` ya dar… `"[]"` yolu durur»: dict-guard `claude`/`agy`; codex JSONL’de dict olmayan satır `continue`; grok zaten korumalıydı. `kart_motoru` `except (TypeError, ValueError)`. `test_json_dizi_non_dict_cozumle_attributeerror_kacmadan_hata_doner` dört motor. `[]` / `"[]"` → `hata` → `park` (01–04 kilidi). `Exception` yok.
- **13** «tek ortak stub… `isi_ilerlet` kanıtı durur»: `tests/surucu_yolu.py::HataKosucu`. İç seam `test_kart_motoru::test_kosucu_oserror_hata_sinyali_doner` + birincil `test_surucu_motor::test_kosucu_oserror_motor_hatasi_olur_parkta_biter`. Katmanlar birleştirilmedi.

**01–04 regresyon:** yok. Sinyal `basari`/`hata`; birincil `isi_ilerlet`; `bos` → `park` + `plan.md`/`paket.md`; S3 Motor durumunda kalır; `hata` → `hata` → `park`; yeni public seam yok; `HafizaDeposu` bağlı değil; `kapi`/`dongu`/iskelet/kart/şablon bu dilimde yok. US 43/55: unittest subprocess/ağ açmıyor. Bilinen `test_kit` Bekçi kırmızısı suite-sagligi.

## Çalıştırılan testler ve karşılaştırma

Ortam: Python 3.13.5, Linux, uid 1000. Gerçek Motor/CLI veya ağ çağrısı kullanılmadı. Testlerin sahte koşucuları ve geçici dosyaları kullanıldı.

| Komut / çalışma bağlamı | Sonuç |
| --- | --- |
| `python3 -m unittest discover -s tests` — çalışma ağacı | **124 test, 1 failure**, yalnız bilinen Bekçi |
| Aynı discovery — `git archive e5d8e93` temiz kopya | **119 test, 1 failure**, aynı Bekçi |
| Aynı discovery — `git archive e69a5a8` temiz kopya | **121 test, 1 failure**, aynı Bekçi |
| `tests.test_motorlar` + `test_kart_motoru` + `test_surucu*` + çekirdek/durum — `e69a5a8` arşiv | **77/77 geçti** |

Temiz kopyalarda tam commit içeriği test edildi. Çalışma ağacındaki untracked hafıza testleri (`tests/test_hafiza_deposu.py`, 3 test) 124/121 farkını açıklar. `e69a5a8` iki test ekler: `test_butce_verilmezse_max_budget_usd_argvde_yok`, `test_json_dizi_non_dict_cozumle_attributeerror_kacmadan_hata_doner`. `test_kapi.py:29` dosya kapatma uyarıları önceden mevcut.

Bilinen kırmızı: `test_kit.BekciKatmanA.test_kosuda_anayasaya_dokunan_ajan_red`, `tests/test_kit.py:268`, `'tamam' != 'red'`. Sabit noktada da aynen oluştu. **Yeni regresyon değildir; verdict nedeni değildir.** Mevcut takip: `.scratch/suite-sagligi/issues/01-test-kit-bekci-kirmizi.md`.

### Debt kanıtları (`git archive` kopyalarında, çalışma ağacına kod yazılmadan)

| Senaryo | `e5d8e93` | `e69a5a8` |
| --- | --- | --- |
| Claude `komut(..., butce_usd=None)` | argv’de `--max-budget-usd` `None` | bayrak yok; `None` yok |
| `claude.cozumle("[]")` | `AttributeError: 'list' object has no attribute 'get'` (kart_motoru 04/05’te yakalıyordu) | `hata=True` (`bozuk`); AttributeError yok |
| Dört motor `cozumle("[]")` | — | hepsi `hata` |
| `isi_ilerlet(SahteMotor(metin="\ud800"))` | S3 red, boş `plan.md` kalıntısı (REVIEW-03 SP-D3) | S3 red; `plan.md` yok; bitiş `planlaniyor` |
| `isi_ilerlet(SahteMotor(metin=b"\xff\xfe\x00\x00"))` | — | S3 red; dosya o baytlar; bitiş `planlaniyor` |
| Mutlu yol `SahteMotor(metin="plan içeriği")` | `bos` → `park`; `plan.md` + `paket.md` | aynı |
| `basari` + boş metin | bitiş `planlaniyor`; `park` değil | aynı |
| `Sinyal.HATA` | `hata` → `park`; `plan.md` yok | aynı |
| Şablon silme yardımcısı | kalan dosyayı dolaşır, silineni kaçırır | tam sözlük; silinen ve eklenen yakalanır |

## Kapanış

Debt 06/07/09–13 birlikte **merge-ready**. Engelleyici madde yok. Bu incelemede yeni ticket açılmadı; yeni numaralı ST-D / SP-D yok. `SahteKosucu` tekrarı ve `test_kit` Bekçi kırmızısı önceden açık izlerdir, bu dilimde kötüleşmedi.

**Eksen özeti:** Standards: 0 engelleyici + 0 yeni debt, en ağır bulgu yargı düzeyinde mevcut `SahteKosucu` kopyası (bu dilimde değil); Spec: 0 engelleyici + 0 debt, en ağır bulgu yok.
