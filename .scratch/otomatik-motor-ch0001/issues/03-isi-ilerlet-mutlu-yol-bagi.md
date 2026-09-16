# 03: Fabrika Motorunu mevcut isi_ilerlet mutlu yoluna bağla

**Spec:** `.scratch/otomatik-motor-ch0001/spec.md`

**What to build:**
01'deki fabrika Motor'unu mevcut `isi_ilerlet` girişine ver. Enjekte koşucu her Motor durumunda başarı çıktısı döner. Tek çağrı, insan müdahalesi olmadan, işi `bos`'tan `park`'a götürür. Durum kaydını Sürücü yazar; Motor yazmaz. Koşucu yalnız `planlaniyor` ve `delege_hazirlaniyor` için çalışır. Sonraki durum iskelettendir; Motor metni hedef seçmez.

`isi_ilerlet(motor, ...)` imzası aynı kalır. İsteğe bağlı ince kart girişi yalnız fabrika + `isi_ilerlet` sarmalayıcısı olabilir. Mevcut `SahteMotor` e2e testleri kırılmaz; SahteMotor silinmez. Şirket döngüsü/sürücüsü bu bağa zorlanmaz.

**Blocked by:** 01 Karttan Motor fabrikası: tek çağrıda Sinyal

**Status:** done

- [x] Fabrika Motor'u `isi_ilerlet`'e verilir; imza `motor` callable almaya devam eder
- [x] Tek çağrı `bos` → `park` (mutlu yol); durum kaydında bitiş `park`, iş kimliği yazılır
- [x] Koşucu yalnız `planlaniyor` ve `delege_hazirlaniyor` için çağrılır
- [x] Motor `durum.json` yazmaz; yazan Sürücü'dür. Kart ve iskelet yazılmaz
- [x] Motor çıktısının `metin` / `yapisal` alanları sonraki durumu belirlemez
- [x] Mevcut SahteMotor mutlu yol e2e'si geçmeye devam eder
- [x] İnce kart girişi varsa yalnızca fabrika + `isi_ilerlet`'tir; yeni makine açmaz
- [x] Testler CLI/ağ açmaz; `python3 -m unittest discover -s tests`

## Comments

- 2026-09-15: yayınlandı (to-tickets). Durum: ready-for-agent.
- 2026-09-15: Fabrika Motoru `isi_ilerlet`'e verildi; `karti_ilerlet` ince sarmalayıcı. Mutlu yol `bos` → `park`; koşucu yalnız iki Motor durumunda. SahteMotor e2e duruyor. `python3 -m unittest tests.test_surucu_motor` 4/4. `python3 -m unittest discover -s tests -p 'test_surucu*.py'` 33/33.
