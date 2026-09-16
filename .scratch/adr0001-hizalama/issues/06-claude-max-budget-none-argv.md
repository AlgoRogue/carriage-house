# 06: Claude `--max-budget-usd None` argv (debt)

**Spec:** `.scratch/adr0001-hizalama/spec.md`

**What to build:**
Yalnız model ayarı varken Claude komut üreticisi `--max-budget-usd None` üretiyor. Gerçek CLI uyumu doğrulanmadı. Ya None'ı argv'den çıkar ya da şirket motorlar kaydıyla hizala; ağsız unittest argv kanıtıyla sabitle.

H implement'ini bloklamaz. Üretim davranışı değişmeden önce unittest argv kanıtı durur.

**Blocked by:** None (debt; H implement'ini bloklamaz)

**Status:** done

- [x] Yalnız model ayarında argv'de `--max-budget-usd None` yok (veya şirket kaydıyla hizalı ve kabul)
- [x] Ağsız unittest argv kanıtı, üretim davranışı değişmeden önce durur
- [x] Gerçek CLI / ağ açılmaz

## Comments

- 2026-09-16: Codex REVIEW-01 (ticket 01, engelleyici değil; merge engeli sayılmadı). Kaynak: `.scratch/adr0001-hizalama/REVIEW-01.md`.
- 2026-09-16: uygulandı (Claude Code). `bin/motorlar/claude.py` `komut()`: `--max-budget-usd` yalnız `ayarlar.get("butce_usd") is not None` iken argv'ye eklenir; diğer motorlar (agy/codex/grok) zaten aynı desende opsiyonel bayrak ekliyordu, claude buna hizalandı. Regresyon: `tests/test_motorlar.py::ClaudeTesti::test_butce_verilmezse_max_budget_usd_argvde_yok` (yalnız model ayarında argv'de ne `--max-budget-usd` ne `None` var). Ağsız/CLI'sız.
