# 05: Test SahteKosucu / setUp tekrarını ortaklaştır

**What to build:**
agy Spec∥Standards review (Motor dilimi) Standards ekseninde iki zayıf Duplicated Code notu bıraktı.
Bunlar blocker değil; davranış doğru. Orijinal Motor biletleri (01-04) bittikten sonra ele alınacak borç.

1. `tests/test_kart_motoru.py` ve `tests/test_surucu_motor.py` içindeki `SahteKosucu` birebir.
2. `tests/test_surucu_motor.py` içinde mutlu yol / hata yolu sınıflarının `setUp`/`tearDown` kopyası.

Ortak yardımcı veya base sınıf ile tek yere çek; ağsız testler yeşil kalsın. Üretim koduna dokunma.

**Blocked by:** 01, 02, 03, 04 (Motor dilimi bitti; borç sırası)

**Status:** ready-for-agent

- [ ] `SahteKosucu` tek ortak yardımcıda (veya eşdeğer) toplanır; iki test dosyası onu kullanır
- [ ] `test_surucu_motor` setUp/tearDown tekrarı base sınıf veya yardımcı ile iner
- [ ] `python3 -m unittest discover -s tests -p 'test_*motor*.py'` ve `test_surucu*.py` yeşil kalır
- [ ] Üretim `kart_motoru.py` / Sürücü davranışı değişmez

## Comments

- 2026-09-16: agy (gemini-3.1-pro-high) Standards judgement - Duplicated Code; Spec 0 bulgu. Kullanıcı politikası: blocker değil, standardı düşüren bulgu borç ticket; orijinal dilim bitince.
- 2026-09-16: ADR-0001 ticket-01 Codex REVIEW-01 yeniden gördü; bkz `.scratch/adr0001-hizalama/REVIEW-01.md`
