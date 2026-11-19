import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import numpy as np, skia
from nb import *
import nb

SLUG = "yumurta-neden-katilasir"
nb.THEME.update(bg=["#8a4a14", "#5a2c0c", "#2e1606"], accent="#ffd34d")
NARRATION = [
 "Yumurta pişince neden katılaşır? Cevap, proteinlerde saklı.",
 "Çiğ yumurtanın akı, suyun içinde yüzen proteinlerle doludur. Her protein, bir yumak gibi sıkıca katlanmıştır.",
 "Yumurta ısınınca bu yumaklar sarsılır ve açılır. Buna denatürasyon denir.",
 "Açılan proteinler birbirine yapışır ve suyu içinde hapseden bir ağ örer. Sıvı ak, böylece katılaşır.",
 "Topaklanan proteinler ışığın düz geçmesini engeller. Bu yüzden şeffaf ak, bembeyaz görünür.",
 "Ak, altmış ile altmış beş derece arasında katılaşmaya başlar. Sarısı biraz daha yüksek sıcaklık ister. Ve bu değişim geri dönmez.",
 "Pişen yumurta bir daha çiğe dönmez. Neden böyle? Artık biliyorsunuz.",
]
WHITE, YOLK, PAN = "#fbf6ea", "#ffb81f", "#3b3b44"

def fried_egg(c, x, y, s, t):
    for dx, dy, r in ((-60, -20, 110), (55, -40, 100), (70, 50, 105), (-50, 60, 100), (0, 0, 120)):
        circ(c, x + dx * s, y + dy * s, r * s, WHITE)
    circ(c, x + 8 * s, y + 4 * s, 58 * s, YOLK); circ(c, x - 10 * s, y - 14 * s, 16 * s, "#ffe7a3", 0.9)

def hero(c, t):
    line(c, 760, 820, 1000, 700, "#2a2a30", 46)
    circ(c, 540, 900, 300, "#24242a"); circ(c, 540, 900, 270, PAN)
    fried_egg(c, 540, 900, 1.25, t)
    for k in range(3):
        u = (t * 0.5 + k / 3) % 1
        puff(c, 420 + k * 120 + 12 * math.sin(t * 2 + k), 610 - u * 90, 26 + u * 20, 0.5 * (1 - u))

def coil(c, x, y, r, t, u, color=GOLD, w=9, ang=0.0, seed=0):
    """Protein zinciri: u=0 yumak gibi katlanmış, u=1 açılmış uzun iplik."""
    p = skia.Path(); n = 90; L = r * 3.2
    ca, sa = math.cos(ang), math.sin(ang)
    for k in range(n + 1):
        s = k / n; ph = seed * 1.7 + t * 1.2
        fx = r * 0.85 * math.sin(s * 2 * math.pi * 3 + ph) * math.cos(s * 2 * math.pi * 1.3)
        fy = r * 0.85 * math.cos(s * 2 * math.pi * 2.6 + ph * 0.7) * math.sin(s * 2 * math.pi * 1.1 + 0.6)
        ux = (s - 0.5) * L; uy = r * 0.18 * math.sin(s * 2 * math.pi * 4 + ph)
        lx = lerp(fx, ux, u); ly = lerp(fy, uy, u)
        X = x + lx * ca - ly * sa; Y = y + lx * sa + ly * ca
        p.moveTo(X, Y) if k == 0 else p.lineTo(X, Y)
    c.drawPath(p, stroke(color, w))

def water(c):
    rrect(c, 90, 500, 900, 610, 40, "#9fd8ff", 0.13); rrect(c, 90, 500, 900, 610, 40, "#9fd8ff", 0.35, sw=4)

POS = [(270, 640), (560, 600), (820, 680), (380, 900), (700, 930), (230, 1010)]
def i1(c, t, d):
    water(c)
    for k, (x, y) in enumerate(POS):
        a = ss(0.3 + k * 0.25, 0.8 + k * 0.25, t)
        c.saveLayerAlpha(None, int(255 * a)); coil(c, x + 10 * math.sin(t + k), y + 8 * math.cos(t * 1.3 + k), 60, t, 0, seed=k); c.restore()
    tag(c, "su", 140, 560, "#bfe6ff", ss(1.2, 1.7, t), 40, "l", "Bold")
    tag(c, "katlanmış protein", 560, 1075, THEME["accent"], ss(3.0, 3.5, t), 40, "c", "Bold")

def i2(c, t, d):
    water(c)
    u = ss(1.2, 3.6, t)
    for k, (x, y) in enumerate(POS):
        jit = (4 + 10 * u) * math.sin(t * 14 + k * 2)
        coil(c, x + jit, y + 50, 60, t, u, ang=(k - 2.5) * 0.18, seed=k)
    flames(c, 540, 1180, 9, t, ss(0.2, 0.8, t), gap=90)
    tag(c, "ısı", 950, 1080, "#ff9a5c", ss(0.6, 1.1, t), 46, "r", "Bold")
    tag(c, "yumaklar açılır", 540, 565, THEME["accent"], ss(3.3, 3.8, t), 44, "c", "Bold")

_r = np.random.default_rng(5)
STR = [(float(_r.uniform(250, 830)), float(_r.uniform(690, 930)), float(_r.uniform(0, math.pi))) for _ in range(9)]
def i3(c, t, d):
    water(c)
    g = ss(0.8, 3.0, t)
    for k, (x, y, a) in enumerate(STR):
        sx = lerp(540 + (x - 540) * 1.5, x, g); sy = lerp(800 + (y - 800) * 1.4, y, g)
        coil(c, sx, sy, 70, t * 0.3, 1, ang=a, seed=k, w=8)
    k2 = ss(3.0, 3.6, t)
    if k2 > 0:
        for i in range(len(STR)):
            for j in range(i + 1, len(STR)):
                x0, y0, _ = STR[i]; x1, y1, _ = STR[j]
                if math.hypot(x1 - x0, y1 - y0) < 260:
                    circ(c, (x0 + x1) / 2, (y0 + y1) / 2, 11 * eback(k2), "#ffffff", 0.95)
    for k, (x, y) in enumerate([(360, 760), (620, 720), (480, 900), (720, 880), (300, 940)]):
        drop(c, x, y, 20, ss(4.0 + k * 0.2, 4.5 + k * 0.2, t))
    tag(c, "ağ suyu hapseder", 540, 1075, THEME["accent"], ss(4.6, 5.1, t), 42, "c", "Bold")

def i4(c, t, d):
    # sol: çiğ ak (şeffaf)
    rrect(c, 100, 640, 340, 340, 60, "#e8f6ff", 0.18); rrect(c, 100, 640, 340, 340, 60, "#e8f6ff", 0.6, sw=4)
    p = ss(0.6, 1.8, t); arrow(c, 60, 810, lerp(60, 490, p), 810, GOLD, 10, ss(0.5, 0.7, t))
    tag(c, "çiğ: şeffaf", 270, 1110, "#cfeaff", ss(1.6, 2.1, t), 40, "c", "Bold")
    # sağ: pişmiş ak (beyaz)
    k = ss(2.0, 2.6, t)
    for dx, dy, r in ((-60, -60, 110), (60, -50, 100), (55, 60, 110), (-55, 55, 105), (0, 0, 120)):
        circ(c, 800 + dx * 0.85, 810 + dy * 0.85, r * 0.85, WHITE, k)
    q = ss(2.8, 3.4, t); arrow(c, 540, 810, lerp(540, 640, q), 810, GOLD, 10, ss(2.7, 2.9, t))
    if t > 3.4:
        for j in range(10):
            ang = j * math.pi / 5 + 0.3; L = ((t - 3.4) * 70 + j * 13) % 60; a = 1 - L / 60
            line(c, 800 + math.cos(ang) * (170 + L), 810 + math.sin(ang) * (170 + L), 800 + math.cos(ang) * (200 + L), 810 + math.sin(ang) * (200 + L), GOLD, 7, a)
    tag(c, "pişmiş: beyaz", 800, 1110, THEME["accent"], ss(3.8, 4.3, t), 40, "c", "Bold")

SCENES = [
 title_scene("Yumurta pişince", "neden katılaşır?", "Cevap proteinlerde saklı", hero),
 reason_scene("ADIM 1", "Katlanmış proteinler", ["Çiğ ak, suda yüzen proteinlerle dolu;", "her biri yumak gibi katlanmış."], i1),
 reason_scene("ADIM 2", "Isı yumakları açar", ["Isınan proteinler sarsılır ve açılır.", "Buna denatürasyon denir."], i2),
 reason_scene("ADIM 3", "Proteinler ağ örer", ["Açılan proteinler birbirine yapışır;", "ağ suyu hapseder, ak katılaşır."], i3),
 reason_scene("ADIM 4", "Şeffaftan beyaza", ["Topaklar ışığın düz geçmesini engeller;", "bu yüzden ak bembeyaz görünür."], i4),
 cards_scene("ÖZET", "Kaç derecede pişer?", [("Ak: 60–65 °C", "Bu aralıkta katılaşmaya başlar"), ("Sarı biraz daha geç", "Daha yüksek sıcaklık ister"), ("Geri dönüşü yok", "Pişen yumurta çiğe dönmez")]),
 end_scene("Pişen yumurta", "çiğe dönmez.", hero),
]
if __name__ == "__main__":
    nb.main(SLUG, NARRATION, SCENES)
