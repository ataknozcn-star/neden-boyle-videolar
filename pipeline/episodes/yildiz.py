import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import numpy as np, skia
from nb import *
import nb

SLUG = "yildizlar-neden-goz-kirpar"
nb.THEME.update(bg=["#17204a", "#0d1330", "#05081a"], accent="#bfe3ff")
NARRATION = [
 "Yıldızlar neden göz kırpar? Aslında titreyen yıldız değil, havamız.",
 "Yıldızlar çok uzaktadır. Bu yüzden bize, tek bir ışık noktası gibi görünürler.",
 "Yıldız ışığı gözümüze ulaşmadan önce, kilometrelerce kalınlıkta havadan geçer.",
 "Havada sıcak ve soğuk katmanlar sürekli hareket eder. Her katman ışığı biraz farklı büker.",
 "Işığın yolu bir an sağa, bir an sola kayar. Parlaklığı da sürekli değişir. İşte bu, göz kırpmadır.",
 "Ufka yakın yıldızlar daha çok titrer, çünkü ışık daha uzun hava yolu geçer. Gezegenler ise nokta değil, küçük bir disk olduğu için daha az titrer. Uzayda ise yıldızlar hiç titremez.",
 "Yıldız titremiyor; ışığı havada dans ediyor. Neden böyle? Artık biliyorsunuz.",
]
STAR = "#fff6d8"

def star(c, x, y, r, a=1.0, color=STAR):
    if a <= 0.01: return
    p = skia.Path()
    for k in range(8):
        ang = -math.pi / 2 + k * math.pi / 4; rr = r if k % 2 == 0 else r * 0.32
        px, py = x + rr * math.cos(ang), y + rr * math.sin(ang)
        p.moveTo(px, py) if k == 0 else p.lineTo(px, py)
    p.close(); c.drawPath(p, fill(color, a)); circ(c, x, y, r * 0.55, color, 0.18 * a)

_r = np.random.default_rng(7)
SKY = [(float(_r.uniform(70, 1010)), float(_r.uniform(560, 1180)), float(_r.uniform(2.5, 5)), float(_r.uniform(0, 6))) for _ in range(38)]
def sky(c, t, a=1.0, ymin=0, ymax=2000):
    for (x, y, r, ph) in SKY:
        if ymin <= y <= ymax: circ(c, x, y, r, "#ffffff", a * (0.35 + 0.3 * math.sin(t * 3 + ph)))

def twinkle(t, ph=0.0, k=1.0):
    return 1 + k * (0.28 * math.sin(t * 11 + ph) + 0.18 * math.sin(t * 17.3 + ph * 2))

def hero(c, t):
    sky(c, t)
    s = twinkle(t)
    circ(c, 540, 870, 150 * s, STAR, 0.08); circ(c, 540, 870, 95 * s, STAR, 0.12)
    star(c, 540, 870, 120 * s)
    star(c, 300, 700, 38 * twinkle(t, 2.0)); star(c, 800, 1040, 46 * twinkle(t, 4.0))

def i1(c, t, d):
    sky(c, t, 0.5)
    # uzaktaki yıldız: büyük güneş gibi top küçülüp noktaya dönüşür
    p = ss(0.8, 2.6, t); r = lerp(150, 10, eout(p)); x = lerp(540, 880, eout(p)); y = lerp(820, 600, eout(p))
    circ(c, x, y, r * 1.25, GOLD, 0.15); circ(c, x, y, r, GOLD)
    # Dünya
    circ(c, 200, 1060, 70, "#3f7fd0"); circ(c, 185, 1040, 24, GREEN, 0.9); circ(c, 225, 1080, 18, GREEN, 0.9)
    q = ss(2.6, 3.6, t)
    if q > 0: line(c, 880, 600, lerp(880, 260, q), lerp(600, 1010, q), STAR, 4, 0.9)
    tag(c, "çok çok uzak", 860, 560, THEME["accent"], ss(2.4, 2.9, t), 36, "c", "Bold")
    tag(c, "tek ışık noktası", 600, 1020, STAR, ss(3.4, 3.9, t), 36, "c")

def layers(c, t, x0=80, x1=1000, y0=700, y1=1080, n=5, a=1.0):
    h = (y1 - y0) / n
    for k in range(n):
        warm = k % 2 == 0; colr = "#ff9a6b" if warm else "#6fb6ff"
        p = skia.Path(); yy = y0 + k * h
        for j in range(0, int(x1 - x0) + 1, 10):
            x = x0 + j; off = 10 * math.sin(j / 120 + t * (1.5 + k * 0.4) + k)
            p.moveTo(x, yy + off) if j == 0 else p.lineTo(x, yy + off)
        for j in range(int(x1 - x0), -1, -10):
            x = x0 + j; off = 10 * math.sin(j / 120 + t * (1.5 + k * 0.4) + k + 1.3)
            p.lineTo(x, yy + h + off)
        p.close(); c.drawPath(p, fill(colr, 0.16 * a))

def person(c, x, y, a=1.0):
    circ(c, x, y, 30, "#ffd7b0", a); rrect(c, x - 30, y + 34, 60, 74, 24, GOLD, a)

def i2(c, t, d):
    star(c, 540, 540, 34 * twinkle(t, 0, 0.3))
    k = ss(0.6, 1.4, t); layers(c, t, 100, 980, 640, 1040, 4, k)
    tag(c, "atmosfer", 960, 700, THEME["accent"], ss(1.2, 1.7, t), 34, "r", "Bold")
    rrect(c, 80, 1080, 920, 40, 16, "#2e7d4f")
    person(c, 540, 1000)
    q = ss(1.6, 3.4, t)
    if q > 0: line(c, 540, 580, 540, lerp(580, 960, q), STAR, 6)
    tag(c, "kilometrelerce hava", 540, 1170, STAR, ss(3.2, 3.7, t), 36, "c")

def i3(c, t, d):
    star(c, 540, 520, 32)
    layers(c, t, 100, 980, 620, 1060, 5)
    tag(c, "sıcak", 130, 665, "#ffb38f", ss(0.8, 1.3, t), 32, "l", "Bold")
    tag(c, "soğuk", 130, 753, "#9cc6ff", ss(1.4, 1.9, t), 32, "l", "Bold")
    # büküle büküle inen ışık
    q = ss(2.0, 3.8, t); n = 5; h = 440 / n
    pts = [(540, 560)]; x = 540
    for k in range(n):
        dx = (26 if k % 2 == 0 else -18) * math.sin(t * 2.2 + k * 1.7) + (14 if k % 2 == 0 else -14)
        x += dx; pts.append((x, 620 + (k + 1) * h))
    seg = q * n
    for k in range(n + 1 if q >= 1 else int(seg) + 1):
        if k >= len(pts) - 1: break
        f = 1 if k < int(seg) or q >= 1 else seg - int(seg)
        (ax, ay), (bx, by) = pts[k], pts[k + 1]
        line(c, ax, ay, lerp(ax, bx, f), lerp(ay, by, f), STAR, 6)
    tag(c, "her katman farklı büker", 540, 1140, THEME["accent"], ss(3.4, 3.9, t), 36, "c", "Bold")

def i4(c, t, d):
    layers(c, t, 100, 980, 600, 900, 3, 0.8)
    rrect(c, 80, 1100, 920, 36, 16, "#2e7d4f")
    # göz
    eye(c, 540, 1010, 190, 90, look=(0, -0.6))
    # kayan ışın
    sx = 540 + 70 * math.sin(t * 6) + 40 * math.sin(t * 13)
    star(c, 540 + 22 * math.sin(t * 6), 520, 38 * twinkle(t, 0, 1.0))
    line(c, 540, 560, sx, 900, STAR, 5, 0.9); line(c, sx, 900, 540, 960, STAR, 5, 0.9 * (0.5 + 0.5 * math.sin(t * 9)))
    # parlaklık göstergesi
    bars = [0.5 + 0.5 * math.sin(t * 9 - j * 0.9) for j in range(6)]
    for j, b in enumerate(bars):
        h = 30 + 90 * b; rrect(c, 820 + j * 26, 790 - h, 18, h, 6, THEME["accent"], 0.75 * ss(2.5, 3.0, t))
    tag(c, "parlaklık", 885, 830, THEME["accent"], ss(2.5, 3.0, t), 30, "c")
    tag(c, "sağa, sola, söner, parlar", 540, 1180, STAR, ss(3.6, 4.1, t), 34, "c")

SCENES = [
 title_scene("Yıldızlar neden", "göz kırpar?", "Titreyen yıldız değil, hava", hero),
 reason_scene("NEDEN 1", "Uzak bir ışık noktası", ["Yıldızlar çok uzaktadır;", "bize tek bir nokta gibi görünür."], i1),
 reason_scene("NEDEN 2", "Işık havadan geçer", ["Gözümüze ulaşmadan önce", "kilometrelerce hava aşar."], i2),
 reason_scene("NEDEN 3", "Katmanlar ışığı büker", ["Sıcak ve soğuk hava katmanları", "ışığı her an farklı büker."], i3),
 reason_scene("NEDEN 4", "Işık kayar, titreşir", ["Işığın yolu ve parlaklığı", "sürekli değişir: göz kırpma!"], i4),
 cards_scene("BONUS", "Kim çok, kim az titrer?", [("Ufka yakın yıldız", "Daha uzun hava yolu: çok titrer"), ("Gezegenler", "Küçük disk: daha az titrer"), ("Uzaydan bakınca", "Hava yok: hiç titremez")]),
 end_scene("Yıldız titremiyor;", "ışığı havada dans ediyor.", hero),
]
if __name__ == "__main__":
    nb.main(SLUG, NARRATION, SCENES)
