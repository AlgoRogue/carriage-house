# Modüler monolit (şimdi); mikroservis sonra

Carriage House **şimdi** modüler monolit: tek repo, klasör/paket sınırları, ayrı process veya ağ servisi yok. İş dosya + CLI ile aynı makinede yürür.

## Neden mikroservis şimdi değil

- Ortada henüz net sınırlı, bağımsız ölçeklenen bir yük yok; olan şey tek ajanın durum makinesi + CLI çağrısı.
- Servis bölmek: ağ, sürüm, gözlem, hata sınırı demektir. Bunlar bugünkü asıl soruyu (Sürücü Motor'u nasıl sürer; mühendis ajanı nasıl tohumlanır) geciktirir.
- Ekip/operasyon maliyeti yüksek; tek geliştirici + CLI ajanları için erken.

## Ne zaman geri gelebilir

Mikroservis (veya en azından ayrı process) **ancak** şunlardan biri somutlaşınca yeniden açılır:

1. İki bileşen farklı hızda ölçeklenmek / ayrı deploy edilmek zorunda kalır (ölçülmüş ihtiyaç).
2. Güvenlik veya yetki sınırı process izolasyonu ister (Kapı + çok kiracı vb.).
3. Bir alt sistemin çökmesi tüm monolitı düşürüyordur ve izolasyon şarttır.
4. Ayrı dil/runtime zorunlu hale gelir ve sınır HTTP/event ile netleşir.

O güne kadar "mikroservis" kapsam dışı değil; **tetik koşullu ertelenmiş**. Tetik gelince yeni ADR eskiyi supersede eder.

## Şekil

Tek repo; paket sınırları ADR-0004 + `personel/CH-0001/bin/README.md`.

## Import / path

Simdi `sys.path` ile `bin/` ve personel `bin` ekleniyor. Bu bilincli borc (G8). Hizalama ticket'larindan birinde gercek paket importuna gecilir; bu ADR'nin monolit karari path hack'i onaylamaz, sadece "servis yok"u sabitler.
