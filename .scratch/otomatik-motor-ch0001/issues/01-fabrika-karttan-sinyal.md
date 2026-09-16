# 01: Karttan Motor fabrikası: tek çağrıda Sinyal

**Spec:** `.scratch/otomatik-motor-ch0001/spec.md`

**What to build:**
Cengizhan'ın Personel kartını okuyan bir fabrika. Karttaki Motor (`cli` + `model`) ile kayıtlı adaptörü çözer ve Sürücü'nün beklediği Motor'u döner: durum adını alır, `motor_ciktisi` veya `motor_hatasi` Sinyali verir.

Bu bilet tek bir mutlu çağrıyı kanıtlar. Kart CH-0001'inki gibi `claude` / `sonnet` taşır. Koşucu enjekte edilir, hazır başarı çıktısı döner, CLI açılmaz. Koşucuya giden komutun ilk token'ı karttaki `cli`'dir; model karttan komuta yansır. Kart dosyası yazılmaz. Durum makinesi ve `isi_ilerlet` bu bilette yok.

**Blocked by:** None (can start immediately)

**Status:** done

- [x] Fabrika Personel kartı arka yüzündeki `motor.cli` ve `motor.model` alanlarını okur
- [x] Dönüş değeri `callable(durum) -> Sinyal` sözleşmesine uyar
- [x] Enjekte koşucu kullanılır; unittest CLI veya ağ açmaz
- [x] CH-0001 benzeri kart (`claude`, `sonnet`) + başarı stdout → `motor_ciktisi`
- [x] Koşucuya giden komutun ilk token'ı `cli` değeridir; model karttan komutta görünür
- [x] Kart dosyası çağrı sonrası değişmez
- [x] Test `tests/` altında, `python3 -m unittest discover -s tests` ile ağsız koşar

## Comments

- 2026-09-15: yayınlandı (to-tickets). Durum: ready-for-agent.
- 2026-09-15: `motor_uret(kart, kosucu)` kırmızı-yeşil. CH-0001 kartı (`claude`/`sonnet`) + sahte koşucu başarı stdout → `motor_ciktisi`; komutun ilk token'ı `claude`, model karttan. Kart yazılmaz. `python3 -m unittest tests.test_kart_motoru` 5/5 geçti.
