# Sürücü Motor'u nasıl sürer

Deterministik **Sürücü**, stokastik **Motor**'u şöyle sürer: duruma göre ince bir **Prompt şablonu** seçer ve yalnız kendisi doldurur; kimlik ve yasaklar her çağrıda yeniden yazılmaz, Personel kaydı ile CLI kalıcı yönlendirmesinde (`CLAUDE.md`, skill, hook) kalır. Şablon bu adımın işini "şu **İş artefaktı** yolunu oku / şu yola yaz"a indirger. Sürücü Motor'u tek atım çağırır; CLI içinde araçlı çok tur olabilir. Kontrol akışı kapalı **Sinyal** sözlüğüyle yürür (ilk dilim: `basari` / `hata`); Motor metni Sinyal değildir. İçerik **İş artefaktı** olarak `personel/<numara>/isler/<is_id>/` altında dosyaya yazılır. `basari` ama kabul edilebilir artefakt yoksa Sürücü ilerletmez. Otonomi: tek çağrıda `park`'a kadar (Kapı sonra). Erken boş hafıza lift'i yok sayılır; Defter/eşleyici parçaları Motor girdisine sonradan girer.

## Considered Options

- Motor'a yalnız durum adı veya ham iş metni vermek (red: ne üreteceği belirsiz / kontrol zayıf)
- Her çağrıda rol ezberi bloğu (red: kimlik zaten personel + CLI zemininde çözülmüş)
- Artefakt metnini şablona yapıştırmak (red: adres/yol gömülür; Motor okur)
- Serbest metni kontrol sinyali saymak (red: kapalı sözlük)
- Her adımda şablonsuz yalnız CLAUDE.md (red: "bu adımda ne" deterministik kontrolü zayıflar; hibrit C seçildi)

## Consequences

- Mevcut CH-0001 `kart_motoru` (durum adını istem saymak) bu ADR ile uyumsuz; yeniden lift ayrı iş.
- Prompt şablon dosyaları personel altında durum adına göre tutulacak; henüz üretilmedi.
- `yeniden` sinyali ve Kapı ilk dilimde yok.
