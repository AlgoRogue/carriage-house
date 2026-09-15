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
python3 -m unittest discover -s tests      # ağ yok, motor yok, para yok
python3 bin/ayar.py                        # tavanlar, evre: bos, .env var mı
python3 bin/kapi.py durum                  # "sıradaki: python3 bin/dongu.py …"
python3 bin/kos.py sistem-sevk --kuru      # evre bos → "ATLANIR"; istemi yine de basar
```

## Adım 3 · İnsanın dosyalarını oku (ve gerekiyorsa değiştir)

Bunlar senindir, ajan dokunamaz: `ANAYASA.md`, `hedef.md`, `kararlar.md`, `kapsam-disi.md`, `sema/`,
`takimlar/*/kurallar.md`, `bin/kapi.py`, `bin/dongu.py`. Tavanları `bin/ayar.py` başındaki sabitlerden değiştirirsin
(15 dk, 2 USD, 6 koşu/gün, 10 USD/gün). Motor tersini `bin/motorlar/__init__.py` içindeki `TERS_MOTOR`'dan.

## Adım 4 · Kuru prova — motor çağırmadan bütün evreleri gör

```bash
python3 bin/kapi.py talep "kapi.py durum komutu son üç geçmiş olayını da bassın"
python3 bin/kapi.py durum                  # inc-001 · evre: sozlesme
python3 bin/kos.py sistem-sevk --kuru      # KOŞAR; istemde okuma sırası, increment bağlamı, şema talimatı
python3 bin/kos.py sistem-insaat --kuru    # ATLANIR — evre insaat değil (doğru davranış)
python3 bin/kapi.py red "kuru prova"       # evreyi kapat
```

## Adım 5 · Gerçek döngü (para harcar: her adım bir CLI çağrısı)

Tek komut. İş küçük ve tek davranış olsun.

```bash
python3 bin/dongu.py "kapi.py durum komutu son üç geçmiş olayını da bassın"   # [--motor grok] [--deneme 2]
#   → sevk (claude) sözleşme keser → otomatik onay → inşaat (codex) → bekçi (claude)
#   → FAIL ise inşaat raporu okuyup düzeltir (en fazla 2 tekrar) → PASS ise durur, "İNSAN KARARI" der
cat increment/inc-00N/increment.md            # ne yapıldı (1 dakika)
cat increment/inc-00N/bekci-raporu.json       # kanıtlar
python3 bin/kapi.py yayinla                   # onay: kararlar.md satırı + git commit + evre kapanır
#   ya da
python3 bin/kapi.py revize "CSS de olsun"     # notunla sözleşmeye döner; sonra: python3 bin/dongu.py --devam
python3 bin/kapi.py red "vazgeçtim"           # kapatır
```

Döngü 5-30 dk sürer; terminali bloklar. Arkaya atmak için `nohup python3 bin/dongu.py "…" > /tmp/dongu.log &`,
evreyi `python3 bin/kapi.py durum` ya da `python3 bin/uygulama.py` → http://127.0.0.1:8765 ile izle.

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
| `atlandı — motor çözülemedi` | `motor: sozlesme`/`ters` ama sözleşme onaylanmamış; ya da bilinmeyen motor adı. |
| `son_sonuc: gecersiz` | Motor JSON döndürdü ama şemaya uymuyor; `durum.json.son_sebep` hatayı yazar. Sevk'i yeniden koştur. |
| `son_sonuc: red` | Katman A: boş kayıt, gizli veri ya da korunan dosyaya dokunma; ya da sevk/bekçi klasörü dışına yazdı. |
| `son_sonuc: hata` | Motor başlatılamadı, süre aştı ya da koşu kaydı yazılmadı; koşu kaydının sonunda ham çıktı var. |
| Bekçi raporunda `motor` yanlış | Ajan üreten motoru yazmış; sürücü geçersiz sayar. Ters motor `evre.json.motor.bekci`'de. |
