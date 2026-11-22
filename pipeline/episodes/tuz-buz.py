import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import numpy as np, skia
from nb import *
import nb

SLUG = "tuz-buzu-neden-eritir"
nb.THEME.update(bg=["#0f4c5c", "#0a3440", "#06212a"], accent="#ffd166")
NARRATION = [
 "Kışın yollara neden tuz dökülür? Tuz, buzu nasıl eritir?",
 "Buzun yüzeyinde hep çok ince bir su tabakası vardır. Tuz bu suda çözünür ve tuzlu su oluşur.",
 "Su donarken molekülleri düzenli bir kristal kurar. Araya giren tuz parçacıkları bu düzeni bozar.",
 "Bu yüzden tuzlu su sıfır derecede donmaz; donmak için daha da soğuması gerekir. Buna donma noktası alçalması denir.",
 "Hava sıfırın biraz altındaysa, tuzlu suya değen buz erir. Oluşan su yeni tuz çözer ve erime yayılır.",
 "Ama tuzun da sınırı var. Hava çok soğursa etkisi iyice azalır; o zaman yola kum da serpilir. Aynı ilkeyle deniz suyu da, yaklaşık eksi iki derecede donar.",
 "Tuz buzu ısıtmaz; donmayı zorlaştırır. Neden böyle? Artık biliyorsunuz.",
]
ICE = "#bfe9ff"
ICE_D = "#8fd0f0"
BRINE = "#4fb3d9"
SALT = "#ffffff"
ROAD = "#33414c"

def grain(c, x, y, s, rot=0.0, a=1.0, color=SALT):
    c.save(); c.translate(x, y); c.rotate(rot)
    rrect(c, -s / 2, -s / 2, s, s, s * 0.18, color, a)
    c.restore()

def shaker(c, x, y, s, tilt, a=1.0):
    c.save(); c.translate(x, y); c.rotate(tilt)
    rrect(c, -45 * s, -70 * s, 90 * s, 140 * s, 22 * s, "#e8eef3", a)
    rrect(c, -45 * s, -70 * s, 90 * s, 34 * s, 14 * s, "#9fb3c2", a)
    for k in range(3): circ(c, (k - 1) * 22 * s, -53 * s, 5 * s, "#33414c", a)
    rrect(c, -30 * s, 0, 60 * s, 40 * s, 10 * s, "#cfd9e1", a)
    c.restore()

_rh = np.random.default_rng(4)
HG = [(float(_rh.uniform(-1, 1)), float(_rh.uniform(0, 1)), float(_rh.uniform(0, 6.28))) for _ in range(14)]
def hero(c, t):
    # yol + buz tabakası
    poly(c, [(150, 1180), (930, 1180), (760, 760), (320, 760)], ROAD)
    poly(c, [(250, 1130), (830, 1130), (720, 830), (360, 830)], ICE, 0.85)
    for k in range(4):
        line(c, 400 + k * 90, 860 + k * 50, 460 + k * 90, 880 + k * 50, "#ffffff", 5, 0.7)
    # eriyen birikinti
    m = 0.5 + 0.5 * math.sin(t * 1.2)
    c.save(); c.translate(560, 1020); c.scale(1.0 + 0.15 * m, 0.42)
    circ(c, 0, 0, 120, BRINE, 0.85); c.restore()
    # tuzluk ve dökülen tuz
    shaker(c, 690, 630, 1.0, 150 + 6 * math.sin(t * 3))
    for (u, v, ph) in HG:
        f = (t * 0.6 + v) % 1
        gx = 712 + u * 30 - 110 * f; gy = 690 + 300 * f
        grain(c, gx, gy, 12, ph + t * 2, 1 - 0.6 * f)

_r1 = np.random.default_rng(7)
G1 = [(float(_r1.uniform(170, 910)), float(_r1.uniform(0, 1)), float(_r1.uniform(0, 6.28))) for _ in range(16)]
def i1(c, t, d):
    rrect(c, 120, 820, 840, 320, 34, ICE)
    for k in range(5):
        line(c, 190 + k * 160, 900, 250 + k * 160, 1060, "#ffffff", 6, 0.5)
    w = ss(0.4, 1.4, t)
    rrect(c, 120, 790, 840 * w, 44, 22, BRINE, 0.9)
    tag(c, "ince su tabakası", 540, 740, "#ffffff", ss(1.2, 1.7, t) * (1 - ss(4.2, 4.6, t)), 40, "c", "Bold")
    for (x, v, ph) in G1:
        t0 = 2.6 + v * 1.4
        if t < t0: continue
        f = ss(t0, t0 + 0.7, t)
        y = lerp(520, 805, f)
        dis = ss(t0 + 0.8, t0 + 2.2, t)
        grain(c, x, y, 22 * (1 - 0.7 * dis), ph + f * 4, 1 - dis)
        if dis > 0: circ(c, x, 812, 10 + 20 * dis, "#ffffff", 0.35 * (1 - dis))
    k = ss(4.4, 5.4, t)
    if k > 0:
        rrect(c, 120, 790, 840, 44, 22, THEME["accent"], 0.35 * k)
        tag(c, "tuzlu su", 540, 740, THEME["accent"], k, 44, "c", "Bold")

def lattice(c, cx, cy, n, gap, t, chaos, a=1.0, seed=0):
    rng = np.random.default_rng(seed)
    pts = {}
    for i in range(n):
        for j in range(n):
            jx = float(rng.uniform(-1, 1)); jy = float(rng.uniform(-1, 1)); ph = float(rng.uniform(0, 6.28))
            x = cx + (i - (n - 1) / 2) * gap + chaos * (jx * gap * 0.38 + 8 * math.sin(t * 5 + ph))
            y = cy + (j - (n - 1) / 2) * gap + chaos * (jy * gap * 0.38 + 8 * math.cos(t * 5 + ph))
            pts[(i, j)] = (x, y)
    for (i, j), (x, y) in pts.items():
        for di, dj in ((1, 0), (0, 1)):
            q = pts.get((i + di, j + dj))
            if q: line(c, x, y, q[0], q[1], "#ffffff", 4, a * 0.45 * (1 - chaos))
    for (x, y) in pts.values():
        circ(c, x, y, 15, ICE, a)
    return pts

def i2(c, t, d):
    lattice(c, 290, 860, 5, 66, t, 0.0, 1, seed=1)
    tag(c, "saf su: düzenli", 290, 1150, ICE, ss(1.0, 1.5, t), 36, "c", "Bold")
    ch = ss(3.0, 4.6, t)
    lattice(c, 790, 860, 5, 66, t, ch, ss(1.6, 2.2, t), seed=2)
    if t > 2.6:
        rng = np.random.default_rng(11)
        for k in range(7):
            tx = 790 + float(rng.uniform(-150, 150)); ty = 860 + float(rng.uniform(-150, 150))
            f = ss(2.6 + k * 0.1, 3.4 + k * 0.1, t)
            x = lerp(790 + (k - 3) * 40, tx, f); y = lerp(560, ty, f)
            circ(c, x, y, 13, THEME["accent"] if k % 2 else "#7ee08a", 0.95 * f)
    tag(c, "tuz: düzeni bozar", 790, 1150, THEME["accent"], ss(4.2, 4.7, t), 36, "c", "Bold")

def thermo(c, x, y, frac, color, a=1.0, h=360):
    rrect(c, x - 24, y - h, 48, h, 24, "#ffffff", 0.22 * a)
    rrect(c, x - 24, y - h, 48, h, 24, "#ffffff", 0.7 * a, sw=4)
    hh = (h - 30) * clamp(frac); rrect(c, x - 12, y - 12 - hh, 24, hh + 14, 12, color, a)
    circ(c, x, y + 20, 38, color, a); circ(c, x, y + 20, 38, "#ffffff", 0.7 * a, sw=4)

def i3(c, t, d):
    # sol: saf su 0 °C'de donar
    f1 = 0.62 - 0.22 * ss(0.8, 2.4, t)
    thermo(c, 300, 1040, f1, "#6ec6f0")
    zy = 1040 - 12 - (360 - 30) * 0.40
    line(c, 200, zy, 400, zy, "#ffffff", 4, 0.8)
    tag(c, "0 °C", 190, zy + 12, "#ffffff", 1, 34, "r", "Bold")
    k1 = pop(t, 2.4)
    if k1 > 0:
        rrect(c, 160, 560, 280, 90, 24, ICE, 0.9 * clamp(k1)); tag(c, "su: donar", 300, 620, "#0a3440", clamp(k1), 38, "c", "Bold")
    # sağ: tuzlu su daha soğukta donar
    f2 = 0.62 - 0.42 * ss(3.0, 5.6, t)
    thermo(c, 780, 1040, f2, THEME["accent"])
    line(c, 680, zy, 880, zy, "#ffffff", 4, 0.5)
    zy2 = 1040 - 12 - (360 - 30) * 0.20
    line(c, 680, zy2, 880, zy2, THEME["accent"], 4, ss(4.6, 5.2, t))
    tag(c, "0 °C altı", 670, zy2 + 12, THEME["accent"], ss(4.6, 5.2, t), 32, "r", "Bold")
    k2 = pop(t, 5.6)
    if k2 > 0:
        rrect(c, 600, 560, 360, 90, 24, THEME["accent"], 0.9 * clamp(k2)); tag(c, "tuzlu su: sonra", 780, 620, "#0a3440", clamp(k2), 36, "c", "Bold")
    tag(c, "donma noktası alçalır", 540, 1170, "#ffffff", ss(6.4, 7.0, t), 38, "c", "Bold")

_r4 = np.random.default_rng(13)
G4 = [(float(_r4.uniform(-1, 1)), float(_r4.uniform(-1, 1)), float(_r4.uniform(0, 6.28))) for _ in range(22)]
def i4(c, t, d):
    tag(c, "hava: -5 °C", 540, 540, "#ffffff", ss(0.4, 0.9, t), 40, "c", "Bold")
    rrect(c, 110, 700, 860, 420, 40, ROAD)
    melt = ss(1.0, d - 0.6, t)
    rrect(c, 150, 740, 780, 340, 34, ICE, 0.9 * (1 - 0.75 * melt))
    r = 60 + 300 * melt
    c.save(); c.translate(540, 910); c.scale(1.0, 0.48)
    circ(c, 0, 0, r, BRINE, 0.9); c.restore()
    for (u, v, ph) in G4:
        x = 540 + u * (r * 1.05 + 40); y = 910 + v * (r * 0.5 + 30)
        dis = ss(0.0, 1.0, (math.hypot(u, v) * 0.7 - melt + 0.4) * -2.5 + 1)
        grain(c, x, y, 18, ph, 1 - dis)
    k = ss(2.6, 3.2, t)
    if k > 0:
        arrow(c, 210, 650, 360, 650, THEME["accent"], 8, k, 20)
        tag(c, "erir", 160, 662, THEME["accent"], k, 38, "c", "Bold")
        tag(c, "yeni tuz çözer", 600, 662, THEME["accent"], k, 38, "c", "Bold")
        arrow(c, 820, 650, 960, 650, THEME["accent"], 8, ss(3.4, 4.0, t), 20)
    tag(c, "erime yayılır", 540, 1180, "#ffffff", ss(4.6, 5.2, t), 40, "c", "Bold")

SCENES = [
 title_scene("Tuz buzu", "neden eritir?", "Kış yollarının sırrı", hero),
 reason_scene("NEDEN 1", "Buzun üstünde su var", ["Buzun yüzeyinde ince bir su olur;", "tuz bu suda çözünür, tuzlu su oluşur."], i1),
 reason_scene("NEDEN 2", "Tuz düzeni bozar", ["Donan su düzenli kristal kurar;", "araya giren tuz bu düzeni bozar."], i2),
 reason_scene("NEDEN 3", "Donma noktası düşer", ["Tuzlu su sıfır derecede donmaz;", "donmak için daha çok soğumalı."], i3),
 reason_scene("NEDEN 4", "Erime yayılır", ["Tuzlu suya değen buz erir; oluşan", "su yeni tuz çözer, erime yayılır."], i4),
 cards_scene("AMA", "Tuzun da sınırı var", [("Çok soğukta zayıflar", "Sert ayazda etkisi iyice azalır"), ("Yola kum da serpilir", "Eritmez ama kaymayı azaltır"), ("Deniz suyu geç donar", "Yaklaşık eksi iki derecede")]),
 end_scene("Tuz buzu ısıtmaz;", "donmayı zorlaştırır.", hero),
]
if __name__ == "__main__":
    nb.main(SLUG, NARRATION, SCENES)
