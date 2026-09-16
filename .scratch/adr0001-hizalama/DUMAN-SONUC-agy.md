# Canlı Motor dumanı — agy

**Zaman:** 2026-09-16T16:14:57+00:00
**Süre:** 302.9s
**cli / model:** `agy` / `gemini-3.8-flash-high`
**is_id:** `DUMAN-AGY`
**Geçici kök:** `/tmp/duman-agy-oqipatj8`
**Mutlu yol:** HAYIR
**Takılma:** bitiş=planlaniyor yol=bos → is_alindi → planlaniyor; motor çağrı sayısı=1 (beklenen 2); plan.md yok/boş; paket.md yok/boş

## Sürücü sonucu

- başlangıç: `bos`
- bitiş: `planlaniyor`
- yol: `bos → is_alindi → planlaniyor`

## Geçici durum.json (ürün değil)

```json
{
  "personel_numarasi": "CH-0001",
  "durum": "planlaniyor",
  "is_id": "DUMAN-AGY",
  "son_sinyal": null,
  "not": "iskelet kayit; surucu henuz yok"
}
```

## Motor çağrıları

Sayı: **1** (beklenen 2)

- #1: argv0=`agy` sure=302.9s rc=0 stdout=261B p_len=183

## Artefaktlar

- `plan.md`: YOK
- `paket.md`: YOK

## Ürün koruması (byte-eşit)

- kart: OK
- durum: OK
- iskelet: OK
- sablonlar: OK

## Loglar

`/workspace/carriage-house/.scratch/adr0001-hizalama/duman-logs-agy`

## Not

Acceptance unittest değil. Codex bu turda yok (kota).
