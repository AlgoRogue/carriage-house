# 05: Boş stdout AttributeError → hata Sinyali (debt)

**Spec:** `.scratch/adr0001-hizalama/spec.md`

**What to build:**
Sahte koşucu `[]` stdout verdiğinde Claude/agy/codex çözümleyicilerinden AttributeError kaçıyor; kart_motoru yalnız TypeError/ValueError yakalıyor. Sürücü döngüsü patlamamalı; sonuç `hata` Sinyali olmalı.

04'ün "bozuk stdout, cozumle hatası" acceptance'ına dahil (04 yapılırken kapatılabilir). Ayrı debt olarak kuyrukta durur; 04 acceptance'ına gömülmüş olsa bile görünür kalsın.

**Blocked by:** 02 Mutlu yol: Prompt şablonu, İş artefaktı, park

**Status:** done

- [x] Sahte koşucu `[]` stdout → AttributeError Sürücü döngüsünü düşürmez
- [x] Sonuç `hata` Sinyali; unittest CLI/ağ açmaz
- [x] 04 ile aynı frontier; 04 yapılırken birleştirilip kapatılabilir

## Comments

- 2026-09-16: Codex REVIEW-01 (ticket 01, engelleyici değil). Ticket 04 kapsamında ele alınmalı; 04 ile aynı frontier (02 bitince). 04 acceptance'a da madde eklendi. Kaynak: `.scratch/adr0001-hizalama/REVIEW-01.md`.
- 2026-09-16: agy implement tamamlandı (TDD, Ticket 04 ile birlikte). `kart_motoru.py` içindeki cozumle istisna yakalaması `(TypeError, ValueError, AttributeError)` olarak genişletildi. Sahte koşucu `[]` ve `"[]"` için Sürücü döngüsünün düşmediği ve `(Sinyal.HATA, "")` döndüğü `test_kart_motoru.py` ve `test_surucu_motor.py` ile doğrulandı.
