# Sürücü çekirdeği Python (kaçış kapılı)

Personel **Sürücü** dilimi (durum makinesi, dosya, CLI Motor çağrısı) **Python**da kalır.

## Neden (bugünün şekli değil; omurga uygunluğu)

Bu ürünün zor omurgası deterministik katmanın stokastik CLI Motor'u sürmesidir: dosya, subprocess, kapalı Sinyal, İş artefaktı. Bu iş Python'da çıkmaz değildir; 1k-10k satırda asıl risk dil değil, sınırların bulanıklaşmasıdır. Mevcut `bin/motorlar` ve şirket betikleri Python olduğu için çekirdek aynı dilde tutulur; bu uyum gerekçedir, tek başına "taşımak pahalı" gerekçesi değildir.

TypeScript sektörde UI/fullstack için yaygındır. Bu ADR TS'yi reddetmez: **şimdi Sürücü çekirdeğini TS'ye yeşilden yazmak**, mühendis ajanı tohumunu taşıma şantiyesine çevirir; asıl sorunu geciktirir.

## Kaçış / ne zaman dil yeniden açılır

Yeni dil (çoğunlukla TS) veya bilinçli çift dil ADR'si **ancak** şu tetiklerden biri somutlaşınca açılır:

1. İnsan yüzü (web UI) ürünün ağırlık merkezi olur ve tek tip/ekip yığını TS ister.
2. Tarayıcıda veya paylaşılan tip paketinde ajan+UI sözleşmesi zorunlu hale gelir.
3. Ölçülmüş şekilde Python çekirdek, işe alım / araç / entegrasyon yüzünden fiili engel olur.

Tetik gelmeden "hepsini TS yapalım" yok. Tetik gelince seçenekler: kenar TS + çekirdek Python, veya paket paket göç; hangisi ayrı ADR.

## Kapsam

Bu ADR yalnız personel Sürücü / Motor bağlama / ilgili test dilimini bağlar. İlerideki UI framework seçimi burada sabitlenmez.
