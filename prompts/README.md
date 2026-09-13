# Prompt'lar — kamera karşısında, sırayla

Bu klasör, videoda A Şirketi'ni sıfırdan kurarken Claude Code'a verilen prompt'ların tamamıdır.
Her dosyada prompt metni **kamerada kullanıldığı hâliyle**, tek bir kod bloğunda durur; altında
beklenen çıktı ve varsa dikkat notu vardır.

Videodaki başlangıç durumu: `~/a-sirketi` klasörü açıldı, boş. Claude Code o klasörün içinde
başlatıldı (`cd ~/a-sirketi && claude`). Kod yazdırılmadı — betikler hazırdı (`~/a-sirketi-kit`),
Claude Code yalnızca kopyaladı ve belge dosyalarını yazdı.

> **Repoyu klonladıysan:** kopyalama prompt'ları (P1, P2) sana gerekmez — `bin/`, `skills/`,
> `sirket/`, `.claude/settings.json`, `tests/` ve `takimlar/_iskelet/` zaten yerinde. Prompt
> metinlerindeki `~/a-sirketi-kit` yolları kamerada öyle olduğu için olduğu gibi bırakıldı.

## Sıra

| # | Dosya | Ne yapar | Klonladıysan |
|---|---|---|---|
| P0 | [P00-claude-md.md](P00-claude-md.md) | `CLAUDE.md` — projeye kimlik ver | dosya hazır; kendin yazmak istersen kullan |
| P1 | [P01-klasor-git-anahtar.md](P01-klasor-git-anahtar.md) | git, `.gitignore`, `.env` | **atla** |
| P2 | [P02-iskelet.md](P02-iskelet.md) | betikler, bekçi hook'u, yetenekler, kimlik | **atla** |
| P3 | [P03-anayasa.md](P03-anayasa.md) | `ANAYASA.md` — beş madde | dosya hazır; kendi maddeni yazmak istersen kullan |
| P4 | [P04-uc-takim.md](P04-uc-takim.md) | üç takım klasörünü aç | üçü hazır; dördüncüyü açacaksan kullan |
| P5a | [P05a-x-icerik-takim.md](P05a-x-icerik-takim.md) | `x-icerik/takim.md` | hazır; şablon olarak kullan |
| P5b | [P05b-youtube-analiz-takim.md](P05b-youtube-analiz-takim.md) | `youtube-analiz/takim.md` | hazır; şablon olarak kullan |
| P5c | [P05c-twitter-icerik-takim.md](P05c-twitter-icerik-takim.md) | `twitter-icerik/takim.md` | hazır; şablon olarak kullan |
| P6 | [P06-ajan-dosyalari.md](P06-ajan-dosyalari.md) | `.claude/agents/<takim>.md` üret | çalıştır |
| P7 | [P07-kuru-kosu.md](P07-kuru-kosu.md) | kuru koşu — claude çağırmadan akış | çalıştır |
| P8 | [P08-gercek-kosu.md](P08-gercek-kosu.md) | gerçek koşu — telefondan link | çalıştır |
| P9 | [P09-dagitici.md](P09-dagitici.md) | dağıtıcı — zincir | çalıştır |
| P10 | [P10-github.md](P10-github.md) | commit ve GitHub | kendi kopyan için |

## Prompt yazmak yerine hazır dosyayı almak

Prompt'ların ürettiği her dosyanın son hâli bu repoda duruyor. Takıldığın ya da kamerada zaman
kaybetmek istemediğin yerde prompt'u atlayıp dosyayı doğrudan alabilirsin:

| Prompt | Hazır dosya |
|---|---|
| P0 | [`CLAUDE.md`](../CLAUDE.md) |
| P3 | [`ANAYASA.md`](../ANAYASA.md) |
| P5a · P5b · P5c | [`takimlar/x-icerik/takim.md`](../takimlar/x-icerik/takim.md) · [`youtube-analiz`](../takimlar/youtube-analiz/takim.md) · [`twitter-icerik`](../takimlar/twitter-icerik/takim.md) |
| P2 (kimlik ve yetenekler) | [`sirket/AJAN-KIMLIGI.md`](../sirket/AJAN-KIMLIGI.md) · [`sirket/YETENEKLER.md`](../sirket/YETENEKLER.md) · [`skills/`](../skills/) |

Videoda kullanılan yedek cümle buydu: "hazır olanı alıyorum". Prompt'u atlamak sistemi bozmaz —
tek kaynak dosyanın kendisidir, onu nasıl yazdığın değil.

Zaman daralırsa atlanabilecek tek takım `youtube-analiz`'dir (P5b): zinciri görmek için
`x-icerik` + `twitter-icerik` yeter.
