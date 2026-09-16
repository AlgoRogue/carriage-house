# 02: Kayıtlı Motor adları ve çözülemeyen kart

**Spec:** `.scratch/otomatik-motor-ch0001/spec.md`

**What to build:**
Aynı fabrika, karttaki `cli` kayıtlı dört Motor adından (`claude`, `agy`, `codex`, `grok`) hangisi olursa olsun çözülür. Her ad için enjekte koşucu, o CLI'nin ilk token'ını görür; sahte başarı çıktısı `motor_ciktisi`, sahte hata/bozuk çıktı `motor_hatasi` üretir.

Bilinmeyen `cli`, veya eksik/bozuk `arka_yuz.motor`, koşucu hiç çağrılmadan başarısız olur. Skill listesi okunmaz. Bu bilet Sürücü zincirini açmaz; yalnız çözümleme ve adaptör-Sinyal sözleşmesi.

**Blocked by:** 01 Karttan Motor fabrikası: tek çağrıda Sinyal

**Status:** done

- [x] `cli` değeri `claude`, `agy`, `codex`, `grok` olan kartlar fabrikadan Motor üretir
- [x] Her kayıtlı ad için koşucuya giden komutun ilk token'ı o `cli`'dir
- [x] Her kayıtlı ad için sahte başarı stdout → `motor_ciktisi`; hata veya bozuk stdout → `motor_hatasi`
- [x] Bilinmeyen `cli` koşucu çağrılmadan başarısız olur
- [x] Eksik veya bozuk `arka_yuz.motor` (cli yok, motor nesnesi yok) koşucu çağrılmadan başarısız olur
- [x] Karttaki skill listesi bu davranışa etki etmez
- [x] Testler CLI spawn etmez; `python3 -m unittest discover -s tests` ile ağsız koşar

## Comments

- 2026-09-15: yayınlandı (to-tickets). Durum: ready-for-agent.
- 2026-09-15: Dört kayıtlı cli çözülür; başarı/hata/bozuk stdout Sinyal eşlemesi; bilinmeyen cli ve bozuk kart koşucudan önce ValueError. Skill listesi komuta girmez. `python3 -m unittest tests.test_kart_motoru` 5/5 geçti.
