# Kurallar — sistem-insaat

> Bekçi bu dosyayı okur. Yalnızca insan değiştirir.

## Neye göre çalışır
- ANAYASA'nın tamamı geçerlidir; aşağıdakiler ona ektir.
- Tek yetki kaynağı `increment/<id>/sozlesme.onayli.json`. Taslak (`sozlesme.json`), sohbet, tahmin yetki değildir.

## Asla yapmaz
- `dokunulacak_yollar` ∪ `yeni_dosyalar` dışına yazmaz. Kendi klasörü (`takimlar/sistem-insaat/`) ve
  `increment/<id>/` istisnadır (koşu kaydı, defter, park).
- İnsanın dosyalarına dokunmaz: `ANAYASA.md`, `hedef.md`, `kararlar.md`, `kapsam-disi.md`, `sema/`,
  `takimlar/*/kurallar.md`, `sozlesme.onayli.json`, `bin/kapi.py` — sözleşme bunlardan birini listelese bile
  önce `park.md`'ye yazar, insan onayı olmadan değiştirmez.
- Sözleşme dışı özellik, "iyileştirme", refactor, yeniden adlandırma yapmaz.
- Kabul kriterini çalıştırmadan "geçti" demez; geçmeyen kriteri `yapilmayanlar`dan saklamaz.
- `git commit`, `git push`, `git tag`, `git reset`, `git checkout -- .` çalıştırmaz. Commit insanın Kapı 2 işidir.
- Paket kurmaz (`pip install`, `npm install` …), ağ çağrısı yapmaz, dış servis anahtarı kullanmaz.
- `sozlesme.onayli.json` üzerinde chmod/yeniden yazma yapmaz.

## Çıktı kalite ölçütleri
- `diff_ozeti` dosya başına bir satır; `git diff --stat` ile tutarlı.
- `calistirilan_komutlar` her kabul kriterinin komutunu içerir.
- Yeni Python kodu mevcut kodun dilinde: Türkçe adlar, kısa docstring, stdlib, ağ yok, `python3 -m unittest`
  ile koşan test.
- `park.md` varsa her madde "ne ertelendi · neden · kim netleştirmeli" biçiminde.
