# 04: Hata Sinyali: iskelet hata yolu, kapı açılmaz

**Spec:** `.scratch/adr0001-hizalama/spec.md`

**What to build:**
Motor `hata` Sinyali (bozuk stdout, `cozumle` hatası veya koşucu `OSError`) verince mevcut iskelet yolu işler: `planlaniyor` → `hata` → `park` (veya delege eşdeğeri) tek `isi_ilerlet` çağrısında. Başarı kapısı açılmaz; `metin` / `yapisal` / `maliyet` / `oturum` sonraki durumu seçmez. Sürücü döngüsü patlamaz.

03'teki kapı reddi ile karışmaz: bu dilim Sinyal `hata`; 03 Sinyal `basari` + kötü artefakt. Kanıt yine birincil seam (`isi_ilerlet`): SahteMotor ve kart/CLI + sahte koşucu. Unittest CLI/ağ açmaz.

**Blocked by:** 02 Mutlu yol: Prompt şablonu, İş artefaktı, park

**Status:** done

- [x] `hata` Sinyali → `hata` durumu → `park`; `son_sinyal` yeni sözlük
- [x] Koşucu `OSError` → `hata` Sinyali; unittest CLI/ağ açmaz
- [x] Motor `hata` iken artefakt kapısı `plan_hazir` / `paket_hazir` açmaz
- [x] `cozumle` içindeki `yapisal` (ör. `usta_atandi`) durum seçmez; yazan yalnız Sürücü
- [x] 03'teki kapı reddi ile karışmaz: bu dilim Sinyal `hata`; 03 Sinyal `basari` + kötü artefakt
- [x] Sahte koşucu `[]` stdout → `cozumle` AttributeError kaçmaz; `hata` Sinyali; Sürücü döngüsü patlamaz
- [x] `python3 -m unittest discover -s tests` ağsız yeşil (yalnız bilinen Bekçi kırmızısı)

## Comments

- 2026-09-16: yayınlandı (to-tickets adım 5). Durum: ready-for-agent. 02 bitince 03 ile paralel frontier.
- 2026-09-16: Codex REVIEW-01 (ticket 01): sahte koşucu `[]` stdout AttributeError kaçıyor; kart_motoru yalnız TypeError/ValueError yakalıyor. Bu dilimin "bozuk stdout, cozumle hatası … Sürücü döngüsü patlamaz" kapsamında. Ayrı debt: `05-bos-stdout-attributeerror.md` (04 ile birleştirilebilir). Kaynak: `.scratch/adr0001-hizalama/REVIEW-01.md`.
- 2026-09-16: agy implement tamamlandı (TDD). Sahte koşucu `[]` ve `"[]"` çıktılarında AttributeError yakalaması `kart_motoru.py` içinde genişletildi; Debt 05 ile birlikte kapatıldı. Motor hata Sinyali verildiğinde artefakt kapısının (`plan_hazir`/`paket_hazir`) açılmadığı, artefakt yazılmadığı, `cozumle` içindeki yapısal/maliyet/oturum verilerinin durum seçmediği ve `hata` -> `park` yolunun tek çağrıda işlediği birincil seam (`isi_ilerlet`), `SurucuAdim` ve `kart_motoru` üzerinden doğrulandı.
