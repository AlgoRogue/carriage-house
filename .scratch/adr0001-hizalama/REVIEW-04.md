# Ticket 04 + Debt 05 — TAM Spec ∥ Standards incelemesi

**Verdict: merge-ready**  
**Tarih:** 2026-09-16  
**Sabit nokta:** `ee194aa252288d0c31f44aafd2107722d5ed3efa`  
**İncelenen HEAD:** `e5d8e9338a751de726c9d8fde2afc33b77ebd311`  
**Diff:** `git diff ee194aa...e5d8e93`  
**Commitler:**
- `e5d8e93 ticket-04: Hata Sinyali: iskelet hata yolu, kapı açılmaz (+ Debt 05)`

İki eksen ayrı, paralel ajanlarla incelendi; bulgular birleştirilip eksenler arasında sıralanmadı. Kod değiştirilmedi; yalnız bu rapor yazıldı. Çalışma ağacındaki `CONTEXT.md` değişikliği, untracked hafıza testleri ve diğer `.scratch/` dosyaları bu commit’e mal edilmedi.

Uygulanan skill: `/workspace/mattpocock-skills/skills/engineering/code-review/SKILL.md`; companion `agents/openai.yaml` yalnız arayüz metadata'sı içeriyor. Yerel tracker `docs/agents/issue-tracker.md` uyarınca okundu. Gereksinim kaynakları: `issues/04-hata-sinyali-iskelet-yolu.md`, birlikte ele alınan `issues/05-bos-stdout-attributeerror.md`, `spec.md` (özellikle US 19–24, 40, 43, 55) ve `SEAMS.md` (S1–S5, davranış 3). Standart kaynakları: `CLAUDE.md`, `ANAYASA.md`, `docs/agents/domain.md`, `CONTEXT.md`, ADR-0001–0005 ve skill'in Fowler smell baseline'ı.

Üretim farkı bir satır: `personel/CH-0001/bin/kart_motoru.py` içinde `cozumle` yakalaması `(TypeError, ValueError, AttributeError)`. İskelet `hata` → `park` yolu 01–03’te duruyordu; bu dilim onu birincil seam testleriyle kilitler ve Debt 05’i kapatır.

## Standards

**Eksen verdict'i: merge-ready. Engelleyici standart ihlali yok; iki yargı debt’i var.** Türkçe adlandırma, stdlib, ağsız `unittest`, personel altında kod konumlandırma, Python ve modüler monolit kuralları korunuyor. Yeni public seam, saf çekirdeğe I/O veya korunan insan dosyalarında değişiklik yok. Tooling'in denetlediği biçim konuları bulgu sayılmadı.

**ST-D1 — Engelleyici olmayan debt (yargı; spec baskın): geniş `except AttributeError`.** `personel/CH-0001/bin/kart_motoru.py:39`: `except (TypeError, ValueError, AttributeError)` yalnız `modul.cozumle(stdout)` çevresinde. Fowler: gerçek adapter bug’ını gizleyebilir. Repo: ticket 04 / Debt 05 / spec «bozuk stdout, `cozumle` hatası → hata Sinyali; döngü patlamaz». `Exception` değil; yakalama yeri doğru. Spec kazanır; merge engeli değil.

**ST-D2 — Engelleyici olmayan debt (yargı): Duplicated Code (`HataKosucu`).** Yeni `tests/test_kart_motoru.py:196–201` iç-seam OSError stub’ı, mevcut `tests/test_surucu_motor.py:167–173` birincil-seam `HataKosucu` ile aynı şekil. SEAMS: iç OSError testi *olabilir*; birincil kanıt `isi_ilerlet`. İki katman kasıtlı; stub kopyası debt. Engelleyici değil.

SahteKosucu tekrarı (REVIEW-01) bu diff’te üçüncü kopya eklemedi; kötüleşmedi.

Shotgun Surgery değil: üretim 1 satır; dört test dosyası SEAMS «birincil `isi_ilerlet` + iç seam MAY» düzeni (repo baskın).

Olumlu kapsam: Türkçe adlar (`HataKosucu`, `bozuk_cikti`); stdlib/`unittest`; ağ yok (`subprocess` patch); kod `personel/CH-0001/bin/`; `.env` yok; ANAYASA §5 insan dosyalarına dokunulmamış; ADR-0002 Python; ADR-0003 yeni process yok; ADR-0004 çekirdek I/O’suz, `kart_motoru` fabrika; S1 yeni public seam yok; ADR-0005 iş sözleşmesi icat edilmedi; CONTEXT terimleri (Sinyal, Motor, İş artefaktı) duruyor; reddedilen `motor_ciktisi` yok.

## Spec

**Eksen verdict'i: merge-ready. Engelleyici veya debt bulgusu yok.** Ticket 04 + Debt 05 acceptance’ı birincil seam’de (`isi_ilerlet`) SahteMotor ve kart/CLI + sahte koşucu ile kilitli.

**`son_sinyal`:** Ticket «`son_sinyal` yeni sözlük». Park kaydı `None`. Bu eksik/yanlış değil: US 18 / S5 sözlüğü `basari`/`hata` yapar; çekirdek «Motor dışında sinyal yalnız None»; REVIEW-01 Motor-dışı `None`'u kilitler. `hata`→`park` Motor-dışı geçiştir; ara `hata` durumunda yazılan değer yeni sözlüktür, hurda `motor_hatasi` değildir.

**Olumlu kapsam**
- US 20 / SEAMS 3: `hata` → `hata` → `park`, tek `isi_ilerlet` (SahteMotor + fabrika/sahte koşucu).
- US 23 / S2: hata + dolu `metin` artefakt yazmaz, `plan_hazir`/`paket_hazir` açılmaz; eski `plan.md` varken de kapı açılmaz.
- US 24: `yapisal`/`maliyet`/`oturum` durum seçmez (yanıltıcı `usta_atandi` JSON).
- US 40: koşucu `OSError` → `hata` (birincil seam, 01–03 kilidi; bu dilim iç seam birim testi ekler).
- US 19 / S3: 04 `park`'a gider; 03 `basari`+boş artefakt `planlaniyor`'da kalır.
- Debt 05: `[]` (falsy → `cozumle` `bozuk` yolu, zaten `hata`) ve `"[]"` (claude/agy/codex `.get` `AttributeError`); grok dict koruması. `kart_motoru` `(TypeError, ValueError, AttributeError)` → `HATA`; döngü düşmez. Dört `cli` iç seam; CH-0001 claude `isi_ilerlet`.
- US 43 / 55: subprocess yamalı; unittest CLI/ağ açmaz.
- S1: birincil kanıt `isi_ilerlet` (SahteMotor ve kart/CLI). Üretim farkı bir satır; iskelet yolu 01–03. Yeni public seam, Bekçi, iskelet, insan dosyası, `kos`/`dongu` yok.

## Çalıştırılan testler ve karşılaştırma

Ortam: Python 3.13.5, Linux, uid 1000. Gerçek Motor/CLI veya ağ çağrısı kullanılmadı. Testlerin sahte koşucuları ve geçici dosyaları kullanıldı.

| Komut / çalışma bağlamı | Sonuç |
| --- | --- |
| `python3 -m unittest discover -s tests -p 'test_surucu*.py' -v` — çalışma ağacı | **58/58 geçti** |
| `python3 -m unittest tests.test_kart_motoru -v` — çalışma ağacı | **7/7 geçti** |
| `python3 -m unittest discover -s tests` — çalışma ağacı | **122 test, 1 failure**, yalnız bilinen Bekçi |
| Aynı discovery — `git archive ee194aa` ile temiz geçici kopya | **110 test, 1 failure**, aynı Bekçi |
| Aynı discovery — `git archive e5d8e93` ile temiz geçici kopya | **119 test, 1 failure**, aynı Bekçi |

Temiz kopyalarda tam commit içeriği test edildi; kullanıcı çalışma ağacındaki untracked hafıza testleri (`tests/test_hafiza_deposu.py`, 3 test) 122/119 farkını açıklıyor. `e5d8e93` dokuz regresyon testi ekliyor. `test_kapi.py:29` dosya kapatma uyarıları önceden mevcut.

Bilinen kırmızı: `test_kit.BekciKatmanA.test_kosuda_anayasaya_dokunan_ajan_red`, `tests/test_kit.py:268`, `'tamam' != 'red'`. Sabit noktada da aynen oluştu. **Yeni regresyon değildir; verdict nedeni değildir.** Mevcut takip: `.scratch/suite-sagligi/issues/01-test-kit-bekci-kirmizi.md`.

### Birincil seam ek kanıtları

Aşağıdaki karşılaştırmada aynı `isi_ilerlet` + `motor_uret` + sahte koşucu düzeni `git archive` kopyalarında çalıştırıldı. Çalışma ağacına kod/test yazılmadı. Kart CH-0001 `claude`.

| Senaryo | `ee194aa` | `e5d8e93` |
| --- | --- | --- |
| Sahte koşucu `"[]"` (JSON dizi dizgisi) | **`AttributeError: 'list' object has no attribute 'get'`** — Sürücü döngüsü düşer | `hata` → `park`; `plan.md` yok; `son_sinyal` park’ta `None` |
| Sahte koşucu `[]` (Python listesi, falsy) | Normal `hata` → `park` (`cozumle` `bozuk` yolu) | Aynı: `hata` → `park` |
| Koşucu `OSError` | `hata` Sinyali (01–03 kilidi) | Aynı |

Debt 05’in kaçışı `"[]"` idi; Python `[]` zaten `stdout or ""` ile boş dizgiye düşüp `ValueError`/`bozuk` üzerinden `hata` oluyordu. Bu dilim `"[]"` AttributeError’unu `HATA, ""` yapıyor.

Hedefte ayrıca: hata + dolu metin → artefakt yok, `plan_hazir` yok; delege hata + dolu metin → `plan.md` durur, `paket.md` yok, `paket_hazir` yok; 03 karşılaştırması (`basari`+boş → `planlaniyor`) yeşil.

## Kapanış

Ticket 04 + Debt 05 birlikte **merge-ready**. ST-D1 (geniş `AttributeError` yakalama; spec ezer) ve ST-D2 (OSError stub kopyası) engelleyici olmayan debt adaylarıdır; bu incelemede yeni ticket açılmadı. Bilinen Bekçi failure’ı ayrı takip edilmelidir.

**Eksen özeti:** Standards: 0 engelleyici + 2 debt, en ağır bulgu yargı düzeyinde geniş `except AttributeError` (spec baskın); Spec: 0 engelleyici + 0 debt, en ağır bulgu yok.
