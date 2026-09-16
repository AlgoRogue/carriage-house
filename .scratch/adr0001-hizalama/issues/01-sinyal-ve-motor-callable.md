# 01: Prefactor: Sinyal sözlüğü ve Motor callable şekli

**Spec:** `.scratch/adr0001-hizalama/spec.md`

**What to build:**
Sürücü module'ünün iç Motor seam'i ve kapalı Sinyal sözlüğü, onaylı şekle çekilir. Üretim ve `son_sinyal` yalnız `basari` / `hata` yazar; `motor_ciktisi` / `motor_hatasi` hurdaya çıkar. İki adapter (SahteMotor ve kart/CLI) aynı interface'i karşılar. Onaylı şekil (SEAMS.md):

```
motor(girdi: str) -> (Sinyal, metin)
```

`girdi` henüz doldurulmuş Prompt şablonu olmak zorunda değildir — bu dilimde geçici olarak durum adı kalabilir. `metin` içerik kanalıdır, Sinyal değildir. Durum adı `hata` iskelette durur; Sinyal `hata` ile birleştirilmez.

Birincil seam durur: `isi_ilerlet(motor, …)` adı ve "Motor enjekte" şekli değişmez. Yeni public seam yok. `isi_ilerlet` hâlâ `park`'a gider ama Prompt şablonu doldurmaz ve İş artefaktı yazmaz. Çekirdek kural module'ü saf kalır (I/O yok).

Bu dilim ürün davranışını ADR-0001'e tamamlamaz; 02'nin yeşil inmesi için çağıranları tek sözlüğe ve tek callable şekline çeker (prefactor: **locality** — sözlük ve şekil bir yerde, sonra N çağıran).

**Blocked by:** None (can start immediately)

**Status:** done

- [x] Üretim ve `son_sinyal` yalnız `basari` / `hata`; eski dizgiler yok
- [x] Durum adı `hata` iskelette durur; Sinyal ile birleştirilmez
- [x] Her iki adapter yeni Motor interface'ini karşılar; `metin` içerik kanalıdır, Sinyal değildir
- [x] `isi_ilerlet(motor, …)` adı ve "Motor enjekte" şekli durur; yeni durum makinesi yok; yeni public seam yok
- [x] Mevcut SahteMotor e2e (`bos` → `park`) yeni interface ile yeşil; şablon/artefakt henüz yok
- [x] Çekirdek kural module'ü saf kalır (şablon ve dosya I/O girmez)
- [x] `python3 -m unittest discover -s tests` ağsız yeşil

## Comments

- 2026-09-16: yayınlandı (to-tickets adım 5). Durum: ready-for-agent. Frontier.
- 2026-09-16: uygulandı (Claude Code). `surucu_cekirdek.Sinyal` → `basari`/`hata`; `SahteMotor` ve `kart_motoru.motor_uret` `motor(girdi) -> (Sinyal, metin)` döner. `SurucuAdim` `metin`'i bu dilimde yok sayar (şablon/artefakt 02'de). Sürücü/kart_motoru test dosyaları yeni sözlük ve tuple dönüşe çekildi. `python3 -m unittest discover -s tests` yeşil; tek istisna `test_kit.BekciKatmanA.test_kosuda_anayasaya_dokunan_ajan_red` — bu bilette dokunulmayan, önceden kırmızı `suite-sagligi` borcu (spec Out of Scope).
