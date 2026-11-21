import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import numpy as np, skia
from nb import *
import nb

SLUG = "bal-neden-sekerlenir"
nb.THEME.update(bg=["#8a5410", "#5a3409", "#2a1803"], accent="#ffc94a")
NARRATION = [
 "Bal neden şekerlenir? Bozuldu mu sandınız? Hiç de değil.",
 "Bal, aslında şekerle dolu bir sudur. İçinde, suyun normalde tutabileceğinden çok daha fazla şeker çözünmüştür.",
 "Baldaki iki ana şeker glikoz ve früktozdur. Glikoz suda daha zor çözünür; fazlası sıvıdan ayrılmak ister.",
 "Glikoz molekülleri, polen ya da minik bir hava kabarcığı gibi küçük parçacıkların çevresinde dizilir. İlk kristaller böyle oluşur ve büyür.",
 "Serinlik bu süreci hızlandırır. Bal en hızlı, on ile on beş derece arasında şekerlenir.",
 "Şekerlenmiş bal bozulmuş değildir. Kavanozu ılık suda bekletirseniz, kristaller yeniden çözünür.",
 "Şekerlenme, balın doğasında var. Neden böyle? Artık biliyorsunuz.",
]
HONEY, HONEY2, CRYS = "#f5a623", "#ffcf5c", "#fff4d6"

def hexa(c, x, y, r, color, a=1.0, sw=0, rot=0.0):
    poly(c, [(x + r * math.cos(rot + k * math.pi / 3), y + r * math.sin(rot + k * math.pi / 3)) for k in range(6)], color, a, sw)
def penta(c, x, y, r, color, a=1.0, sw=0, rot=0.0):
    poly(c, [(x + r * math.cos(rot - math.pi / 2 + k * 2 * math.pi / 5), y + r * math.sin(rot - math.pi / 2 + k * 2 * math.pi / 5)) for k in range(5)], color, a, sw)
def jar(c, x, y, w, h, level=0.8, cry=0.0, a=1.0, t=0.0):
    # x,y: alt orta
    top = y - h
    rrect(c, x - w / 2, top, w, h, 46, "#ffffff", 0.12 * a)
    lh = h * level
    rrect(c, x - w / 2 + 10, y - lh, w - 20, lh - 10, 38, mixcol(HONEY, "#e8c27a", cry), a)
    if cry > 0:
        rng = np.random.default_rng(4)
        for _ in range(70):
            px = x + rng.uniform(-w / 2 + 30, w / 2 - 30); py = y - rng.uniform(25, lh - 20)
            circ(c, px, py, rng.uniform(3, 7), CRYS, 0.75 * cry * a)
    rrect(c, x - w / 2 + 28, y - lh + 20, 22, lh - 60, 11, "#ffffff", 0.22 * a)
    rrect(c, x - w / 2, top, w, h, 46, "#ffffff", 0.7 * a, sw=6)
    rrect(c, x - w / 2 - 16, top - 58, w + 32, 66, 18, "#c0392b", a)
    rrect(c, x - w / 2 - 16, top - 58, w + 32, 66, 18, "#7d1f16", a, sw=5)
def hero(c, t):
    jar(c, 540, 1110, 330, 380, 0.82, 0.0)
    # kaşık ve damla
    line(c, 720, 640, 850, 560, "#d9a35c", 22); circ(c, 720, 660, 34, "#d9a35c")
    yy = 700 + ((t * 120) % 140)
    drop(c, 720, yy, 20, 1.0, HONEY)
    for k, (dx, dy) in enumerate(((-240, 880), (250, 980), (-220, 1040))):
        hexa(c, 540 + dx, dy + 8 * math.sin(t * 2 + k), 34, CRYS, 0.9, rot=t * 0.4)
def i1(c, t, d):
    # bardak suya şeker küpleri
    rrect(c, 330, 620, 420, 480, 40, "#ffffff", 0.1); rrect(c, 330, 620, 420, 480, 40, "#ffffff", 0.7, sw=6)
    lvl = 300 + 80 * ss(1.0, 4.5, t)
    rrect(c, 340, 1090 - lvl, 400, lvl, 34, mixcol("#9fd3ff", HONEY, ss(1.0, 5.0, t)), 0.85)
    for k in range(10):
        t0 = 0.6 + k * 0.42; p = ss(t0, t0 + 0.55, t)
        if p <= 0: continue
        x = 400 + (k * 73) % 280; y = lerp(470, 1090 - lvl + 40 + (k % 3) * 60, p)
        fade = 1 - ss(t0 + 0.6, t0 + 1.4, t)
        rrect(c, x, y, 50, 50, 8, "#ffffff", 0.95 * fade)
    tag(c, "su", 210, 900, "#9fd3ff", ss(0.6, 1.1, t), 40, "c", "Bold")
    tag(c, "+ çok şeker", 880, 560, CRYS, ss(1.2, 1.7, t), 40, "c", "Bold")
    tag(c, "aşırı doymuş", 540, 1192, THEME["accent"], ss(4.6, 5.1, t), 40, "c", "Bold")
def i2(c, t, d):
    rrect(c, 120, 520, 840, 600, 40, HONEY, 0.25); rrect(c, 120, 520, 840, 600, 40, HONEY2, 0.6, sw=5)
    rng = np.random.default_rng(7)
    for k in range(9):
        x = 200 + rng.uniform(0, 680); y = 600 + rng.uniform(0, 440)
        penta(c, x + 14 * math.sin(t * 1.5 + k), y + 10 * math.cos(t * 1.3 + k), 30, "#ffb3d1", 0.9, rot=t * 0.5 + k)
    for k in range(7):
        x0 = 200 + rng.uniform(0, 680); y0 = 600 + rng.uniform(0, 260)
        p = ss(3.2 + k * 0.15, 5.2 + k * 0.15, t)
        hexa(c, lerp(x0, 260 + k * 92, p), lerp(y0, 1060, p), 32, CRYS, 0.95, rot=k * (1 - p))
    tag(c, "früktoz: çözünük kalır", 540, 490, "#ffb3d1", ss(0.9, 1.4, t), 36, "c", "Bold")
    tag(c, "glikoz: dışarı çıkar", 540, 1170, CRYS, ss(3.3, 3.8, t), 36, "c", "Bold")
def i3(c, t, d):
    cx, cy = 540, 830
    tag(c, "polen", cx, cy - 70, "#d8f59c", ss(0.8, 1.3, t) * (1 - ss(1.9, 2.4, t)), 34, "c", "Bold")
    # bal ızgarası yerleşimi
    slots = []
    for ring in range(1, 4):
        for j in range(6 * ring):
            ang = j * 2 * math.pi / (6 * ring) + ring * 0.3
            slots.append((cx + ring * 84 * math.cos(ang), cy + ring * 84 * math.sin(ang)))
    for k, (sx, sy) in enumerate(slots):
        t0 = 2.0 + k * 0.12; p = eout((t - t0) / 0.6) if t > t0 else 0
        if p <= 0: continue
        ang = k * 2.4; fx = sx + 300 * math.cos(ang) * (1 - p); fy = sy + 300 * math.sin(ang) * (1 - p)
        hexa(c, fx, fy, 37, CRYS, 0.9 * p); hexa(c, fx, fy, 37, HONEY, 0.8 * p, sw=4)
    circ(c, cx, cy, 30, "#b5e06a")
    for k in range(8):
        ang = k * math.pi / 4; line(c, cx + 30 * math.cos(ang), cy + 30 * math.sin(ang), cx + 42 * math.cos(ang), cy + 42 * math.sin(ang), "#b5e06a", 6)
    tag(c, "kristal büyür", 540, 1170, THEME["accent"], ss(5.0, 5.5, t), 38, "c", "Bold")
def thermo(c, x, y, k, a=1.0):
    rrect(c, x - 26, y - 420, 52, 420, 26, "#ffffff", 0.2 * a); rrect(c, x - 26, y - 420, 52, 420, 26, "#ffffff", 0.8 * a, sw=5)
    h = lerp(320, 150, k); rrect(c, x - 13, y - h, 26, h, 13, "#6ec6f0", a); circ(c, x, y + 20, 48, "#6ec6f0", a)
def i4(c, t, d):
    k = ss(0.6, 2.4, t)
    thermo(c, 250, 1050, k)
    tag(c, "serin", 250, 560, "#9fdcff", ss(0.6, 1.1, t), 38, "c", "Bold")
    jar(c, 680, 1110, 300, 420, 0.82, ss(1.6, 4.8, t))
    tag(c, "10–15 °C: en hızlı", 540, 1180, THEME["accent"], ss(3.4, 3.9, t), 40, "c", "Bold")
SCENES = [
 title_scene("Bal neden", "şekerlenir?", "Bozulmadı, kristallendi", hero),
 reason_scene("NEDEN 1", "Fazla şekerli su", ["Bal, suyun normalde tutabileceğinden", "çok daha fazla şeker taşır."], i1),
 reason_scene("NEDEN 2", "Glikoz ayrılmak ister", ["Früktoz çözünük kalır;", "glikozun fazlası sıvıdan ayrılır."], i2),
 reason_scene("NEDEN 3", "Kristal tohumları", ["Polen ve kabarcıklar çekirdek olur;", "glikoz çevrelerine dizilir."], i3),
 reason_scene("NEDEN 4", "Serinlik hızlandırır", ["Bal en hızlı on ile on beş", "derece arasında şekerlenir."], i4),
 cards_scene("ÖZET", "Şekerlenen bal bozuk mu?", [("Bozulmuş değildir", "Sadece kristallenmiştir"), ("Ilık su banyosu", "Kristaller yeniden çözünür"), ("Hız bala göre değişir", "Glikoz çoksa daha çabuk")]),
 end_scene("Şekerlenme,", "balın doğasında var.", hero),
]
if __name__ == "__main__":
    nb.main(SLUG, NARRATION, SCENES)
