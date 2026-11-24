import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import numpy as np, skia
from nb import *
import nb

SLUG = "yagmur-kokusu"
nb.THEME.update(bg=["#2f4a4f", "#1d3034", "#11201f"], accent="#9fe0c0")
NARRATION = [
 "Yağmurdan sonra toprak neden böyle güzel kokar? Bu kokunun bir adı bile var.",
 "Kurak günlerde bitkilerin salgıladığı yağlar, toprakta ve taşlarda birikir.",
 "Topraktaki bazı bakteriler de geosmin adlı bir madde üretir. Toprak kokusunun en belirgin parçası budur.",
 "Yağmur damlası toprağa çarpınca küçük hava kabarcıklarını hapseder. Kabarcıklar yükselip patlar ve kokuyu havaya savurur.",
 "Burnumuz geosmine çok duyarlıdır. Havadaki çok az miktarını bile fark eder.",
 "Bilim insanları bu kokuya petrikor adını verdi. Fırtına öncesindeki keskin koku ise şimşeğin oluşturduğu ozondan gelir.",
 "Yağmur kokusu, aslında toprağın nefesidir. Neden böyle? Artık biliyorsunuz.",
]
SOIL, SOIL2, LEAF = "#7a5236", "#5b3b26", "#6fd08c"

def ground(c, y=1060, h=110):
    rrect(c, 70, y, 940, h, 26, SOIL); rrect(c, 70, y, 940, 26, 13, SOIL2)
    for k in range(14): circ(c, 110 + k * 66, y + 60 + 18 * math.sin(k * 2.1), 7, "#a07a56", 0.8)
def sprout(c, x, y, s=1.0):
    line(c, x, y, x, y - 90 * s, "#4fa86a", 9 * s)
    for sgn in (-1, 1):
        p = skia.Path(); p.moveTo(x, y - 70 * s); p.quadTo(x + sgn * 70 * s, y - 120 * s, x + sgn * 80 * s, y - 70 * s)
        p.quadTo(x + sgn * 40 * s, y - 50 * s, x, y - 70 * s); p.close(); c.drawPath(p, fill(LEAF))
def wave_smell(c, x, y, t, a=1.0, color=None, n=3, h=180):
    color = color or THEME["accent"]
    for k in range(n):
        u = (t * 0.5 + k / n) % 1; yy = y - u * h; al = a * ss(0, 0.2, u) * (1 - ss(0.7, 1, u))
        p = skia.Path()
        for j in range(0, 61, 4):
            xx = x - 30 + j; py = yy + 10 * math.sin(j / 10 + t * 3)
            p.moveTo(xx, py) if j == 0 else p.lineTo(xx, py)
        c.drawPath(p, stroke(color, 7, al))
def rain(c, t, x0, x1, y0, y1, n=12, a=1.0, seed=1):
    for k in range(n):
        x = x0 + (x1 - x0) * ((k * 0.618 + seed * 0.3) % 1); u = (t * 0.9 + k * 0.37) % 1
        drop(c, x, lerp(y0, y1, u), 13, a * (1 - ss(0.85, 1, u)))

def hero(c, t):
    cloud(c, 540 + 10 * math.sin(t), 690, 1.25, 0.95, "#c8d6dc")
    rain(c, t, 420, 680, 760, 1000, 8)
    ground(c, 1010, 100)
    sprout(c, 330, 1012); sprout(c, 760, 1012, 0.8)
    wave_smell(c, 230, 1000, t, 0.9); wave_smell(c, 860, 1000, t + 0.4, 0.9)

def i1(c, t, d):
    sun(c, 860, 600, 60, t)
    ground(c)
    for x, s in ((260, 1.1), (520, 0.9), (780, 1.0)): sprout(c, x, 1062, s)
    for k in range(10):
        u = ((t - 0.8) * 0.45 + k * 0.1) % 1 if t > 0.8 else 0
        if t > 0.8:
            x = 260 + (k % 3) * 260 + 20 * math.sin(k); y = lerp(930, 1110, u)
            circ(c, x, y, 10, GOLD, 0.9 * ss(0, 0.15, u) * (1 - ss(0.85, 1, u)))
    rrect(c, 820, 1080, 120, 60, 26, "#9a9a9a")
    for k in range(5): circ(c, 840 + k * 22, 1100 + 8 * (k % 2), 6, GOLD, ss(2.0 + k * 0.2, 2.4 + k * 0.2, t))
    tag(c, "bitki yağları", 300, 700, GOLD, ss(1.2, 1.7, t), 40, "c", "Bold")
    tag(c, "toprakta birikir", 300, 760, CREAM, ss(2.4, 2.9, t), 36, "c")

def bacterium(c, x, y, ang, s=1.0, a=1.0):
    c.save(); c.translate(x, y); c.rotate(ang)
    rrect(c, -55 * s, -20 * s, 110 * s, 40 * s, 20 * s, "#c58fe0", a); rrect(c, -55 * s, -20 * s, 110 * s, 40 * s, 20 * s, "#ffffff", 0.5 * a, sw=3)
    c.restore()
def i2(c, t, d):
    rrect(c, 90, 560, 900, 560, 60, SOIL2, 0.9); circ(c, 540, 840, 270, SOIL, 0.6)
    pos = [(330, 700, 20), (700, 680, -35), (480, 900, 60), (760, 960, 10), (300, 1000, -15)]
    for k, (x, y, an) in enumerate(pos):
        bacterium(c, x + 6 * math.sin(t * 2 + k), y, an + 8 * math.sin(t + k), 1.0, pop(t, 0.6 + k * 0.2))
    if t > 2.4:
        for k, (x, y, _) in enumerate(pos):
            u = ((t - 2.4) * 0.6 + k * 0.21) % 1
            circ(c, x + 40, y - 30 - u * 120, 9, THEME["accent"], (1 - u) * ss(2.4, 2.8, t))
    tag(c, "bakteriler", 540, 530, "#e0b8f5", ss(1.0, 1.5, t), 40, "c", "Bold")
    tag(c, "geosmin üretir", 540, 1170, THEME["accent"], ss(2.6, 3.1, t), 44, "c", "Bold")

def i3(c, t, d):
    ground(c, 980, 150)
    # düşen damla
    T = 1.8
    if t < T:
        drop(c, 540, lerp(520, 960, eout(t / T)), 34)
    else:
        u = t - T
        circ(c, 540, 975, 70, BLUE, 0.6 * (1 - ss(0.8, 2.0, u)))
        for k in range(9):
            r = ((u * 0.55 + k * 0.11) % 1); x = 540 + (k - 4) * 34; y = 1060 - r * 520
            al = ss(0, 0.1, r) * (1 - ss(0.85, 1, r))
            if r < 0.85: circ(c, x, y, 13, "#ffffff", 0.75 * al, sw=4)
            else:
                for j in range(6):
                    ang = j * math.pi / 3; L = (r - 0.85) * 300
                    circ(c, x + math.cos(ang) * L, y + math.sin(ang) * L, 5, THEME["accent"], 1 - ss(0.85, 1, r))
        wave_smell(c, 300, 760, t, ss(T + 2, T + 2.5, t)); wave_smell(c, 790, 760, t + 0.5, ss(T + 2, T + 2.5, t))
    tag(c, "hava kabarcıkları", 250, 900, CREAM, ss(T + 0.6, T + 1.1, t), 34, "c")
    tag(c, "patlar, koku yayılır", 540, 560, THEME["accent"], ss(T + 2.4, T + 2.9, t), 40, "c", "Bold")

def nose(c, x, y, s=1.0):
    circ(c, x - 120 * s, y, 170 * s, "#ffd7b0")
    poly(c, [(x + 20 * s, y - 70 * s), (x + 95 * s, y + 40 * s), (x + 30 * s, y + 50 * s)], "#ffd7b0")
    circ(c, x - 20 * s, y - 50 * s, 14 * s, "#3a2a20")
    line(c, x - 10 * s, y + 95 * s, x + 30 * s, y + 95 * s, "#c8846a", 8 * s)
def i4(c, t, d):
    nose(c, 420, 900, 1.0)
    for k in range(7):
        u = ((t * 0.35 + k / 7) % 1); x = lerp(980, 530, u); y = 940 + 60 * math.sin(k * 1.9 + u * 6) * (1 - u)
        circ(c, x, y, 11, THEME["accent"], ss(0, 0.1, u) * (1 - ss(0.9, 1, u)) * (0.4 if k > 1 else 1.0))
    k = ss(2.0, 2.6, t)
    if k > 0:
        for r in (90, 140):
            circ(c, 515, 940, r * (0.8 + 0.2 * math.sin(t * 4)), GOLD, 0.6 * k, sw=6)
    tag(c, "çok az bile yeter", 700, 640, THEME["accent"], ss(2.2, 2.7, t), 40, "c", "Bold")

SCENES = [
 title_scene("Yağmurdan sonra", "toprak neden kokar?", "Kokunun bir adı bile var", hero),
 reason_scene("NEDEN 1", "Bitki yağları birikir", ["Kurak günlerde bitkilerin yağları", "toprakta ve taşlarda birikir."], i1),
 reason_scene("NEDEN 2", "Bakteriler: geosmin", ["Topraktaki bazı bakteriler", "geosmin adlı maddeyi üretir."], i2),
 reason_scene("NEDEN 3", "Damla kabarcık yapar", ["Damla toprağa çarpınca kabarcıklar", "yükselip patlar, kokuyu savurur."], i3),
 reason_scene("NEDEN 4", "Burnumuz çok duyarlı", ["Burnumuz geosmini havada", "çok az miktarda bile fark eder."], i4),
 cards_scene("BONUS", "Kokunun bir adı var", [("Adı: petrikor", "Bilim insanları koydu"), ("Fırtına öncesi koku", "Keskin koku ozondur"), ("Ozonu şimşek üretir", "Rüzgârla aşağı iner")]),
 end_scene("Yağmur kokusu,", "toprağın nefesi.", hero),
]
if __name__ == "__main__":
    nb.main(SLUG, NARRATION, SCENES)
