# 03: Kapı: `basari` ama kabul edilemez İş artefaktı

**Spec:** `.scratch/adr0001-hizalama/spec.md`

**What to build:**
Motor `basari` deyip kabul edilebilir İş artefaktı bırakmazsa Sürücü module'ü ilerletmez (S3). Döngü durur; durum Motor durumunda kalır (`planlaniyor` veya `delege_hazirlaniyor`). Otomatik `hata` durumu yok. İş sessizce `park`'a kaçmaz.

Kanıt birincil seam üzerinden: `isi_ilerlet` sonrası durum kaydı + eksik/boş dosya + bitiş durumu. Kapı Sürücü implementation'ındadır; ayrı public seam açılmaz. Mutlu yol (02) kırılmaz.

**Blocked by:** 02 Mutlu yol: Prompt şablonu, İş artefaktı, park

**Status:** done

- [x] `basari` + boş veya yok (veya UTF-8 okunamayan) artefakt → geçiş yok, bitiş Motor durumu, `park` değil
- [x] Kapı reddi iskeletteki `hata` durumuna çevirilmez
- [x] Kabul: dosya var, UTF-8, boş değil; içerik şeması yok
- [x] Mutlu yol (02) kırılmaz: kabul edilebilir iki artefaktta `bos` → `park` durur
- [x] `python3 -m unittest discover -s tests` ağsız yeşil (yalnız bilinen Bekçi kırmızısı)

## Comments

- 2026-09-16: yayınlandı (to-tickets adım 5). Durum: ready-for-agent. 02 bitince 04 ile paralel frontier.
- 2026-09-16: Codex REVIEW-02 (ticket 02) SP-D1: `surucu_adim` docstring yazılamazsa reddet diyor ama `mkdir`/`write_text` IO yakalanmıyor; `NotADirectoryError` kaçıyor. Bu dilimin kabul edilemez artefakt kapısı kapsamında; uygulama ve belge birlikte hizalanmalı. Ayrı debt: `08-artefakt-io-hata-belge.md` (03 ile birlikte). Kaynak: `.scratch/adr0001-hizalama/REVIEW-02.md`.
- 2026-09-16: agy implement tamamlandı (TDD). NotADirectoryError, UTF-8 okunamayan ve boş artefakt reddi kanıtlandı; docstring hizalandı; Debt 08 ile birlikte kapatıldı.
