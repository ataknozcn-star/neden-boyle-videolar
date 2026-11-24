import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import numpy as np, skia
from nb import *
import nb

SLUG = "metal-neden-soguk-hissettirir"
nb.THEME.update(bg=["#24425a", "#172b3d", "#0c1622"], accent="#8fd3ff")
NARRATION = [
 "Metal neden tahtadan daha soğuk hissettirir? Üstelik ikisi aynı sıcaklıktayken.",
 "Şaşırtıcı ama gerçek: Aynı odadaki metal ve tahta, aynı sıcaklıktadır. Termometre bunu kanıtlar.",
 "Elimiz, odadaki eşyalardan daha sıcaktır. Bir cisme dokununca ısı, sıcak elden serin cisme akar.",
 "Metal ısıyı çok iyi iletir; elimizdeki ısıyı hızla çekip uzaklaştırır. Tahta ise ısıyı çok yavaş iletir.",
 "Derimiz cismin sıcaklığını ölçemez; kendi ısısını ne kadar hızlı kaybettiğini hisseder. Isı hızla kaçınca, metal daha soğuk gelir.",
 "Peki tersi? Güneşte ısınan metal ve tahta aynı sıcaklıktaysa, bu kez metal daha sıcak hissettirir. Çünkü ısıyı elimize çok daha hızlı aktarır.",
 "Elimiz bir termometre değil, ısı akışını hisseder. Neden böyle? Artık biliyorsunuz.",
]
MET, METL, METD = "#a9b6c3", "#dde6ee", "#6f7d8a"
WOOD, WOODD = "#b07a45", "#7d5129"
SKIN, SKIND = "#f2c49b", "#d9a477"
HEAT, COLD = "#ff8a4c", "#8fd3ff"

def metal_block(c, x, y, w, h, a=1.0):
    rrect(c, x, y, w, h, 22, MET, a); rrect(c, x + 14, y + 12, w - 28, h * 0.22, 14, METL, a * 0.7)
    rrect(c, x, y + h * 0.78, w, h * 0.22, 22, METD, a * 0.6)
    line(c, x + w * 0.18, y + h * 0.45, x + w * 0.36, y + h * 0.45, METL, 8, a * 0.6)

def wood_block(c, x, y, w, h, a=1.0):
    rrect(c, x, y, w, h, 22, WOOD, a)
    for k in range(4):
        p = skia.Path(); yy = y + h * (0.2 + k * 0.2)
        for j in range(0, int(w) - 30, 8):
            xx = x + 15 + j; py = yy + 7 * math.sin(j / 37 + k)
            p.moveTo(xx, py) if j == 0 else p.lineTo(xx, py)
        c.drawPath(p, stroke(WOODD, 5, a * 0.8))
    c.drawOval(skia.Rect.MakeXYWH(x + w * 0.6, y + h * 0.42, 40, 22), stroke(WOODD, 5, a * 0.8))

def thermo(c, x, y, lvl, a=1.0, h=230):
    rrect(c, x - 20, y, 40, h, 20, "#ffffff", a * 0.9); circ(c, x, y + h + 18, 36, "#ffffff", a * 0.9)
    circ(c, x, y + h + 18, 26, "#ff5d5d", a); rrect(c, x - 9, y + h - (h - 30) * lvl, 18, (h - 30) * lvl + 20, 9, "#ff5d5d", a)

def finger(c, x, ybot, a=1.0, w=120, h=330):
    rrect(c, x - w / 2, ybot - h, w, h, w / 2, SKIN, a)
    rrect(c, x - w / 2 + 14, ybot - h, 26, h - 30, 13, "#ffffff", a * 0.18)
    rrect(c, x - 30, ybot - 95, 60, 70, 26, "#ffe3cc", a * 0.85)
    for k in range(2): line(c, x - 30, ybot - 170 - k * 26, x + 30, ybot - 170 - k * 26, SKIND, 5, a * 0.8)

def heat_dots(c, x0, y0, x1, y1, n, speed, t, color, a=1.0, r=12):
    for k in range(n):
        u = (t * speed + k / n) % 1
        circ(c, lerp(x0, x1, u), lerp(y0, y1, u), r, color, a * math.sin(u * math.pi))

def snow(c, x, y, r, a=1.0, color=COLD):
    for k in range(3):
        ang = k * math.pi / 3; dx, dy = r * math.cos(ang), r * math.sin(ang)
        line(c, x - dx, y - dy, x + dx, y + dy, color, 8, a)
    circ(c, x, y, r * 0.22, color, a)

def hero(c, t):
    metal_block(c, 110, 860, 390, 230)
    wood_block(c, 580, 860, 390, 230)
    snow(c, 305, 720 + 8 * math.sin(t * 2), 70, 0.95)
    for k in range(3):
        u = (t * 0.5 + k / 3) % 1
        circ(c, 735 + k * 40, 790 - 90 * u, 14, HEAT, 0.7 * math.sin(u * math.pi))
    tag(c, "metal", 305, 1150, METL, 1, 40, "c", "Bold"); tag(c, "tahta", 775, 1150, "#e2b17d", 1, 40, "c", "Bold")

def i1(c, t, d):
    metal_block(c, 100, 880, 380, 200); wood_block(c, 600, 880, 380, 200)
    lv = 0.55 * ss(0.8, 2.2, t)
    thermo(c, 290, 570, lv); thermo(c, 790, 570, lv)
    tag(c, "20 °C", 290, 545, "#ffffff", ss(2.2, 2.7, t), 46, "c", "Bold")
    tag(c, "20 °C", 790, 545, "#ffffff", ss(2.2, 2.7, t), 46, "c", "Bold")
    tag(c, "aynı sıcaklık!", 540, 1140, THEME["accent"], ss(3.4, 3.9, t), 46, "c", "Bold")

def i2(c, t, d):
    metal_block(c, 200, 960, 680, 170)
    k = eout(ss(0.4, 1.4, t)); finger(c, 540, lerp(780, 965, k))
    if t > 1.6:
        for j in range(5):
            xx = 450 + j * 45
            heat_dots(c, xx, 900, xx + (j - 2) * 40, 1100, 2, 0.8, t + j * 0.3, HEAT, ss(1.6, 2.1, t), 11)
    tag(c, "el: sıcak", 820, 640, HEAT, ss(1.0, 1.5, t), 42, "c", "Bold")
    tag(c, "cisim: serin", 540, 1180, COLD, ss(1.6, 2.1, t), 40, "c", "Bold")
    arrow(c, 740, 700, 640, 850, HEAT, 8, ss(2.4, 2.9, t), 24)
    tag(c, "ısı akar", 270, 900, "#ffd0b0", ss(2.6, 3.1, t), 42, "c", "Bold"); arrow(c, 330, 920, 440, 995, "#ffd0b0", 7, ss(2.6, 3.1, t), 20)

def i3(c, t, d):
    metal_block(c, 90, 960, 420, 170); wood_block(c, 570, 960, 420, 170)
    finger(c, 300, 965, w=110, h=300); finger(c, 780, 965, w=110, h=300)
    a = ss(0.8, 1.3, t)
    for j in range(5):
        heat_dots(c, 300, 950, 120 + j * 90, 1110, 3, 1.3, t + j * 0.2, HEAT, a, 10)
    b = ss(4.4, 4.9, t)
    heat_dots(c, 780, 950, 780, 1020, 2, 0.25, t, HEAT, b, 10)
    tag(c, "metal: hızlı", 300, 600, METL, ss(1.4, 1.9, t), 44, "c", "Bold")
    tag(c, "tahta: yavaş", 780, 600, "#e2b17d", ss(4.6, 5.1, t), 44, "c", "Bold")

def i4(c, t, d):
    tag(c, "elden kaçan ısı", 540, 560, THEME["text"], ss(0.6, 1.1, t), 42, "c", "Bold")
    for j, (lbl, colr, full, t0) in enumerate((("metal", MET, 0.95, 1.2), ("tahta", WOOD, 0.25, 2.2))):
        y = 680 + j * 200; k = eout(ss(t0, t0 + 1.0, t))
        tag(c, lbl, 120, y + 62, colr, ss(t0 - 0.3, t0, t), 44, "l", "Bold")
        rrect(c, 330, y, 640, 90, 45, "#ffffff", 0.12)
        if k > 0: rrect(c, 330, y, 640 * full * k, 90, 45, HEAT, 1)
    s = ss(5.4, 6.0, t)
    snow(c, 400, 1080, 50, s); tag(c, "çok soğuk!", 640, 1100, COLD, s, 46, "c", "Bold")

SCENES = [
 title_scene("Metal neden", "daha soğuk?", "Aynı sıcaklık, farklı his", hero),
 reason_scene("NEDEN 1", "Aynı sıcaklıktalar", ["Odada bekleyen metal ve tahta", "aynı sıcaklıktadır."], i1),
 reason_scene("NEDEN 2", "Isı elden cisme akar", ["Elimiz odadaki eşyalardan sıcaktır;", "dokununca ısı cisme akar."], i2),
 reason_scene("NEDEN 3", "Metal ısıyı iyi iletir", ["Metal ısıyı hızla çeker,", "tahta ise çok yavaş iletir."], i3),
 reason_scene("NEDEN 4", "Deri ısı kaybını sezer", ["Deri cismin sıcaklığını ölçemez;", "ısı hızla kaçınca soğuk hissederiz."], i4),
 cards_scene("BONUS", "Güneşte tam tersi!", [("İkisi de aynı sıcaklıkta", "Güneşte ısınan metal ve tahta"), ("Metal daha sıcak gelir", "Isıyı ele hızlı aktarır"), ("Tahta daha ılık gelir", "Isıyı yavaş iletir")]),
 end_scene("Elimiz termometre değil;", "ısı akışını hisseder.", hero),
]
if __name__ == "__main__":
    nb.main(SLUG, NARRATION, SCENES)
