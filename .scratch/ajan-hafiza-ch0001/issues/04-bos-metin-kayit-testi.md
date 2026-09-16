# 04: Boş metin ("") kaydı için doğrudan test

**What to build:**
agy Spec review notu: boş `metin` kabul ediliyor ama doğrudan unittest yok.
Blocker değil. Hafıza 01-03 bitti; bu borç sırası.

`HafizaDeposu.ekle("")` sonrası `oku()` içinde `{"metin": ""}` kaydını kanıtlayan ağsız test ekle. Üretim doğrulama tiyatrosu ekleme.

**Blocked by:** 01, 02, 03

**Status:** ready-for-agent

- [ ] Boş metin ekleme davranışı unittest ile kanıtlanır
- [ ] Mevcut 3 hafıza testi yeşil kalır
- [ ] Üretim API değişmez (yalnız test)

## Comments

- 2026-09-16: agy Spec judgement (kısmi user story 32). Standards 0 bulgu.
