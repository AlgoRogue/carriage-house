# inc-001 — salt-okur durum sayfası (`bin/uygulama.py`)

**Ne:** `python3 bin/uygulama.py [--port 8765]` yalnız `127.0.0.1`'de dinler. `GET /` her istekte
`increment/evre.json` ve aktif `increment/<id>/` klasörünü okuyup tek bir HTML sayfası döner: increment id, evre,
bekleyen onay, kilitli motorlar (inşaat/bekçi), talep, kapsam sapması, son olay, **sıradaki adım**
(`bin/kapi.py durum` ile aynı komut metni), varsa bekçi kararı ve artefakt bağlantıları.
Bağlantılar `GET /evre.json` ve `GET /artefakt/<ad>` (yalnız aktif klasördeki dosya adı; `/` ya da `..` → 404)
ile `text/plain` olarak açılır. GET dışı her yöntem `405`; hiçbir istek dosya yazmaz.

**Neden:** Etkileşim katmanının ilk parçası (`hedef.md` → Sonrası → 1). Uygulama ikinci bir sistem değil,
dosyaların insan yüzü: kendi durumu, kuyruğu, önbelleği yok. Bu increment aynı zamanda döngünün ilk uçtan uca
geçişi — bitiş çizgisi bununla aşılır.

**Nasıl doğrulanır:** `bin/uygulama.py` ve `tests/test_uygulama.py` var; `python3 -m unittest discover -s tests`
geçer (test sahte kökte, port 0'da, loopback'te koşar: sayfa içeriği, artefakt bağlantısı, `..` → 404, POST → 405,
istek sonrası dosyalar değişmemiş); `bin/uygulama.py` yalnız stdlib + `bin/ayar.py` içe alır (AST kontrolü);
canlı kontrol: sunucu 8765'te açılır, `GET /` içinde `inc-001` ve `<html` var, POST 405, `evre.json` özeti aynı.

**Motor:** `codex` — tek dosya + tek test, diff'e kilitli iş. Bekçi: `claude`.

**Dışarıda:** her türlü yazma (talep/red/onayla/yayinla/kos tetiği), `0.0.0.0`/uzak erişim/kimlik, otomatik
yenileme (polling/meta refresh), JS/CSS, `bin/kapi.py`/`sema/`/SoT değişikliği, LLM çağrısı, servis dosyası.

**Durma:** sayfayı üretmek `bin/kapi.py`'ye ya da `sema/`'ya dokunmayı gerektiriyorsa; "sıradaki adım" metni
`kapi.durum` ile çelişmeden türetilemiyorsa → `park.md`, iade.

**Yayın anlamı (Kapı 2):** `bin/uygulama.py` canlıya alınır; `kararlar.md`'ye "etkileşim katmanı 1/5: salt-okur
durum sayfası" satırı düşer. SoT değişmez — uygulama SoT değil, `evre.json` + artefaktların yüzüdür.
