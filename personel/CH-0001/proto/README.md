# Cengizhan — Sürücü LOGIC prototipi

**PROTOTYPE / THROWAWAY:** geçici, üretim dışı keşif kodu.

## Açılış

`index.html` dosyasını çift tıklayarak tarayıcıda açın. İnternet, kurulum, sunucu veya derleme gerekmez. Paylaşmak için yalnızca bu HTML dosyası yeterlidir.

## Soru

Cengizhan’ın kilitli durum makinesi, ilk dilim `bos → is_alindi → planlaniyor → plan_hazir → delege_hazirlaniyor → paket_hazir → park` yolunu sapmadan koşturuyor mu; durumu yalnız Sürücü mü yazıyor ve Motor yalnızca planlaniyor/delege_hazirlaniyor’da kavramsal mı?

## Kullanım ve model

- Serbest denemede mevcut durumdan yasal geçişler düğme olarak görünür.
- Rehberli sekmeler: mutlu yol → park, yasadışı geçiş denemesi, planlanıyor → hata → park. Sekme seçmek makineyi sıfırlar; serbest bir işlem rehberi sonlandırır.
- Motor durumlarında “Motor çıktısı geldi” sinyali üzerine Sürücü sabit iskelet hedefini yazar. “Motor hatası geldi” sinyali hata durumuna götürür. Motor hedef seçmez ve gerçek çağrı yapılmaz.
- Reddedilen işlemler durumu değiştirmez. Durum paneli ve bellekteki hareket listesi her işlemden sonra güncellenir.
- Park bu dilimin sonudur. Kaynaktaki park → usta_atandi ve sonraki geçişler gömülü iskelette korunur, ancak prototipin etkin geçişleri arasında değildir.

## Taşınabilir makine

İstenen tek dosya biçimi nedeniyle ayrı JS dosyası yoktur. `index.html` içindeki `surucu-makine` kimlikli ilk script bloğu bağımsız saf modüldür; DOM, depolama, zamanlayıcı veya ağ erişimi içermez. İkinci script geçici sayfa ve Sürücü temsilcisidir.

`SurucuMakine.createMachine()` şu API'yi verir:

- `getState()` — geçerli durum kimliği.
- `listLegalTransitions()` — etkin dilimdeki kaynak geçişlerinin kopyaları; Motor durumlarında sinyal gerekir.
- `applyTransition(to)` — Sürücü geçişi; yasadışı hedefleri ve sinyalsiz Motor çıkışlarını reddeder.
- `dispatch('motor_ciktisi' | 'motor_hatasi')` — taklit sinyali alır; Sürücü hedefi belirler. Diğer durumlardaki sinyaller reddedilir.
- `reset()` — durumu `bos` yapar.

Geçiş/sinyal sonucu `ok`, `state` ve `message` içerir. Makinenin durumu dışarıdan yazılamaz. `getSkeleton()` kaynak iskeletin bağımsız kopyasını döndürür. İskelet, `../aksiyon-iskeleti.json` dosyasından bütünüyle gömülmüştür; kaynak değişirse bu anlık kopyanın elle güncellenmesi gerekir.

## Kapsam dışı ve değerlendirme

Kapı, defter, hafıza, gerçek Motor çağrısı, gerçek Sürücü servisi/kodu, CLI, usta ataması, park sonrası yürütme, otomatik yeniden deneme ve kalıcı kayıt yoktur. Oturum hareketleri yalnızca sayfa belleğindedir.

Bu dosya soruyu elle keşfetmek için hazırlanmıştır; doğrulanmış ürün kararı veya başarılı çalıştırma iddiası değildir. Test, unittest veya smoke çalıştırılmadı. Commit, dal, issue veya kapsam dışı gerçek kod değişikliği yapılmadı. Kullanıcının kapsam ve commit yasağı, becerinin üretim koduna aktarma ve commit ile yakalama adımlarının yerine geçer.
