# Ajan hafızası prototipi - CH-0001 (Cengizhan)

Status: ready-for-agent

## Problem Statement

Cengizhan'ın Personel kaydı dizininde kart, dosya, durum ve Sürücü var. Ajan hafızası yok. CONTEXT bunu tek ajana ait kalıcı bilgi katmanı olarak kilitler; Anlamsal eşleyici ileride buraya bakacak. Defter o deponun sıcak yüzüdür, deponun kendisi değildir.

Bugün ajanın "hafızası" sanılan şeyler yanlış yerde duruyor: takım `defter.md` dersleri, koşu kaydı, anlık `durum.json`. Hiçbiri CH-0001 Ajan hafızası değil. Boş bir depo da yok. Yazılacak yer olmadığı için sonraki adım (anlamsal eşleme) bakacak bir şey bulamaz.

Bu dilim üretimi değil, küçük bir prototiptir: bir ajan, boş başlayan, yazılınca diskte kalan bir depo. Sürücü, Motor ve orkestrasyon henüz bunu okumaz.

## Solution

CH-0001 Personel kaydı dizininde tek bir kalıcı Ajan hafızası dosyası tut. İlk hali boş bir kayıt listesidir. Personel-kapsamlı bir okuma/ekleme API'si bu dosyayı okur ve sona kayıt ekler. Ağsız unittest üç şeyi kanıtlar: boş başlangıç, yazının diskte kalması, yeni okuyucunun yazılanı dönmesi.

Defter üretilmez. Anlamsal eşleyici yazılmaz. Sürücü, Motor, Kapı, usta ve şirket orkestrasyonu bu depo ile bağlanmaz.

## User Stories

1. As a human operator, I want CH-0001 (Cengizhan) to have its own Ajan hafızası, so that this agent's durable knowledge is not mixed with another agent's store.
2. As a human operator, I want that Ajan hafızası to live in CH-0001's Personel kaydı dizini, so that identity and memory share one personnel record.
3. As a human operator, I want the store to start empty, so that the prototype is honest: nothing has been remembered yet.
4. As a human operator, I want to be able to write an entry, so that the store is not a read-only placeholder.
5. As a human operator, I want a written entry to still be there after a new reader is opened, so that memory outlives one process.
6. As a human operator, I want Defter left unbuilt, so that a hot face is not mistaken for the store.
7. As a human operator, I want Anlamsal eşleyici left unbuilt, so that this slice stays a durable store, not a search engine.
8. As a human operator, I want Orkestrasyon hafızası left untouched, so that agent memory and orchestration memory stay separate layers.
9. As a human operator, I want Kapı, usta assignment, and park-sonrası states left out, so that this prototype does not pretend to be workflow.
10. As a developer, I want a single JSON object whose `kayitlar` array is the store, so that empty start is `[]` and not a missing file convention.
11. As a developer, I want each kayıt to be `{"metin": "<opaque string>"}`, so that later Anlamsal eşleyici has text to look at without this slice inventing embeddings.
12. As a developer, I want no extra kayıt fields in this slice (no clock, no embedding, no tag list), so that the prototype stays the smallest honest shape.
13. As a developer, I want a `HafizaDeposu` next to the existing personel-scoped Sürücü helpers, so that the new seam copies `DurumDeposu` rather than inventing a second persistence style.
14. As a developer, I want `oku()` to return the `kayitlar` list, so that empty start is an empty list and not a sentinel or exception.
15. As a developer, I want `ekle(metin)` to append one kayıt and write the file, so that write is append-only rather than replace-the-store.
16. As a developer, I want the constructor to take an injectable path, so that tests never have to write the committed personnel file.
17. As a developer, I want the default path to be CH-0001's committed store, so that a caller with no test path still reads this agent's memory.
18. As a developer, I want a unittest that reads the empty store and sees no kayıt, so that empty start is proven, not assumed.
19. As a developer, I want a unittest that writes one kayıt, opens a new `HafizaDeposu` on the same path, and reads that kayıt back, so that persistence is proven across instances.
20. As a developer, I want that persistence test to compare `metin` values, so that "read returns what was written" is external behavior.
21. As a developer, I want a unittest that appends a second kayıt and reads both in order, so that the second write does not clobber the first.
22. As a developer, I want write tests to use a temporary file, so that the committed empty store stays empty.
23. As a developer, I want write tests to assert the committed personnel store is byte-equal before and after, so that isolation of the product file is proven.
24. As a developer, I want tests under `tests/` discovered by `python3 -m unittest discover -s tests`, so that this slice uses the repo's existing runner.
25. As a developer, I want those tests to open no network, no CLI, and no Motor, so that the store is proven without a harness.
26. As a developer, I want `HafizaDeposu` not to import or call Sürücü / Motor / `isi_ilerlet`, so that prototype isolation is a module fact, not a comment.
27. As a developer, I want this slice not to change `aksiyon-iskeleti.json`, `kart.json`, or `durum.json`, so that action state and memory stay different records.
28. As a developer, I want this slice not to change `bin/kos.py`, `bin/dongu.py`, or `bin/kapi.py`, so that şirket orkestrasyonu is not pulled in.
29. As a developer, I want UTF-8 JSON with `ensure_ascii=False`, so that Turkish `metin` round-trips.
30. As a developer, I want stdlib only, so that the prototype matches the repo's no-dependency rule.
31. As a developer, I want Turkish module and type names (`HafizaDeposu`, `oku`, `ekle`, `kayitlar`, `metin`), so that naming matches `DurumDeposu`.
32. As a developer, I want empty `metin` (`""`) to still be a kayıt, so that this slice does not invent validation theater.
33. As a developer, I want a missing default file to be out of product behavior (the committed empty file is the empty start), so that "starts empty" is not "starts absent".
34. As a future Anlamsal eşleyici, I want a list of `metin` kayıtlar already on disk, so that step 4 can look at this store without inventing it.
35. As a developer, I want no Defter file and no projection from store to Defter, so that the hot face is not smuggled in as "just a view".
36. As a developer, I want no `.env` read, so that secrets stay out of a memory prototype.
37. As a developer, I want other Personel kaydı dizinleri and `_iskelet` left unchanged, so that this prototype is CH-0001 only.
38. As a human operator, I want this slice documented on the roadmap as in progress prototype, so that step 3 is not still labeled "next" while a spec exists.

## Implementation Decisions

Locked seams (this slice does not reopen them):

1. **One seam: `HafizaDeposu`.** Highest existing persistence style is `DurumDeposu` (injectable path, JSON on disk, `oku` / `yaz`). Ajan hafızası is not anlık durum, so `durum.json` is not reused. The new seam copies that style: one class, two operations (`oku`, `ekle`), default path inside CH-0001's Personel kaydı dizini.
2. **Store shape: one JSON file, not a directory.** A `hafiza/` tree needs an index, multiple files, and an empty-dir git placeholder. A single `hafiza.json` is the smallest commitable empty store and matches `durum.json` / `kart.json`.
3. **File location:** `personel/CH-0001/hafiza.json`. Not şirket `bin/`, not `takimlar/*/defter.md`, not `durum.json`.
4. **On-disk document** (decision shape, not a demo):

```json
{
  "kayitlar": []
}
```

5. **Kayıt shape** (this slice; later fields are out):

```json
{ "metin": "<opaque unicode string>" }
```

6. **API contract:**

```
HafizaDeposu(yol=varsayilan)
oku() -> list[dict]          # belge["kayitlar"]
ekle(metin: str) -> None     # append {"metin": metin}, then write
```

Default `yol` is CH-0001's `hafiza.json`. Tests pass a temp path.

7. **Empty start is a committed empty list**, not a missing file. Product `oku()` on the default path returns `[]`. Write tests do not use the default path.
8. **Append-only.** `ekle` does not replace `kayitlar`. A second `ekle` leaves the first kayıt in place, first then second.
9. **Code lives under `personel/CH-0001/bin/`** (module `hafiza_deposu.py`), adjacent to `durum_deposu.py`. Not repo-root `bin/`.
10. **Write format** matches `DurumDeposu`: UTF-8, `ensure_ascii=False`, indent 2, trailing newline.
11. **No wiring.** This module does not import Sürücü, Motor, kart fabrikası, `isi_ilerlet`, şirket `kos` / `dongu` / `kapi`. Those callers do not gain a hafıza argument.
12. **No Defter, no eşleyici, no Kapı, no usta.** No second file that "is easier to read". No similarity function. No yetki check before `ekle`.
13. **CH-0001 only.** `_iskelet` and other personel numbers stay unchanged.
14. **Aksiyon iskeleti `bilincli_disi` still lists `hafiza`.** That list is the Sürücü tanımı, not this isolated prototype. This slice does not edit the iskelet to claim Sürücü now owns memory.

## Testing Decisions

- A good test measures external behavior: what `oku()` returns, what the JSON file contains, and that the committed personnel file is untouched by write tests. It does not inspect private helpers or "how JSON was dumped".
- Module under test: `HafizaDeposu` only. Do not re-unit Sürücü, Motor, or şirket `kos`.
- Prior art: `tests/test_surucu_durum.py` copies `durum.json` into a temp path, injects `DurumDeposu(yol)`, and asserts the production `durum.json` bytes are unchanged in `tearDown`. Hafıza tests follow that pattern. Discover path: `python3 -m unittest discover -s tests`. `tests/surucu_yolu.py` already puts `personel/CH-0001/bin` on `sys.path`.
- Scenarios that must be proven:
  - Empty start: `oku()` returns `[]` (committed store, or a copy of it).
  - One write persists: `ekle` on a temp file, new `HafizaDeposu` instance, `oku()` returns one kayıt whose `metin` matches.
  - Second append: two `ekle` calls, `oku()` returns both in order.
  - Isolation: write tests leave committed `hafiza.json` byte-equal; they do not open network, CLI, or Motor.
- Tests live under `tests/` (name aligned with `test_surucu_durum.py`, e.g. `test_hafiza_deposu.py`). No subprocess, no PATH lookup, no `.env`.

## Out of Scope

- Defter (sıcak yüz, `defter.md`, projection, "context window" assembly).
- Anlamsal eşleyici (embedding, similarity, RAG, stokastik ada).
- Orkestrasyon hafızası.
- Binding this store into Sürücü, Motor, `isi_ilerlet`, şirket `kos` / `dongu` / `kapi`.
- Kapı, Kapı yetkileri, usta ataması, park-sonrası durumlar.
- Multi-agent stores, `_iskelet` copy, shared memory.
- Directory-of-files store, database, cache.
- Timestamps, ids, tags, embeddings, or `is_id` on kayıt (can wait for a later slice).
- Concurrent writers, file locks, migration.
- Editing `aksiyon-iskeleti.json`, `kart.json`, `durum.json`, ANAYASA / SoT / `sema/`.
- Production CLI or HTTP for hafıza.
- This session does not implement the production module, the JSON file, or the tests; it publishes spec and tickets only.

## Further Notes

Glossary: CONTEXT.md "Hafıza ve eşleme" (`Ajan hafızası`, `Defter`, `Orkestrasyon hafızası`, `Anlamsal eşleyici`). Flagged ambiguity still holds for Defter: the split is locked; this slice adds only the store.

Roadmap: root `ROADMAP.md` step 3, in progress (prototype). Step 4 (Anlamsal eşleyici) stays after hafıza. Step 5 (Motor bağlama) is already done and is not reopened here.

Previous CH-0001 slices (`.scratch/otomatik-surucu-ch0001/`, `.scratch/otomatik-motor-ch0001/`) listed hafıza as out of scope. This spec is that deferred prototype, still isolated: Sürücü does not start reading memory.

Seams were locked in this spec without an interview: single `hafiza.json`, `HafizaDeposu.oku` / `ekle`, networkless unittest, no Sürücü/Motor/orkestrasyon wiring.
