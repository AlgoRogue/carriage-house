# 15: Canlı Motor dumanı — agy ve grok (debt)

**Spec:** `.scratch/adr0001-hizalama/spec.md`

**What to build:**
Canlı Motor dumanını agy ve grok ile tekrarla. Geçici durum/isler; ürün kart/durum/iskelet/şablon kirlenmez. Nerede takıldığını not et.

Claude duman-2 referans: `.scratch/adr0001-hizalama/DUMAN-SONUC.md`. Script: `duman_motor.py` (cli/model enjekte edilebilir hale getirilebilir). Acceptance unittest değil.

H implement'ini bloklamaz.

**Blocked by:** None

**Status:** ready-for-agent

- [ ] agy canlı duman: geçici kök, ürün byte-eşit; nerede takıldığı not
- [ ] grok canlı duman: geçici kök, ürün byte-eşit; nerede takıldığı not
- [ ] Claude duman-2 referans: `DUMAN-SONUC.md`
- [ ] Script `duman_motor.py`; cli/model enjekte edilebilir hale getirilebilir
- [ ] Codex bu bilette yok (16)

## Comments

- 2026-09-16: debt kuyruğa alındı. Claude duman-2 `bos`→`park` OK (`DUMAN-SONUC.md`). Codex şimdilik PAS — kota bitik; sonra 16.
