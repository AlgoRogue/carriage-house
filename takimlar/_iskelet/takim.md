---
name: TAKIM
description: TAKIM takımı — (tek cümle: ne girer, ne çıkar)
motor: claude
tools: [Read, Write, Glob, Grep]
cikti_semasi:
gerekli_anahtarlar: []
skills: []
butce_usd: 2
---

# TAKIM

## Varoluş amacı
(tek paragraf)

## Girdi
- (yol / dosya)

## Koşu adımları
1. `increment/evre.json`'u ve kendi `durum.json`'unu oku.
2. Girdiyi oku (yukarıda).
3. Çıktıyı üret (aşağıdaki sözleşmeye göre).
4. `durum.json`'u güncelle: `son_kosu`, `defter_son_ders`.
5. `defter.md`'ye bu koşudan çıkan **tek** dersi ekle (ders yoksa ekleme).
6. Koşu kaydını `SIRKET_KOSU` yoluna yaz: ne okudun, ne ürettin, ne kaldı.

## Asla yapmaz
1.
2.

## Motor
`claude` | `agy` | `codex` | `grok` | `sozlesme` (evre.motor.insaat) | `ters` (evre.motor.bekci)

## Çıktı sözleşmesi
- (dosya adı deseni ve içinde ne olduğu; `cikti_semasi` doluysa son cevap o şemaya uyan JSON'dur ve sürücü yazar)
