# Canlı Motor dumanı — sonuç

**Zaman:** 2026-09-16T15:37:38+00:00
**Süre:** 110.8s
**is_id:** `DUMAN-001`
**Geçici kök:** `/tmp/duman-motor-h8205znj`
**Mutlu yol:** EVET

## Sürücü sonucu

- başlangıç: `bos`
- bitiş: `park`
- yol: `bos → is_alindi → planlaniyor → plan_hazir → delege_hazirlaniyor → paket_hazir → park`

## Geçici durum.json (ürün değil)

```json
{
  "personel_numarasi": "CH-0001",
  "durum": "park",
  "is_id": "DUMAN-001",
  "son_sinyal": null,
  "not": "iskelet kayit; surucu henuz yok"
}
```

## Motor çağrıları

Sayı: **2** (beklenen 2)

- #1: sure=77.1s rc=0 stdout=3862B p_len=185
- #2: sure=33.7s rc=0 stdout=4213B p_len=312

## Artefaktlar

- `plan.md`: var, 1729 karakter
- `paket.md`: var, 1649 karakter

### plan.md (ilk 800 karakter)

```
İş DUMAN-001, elimde somut bir gereksinim metni yok — sadece bir kimlik (`DUMAN-001`) var. Bu, gerçek bir inşaat işinden gelen bir iş tarifi değil; sistemin uçtan uca akışını (bos → is_alindi → planlaniyor → plan_hazir → delege_hazirlaniyor → paket_hazir → park) doğrulamak için verilmiş bir duman/iskelet iştir. Buna göre, gerçek bir kapsam icat etmek yerine, bu durumu açıkça plan'a yazıyorum ve akışı doğrulayacak asgari, dürüst bir parçalama hazırlıyorum.

# Plan — DUMAN-001

## Durum
Bu iş için insan tarafından verilmiş bir amaç/kabul ölçütü metni yok; yalnız iş kimliği geldi. Bu, sürücü/motor/kart hattının doğru çalıştığını doğrulamak için kullanılan bir duman (smoke) işidir; üretim kapsamı taşımaz.

## Parçalar
1. **Hat doğrulama** — Kartın `bos`'tan `park`'a kadar beklenen 6 geçişi (`i
```

### paket.md (ilk 800 karakter)

```
# Delege Paketi — DUMAN-001

## Durum
`plan.md` içeriğine sadıkım: bu iş için insandan gelen gerçek bir amaç/kabul ölçütü metni yok, yalnızca iş kimliği (`DUMAN-001`) var. Bu bir duman/iskelet işi — sürücü → kart → motor hattının `bos`'tan `park`'a kadar doğru ilerlediğini kanıtlamak için kullanılıyor. Aşağıdaki paket, icat edilmiş bir üretim kapsamı değil; plan'daki üç parçayı delegasyon biçimine sokan dürüst bir aktarımdır.

## Kapsam
Üretim kodu, sözleşme ya da usta ataması içermez. Paket, `plan.md`'de tanımlı üç doğrulama parçasını taşır:

1. **Hat doğrulama** — Kart `bos → is_alildi → planlaniyor → plan_hazir → delege_hazirlaniyor → paket_hazir → park` yolunu sırayla izlemeli; motor çağrısı sayısı 2 olmalı.
2. **Artefakt bütünlüğü** — `plan.md` ve bu `paket.md` boş olmamalı, UTF-8 ve 
```

## Ürün koruması (byte-eşit)

- kart: OK
- durum: OK
- iskelet: OK
- sablonlar: OK

## Loglar

`/workspace/carriage-house/.scratch/adr0001-hizalama/duman-logs` — her çağrının stdout/stderr/-p yükü

## Not

Acceptance unittest değil. Kapı/hata dumanı bu turda yok.
Ham CLI çıktıları log klasöründe; maliyet Claude JSON `total_cost_usd` alanında olabilir.
