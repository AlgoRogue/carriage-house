# Videodaki tahta ve sunum panoları

Bölüm 1'de kamera karşısında üstüne çizilen tahtanın on panosu ve sunumun on sahnesi.
Görseller `docs/tahta/` ve `docs/sunum/` altında; videoda geçen sıralamayla.
Panolardaki sayılar (tur, kelime, USD) Selma'nın kendi şirketinin 10-11 Eylül 2026 koşu
kayıtlarından gelir; bu repodaki A Şirketi o kayıtları içermez, örnek koşu için
[ornek-kosu/](ornek-kosu/) klasörüne bak.

## Tahta — on pano

| # | Pano | Ne anlatıyor | Repoda karşılığı |
|---|---|---|---|
| 0 | ★ Neden şirket? | Sorun: her gün elle yapılan işler. Fikir: chatbot değil, şirket — her işin takımı, tanımı, kuralı, defteri var. Sekizinci koltuk (zevk, karar, ilişki, yayın düğmesi) insanda kalır. | `ANAYASA.md` §1 |
| 1 | On dört takım | Selma'nın gerçek şirketindeki on dört takım; bu bölümde yalnızca üçü + bekçi hook'u kuruluyor. | `takimlar/` |
| 2 | Üç anahtar, üç ajan | Telegram → x-icerik · Apify → youtube-analiz · fal → twitter-icerik. Zincir ve `.env`. | `.env.example`, [01-nasil-calisir.md](01-nasil-calisir.md) |
| 3 | Dört dosya | `takim.md` (kim) · `kurallar.md` (sınır) · `defter.md` (ders) · `durum.json` (kuyruk) · `kosu/` (kayıt). Defter = hafıza; ajan kendini geliştirir. | `takimlar/_iskelet/` |
| 4 | Anayasa | Beş madde: yayın düğmesi insanın · kaynaksız sayı yok · bekçi ayrı kafa · her koşunun tavanı var · defter ajanın, kural insanın. | `ANAYASA.md` |
| 5 | Döngü: tek prompt → onlarca tur | Link → `telegram_oku` → `kos.py` → ajan turları → bekçi → `durum.json` → dağıtıcı → twitter-icerik → bekçi → masa → insan. Dış döngü (vardiya) ve iç döngü (turlar) ayrımı. Tavanlar. | [02-dongu.md](02-dongu.md) |
| 6 | Bekçi | Üretici / ön kontrol / bekçi / kanıt. Gerçek bir red örneği. "Dürüstlük anı": OpenAI anahtarı yoksa bekçi aynı aileden (Haiku) ve bunu kayda yazar. | [03-bekci.md](03-bekci.md) |
| 7 | A şirketi — sıfırdan | Altı adım: klasör + git + `.env` → iskelet → ANAYASA → üç takım → döngüyü kapat → GitHub. Beklerken ne anlatılır, kanıt nedir. | `KURULUM.md`, `prompts/` |
| 8 | Bugün: çalışan / eksik | 11 Eylül sabahı dürüst envanter: gece döngüsü döndü, bekçi gerçek red verdi; eksikler (OpenAI anahtarı yok, 7/24 yok, video-edit elle). | — |
| 9 | Kapanış → Bölüm 2 | Sen de kur, repo linki, Bölüm 2'de kalan takımlar + gece→sabah döngüsü. | bu repo |

### Görseller

![Pano 0](tahta/pano-0.png)
![Pano 1](tahta/pano-1.png)
![Pano 2](tahta/pano-2.png)
![Pano 3](tahta/pano-3.png)
![Pano 4](tahta/pano-4.png)
![Pano 5](tahta/pano-5.png)
![Pano 6](tahta/pano-6.png)
![Pano 7](tahta/pano-7.png)
![Pano 8](tahta/pano-8.png)
![Pano 9](tahta/pano-9.png)

## Sunum — on sahne (CRT ekranlar)

Sunum, tahtayla aynı bilgiyi kesme görüntü olarak taşır: her sahne bir CRT fotoğrafının
ekranında yazar.

| # | Sahne |
|---|---|
| 0 | Açılış (boot) |
| 1 | Tez: "Her gün elle yaptığım işleri bir şirkete verdim; üç ajanını sizinle sıfırdan kuruyoruz." |
| 2 | On dört takım, üçü işaretli |
| 3 | Üç anahtar, üç ajan |
| 4 | Dört dosya |
| 5 | Anayasa |
| 6 | Döngü diyagramı (dış/iç döngü, tavanlar) |
| 7 | Bekçi |
| 8 | A şirketi — altı adım + komutlar |
| 9 | Bugün + kapanış |

![Sahne 0](sunum/sahne-0.png)
![Sahne 1](sunum/sahne-1.png)
![Sahne 2](sunum/sahne-2.png)
![Sahne 3](sunum/sahne-3.png)
![Sahne 4](sunum/sahne-4.png)
![Sahne 5](sunum/sahne-5.png)
![Sahne 6](sunum/sahne-6.png)
![Sahne 7](sunum/sahne-7.png)
![Sahne 8](sunum/sahne-8.png)
![Sahne 9](sunum/sahne-9.png)

## Tahta nasıl yapıldı

Tahta tek bir HTML dosyası: sürüklenen kartlar, kalem/ok/kutu çizimi, 0-9 tuşlarıyla pano
geçişi, amber fosfor teması. Bu repo tahtanın kendisini içermez; panolar headless Chrome ile
`?shot=1&pano=N` parametresiyle ekran görüntüsü olarak alındı. Robot görselleri ve CRT
fotoğrafları fal üzerinden üretildi.
