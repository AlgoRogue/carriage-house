# 16: Canlı Motor dumanı — Codex, kota sonrası (debt)

**Spec:** `.scratch/adr0001-hizalama/spec.md`

**What to build:**
Codex canlı duman — kota bitince. Geçici durum/isler; ürün kirlenmez. Nerede takıldığını not et.

Claude duman-2 referans: `.scratch/adr0001-hizalama/DUMAN-SONUC.md`. Script: `duman_motor.py` (cli/model enjekte edilebilir). Acceptance unittest değil.

H implement'ini bloklamaz.

**Blocked by:** None

**Status:** ready-for-agent

- [ ] Codex canlı duman, kota bitince: geçici kök, ürün byte-eşit
- [ ] Nerede takıldığı not
- [ ] Claude duman-2 referans: `DUMAN-SONUC.md`
- [ ] Kota bitikken koşulmaz

## Comments

- 2026-09-16: debt kuyruğa alındı. Kota bitik; şimdilik pas. Kota dönünce koş.
