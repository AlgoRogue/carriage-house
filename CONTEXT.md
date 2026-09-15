# Carriage House

Deterministik bir üst katmandan, kimlikli ajanlara iş veren ve motor olarak yapay zekâ CLI’larını kullanan şirket benzeri sistemin dil modeli.

## Language

### Çekirdek

**Ajan**:
Personel kartı ve personel dosyası ile tanımlanan iş birimi; karar iskeleti deterministiktir.
_Avoid_: Takım, agent (İngilizce genel kullanım), yapı

**Personel kartı**:
Ajanın kısa, taşınabilir kimlik kaydı (ön yüz + arka yüz). İmza, birim/rol görünürlüğü ve kapı geçişi için personel numarasına dayanır.
_Avoid_: Kimlik kartı (eski geçici ad; artık Personel kartı), rozet, geçici token

**Personel kartı ön yüzü**:
Kartın sabit tanıtım yüzü: referans görsel, ad, personel numarası, bağlı **Birim**, birimdeki **Rol**.
_Avoid_: Profil özeti (belirsiz)

**Personel kartı arka yüzü**:
Kartın yetenek ve çalışma bağlama yüzü: skill listesi ile o an atanmış **Motor** (CLI + model). Motor değiştirilirse yeni değer burada kalır; her işte varsayılana dönülmez.
_Avoid_: Config, runtime flags (genel yazılım)

**Personel numarası**:
Personel kartındaki benzersiz numara; ajanın imzasıdır. İşleri bununla imzalar, kendisine ait işleri ayırt eder; kapı geçişinde kimlik olarak kullanılır.
_Avoid_: ID (tek başına belirsiz), UUID (uygulama detayı), session id, Kimlik numarası (eski ad)

**Personel dosyası**:
Ajana dair ayrıntılı kayıt; personel kartında yer almayan uzun açıklamalar, geçmiş, kısıtlar ve diğer dosya bilgileri burada durur. Aynı personel kaydı dizininde tutulur.
_Avoid_: CV, bio, README (genel)

**Personel kaydı dizini**:
Bir ajana ait personel kartı, personel dosyası, kapı yetkileri ve ilgili ayrıntılı kayıtların durduğu yer.
_Avoid_: Home folder, profil klasörü (belirsiz)

**Kapı yetkileri**:
Personel kaydı dizininde, personel dosyasından ayrı duran yetki kaydı; ajanın hangi kapılardan geçebileceğini listeler.
_Avoid_: ACL (genel yazılım), izinler (belirsiz)

**Birim**:
Şirket içi örgüt birimi; ajan personel kartının ön yüzünde bir birime bağlıdır.
_Avoid_: Takım (eski prototip klasör dili), departman (eşanlam; canonical Birim), squad

**Rol**:
Personel kartının ön yüzünde, ajanın bağlı olduğu birim içinde üstlendiği sabit görev.
_Avoid_: Geçici atama, şapka, görev etiketi

**Motor**:
Bir ajanın işi üretmesi için kullandığı CLI aracı ile o araçtaki modelin çifti. Personel kartının arka yüzünde görünür; değiştirilebilir ve değiştirildikten sonra korunur.
_Avoid_: CLI (tek başına), model (tek başına)

**Orkestrasyon**:
İşlerin sırası, evreleri, tavanları ve ajanlar arası sinyalleri yöneten deterministik üst katman.
_Avoid_: Şirket (metafor), framework

**Sürücü**:
Deterministik yürütücü: durumu okur, aksiyon iskeletine göre adımı seçer, gerekirse Motor’u çağırır, sinyali yakalar, sonraki durumu yazar. Kararı LLM vermez.
_Avoid_: Harness (tek başına; AI harness ile karışır), AI harness, agent loop (belirsiz)

**İş**:
Bir ajana verilen görev birimi; prototipteki increment ile aynı kavramdır.
_Avoid_: Görev, task, increment (eş anlamlı; canonical terim İş)

**Sinyal**:
Motorun veya ajanın ürettiği, deterministik katmanın yakaladığı durum bildirimi (ör. tamam, hata).
_Avoid_: Mesaj, log, event (genel yazılım anlamında)

**Skill**:
Personel kartının arka yüzünde listelenen, ajanın yapabildiği adlandırılmış yetenek.
_Avoid_: Yetenek (serbest paragraf), capability (İngilizce genel)

### Hafıza ve eşleme

**Ajan hafızası**:
Tek bir ajana ait kalıcı bilgi katmanı (depo); anlamsal eşleyici buraya bakar.
_Avoid_: memory (İngilizce genel), defter.md (defter hafızanın kendisi değildir)

**Defter**:
Ajan hafızasının sıcak yüzü; ajan ihtiyaç duyduğu context’i buradan okur. Hafızanın kendisi değildir.
_Avoid_: Ajan hafızası, log, koşu kaydı

**Orkestrasyon hafızası**:
Orkestrasyona ait, ajan hafızalarından ayrı kalıcı bilgi katmanı.
_Avoid_: Ortak hafıza, global memory

**Anlamsal eşleyici**:
Bir iş ile ilgili hafıza arasında benzerlik arayan stokastik ada; bulduğu parçaları deterministik ajana girdi olarak verir. Deterministik katmanın yerine geçmez.
_Avoid_: Gömülü model, embedding, RAG

### Denetim ve insan sınırı

**Kapı**:
Bir eylemin yapılmasından önce personel numarası ve **Kapı yetkileri** ile sorulan yetki kontrol noktası (bu personele bu eylem için izin var mı?).
_Avoid_: Evre adımı (iş akışı geçişi; Kapı değil), Gate 1/Gate 2 (eski prototip), insan yayını (ayrı kavram — henüz adlandırılmadı)

**Kuyruk**:
Önceden belirlenmiş veya olayla eklenen işlerin sırayla ilerlemesi.
_Avoid_: Pipeline, backlog

## Relationships

- Bir **Ajan** bir **Personel kaydı dizini** içinde **Personel kartı**, **Personel dosyası** ve **Kapı yetkileri** taşır.
- **Personel kartı ön yüzü**: görsel, ad, **Personel numarası**, **Birim**, **Rol**.
- **Personel kartı arka yüzü**: **Skill** listesi + mevcut **Motor**.
- **Kapı yetkileri**, personel dosyasından ayrı bir kayıttır; aynı dizindedir.
- **Orkestrasyon** **İş**leri **Kuyruk**ta sıraya koyar ve **Sinyal**leri yönlendirir.
- **Sürücü** aksiyon iskeletini işletir; **Motor** yalnız sürücünün açtığı adımda çalışır; sonraki durumu yalnız sürücü yazar.
- **Anlamsal eşleyici**, **İş** ile hafızalar arasında köprü kurar; **Orkestrasyon** anlamsal arama yapmaz.

## Flagged ambiguities

- **Kapı** = yetki kontrolü (A) kilitlendi; hangi eylemlerin kapı sayılacağı envanteri açık.
- Evre geçişi ve insan yayını Kapı değil; ayrı adları henüz yok.
- Eski prototip adı **bekçi**: henüz domain terimi değil; bir ajana **Rol** olarak verilecek, isim değişebilir.
- Personel dosyasının zorunlu bölümleri henüz envanterlenmedi.
- **Defter** ile **Ajan hafızası** ayrımı kilitli; Parça 1’de ikisi de yok (bilinçli).
