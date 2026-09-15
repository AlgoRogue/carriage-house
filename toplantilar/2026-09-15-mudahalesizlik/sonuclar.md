# Müdahalesizlik ve öncelikler — çalışma notu

> Tarih: 2026-09-15  
> Kaynak: sohbet (AR-GE / carriage-house tasarım konuşması)  
> Durum: karar taslağı — kod değişikliği yok; insan aksini söyleyene kadar uygulama yok

## Öncelik (şimdi)

1. Sistem, insan başında olmadan çalışabilsin.
2. Önceden belirlenmiş işleri sırasıyla yapsın.
3. Kurulum ve işletme sorunsuz olsun; ilerlemenin sürekli insan müdahalesine bağlı olduğu bir sistem istenmiyor.
4. UI revizyonu ertelendi (mevcut UI beğenilmiyor; şimdilik ilerletilmeyecek).
5. Yapının daha fazla şekillendirilmesi sonra.

## Müdahalesizlik çerçevesi (üzerinde uzlaşılan orta yol)

Müdahalesizlik = kör uçmak değil. Günlük koşu otomatik; frenler ve görünürlük her an insanda.

| Katman | Davranış |
|--------|----------|
| İş kuyruğu | İnsan yokken sıradaki iş → koş → ölç → sonrakine geç (adım adım insan basmaz) |
| Canlı durum | Hangi iş, hangi evre, son sonuç her an okunabilir |
| Otomatik durma | FAIL / tavan / şüpheli sapmada kuyruk durur; devam için insan |
| Geri alınamaz kapı | Dışarı yayın / kalıcı karar insanda kalır (veya açıkça “otomatik yayın” denmiş işlerde kapatılabilir) |

## Açık / emin olunmayan

- Tam akışın her ayrıntısı henüz kilitli değil; insan, tüm kontrolü kaldırmanın “nereden tutarım?” riskini görüyor.
- Bu yüzden orta yol: otomatik ilerleme + görünür durum + otomatik fren + geri alınamaz kapı.

## Çalışma kuralı (bu aşama)

- İnsan aksini belirtmedikçe **hiçbir dosyada geliştirme / değişiklik yapılmaz**.
- Bu konuşmadan çıkan sonuçlar **yalnızca bu tür not dosyalarına** yazılabilir.
- CLI kurulumları (claude, agy, codex, grok) kutuda hazır; duman testleri geçti. Gerçek `dongu` / üretim koşusu şimdilik istenmedi.

## Sonraki (insan söyleyince)

- Önceden belirlenmiş ilk iş kuyruğunun içeriğini netleştirmek
- Otomatik durma koşullarını somutlaştırmak (hangi FAIL, hangi tavan)
- “Geri alınamaz kapı” listesini kilitlemek
- Ancak o zaman küçük geliştirme parçalarına bölmek

---

## Ajan modeli (2026-09-15 devam)

### Sorun (mevcut)

- Sistem agent’tan çok **yapılardan** oluşuyor.
- `takimlar` parçalarının kimliği / “ruhu” yok; isteklerin bir kısmını karşılasa da kimlik kartı yok.

### Hedef ayrım

| Kavram | Ne | Değişir mi? |
|--------|-----|-------------|
| **Ajan** | Kimlik kartı: ad, kimlik, sorumluluk, yetenekler (“ruh”) | Sabit rol/kimlik; orkestrasyondan bağımsız varlık |
| **Motor** | CLI aracı + o araçtaki model | İstenince değiştirilebilir; ajan kimliğine bağlı değil |
| **Orkestrasyon** | Kuyruk, evre, kapılar, tavanlar, sinyal yönlendirme | Deterministik |

CLI ile iş yaptırmak zaten kanıtlandı; eksik olan ajanın kimlikli, motordan bağımsız tanımı.

### Determinizm kuralı (ajan dahil)

- Ajan da orkestrasyon gibi **deterministik** olmalı.
- Karar yapısı stokastik değil: durumlara karşı alınacak aksiyon **belirli bir yapı içinde** işletilir.
- Deterministik katman **anlamsal ilişki kurmaz**.

### Hafıza

- Her ajanın **kendi hafızası** var.
- Orkestrasyonun **ayrı hafızası** var.

### İş akışı (ajan dizininde JSON belirmesi)

1. Ajan dizininde iş JSON’u oluşur.
2. **Gömülü (embedded) model** — iş metni ile hafıza katmanı arasında anlamsal eşleşme arar.
3. Eşleşen bilgi varsa deterministik ajana **girdi** olarak verilir.
4. Ajan işi CLI’ya devrederken bu bilgiyi **context’e** basar; kalanını CLI halleder.
5. CLI, deterministik yapının yakalayabileceği bir **sinyal** bırakır (ör. işlem tamam, hata alındı).
6. İleride: hata mesajları sınıflanabilir; deterministik yapı hata türüne göre aksiyon seçer.
7. Sinyale göre ajan aksiyon alır — örn. “tamam” → bekçiye “bana verilen işi tamamladım” sinyali.

### Stokastik ada (şimdilik)

- Yalnızca hafıza ↔ iş **anlamsal eşlemesi** (embedded model).
- Üretim / yargı CLI’da; iskelet + ajan + orkestrasyon deterministik.

### Not

- Kod / uygulama yok; yalnızca tasarım kaydı.
