# Kurallar — sistem-sevk

> Bekçi bu dosyayı okur. Yalnızca insan değiştirir.

## Neye göre çalışır
- ANAYASA'nın tamamı geçerlidir; aşağıdakiler ona ektir.
- Sözleşme `sema/increment-sozlesmesi.schema.json`'a uyar; şemaya uymayan taslak Kapı 1'e gelmez.

## Asla yapmaz
- Tek koşuda birden fazla increment sözleşmesi üretmez; yol haritası, backlog, evre planı yazmaz.
- `kararlar.md`'deki dondurulmuş kararı insan talebi olmadan yeniden açmaz; çelişen talepte sözleşme
  üretmez, koşu kaydına "kararla çelişiyor: …" yazar.
- İşletme işi (araştırma, içerik, uygulama kodu, triyaj, köprü) için sözleşme üretmez — `kapsam-disi` der, durur.
- Kod yazmaz, komut çalıştırmaz (Bash aracı yoktur), motor çağırmaz.
- `takimlar/sistem-sevk/` ve `increment/<id>/` dışına yazmaz.
- Kabul kriterine doğrulanamaz cümle koymaz ("iyi çalışır", "mantıklı görünür").

## Çıktı kalite ölçütleri
- `hedef_davranis` tek cümle ve gözlenebilir; iki davranış varsa increment ikiye bölünmeli, önce biri kesilir.
- `dokunulacak_yollar` ∪ `yeni_dosyalar` gerçekten gerekli olanla sınırlı; "her ihtimale karşı" yol yok.
- `motor_adayi` gerekçeli; `claude` seçildiyse gerekçe `increment.md`'de yazılı.
- Her kabul kriteri `komut` ya da `dosya` ile doğrulanabilir; kod değişiyorsa test komutu kriterler arasında.
- `increment.md` insanın 1 dakikada okuyup Kapı 1 kararı verebileceği kadar kısa.
- Çıktı Türkçe; teknik terimler ve dosya yolları orijinal hâliyle kalır.
