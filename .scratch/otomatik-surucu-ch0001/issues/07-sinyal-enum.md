# 07: `MOTOR_*` string sabitleri yerine tipli enum

**What to build:**
CH-0001 kapsamındaki `bin` üretim modüllerinde sinyal/durum değerleri şu an serbest metin
(`MOTOR_*`) string sabitleri olarak tutuluyor. Bu bilet bunları stdlib `Enum` (ya da eşdeğer
tipli bir küme) ile değiştirir; ilgili tüm üretim modülleri karşılaştırma ve atamalarda string
yerine bu enum'u kullanır. Amaç, geçersiz/yazım hatalı bir sinyal değerinin çalışma zamanında
sessizce geçmesi yerine erken yakalanmasıdır. Dışa dönük davranış değişmez.

**Blocked by:** 04 (mutlu yol giriş noktası kurulduktan sonra yapılmalı)

**Status:** done

- [x] `MOTOR_*` string sabitlerinin yerini stdlib `Enum` (veya eşdeğer tipli bir küme) alır
- [x] CH-0001 kapsamındaki tüm `bin` üretim modülleri string sabitler yerine bu enum'u kullanır
- [x] Enum değerlerinin dışa yazılan temsili (ör. `durum.json` içeriği) önceki string değerlerle
      aynı kalır. Kalıcı veri formatı bozulmaz
- [x] Mevcut tüm testler (`python3 -m unittest discover -s tests`) değişiklik sonrası da geçer

## Comments

- 2026-09-15: `Sinyal(StrEnum)` eklendi; üretim karşılaştırma/atamaları enum üzerinden. `python3 -m unittest discover -s tests -p 'test_surucu*.py'` → 27 test, OK.
