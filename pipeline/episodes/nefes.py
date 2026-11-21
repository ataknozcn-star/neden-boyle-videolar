import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import numpy as np, skia
from nb import *
import nb

SLUG = "nefes-neden-gorunur"
nb.THEME.update(bg=["#2b4170", "#1a2848", "#0c1429"], accent="#a8e4ff")
NARRATION = [
 "Soğuk havada nefesimiz neden görünür? Ağzımızdan çıkan o beyaz bulutun sırrı.",
 "Ciğerlerimizden çıkan hava sıcak ve nemlidir. İçinde gözle göremediğimiz bol miktarda su buharı vardır.",
 "Sıcak hava çok su buharı taşıyabilir. Ama hava soğudukça, taşıyabileceği buhar miktarı azalır.",
 "Nefesimiz soğuk havaya karışınca hızla soğur. Taşıyamadığı fazla buhar, minicik su damlacıklarına dönüşür.",
 "Bu milyonlarca damlacık ışığı saçar ve beyaz bir bulut gibi görünür. Az sonra damlacıklar yeniden buharlaşır ve bulut kaybolur.",
 "Hava ne kadar soğuksa, nefesimiz o kadar kolay görünür. Hava nemliyse bulut daha belirgin olur. Sıcak havada ise buhar gaz olarak kalır, hiçbir şey görmeyiz.",
 "Gördüğümüz şey duman değil, nefesimizden doğan minik bir bulut. Neden böyle? Artık biliyorsunuz.",
]
SKIN, HAT, SCARF, VAPC, WARM, COLD, DROPC = "#f2c9a0", "#e2574c", "#f4b942", "#bfeaff", "#ff8a5c", "#7cc8ff", "#9fd8ff"
_r = np.random.default_rng(7)
SNOW = [(float(_r.uniform(80, 1000)), float(_r.uniform(0, 1)), float(_r.uniform(4, 9))) for _ in range(34)]

def snow(c, t, y0=560, y1=1180, a=1.0):
    for (x, ph, r) in SNOW:
        u = (t * 0.12 + ph) % 1
        circ(c, x + 14 * math.sin(t * 1.3 + ph * 9), lerp(y0, y1, u), r, "#ffffff", 0.55 * a * ss(0, 0.1, u) * (1 - ss(0.85, 1, u)))

def head(c, x, y, s=1.0, a=1.0):
    rrect(c, x - 95 * s, y + 85 * s, 190 * s, 58 * s, 26 * s, SCARF, a)          # atkı
    rrect(c, x - 70 * s, y + 120 * s, 46 * s, 100 * s, 18 * s, SCARF, a)
    circ(c, x, y, 110 * s, SKIN, a)                                                # yüz
    circ(c, x + 104 * s, y + 5 * s, 22 * s, SKIN, a)                               # burun
    circ(c, x + 46 * s, y - 22 * s, 11 * s, "#2a2238", a)                          # göz
    circ(c, x - 10 * s, y + 30 * s, 20 * s, "#f7a9a0", 0.6 * a)                    # yanak
    circ(c, x + 86 * s, y + 52 * s, 14 * s, "#7a3a3a", a)                          # üfleyen ağız
    c.save(); c.clipRect(skia.Rect(x - 140 * s, y - 160 * s, x + 140 * s, y - 28 * s))
    circ(c, x, y - 8 * s, 122 * s, HAT, a); c.restore()                           # bere
    rrect(c, x - 124 * s, y - 52 * s, 248 * s, 40 * s, 18 * s, "#f1e6dc", a)
    circ(c, x - 10 * s, y - 138 * s, 30 * s, "#f1e6dc", a)                         # ponpon

def breath(c, mx, my, t, a=1.0, n=9, reach=420, rmax=70, color="#ffffff", op=0.55, speed=0.45):
    for k in range(n):
        u = (t * speed + k / n) % 1
        x = mx + reach * eout(u * 1.1); y = my - 30 * u + 14 * math.sin(t * 2 + k)
        circ(c, x, y, 16 + rmax * u, color, op * a * math.sin(math.pi * u))

def hero(c, t):
    snow(c, t, 600, 1180)
    head(c, 360, 900, 1.25)
    breath(c, 360 + 108 * 1.25, 900 + 65 * 1.25, t, ss(0.4, 1.0, t), 16, 400, 95, op=0.42, speed=0.35)

VAP1 = [(float(_r.uniform(0, 1)), float(_r.uniform(-1, 1))) for _ in range(30)]
def i1(c, t, d):
    snow(c, t, 520, 1150, 0.5)
    head(c, 280, 820, 1.15)
    mx, my = 280 + 124, 820 + 60
    for k, (ph, dy) in enumerate(VAP1):                                           # görünmez buhar
        u = (t * 0.35 + ph) % 1; x = mx + 30 + 520 * u; y = my + dy * 120 * u + 10 * math.sin(t * 3 + k)
        circ(c, x, y, 7, VAPC, 0.75 * ss(0.6, 1.2, t) * math.sin(math.pi * u))
    k = ss(0.9, 1.5, t)
    for j in range(3):
        ang = (j - 1) * 0.25; arrow(c, mx + 40, my, mx + 40 + 300 * k * math.cos(ang), my + 300 * k * math.sin(ang), WARM, 9, 0.85 * k, 26)
    tag(c, "sıcak", 760, 640, WARM, ss(1.6, 2.1, t), 44, "c", "Bold")
    tag(c, "+ nemli", 760, 700, THEME["accent"], ss(2.4, 2.9, t), 44, "c", "Bold")
    tag(c, "görünmez su buharı", 640, 1100, VAPC, ss(3.4, 3.9, t), 38, "c")

BOXA = [(float(_r.uniform(0, 1)), float(_r.uniform(0, 1)), float(_r.uniform(0, 6.28))) for _ in range(40)]
def box(c, x, y, w, h, color, n, t, a=1.0, drops=0.0):
    rrect(c, x, y, w, h, 30, color, 0.10 * a); rrect(c, x, y, w, h, 30, color, 0.9 * a, sw=6)
    for i, (u, v, ph) in enumerate(BOXA[:n]):
        circ(c, x + 30 + (w - 60) * u + 8 * math.sin(t * 2.5 + ph), y + 30 + (h - 60) * v + 8 * math.cos(t * 2.2 + ph), 9, VAPC, 0.85 * a)
    if drops > 0:
        for i, (u, v, ph) in enumerate(BOXA[n:n + 10]):
            dy = (h - 80) * min(1, drops * (0.7 + 0.3 * v))
            drop(c, x + 40 + (w - 80) * u, y + 50 + dy * 0.6 + 20 * v, 13, ss(0, 0.15, drops), DROPC)
def i2(c, t, d):
    box(c, 100, 640, 400, 440, WARM, 34, t, ss(0.4, 0.9, t))
    tag(c, "sıcak hava", 300, 600, WARM, ss(0.6, 1.1, t), 42, "c", "Bold")
    a2 = ss(3.0, 3.5, t)
    box(c, 580, 640, 400, 440, COLD, 9, t, a2, ss(4.0, 5.6, t))
    tag(c, "soğuk hava", 780, 600, COLD, a2, 42, "c", "Bold")
    tag(c, "çok buhar", 300, 1140, THEME["text"], ss(1.4, 1.9, t), 36, "c")
    tag(c, "az buhar", 780, 1140, THEME["text"], ss(3.6, 4.1, t), 36, "c")

VAP3 = [(float(_r.uniform(0, 1)), float(_r.uniform(-1, 1))) for _ in range(40)]
def i3(c, t, d):
    rrect(c, 560, 520, 470, 640, 40, COLD, 0.12)
    for k in range(5):
        fx, fy = 620 + (k * 97) % 380, 650 + (k * 131) % 360
        for j in range(3):
            ang = j * math.pi / 3; line(c, fx - 16 * math.cos(ang), fy - 16 * math.sin(ang), fx + 16 * math.cos(ang), fy + 16 * math.sin(ang), "#ffffff", 4, 0.45)
    tag(c, "soğuk hava", 795, 580, COLD, ss(0.6, 1.1, t), 36, "c", "Bold")
    head(c, 200, 820, 0.85)
    mx, my = 200 + 90, 820 + 45
    k = ss(1.4, 2.4, t)
    for i, (ph, dy) in enumerate(VAP3):
        u = (t * 0.22 + ph) % 1; x = mx + 30 + 680 * u * (0.3 + 0.7 * k); y = my + dy * 160 * u + 8 * math.sin(t * 3 + i)
        a = math.sin(math.pi * min(1, u * 1.05))
        turn = ss(560, 640, x) * ss(2.8, 3.8, t)                                   # soğuk bölgede damlaya döner
        if turn < 0.98: circ(c, x, y, 7, VAPC, 0.8 * a * (1 - turn))
        if turn > 0.02: drop(c, x, y, 6 + 6 * turn, a * turn, DROPC)
    tag(c, "buhar", 330, 1060, VAPC, ss(1.0, 1.5, t), 38, "c")
    arrow(c, 440, 1048, 590, 1048, THEME["text"], 6, ss(3.6, 4.1, t), 20)
    tag(c, "damlacık", 760, 1060, DROPC, ss(4.0, 4.5, t), 38, "c", "Bold")

def i4(c, t, d):
    snow(c, t, 520, 1150, 0.4)
    head(c, 230, 860, 1.0)
    mx, my = 230 + 100, 860 + 55
    fade = 1 - ss(d - 3.2, d - 1.2, t)
    grow = ss(0.4, 2.0, t)
    for k in range(7):
        circ(c, mx + 120 + k * 75, my - 10 + 25 * math.sin(k * 1.7 + t), (40 + k * 12) * grow, "#ffffff", 0.5 * fade)
    sun(c, 900, 590, 48, t, ss(1.6, 2.0, t))
    for j in range(3):
        kk = ss(2.0 + j * 0.3, 2.8 + j * 0.3, t)
        x1, y1 = lerp(860, 600 + j * 110, kk), lerp(640, 880, kk)
        line(c, 860, 640, x1, y1, GOLD, 6, 0.8 * kk * fade)
    if t > 3.0:
        for k in range(10):
            ang = k * math.pi / 5 + 0.3; L = ((t - 3.0) * 120 + k * 29) % 150
            line(c, 700 + math.cos(ang) * (60 + L), 900 + math.sin(ang) * (60 + L), 700 + math.cos(ang) * (85 + L), 900 + math.sin(ang) * (85 + L), GOLD, 5, 0.7 * (1 - L / 150) * fade)
    tag(c, "minik bir bulut", 640, 1120, THEME["accent"], ss(3.4, 3.9, t) * fade, 44, "c", "Bold")
    tag(c, "buharlaşıp kaybolur", 600, 1120, THEME["text"], ss(d - 2.2, d - 1.6, t), 40, "c")

SCENES = [
 title_scene("Soğukta nefesimiz", "neden görünür?", "Ağızdan çıkan bulutun sırrı", hero),
 reason_scene("NEDEN 1", "Nefes sıcak ve nemli", ["Ciğerden çıkan hava sıcaktır;", "içinde görünmez su buharı vardır."], i1),
 reason_scene("NEDEN 2", "Soğuk hava, az buhar", ["Sıcak hava çok buhar taşıyabilir,", "soğuk hava ise çok daha az."], i2),
 reason_scene("NEDEN 3", "Buhar damlaya döner", ["Nefes soğuk havaya karışıp soğur;", "fazla buhar minik damlalara döner."], i3),
 reason_scene("NEDEN 4", "Minik bir bulut", ["Damlacıklar ışığı saçar; beyaz", "bir bulut görürüz, sonra kaybolur."], i4),
 cards_scene("ÖZET", "Ne zaman görünür?", [("Hava soğuksa", "Buhar daha kolay yoğuşur"), ("Hava nemliyse", "Bulut daha belirgin olur"), ("Hava sıcaksa görünmez", "Buhar gaz olarak kalır")]),
 end_scene("Bu duman değil;", "minik bir bulut.", hero),
]
if __name__ == "__main__":
    nb.main(SLUG, NARRATION, SCENES)
