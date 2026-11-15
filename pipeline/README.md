# Neden Böyle — video üretim hattı

Dikey (1080×1920, 30 fps), 35–55 saniyelik, Türkçe seslendirmeli ve 8-bit müzikli kısa bilim videoları üretir.

## Adımlar
1. `bash pipeline/setup.sh` — paketler + Türkçe ses modeli (oturum başına bir kez).
2. `konular.md` dosyasına bak; **daha önce işlenmemiş** bir konu seç.
3. `pipeline/episodes/gokyuzu.py` (kısa, kalıplı örnek; **bunu tercih et**) ya da `sogan.py` (tamamen elle çizilmiş örnek) dosyasını örnek alarak `pipeline/episodes/<slug>.py` yaz. Kalıplar: `title_scene`, `reason_scene`, `cards_scene`, `end_scene`; bölüm başına yalnızca `hero(c, t)` ve dört `iN(c, t, d)` çizimi yazılır:
   - `SLUG`, `NARRATION` (sahne başına bir metin; 7 sahne: giriş, 4 neden, ipuçları/özet, kapanış).
   - Her sahne için `def sN(c, t, d)` çizim fonksiyonu (`t` sahne içi saniye, `d` sahne süresi).
   - İstersen `nb.THEME["bg"]` ve `nb.THEME["accent"]` ile renk temasını konuya göre değiştir.
   - Sonda: `nb.main(SLUG, NARRATION, [s0, ..., s6])`.
4. `cd pipeline && python3 episodes/<slug>.py` — sahne sürelerini yazdırır (süreler seslendirmeden gelir).
5. `python3 episodes/<slug>.py preview` (argümansız: her sahnenin sonuna yakın birer kare) ya da `preview 0:3.5 1:4.0 ...` — her sahnenin en dolu anından tam boy kare çizer,
   `build/<slug>/sheet.jpg` üretir. **Bu görsele mutlaka bak**: taşan/çakışan yazı, kesilen etiket, boş sahne olmasın.
6. `python3 episodes/<slug>.py build` — `build/<slug>/<slug>.mp4` (tek tam render; ~3 dk).
7. Videoyu `videolar/YYYY-AA-GG-<slug>.mp4` olarak kopyala, `konular.md`ye satır ekle, commit + push (main).

## Tasarım kuralları
- Üstte ilerleme çubuğu, küçük etiket (`header`), başlık; ortada (y≈480–1150) çizim; altında (y≈1260–1330) iki satır açıklama (`caption`).
- **Alt 500 piksel boş kalır** (uygulama arayüzü orayı kapatır). Yazılar x=60–1020 aralığından taşmaz.
- Ekrandaki metin kısa olsun: başlık ≤ 22 karakter, açıklama satırı ≤ 42 karakter.
- Animasyon zamanlaması seslendirmeye göre ayarlanır: ses sahnede 0.35. saniyede başlar.
- Hazır şekiller: `drop`, `puff`, `check`, `eye`, `node`, `shield`; yardımcılar: `text`, `fill`, `stroke`, `ss`, `eout`, `eback`, `lerp`, `qbez`.
- Telifli karakter, logo, gerçek kişi çizilmez.

## İçerik kuralları
- Gündelik hayattan "neden?" soruları; yerleşik, tartışmasız bilim. Emin olunmayan iddia yazılmaz.
- Sağlık/tedavi tavsiyesi, siyaset, din, güncel tartışmalı konular yok.
- Rakamlar seslendirmede yazıyla yazılır ("yetmiş derece"). Cümleler kısa tutulur.
- Kapanış her bölümde: "Neden böyle? Artık biliyorsunuz."
