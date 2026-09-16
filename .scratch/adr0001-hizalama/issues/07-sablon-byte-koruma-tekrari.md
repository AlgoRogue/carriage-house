# 07: Şablon bayt koruması tekrarı (debt)

**Spec:** `.scratch/adr0001-hizalama/spec.md`

**What to build:**
`tests/test_surucu_adim.py` ile `tests/test_surucu_motor.py` aynı şablon değişmezliği kontrolünü kopyalar. Koruma kuralı değişince iki sınıf birlikte güncellenmek zorunda. İki kopya da yalnız test sonunda mevcut dosyaları dolaştığından silinen şablonu kaçırır.

Ortak bir test yardımcısında önce/sonra dosya adı→bayt haritalarını karşılaştır; tekrarı ve silme boşluğunu kapat. Ürünün şablon sildiği gösterilmedi; üretim davranışını değiştirme.

**Blocked by:** None (debt; H implement'ini bloklamaz)

**Status:** done

- [x] Şablon bayt koruması tek ortak yardımcıda (veya eşdeğer); iki test sınıfı onu kullanır
- [x] Silinen şablon da kaçmaz (yalnız mevcut dosya dolaşması yetmez)
- [x] Üretim şablon/artefakt davranışı değişmez
- [x] `python3 -m unittest discover -s tests` ağsız yeşil

## Comments

- 2026-09-16: Codex REVIEW-02 (ticket 02, engelleyici değil; Fowler Duplicated Code sezgisi). Kaynak: `.scratch/adr0001-hizalama/REVIEW-02.md` ST-D1.
- 2026-09-16: uygulandı (Claude Code). `tests/surucu_yolu.py`'a ortak `dizin_bayt_haritasi(dizin)` ve `dizin_bayt_korumasini_dogrula(test, dizin, once)` eklendi; ikisi de tam sözlük (`ad -> bayt`) karşılaştırır, bu yüzden silinen bir şablon da (yalnız mevcut dosyaları dolaşmanın kaçırdığı boşluk) yakalanır. `tests/test_surucu_adim.py::SurucuAdimTesti` ve `tests/test_surucu_motor.py::FabrikaMutluYolTesti` artık kendi kopya döngülerini değil bu ortak yardımcıyı kullanıyor. Üretim şablon/artefakt davranışı değişmedi.
