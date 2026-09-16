# 01: Boş başlangıç: CH-0001 Ajan hafızası okunur, kayıt yok

**Spec:** `.scratch/ajan-hafiza-ch0001/spec.md`

**What to build:**
Cengizhan'ın Personel kaydı dizininde Ajan hafızası vardır ve boştur. Bir çağıran depo API'si ile okur ve hiç kayıt almaz. Bu, "boş ama yazılabilir" prototipin okunabilir yarısıdır: depo yok-sayılmaz, eksik dosya da değildir; boş liste döner.

Yazma, ikinci kayıt, Sürücü bağlama bu bilette yok.

**Blocked by:** None (can start immediately)

**Status:** done

- [x] CH-0001 Personel kaydı dizininde kalıcı Ajan hafızası dosyası vardır; `kayitlar` boş listedir
- [x] `HafizaDeposu.oku()` o listeyi döner (boş başlangıç `[]`)
- [x] Varsayılan yol, enjekte yol verilmediğinde bu personel dosyasıdır
- [x] Unittest ağ, CLI veya Motor açmadan boş okumayı kanıtlar (`python3 -m unittest discover -s tests`)
- [x] Bu bilet Sürücü / Motor / `isi_ilerlet` çağırmaz ve onları import etmez
- [x] `aksiyon-iskeleti.json`, `kart.json`, `durum.json` yazılmaz

## Comments

- 2026-09-15: yayınlandı (to-tickets). Durum: ready-for-agent.
- 2026-09-15: `personel/CH-0001/hafiza.json` boş `{"kayitlar": []}`. `HafizaDeposu()` varsayılan yolda `oku()` → `[]`. Sürücü / Motor / `isi_ilerlet` bağlanmadı. `python3 -m unittest tests.test_hafiza_deposu` 3/3 (`test_bos_baslangic_oku_bos_liste_doner` dahil).
