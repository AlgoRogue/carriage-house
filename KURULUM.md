# KURULUM — sıfırdan ilk uçtan uca döngüye

Beş adım. İlk dördü para harcamaz; beşinci adım gerçek motor çağırır.

## Adım 1 · Motorlar ve klon

```bash
which claude agy codex grok     # dördü de yolda olmalı; eksik olan motor koşuda "başlatılamadı" der
git clone <repo> a-sirketi && cd a-sirketi
cp .env.example .env            # bugün yalnız VARSAYILAN_MOTOR var; motorlar kendi oturumunu kullanır
```

Her motorun kendi oturumu açık olmalı (`claude`, `agy`, `codex`, `grok` — hangisini kullanıyorsan onda bir
kez etkileşimli girip oturum aç). Sürücü anahtar yönetmez; `.env` yalnız takım dosyasının
`gerekli_anahtarlar:` alanında istenen değişkenler içindir.

## Adım 2 · Ayakta mı

```bash
python3 -m unittest discover -s tests      # 43 test — ağ yok, motor yok, para yok
python3 bin/ayar.py                        # tavanlar, evre: bos, .env var mı
python3 bin/kapi.py durum                  # "sıradaki: python3 bin/kapi.py talep …"
python3 bin/kos.py sistem-sevk --kuru      # evre bos → "ATLANIR"; istemi yine de basar
```

## Adım 3 · İnsanın dosyalarını oku (ve gerekiyorsa değiştir)

Bunlar senindir, ajan dokunamaz: `ANAYASA.md`, `hedef.md`, `kararlar.md`, `kapsam-disi.md`, `sema/`,
`takimlar/*/kurallar.md`, `bin/kapi.py`. Tavanları `bin/ayar.py` başındaki sabitlerden değiştirirsin
(15 dk, 2 USD, 6 koşu/gün, 10 USD/gün). Motor tersini `bin/motorlar/__init__.py` içindeki `TERS_MOTOR`'dan.

## Adım 4 · Kuru prova — motor çağırmadan bütün evreleri gör

```bash
python3 bin/kapi.py talep "kapi.py durum komutu son üç geçmiş olayını da bassın"
python3 bin/kapi.py durum                  # inc-001 · evre: sozlesme
python3 bin/kos.py sistem-sevk --kuru      # KOŞAR; istemde okuma sırası, increment bağlamı, şema talimatı
python3 bin/kos.py sistem-insaat --kuru    # ATLANIR — evre insaat değil (doğru davranış)
python3 bin/kapi.py red "kuru prova"       # evreyi kapat
```

## Adım 5 · İlk gerçek döngü (para harcar: her koşu bir CLI çağrısı)

Talep küçük olsun — bitiş çizgisi "döngü bir kez uçtan uca işledi"dir, büyük özellik değil.

```bash
python3 bin/kapi.py talep "kapi.py durum komutu son üç geçmiş olayını da bassın"

python3 bin/kos.py sistem-sevk            # claude → increment/inc-001/sozlesme.json + increment.md
cat increment/inc-001/increment.md        # 1 dakikada oku
python3 bin/kapi.py onayla                # KAPI 1 — motor_adayi'nı kabul; ya da --motor grok
python3 bin/kapi.py durum                 # evre: insaat · motor: inşaat=codex bekçi=claude

python3 bin/kos.py sistem-insaat          # codex → kod + teslim.json; kapsam sapması ölçülür
cat increment/inc-001/teslim.json
git diff --stat                           # inşaatın gerçekten dokunduğu dosyalar

python3 bin/kos.py sistem-bekci           # claude → bekci-raporu.json PASS|FAIL
cat increment/inc-001/bekci-raporu.json

python3 bin/kapi.py yayinla               # KAPI 2 — kararlar.md'ye satır; evre: yayinlandi
git add -A && git commit -m "inc-001: …"  # commit senin işin; ajan commit atmaz
```

FAIL gelirse: `kapi.py red "…"` ile kapat ve yeni talep aç, ya da `sozlesme.json`'u düzeltip
(`chmod 644 increment/inc-001/sozlesme.onayli.json` gerekmez — taslağı düzeltirsin) evreyi elle `sozlesme`'ye
alıp yeniden onayla. `red` sebebi `takimlar/sistem-sevk/durum.json`'a düşer; sevk bir sonraki koşuda okur.

## Motor duman testi (isteğe bağlı, ücretli)

Bir motorun JSON çıktısının adaptörle uyuştuğunu doğrulamak için tek satırlık koşu:

```bash
python3 - <<'EOF'
import subprocess, sys; sys.path.insert(0, "bin"); import motorlar
for ad in ("claude", "agy", "codex", "grok"):
    m = motorlar.motor_al(ad)
    sema = {"type": "object", "properties": {"selam": {"type": "string"}}, "required": ["selam"]}
    ayar = {"model": None, "effort": None, "araclar": ["Read"], "butce_usd": 0.1, "json_sema": sema,
            "sema_dosyasi": "/tmp/s.json", "maks_tur": 2}
    open("/tmp/s.json", "w").write(__import__("json").dumps(sema))
    try:
        r = subprocess.run(m.komut('Yalnız {"selam":"merhaba"} döndür.', ayar), capture_output=True, text=True, timeout=120)
        print(ad, m.cozumle(r.stdout))
    except Exception as e:
        print(ad, "hata:", e)
EOF
```
`yapisal` alanı `{"selam": "merhaba"}` dönmeli. Dönmüyorsa o motorun adaptöründe (`bin/motorlar/<ad>.py`)
`cozumle` alan adlarını düzelt — grok için `METIN_ALANLARI` listesi bunun için var.

## Sorun giderme

| Belirti | Sebep / çözüm |
|---|---|
| `atlandı — evre uyuşmuyor` | Takım yanlış evrede çağrıldı. `kapi.py durum` sıradaki komutu söyler. |
| `atlandı — motor çözülemedi` | `motor: sozlesme`/`ters` ama Kapı 1 geçilmemiş; ya da bilinmeyen motor adı. |
| `son_sonuc: gecersiz` | Motor JSON döndürdü ama şemaya uymuyor; `durum.json.son_sebep` hatayı yazar. Sevk'i yeniden koştur. |
| `son_sonuc: red` | Katman A: boş kayıt, gizli veri ya da korunan dosyaya dokunma; ya da sevk/bekçi klasörü dışına yazdı. |
| `son_sonuc: hata` | Motor başlatılamadı, süre aştı ya da koşu kaydı yazılmadı; koşu kaydının sonunda ham çıktı var. |
| Bekçi raporunda `motor` yanlış | Ajan üreten motoru yazmış; sürücü geçersiz sayar. Ters motor `evre.json.motor.bekci`'de. |
