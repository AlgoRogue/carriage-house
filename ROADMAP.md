# Yol haritası

Kalıcı altı adım. Sıra sabittir; atlanan madde iptal sayılmaz.

Hizalama (H) bitti; adım 3 ve 5 claim edildi. Asıl frontier: **4 Anlamsal eşleyici**. Dış debt: SahteKosucu, test_kit Bekçi, hafıza deferred 04.

| # | Adım | Durum |
|---|---|---|
| 1 | Personel kaydı | done |
| 2 | Deterministik aksiyon iskeleti (CH-0001 Sürücü dilimi: `bos` → `park`) | done |
| 3 | Ajan hafızası | done (prototip + depo; Sürücü'ye bağlı değil; deferred: `.scratch/ajan-hafiza-ch0001/issues/04-bos-metin-kayit-testi.md`) |
| 4 | Anlamsal eşleyici | next |
| 5 | Motor bağlama | done (ADR-0001 hizalama + canlı duman; deferred: `.scratch/otomatik-motor-ch0001/issues/05-test-sahte-kosucu-tekrari.md`) |
| H | ADR-0001 hizalama + hurda/kalan | done (tickets 01–13; şablon+Read duman OK) |
| 6 | Orkestrasyon kancası | later |

## Bu dilim (adım 4)

Sıradaki ana ürün dilimi: Anlamsal eşleyici. Hafıza (3) ve Motor (5) claim sonrası. Kapı / Defter / usta / park sonrası hâlâ bilinçli erteleme.

## Bilinçli olarak ertelenenler

Şunlar vazgeçilmiş değil, sırası gelince ele alınacak:

- **Kapı** (personel numarası + Kapı yetkileri ile yetki kontrolü)
- **Defter** (ajan hafızasının sıcak yüzü; hafızanın kendisi değil)
- **Usta** ataması
- **Park sonrası** durumlar (`usta_atandi`, `izleniyor`, `tamam`)

Adım 6 aynı kuralda: ertelendi, terk edilmedi. Adım 4 artık frontier.

## Durum notu

- 2026-09-16: Motor bağlama (5) uygulandı ve Spec∥Standards review geçti. Deferred debt: `.scratch/otomatik-motor-ch0001/issues/05-test-sahte-kosucu-tekrari.md`.
- 2026-09-16: Adım 3 Ajan hafızası prototipi uygulandı (hafiza.json + HafizaDeposu + 3 test). Deferred debt: `.scratch/ajan-hafiza-ch0001/issues/04-bos-metin-kayit-testi.md`.
- 2026-09-16: Sıradaki ana dilim: 4 Anlamsal eşleyici. Motor deferred debt 05 ve hafıza deferred debt 04 bekliyor (orijinal sıradan sonra).
- 2026-09-16: Hafıza adımı prototype skill (LOGIC) ile düzeltildi: `personel/CH-0001/proto/hafiza-demo.html` + `HAFIZA-CEVAP.md`. Erken üretim lift (`hafiza_deposu.py` / testler) verdict bekliyor.

- 2026-09-16: Mimari grill M1-M5 kabul. ADR-0002..0005 yazildi. Sonraki: CLI to-spec (ADR-0001 hizalama + hurda/kalan). Erken "adim 3/5 done" iddialari hizalama bitene kadar gecici sayilir.
- 2026-09-16: G4 uygulandi: 3/5 done geri alindi. G7: test_kit kirmizi icin debt acilacak.
- 2026-09-16: G1 A - ADR-0002 Python + kaçış kapısı kilitlendi. Mimari grill G1-G8 kapandi. Sonraki: CLI to-spec (hizalama).
- 2026-09-16: Hizalama seam S1–S5 onaylandı; spec `.scratch/adr0001-hizalama/spec.md` ready-for-agent. Uygulama henüz yok. G3: ADR-0004 + `personel/CH-0001/bin/README.md` birlikte yeniden okunur.
- 2026-09-16: Hizalama tickets published (`.scratch/adr0001-hizalama/issues/`); frontier = 01 (Sinyal sözlüğü ve Motor callable). 02←01; 03←02; 04←02.
- 2026-09-16: Ticket 01 Codex REVIEW-01 debt kuyruğa alındı: adr0001 05 (boş stdout AttributeError), 06 (Claude `--max-budget-usd None`); mevcut `otomatik-motor-ch0001/issues/05-test-sahte-kosucu-tekrari` ve `suite-sagligi/issues/01-test-kit-bekci-kirmizi` yeniden görüldü. İndeks: `.scratch/adr0001-hizalama/DEBT.md`. Asıl frontier hâlâ 02.
- 2026-09-16: H tickets 01–04 done, debt kuyruk açık. REVIEW-03/04: 09–13. Açık 06, 07, 09–13; 05/08 done. İndeks: `.scratch/adr0001-hizalama/DEBT.md`.

- 2026-09-16: H done claim. Tickets 01–04 + debt 05–13 merge-ready; şablon Sürücü-yazar diline çekildi; Motor salt `Read`; canlı duman-2 `bos`→`park` + gerçek plan/paket. Adım 3 ve 5 done claim (G4 geri alımı kalktı). Frontier: 4 Anlamsal eşleyici. G3 hâlâ açık: ADR-0004 + `personel/CH-0001/bin/README.md` birlikte yeniden okunur.
- 2026-09-16: ADR-0001 debt 14–16 kuyruğa alındı (model listesi CLI; agy/grok duman; Codex duman kota sonrası). 01–13 done. Frontier hâlâ 4 Anlamsal eşleyici.
