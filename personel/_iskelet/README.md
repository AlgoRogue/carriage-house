# _iskelet

Bu klasör, bir personel kaydı açarken kopyalanacak şablondur.

## Kullanım

`personel/_iskelet/` içeriğini `personel/<personel_numarasi>/` altına kopyala ve `kart.json` ile `dosya.md`'yi doldur.

## İçerik

- `kart.json` — ön yüz (kimlik) ve arka yüz (motor/skilller) alanları
- `dosya.md` — görev tarifi, yasaklar, çalışma notları, açık maddeler
- `kurallar.md` — sert sınırlar (dosya.md'den ayrı)

## Bilinçli olarak dışı

Kapı, defter, hafıza — bu şablonun kapsamında değil.

## Parça 2 — aksiyon durumu

`aksiyon-iskeleti.json` (durum makinesi tanımı) ve `durum.json` (anlık durum) da bu şablonla
birlikte kopyalanır; doldurma detayı için ilgili personel kaydındaki `README-aksiyon.md`'ye bakın.
