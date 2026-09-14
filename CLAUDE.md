# A Şirketi

> Farklı yapay zekâ CLI'larını (claude, agy, codex, grok) yöneten deterministik üst katman. Üç ajan sistemi
> bir increment ileri götürür ve durur; yayın düğmesi insanda (iki kapı).

## Ne bu
- **sistem-sevk** — insanın tek cümlesini dondurulmuş increment sözleşmesine çevirir (`claude`).
- **sistem-insaat** — onaylı sözleşmeyi koda işler; motor sözleşmeden gelir (`codex` varsayılan; agy/grok/claude).
- **sistem-bekci** — sözleşmeye karşı kanıtla PASS/FAIL; motor üretenin tersi (`bin/motorlar/TERS_MOTOR`).
- **sürücü** (`bin/kos.py`) — evre kontrolü, motor çözümü, şema zorlamalı çıktı, git ile kapsam ölçümü, evre geçişi.
- **kapı** (`bin/kapi.py`) — insanın düğmeleri: `talep · onayla (Kapı 1) · yayinla (Kapı 2) · red · durum`.
- **bekçi katman A** (`bin/bekci.py`) — LLM'siz: boş kayıt, gizli veri, insanın dosyasına dokunma → red.

Döngü: `kapi talep → kos sistem-sevk → kapi onayla → kos sistem-insaat → kos sistem-bekci → kapi yayinla`.
Sürücü bir sonraki takımı asla kendisi başlatmaz.

## Okuma sırası (her ajan, her koşuda)
1. `ANAYASA.md` — değişmez çerçeve
2. `sirket/AJAN-KIMLIGI.md` — kimsin, döngüdeki yerin
3. `hedef.md` · `kararlar.md` · `kapsam-disi.md` — SoT
4. `takimlar/<takim>/kurallar.md` — takımın sınırları
5. `takimlar/<takim>/takim.md` — koşu adımları ve çıktı sözleşmesi
6. `increment/evre.json` ve `increment/<id>/` — aktif işin artefaktları

## Klasör yapısı
```
bin/                  kos.py · kapi.py · bekci.py · sema.py · ayar.py · agents_uret.py · motorlar/<ad>.py
sema/                 increment-sozlesmesi · teslim · bekci-raporu · evre (.schema.json) — dondurulmuş
increment/            evre.json · <id>/{sozlesme.json, sozlesme.onayli.json, increment.md, teslim.json, park.md, bekci-raporu.json}
takimlar/<takim>/     takim.md · kurallar.md · defter.md · durum.json · kosu/
tests/                python3 -m unittest discover -s tests — ağ yok, motor yok
.env                  anahtarlar — asla commit'e girmez
```
`defter.md` ajanındır, `kurallar.md` insanın. Koşu kaydı `kosu/`; artefakt `increment/<id>/`.

## Bu repoda Claude Code ile çalışırken
- Kod Türkçe adlandırılır, stdlib kullanır, ağ çağırmaz; test `unittest` ile koşar.
- Bir takım için değişiklik istenirse önce `takim.md` (kaynak), sonra `agents_uret.py` `.claude/agents/`'ı üretir.
- Yeni motor = `bin/motorlar/<ad>.py` (`YETENEK`, `komut`, `cozumle`) + `MOTORLAR`/`TERS_MOTOR` + test.

## Yasaklar
- `.env` okuma, açma, ekrana basma — anahtar yalnız süreç ortamından gelir
- Ajan olarak commit/push/tag; sosyal hesaba yazma; mail; dış servise yazma
- Para harcama — abonelik, satın alma, tavan dışı ücretli çağrı
- `ANAYASA.md`, `hedef.md`, `kararlar.md`, `kapsam-disi.md`, `sema/`, `kurallar.md`, `sozlesme.onayli.json`,
  `bin/kapi.py` değiştirme — hepsi insanındır
