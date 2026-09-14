# Kararlar — dondurulmuş

> SoT. Ekleme-yalnız; satır silinmez, tarihli yeni satırla geçersiz kılınır. `bin/kapi.py yayinla` Kapı 2'de
> buraya otomatik satır düşer; elle eklenen kararlar da aynı biçimde. İnsanındır; ajan okur, açmaz.

## Kuruluş kararları (increment 0, 2026-09-14)
- 2026-09-14 · kadro üç takım: `sistem-sevk`, `sistem-insaat`, `sistem-bekci` — A Şirketi'ni *üreten* üç kilit; işletme takımları kadro değil, increment konusu.
- 2026-09-14 · motorlar: claude, agy, codex, grok. Adaptör `bin/motorlar/<ad>.py`; sürücü motoru bilmez.
- 2026-09-14 · sevk motoru `claude` sabit. İnşaat motoru sözleşmeden (`motor_adayi`, Kapı 1'de insan kilitler; varsayılan `codex`). Bekçi motoru üretenin tersi: `codex/agy/grok → claude`, `claude → grok`.
- 2026-09-14 · grok: inşaat adayı + `claude` üretirse bekçi. agy yalnız inşaat adayı.
- 2026-09-14 · yapısal çıktı (sözleşme, teslim, rapor) dört CLI'nin şema bayrağıyla zorlanır; dosyayı sürücü yazar, ajan değil.
- 2026-09-14 · kapsam kontrolü deterministik: sürücü koşu öncesi/sonrası `git status` farkını sözleşme yollarıyla karşılaştırır. Sevk/bekçi sapması → koşu red; inşaat sapması → bekçiye kanıt, tek başına FAIL sebebi.
- 2026-09-14 · insan kapıları `bin/kapi.py`: talep · onayla (Kapı 1) · yayinla (Kapı 2) · red · durum. LLM yok, motor başlatmaz.
- 2026-09-14 · evre makinesi `increment/evre.json`, şeması `sema/evre.schema.json` dondurulmuş. Yalnız sürücü ve kapı yazar.
- 2026-09-14 · bekçi katman A LLM'siz (`bin/bekci.py`): boş kayıt, gizli veri, insanın dosyasına dokunma. OpenAI API yolu kaldırıldı.
- 2026-09-14 · tavanlar: 15 dk/koşu her motorda; 2 USD/koşu ve 10 USD/gün yalnız maliyet raporlayan motorda (claude); 6 koşu/gün/takım. Mesai kontrolü kaldırıldı (tetik insan).
- 2026-09-14 · eski içerik şirketi `icerik-sirketi-v1` etiketinde; main'den silindi.

## Increment yayınları (Kapı 2 — otomatik)
