import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import numpy as np, skia
from nb import *
import nb

SLUG = "buzdolabi-nasil-sogutur"
nb.THEME.update(bg=["#0f5a6e", "#0a3a4a", "#05202b"], accent="#8ff0ff")
ICE = "#8fe3ff"
HOT = "#ff6b4a"
BODY = "#eef6f8"
NARRATION = [
 "Buzdolabı içini nasıl soğutur? Sırrı, borularda dolaşan bir sıvıda.",
 "Buzdolabı soğuk üretmez. İçerideki ısıyı alır ve dışarı taşır.",
 "Borularda soğutucu bir sıvı dolaşır. Bu sıvı içeride buharlaşırken, yiyeceklerden ve havadan ısı çeker.",
 "Isınan gaz, kompresöre gider. Kompresör gazı sıkıştırır; gazın basıncı ve sıcaklığı yükselir.",
 "Sıcak gaz, dolabın arkasındaki borulardan geçer. Isısını odaya verir ve yeniden sıvıya döner. Dolabın arkası bu yüzden ılıktır.",
 "Peki döngü nasıl kapanır? Sıvı dar bir borudan geçer ve basıncı düşer. Sıvı soğur, yeniden içeri girer ve her şey baştan başlar.",
 "Yani buzdolabı soğuk yapmaz; ısıyı dışarı taşır. Neden böyle? Artık biliyorsunuz.",
]

def fridge(c, x, y, s=1.0, a=1.0, open_=False):
    w, h = 300 * s, 520 * s; x0, y0 = x - w / 2, y - h / 2
    rrect(c, x0, y0, w, h, 34 * s, BODY, a)
    if open_:
        rrect(c, x0 + 22 * s, y0 + 22 * s, w - 44 * s, h - 44 * s, 18 * s, "#163e4c", a)
        for k in (1, 2): line(c, x0 + 22 * s, y0 + h * k / 3, x0 + w - 22 * s, y0 + h * k / 3, ICE, 5 * s, 0.6 * a)
    else:
        line(c, x0 + 10 * s, y0 + h * 0.36, x0 + w - 10 * s, y0 + h * 0.36, "#9fb7bf", 6 * s, a)
        rrect(c, x0 + w - 58 * s, y0 + 50 * s, 14 * s, 70 * s, 7 * s, "#9fb7bf", a)
        rrect(c, x0 + w - 58 * s, y0 + h * 0.36 + 40 * s, 14 * s, 110 * s, 7 * s, "#9fb7bf", a)

def flake(c, x, y, r, a=1.0, rot=0.0):
    for k in range(6):
        ang = rot + k * math.pi / 3; ex, ey = x + math.cos(ang) * r, y + math.sin(ang) * r
        line(c, x, y, ex, ey, ICE, max(3, r * 0.14), a)
        for sgn in (-1, 1):
            mx, my = x + math.cos(ang) * r * 0.6, y + math.sin(ang) * r * 0.6
            line(c, mx, my, mx + math.cos(ang + sgn * 0.8) * r * 0.32, my + math.sin(ang + sgn * 0.8) * r * 0.32, ICE, max(2, r * 0.1), a)

def heatwave(c, x, y, h, t, a=1.0, ph=0.0):
    p = skia.Path()
    for k in range(0, int(h) + 1, 6):
        xx = x + 14 * math.sin(k / 26 + t * 4 + ph); yy = y - k
        p.moveTo(xx, yy) if k == 0 else p.lineTo(xx, yy)
    c.drawPath(p, stroke(HOT, 8, a))

def hero(c, t):
    fridge(c, 500, 900, 1.0)
    for k in range(3):
        u = (t * 0.5 + k / 3) % 1
        heatwave(c, 720 + k * 50, 1100 - u * 120, 160, t, (1 - u) * ss(0, 0.2, u), k)
    flake(c, 500, 770, 50, 1, t * 0.4)
    for k, (fx, fy, r) in enumerate([(300, 640, 26), (330, 1120, 22), (250, 880, 18)]):
        flake(c, fx, fy + 8 * math.sin(t * 1.5 + k), r, 0.8, -t * 0.5 + k)

def i1(c, t, d):
    fridge(c, 330, 840, 0.95, 1, True)
    tag(c, "içerisi", 330, 1150, ICE, ss(0.6, 1.1, t), 36, "c", "Bold")
    tag(c, "oda", 820, 1150, "#ffb19c", ss(0.6, 1.1, t), 36, "c", "Bold")
    for k in range(6):
        u = ((t - 1.0) * 0.35 + k / 6) % 1 if t > 1.0 else 0
        if t <= 1.0: continue
        x = lerp(330, 860, u); y = 840 + 120 * math.sin(k * 1.7) * (1 - u) - 60 * u
        circ(c, x, y, 18, HOT, ss(0, 0.1, u) * (1 - ss(0.85, 1, u)))
    arrow(c, 520, 700, 760, 700, HOT, 10, ss(1.2, 1.8, t), 26)
    tag(c, "ısı dışarı", 640, 660, "#ffb19c", ss(1.6, 2.1, t), 34, "c")

def pipe_path(c, pts, color, w=22, a=1.0):
    poly(c, pts, color, a, sw=w, close=False)

def i2(c, t, d):
    rrect(c, 110, 560, 860, 560, 40, "#163e4c")
    rrect(c, 110, 560, 860, 560, 40, ICE, 0.5, sw=4)
    # buharlaştırıcı borusu
    pts = [(170, 650), (910, 650), (910, 760), (170, 760), (170, 870), (910, 870)]
    pipe_path(c, pts, "#7fa9b5", 26)
    # boru içinde akan damlalar -> buhar
    for k in range(10):
        u = (t * 0.18 + k / 10) % 1
        L = [(pts[i], pts[i + 1]) for i in range(len(pts) - 1)]
        seg = min(4, int(u * 5)); f = u * 5 - seg; (ax, ay), (bx, by) = L[seg]
        x, y = lerp(ax, bx, f), lerp(ay, by, f)
        if u < 0.45: drop(c, x, y, 11, 0.95, ICE)
        else: circ(c, x, y, 10 + 6 * ss(0.45, 1, u), "#ffffff", 0.8)
    # yiyecekler
    circ(c, 330, 1030, 62, "#e8463c"); line(c, 330, 968, 340, 945, "#4c8a3c", 8)
    rrect(c, 620, 975, 170, 110, 24, "#f5d36a")
    for k in range(5):
        u = (t * 0.6 + k / 5) % 1; src = (330, 970) if k % 2 else (705, 970)
        circ(c, src[0], lerp(src[1], 885, u), 13, HOT, ss(0, 0.15, u) * (1 - ss(0.8, 1, u)) * ss(1.0, 1.6, t))
    tag(c, "sıvı gaza döner", 540, 610, "#ffffff", ss(1.8, 2.3, t), 34, "c", "Bold")
    tag(c, "ısıyı emer", 540, 945, "#ffb19c", ss(3.0, 3.5, t), 34, "c", "Bold")

def thermo(c, x, y, k, a=1.0):
    rrect(c, x - 22, y - 260, 44, 270, 22, "#ffffff", 0.25 * a)
    rrect(c, x - 12, y - 30 - 210 * k, 24, 40 + 210 * k, 12, mixcol(ICE, HOT, k), a)
    circ(c, x, y + 20, 38, mixcol(ICE, HOT, k), a)

def i3(c, t, d):
    k = ss(1.4, 4.2, t)
    top = 620 + 220 * k
    rrect(c, 230, 600, 440, 520, 26, "#ffffff", 0.9, sw=8)
    rrect(c, 242, top - 50, 416, 50, 10, "#b8c7cc")
    rrect(c, 425, 520, 50, top - 570, 10, "#8ea3aa")
    arrow(c, 450, 470, 450, 540, "#ffffff", 8, ss(1.2, 1.6, t) * (1 - ss(4.2, 4.6, t)), 22)
    rng = np.random.default_rng(5)
    for j in range(22):
        bx = float(rng.uniform(270, 630)); by = float(rng.uniform(0, 1))
        y = lerp(top + 20, 1090, by) + 6 * math.sin(t * (6 + 6 * k) + j)
        circ(c, bx + 6 * math.cos(t * 7 + j), y, 15, mixcol(ICE, HOT, k))
    thermo(c, 850, 1020, k)
    tag(c, "basınç artar", 850, 640, "#ffffff", ss(2.4, 2.9, t), 36, "c", "Bold")
    tag(c, "sıcaklık artar", 850, 700, "#ffb19c", ss(3.0, 3.5, t), 36, "c", "Bold")

def i4(c, t, d):
    pts = [(260, 600)]
    for r in range(7):
        y = 600 + r * 72; pts += [(820, y), (820, y + 36), (260, y + 36), (260, y + 72)] if r < 6 else [(820, y)]
    pts = pts[:-1]
    k = ss(0.8, 4.5, t)
    pipe_path(c, pts, "#5f6d72", 20)
    for j in range(len(pts) - 1):
        f = j / (len(pts) - 1)
        col_ = mixcol(HOT, ICE, ss(0.2, 1, f))
        (ax, ay), (bx, by) = pts[j], pts[j + 1]
        if f < k: line(c, ax, ay, bx, by, col_, 10)
    for q in range(5):
        u = (t * 0.45 + q / 5) % 1
        heatwave(c, 900 + (q % 2) * 50, 980 - u * 300 + q * 20, 120, t, (1 - u) * ss(0, 0.2, u) * ss(1.2, 1.8, t), q)
    tag(c, "ısı odaya", 920, 560, "#ffb19c", ss(1.8, 2.3, t), 34, "c", "Bold")
    for j in range(4):
        drop(c, 340 + j * 140, 1095, 16, ss(3.6 + j * 0.2, 4.0 + j * 0.2, t), ICE)
    tag(c, "gaz sıvıya döner", 540, 1165, ICE, ss(4.0, 4.5, t), 34, "c", "Bold")

SCENES = [
 title_scene("Buzdolabı", "nasıl soğutur?", "Dolaşan sıvının sırrı", hero),
 reason_scene("NEDEN 1", "Soğuk değil, ısı taşır", ["Buzdolabı soğuk üretmez;", "içerideki ısıyı alıp dışarı taşır."], i1),
 reason_scene("NEDEN 2", "Buharlaşma ısı çeker", ["Soğutucu sıvı içeride buharlaşır,", "yiyeceklerden ve havadan ısı çeker."], i2),
 reason_scene("NEDEN 3", "Kompresör sıkıştırır", ["Kompresör gazı sıkıştırır;", "basıncı ve sıcaklığı yükselir."], i3),
 reason_scene("NEDEN 4", "Isı arkadan atılır", ["Sıcak gaz arkadaki borularda", "ısısını odaya verir, sıvıya döner."], i4),
 cards_scene("ÖZET", "Döngü nasıl kapanır?", [("Dar borudan geçer", "Sıvının basıncı düşer"), ("Sıvı soğur", "İçeri girmeye hazır"), ("Döngü baştan başlar", "Isı yine dışarı taşınır")]),
 end_scene("Buzdolabı soğuk yapmaz;", "ısıyı dışarı taşır.", hero),
]
if __name__ == "__main__":
    nb.main(SLUG, NARRATION, SCENES)
