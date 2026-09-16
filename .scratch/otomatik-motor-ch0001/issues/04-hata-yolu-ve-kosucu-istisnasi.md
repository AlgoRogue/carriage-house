# 04: Fabrika Motoru ile hata yolu ve koşucu istisnası

**Spec:** `.scratch/otomatik-motor-ch0001/spec.md`

**What to build:**
03'teki bağlı giriş, Motor hata verdiğinde mevcut Sürücü kuralını korur: `motor_hatasi` → `hata` → `park`, tek çağrı, insan yok. Kanıt iki kaynak için: (1) adaptörün `hata` saydığı stdout, (2) koşucunun fırlattığı OSError benzeri istisna. İkisi de `motor_hatasi`'dir; Sürücü döngüsü patlamaz, durumu yine Sürücü yazar.

Mevcut SahteMotor hata yolu e2e'si kırılmaz. Bu bilet Kapı, yeniden deneme politikası veya gerçek CLI aramaz.

**Blocked by:** 03 Fabrika Motorunu mevcut isi_ilerlet mutlu yoluna bağla

**Status:** done

- [x] Fabrika Motor'u + hata stdout: tek `isi_ilerlet` çağrısı `hata`'dan geçip `park`'ta biter
- [x] Aynı bağlı yol, koşucu OSError benzeri fırlatırsa da `motor_hatasi` üretir ve `park`'ta biter
- [x] Red/patlama yok: Sürücü döngüsü ValueError ile düşmez; durum kaydını Motor değil Sürücü yazar
- [x] Mevcut SahteMotor hata yolu e2e'si geçmeye devam eder
- [x] Testler CLI/ağ açmaz; `python3 -m unittest discover -s tests`

## Comments

- 2026-09-15: yayınlandı (to-tickets). Durum: ready-for-agent.
- 2026-09-15: Hata stdout ve koşucu OSError `motor_hatasi` → `hata` → `park`. Döngü ValueError ile düşmez. SahteMotor hata yolu duruyor. `python3 -m unittest tests.test_surucu_motor` 4/4. `python3 -m unittest discover -s tests -p 'test_surucu*.py'` 33/33.
