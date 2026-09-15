# Aksiyon durumu

## Bu iki dosya ne

- `aksiyon-iskeleti.json` — Cengizhan'ın durum makinesi *tanımı*: olası durumlar ve aralarındaki
  geçişler. Sabittir, iş bazında değişmez.
- `durum.json` — Cengizhan'ın *anlık* durumu: şu an hangi durumda, hangi işe bağlı, son sinyal ne
  zaman geldi. İş ilerledikçe değişen tek kayıt budur.

## Sürücü / Motor ayrımı

Durumdan duruma geçişi yalnız **Sürücü** yazar (`kural.sonraki_durumu_yalniz_surucu_yazar`) —
ajan kendi durumunu değiştiremez. **Motor**, yalnız `motor_cagrilan_durumlar` içinde listelenen
durumlarda (`planlaniyor`, `delege_hazirlaniyor`) çağrılır; bir CLI/LLM çalıştırıp çıktı üretir,
durum geçişine karar vermez. Bu ayrım henüz koda dökülmedi — burada yalnız tanım var, çalıştıran
sürücü kodu yok.

## İlk dilim nerede biter

İlk prototip yolu şudur: `bos → is_alindi → planlaniyor → plan_hazir → delege_hazirlaniyor →
paket_hazir → park`. Usta henüz tanımlı olmadığından iş `park`'ta durur; `usta_atandi` ve
`izleniyor` durumları tanımlı ama sonraki bir dilimde devreye girecek.

## Bilinçli olarak dışı

Kapı, defter, hafıza, motor çağrısı, sürücü kodu — bu kayıt yalnız durum makinesinin ve anlık
durumun tanımını taşır; bunları çalıştıran hiçbir mekanizma içermez.
