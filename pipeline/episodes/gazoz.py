import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import numpy as np, skia
from nb import *
import nb

SLUG = "gazli-icecek-neden-kopurur"
nb.THEME.update(bg=["#0f5a5a", "#0a3b40", "#061f24"], accent="#c6f25a")
NARRATION = [
 "Gazlı içecek açınca neden köpürür? Sırrı, şişenin içindeki basınçta.",
 "Fabrikada içeceğe, yüksek basınçla karbondioksit gazı basılır. Gaz sıvının içinde çözünür ve gözle görünmez.",
 "Kapağı açınca basınç birden düşer. Sıvı artık bu kadar çok gazı tutamaz. Fazla gaz dışarı çıkmak ister.",
 "Gaz, kabarcık olmak için bir başlangıç noktası arar. Bardaktaki çizikler, toz ve lifler bu tohumları sağlar.",
 "Kabarcıklar bu noktalarda büyür, kopar ve yüzeye yükselir. İşte gördüğümüz köpük budur.",
 "Soğuk içecek gazı daha iyi tutar. Çalkalanan şişede küçük kabarcıklar oluşur, açınca taşar. Açık kalan içecek ise zamanla gazını kaybeder.",
 "Köpük, kaçan gazın ta kendisidir. Neden böyle? Artık biliyorsunuz.",
]
DRINK, DRINK2, GLASS, FOAM, CAPC = "#e9d75a", "#c9b23a", "#dff6f6", "#fffbe8", "#e0524a"
_r = np.random.default_rng(7)
BUB = [(float(_r.uniform(-1, 1)), float(_r.uniform(0, 1)), float(_r.uniform(5, 13)), float(_r.uniform(0.5, 1.2))) for _ in range(34)]

def glass(c, x, y, s, t, level=1.0, fizz=1.0):
    top, bot, h = 175 * s, 135 * s, 430 * s
    y0 = y - h / 2; y1 = y + h / 2
    ly = y1 - (h - 50 * s) * level
    lw = lerp(bot, top, (y1 - ly) / h)
    poly(c, [(x - lw, ly), (x + lw, ly), (x + bot, y1), (x - bot, y1)], DRINK, 0.95)
    poly(c, [(x - lw * 0.55, ly), (x - lw * 0.2, ly), (x - bot * 0.25, y1), (x - bot * 0.6, y1)], "#ffffff", 0.18)
    for bx, by, r, sp in BUB:
        u = (by + t * 0.35 * sp) % 1; yy = lerp(y1 - 15 * s, ly + 10 * s, u)
        ww = lerp(bot, lw, u) - 25 * s
        circ(c, x + bx * ww + 6 * s * math.sin(t * 3 + by * 9), yy, r * s * (0.7 + 0.5 * u), "#ffffff", 0.75 * fizz, sw=3)
    if fizz > 0:
        for k in range(9):
            fx = x - lw + 15 * s + k * (2 * lw - 30 * s) / 8
            circ(c, fx, ly - 4 * s + 5 * s * math.sin(t * 4 + k), (24 + 8 * math.sin(k * 2.3)) * s, FOAM, fizz)
    poly(c, [(x - top, y0), (x + top, y0), (x + bot, y1), (x - bot, y1)], GLASS, 0.9, sw=7 * s)

def bottle(c, x, y, s, cap_dy=0.0, cap_rot=0.0, gas=0.0, t=0.0):
    rrect(c, x - 120 * s, y - 170 * s, 240 * s, 420 * s, 60 * s, DRINK, 0.9)
    poly(c, [(x - 120 * s, y - 120 * s), (x + 120 * s, y - 120 * s), (x + 48 * s, y - 300 * s), (x - 48 * s, y - 300 * s)], DRINK, 0.9)
    rrect(c, x - 48 * s, y - 340 * s, 96 * s, 60 * s, 10 * s, DRINK, 0.9)
    rrect(c, x - 120 * s, y - 170 * s, 240 * s, 420 * s, 60 * s, GLASS, 0.9, sw=7 * s)
    rrect(c, x - 90 * s, y - 20 * s, 180 * s, 120 * s, 16 * s, "#ffffff", 0.22)
    c.save(); c.translate(x, y - 365 * s + cap_dy); c.rotate(cap_rot)
    rrect(c, -58 * s, -22 * s, 116 * s, 46 * s, 10 * s, CAPC); c.restore()

DOTS = [(float(_r.uniform(450, 630)), float(_r.uniform(760, 1100))) for _ in range(18)]
def hero(c, t):
    glass(c, 540, 930, 1.0, t)
    for k in range(6):
        u = (t * 0.6 + k / 6) % 1
        circ(c, 470 + k * 28 + 14 * math.sin(t * 2 + k), lerp(700, 560, u), 9 + 5 * u, "#ffffff", 0.7 * (1 - u), sw=3)

def i1(c, t, d):
    bottle(c, 540, 890, 0.95)
    p = ss(0.5, 3.0, t)
    for k, (bx, by) in enumerate(DOTS):
        circ(c, bx + 4 * math.sin(t * 2 + k), by + 4 * math.cos(t * 1.7 + k), 8, "#ffffff", (0.25 + 0.45 * p) * (0.6 + 0.4 * math.sin(t * 3 + k)))
    for k, (ax, ay, dx) in enumerate(((230, 900, 1), (850, 900, -1))):
        q = ss(0.6 + k * 0.2, 1.4 + k * 0.2, t)
        for j in range(3):
            yy = ay - 120 + j * 120
            arrow(c, ax - dx * 40, yy, ax - dx * 40 + dx * 90 * q, yy, THEME["accent"], 10, q, 24)
    tag(c, "yüksek basınç", 540, 510, THEME["accent"], ss(1.2, 1.7, t), 42, "c", "Bold")

def gauge(c, x, y, r, v, a=1.0):
    circ(c, x, y, r, "#ffffff", 0.12 * a); circ(c, x, y, r, "#ffffff", 0.8 * a, sw=6)
    for k in range(7):
        ang = math.radians(150 + k * 40)
        line(c, x + math.cos(ang) * r * 0.78, y + math.sin(ang) * r * 0.78, x + math.cos(ang) * r * 0.92, y + math.sin(ang) * r * 0.92, "#ffffff", 5, a)
    ang = math.radians(150 + 240 * v)
    line(c, x, y, x + math.cos(ang) * r * 0.75, y + math.sin(ang) * r * 0.75, "#ff6b5a", 9, a); circ(c, x, y, 12, "#ff6b5a", a)

def i2(c, t, d):
    op = eout((t - 1.0) / 0.6) if t > 1.0 else 0
    bottle(c, 380, 900, 1.0, cap_dy=-170 * op, cap_rot=40 * op, t=t)
    if op > 0:
        for k in range(10):
            u = ((t - 1.0) * 0.9 + k * 0.1) % 1
            ang = math.radians(-90 + (k - 4.5) * 9)
            circ(c, 380 + math.cos(ang) * 260 * u, 560 + math.sin(ang) * 120 * u - 10, 8 + 6 * u, "#ffffff", 0.8 * (1 - u), sw=3)
        for k in range(14):
            u = (t * 0.5 + k / 14) % 1
            circ(c, 310 + (k * 37) % 140, lerp(1150, 620, u), 7 + 4 * u, "#ffffff", 0.8 * ss(1.2, 2.0, t), sw=3)
    v = lerp(0.92, 0.1, eout((t - 1.1) / 1.2) if t > 1.1 else 0)
    gauge(c, 800, 780, 150, v)
    tag(c, "basınç", 800, 990, "#ffffff", 0.9, 38, "c", "Bold")
    tag(c, "pısss!", 380, 470 + 0 * t, THEME["accent"], ss(1.1, 1.4, t) * (1 - ss(3.0, 3.6, t)), 52, "c", "Bold")
    tag(c, "gaz çıkmak ister", 800, 1080, THEME["accent"], ss(3.2, 3.7, t), 36, "c")

def i3(c, t, d):
    rrect(c, 120, 520, 840, 640, 40, DRINK, 0.85)
    rrect(c, 120, 520, 120, 640, 20, GLASS, 0.55)
    pts = [(240, 640 + k * 8 * (1 if k % 2 else -1)) for k in range(1)]
    sp = [(240, 640, "çizik", 0.6), (240, 860, "toz", 1.8), (240, 1060, "lif", 3.0)]
    p = skia.Path(); p.moveTo(240, 600)
    for k in range(1, 9): p.lineTo(240 - (14 if k % 2 else 0), 600 + k * 10)
    c.drawPath(p, stroke("#5a6b6b", 6))
    circ(c, 238, 860, 11, "#6b5a40")
    q = skia.Path(); q.moveTo(240, 1030); q.quadTo(275, 1060, 238, 1095); c.drawPath(q, stroke("#8a7a5a", 6))
    for j, (sx, sy, nm, t0) in enumerate(sp):
        k = ss(t0, t0 + 0.4, t)
        tag(c, nm, 262, sy + 62, "#1a3030", k, 34, "l", "Bold")
        if t > t0 + 0.4:
            for m in range(4):
                u = ((t - t0 - 0.4) * 0.45 + m * 0.25) % 1
                r = 8 + 22 * ss(0, 0.35, u)
                xx = lerp(sx + 10 + r, 900, ss(0.35, 1, u)); yy = sy - 80 * ss(0.35, 1, u) * (m % 2)
                circ(c, xx + 40 * (1 - ss(0.35, 1, u)) * 0, yy, r, "#ffffff", 0.85 * (1 - ss(0.85, 1, u)), sw=4)
    tag(c, "bardak duvarı", 180, 500, "#ffffff", ss(0.3, 0.8, t), 32, "c")

def i4(c, t, d):
    rrect(c, 160, 560, 760, 600, 40, DRINK, 0.85)
    for k in range(10):
        circ(c, 190 + k * 78, 562 + 6 * math.sin(t * 4 + k), 34 + 8 * math.sin(k * 2.1), FOAM)
    sx, sy = 540, 1120
    rrect(c, 160, 1140, 760, 20, 8, GLASS, 0.8)
    for m in range(5):
        u = (t * 0.32 + m * 0.2) % 1
        if u < 0.3:
            r = 10 + 30 * u / 0.3; circ(c, sx, sy - r, r, "#ffffff", 0.9, sw=4)
        else:
            v = (u - 0.3) / 0.7; r = 40 + 18 * v
            circ(c, sx + 30 * math.sin(v * 7 + m), lerp(sy - 40, 620, v), r, "#ffffff", 0.9 * (1 - ss(0.9, 1, v)), sw=4)
    tag(c, "büyür", 660, 1080, "#1a3030", ss(0.6, 1.0, t), 40, "l", "Bold")
    tag(c, "kopar", 660, 920, "#1a3030", ss(1.4, 1.8, t), 40, "l", "Bold")
    tag(c, "yükselir", 660, 760, "#1a3030", ss(2.2, 2.6, t), 40, "l", "Bold")
    tag(c, "köpük", 540, 510, THEME["accent"], ss(3.3, 3.8, t), 46, "c", "Bold")

SCENES = [
 title_scene("Gazlı içecek", "neden köpürür?", "Sırrı basınçta", hero),
 reason_scene("NEDEN 1", "Gaz basınçla çözünür", ["Karbondioksit yüksek basınçla basılır;", "sıvıda çözünür, gözle görünmez."], i1),
 reason_scene("NEDEN 2", "Basınç birden düşer", ["Kapak açılınca sıvı gazı tutamaz;", "fazla gaz dışarı çıkmak ister."], i2),
 reason_scene("NEDEN 3", "Kabarcık tohum arar", ["Çizik, toz ve lifler", "kabarcıkların başlangıç noktasıdır."], i3),
 reason_scene("NEDEN 4", "Kabarcıklar yükselir", ["Kabarcık büyür, kopar, yüzeye çıkar;", "gördüğümüz köpük budur."], i4),
 cards_scene("İPUÇLARI", "Gazı ne etkiler?", [("Soğuk gazı daha iyi tutar", "Sıcakta gaz daha çabuk kaçar"), ("Çalkalamak taşırır", "Küçük kabarcıklar tohum olur"), ("Açık kalan gazını kaybeder", "Zamanla içecek gazsızlaşır")]),
 end_scene("Köpük, kaçan", "gazın ta kendisi.", hero),
]
if __name__ == "__main__":
    nb.main(SLUG, NARRATION, SCENES)
