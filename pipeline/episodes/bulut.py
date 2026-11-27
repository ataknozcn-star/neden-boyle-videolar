import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import numpy as np, skia
from nb import *
import nb

SLUG = "bulutlar-neden-dusmez"
nb.THEME.update(bg=["#3f86bf", "#25598a", "#11304f"], accent="#bfe9ff")
NARRATION = [
 "Bulutlar neden düşmez? Tonlarca su gökyüzünde nasıl durur?",
 "Bulut, havada asılı milyarlarca minicik su damlacığından oluşur. Her biri, bir saç telinden çok daha incedir.",
 "Damlacık o kadar küçüktür ki, hava direnci onu frenler. Saatte yalnızca birkaç on metre düşer.",
 "Bulutun altında sıcak hava yükselir. Bu yukarı akım, yavaşça düşen damlacıkları havada tutar.",
 "Bulut ağırdır ama suyu çok geniş bir hacme yayılmıştır. Küçük bir bulutta bir milyon kilo kadar su olabilir; aynı hacimdeki hava ise bin kat daha ağırdır.",
 "Peki yağmur ne zaman yağar? Damlacıklar çarpışıp birleşir ve büyür. Büyüyen damla daha hızlı düşer; yukarı akım onu taşıyamaz ve yağmur başlar.",
 "Bulutlar aslında uçmuyor; çok yavaş düşüyor. Neden böyle? Artık biliyorsunuz.",
]
_r = np.random.default_rng(5)
SPARK = [(float(_r.uniform(-150, 150)), float(_r.uniform(-60, 40)), float(_r.uniform(0, 6.28))) for _ in range(22)]
def hero(c, t):
    bob = 10 * math.sin(t * 1.3)
    for k in range(4):
        x = 360 + k * 120; u = (t * 0.5 + k * 0.27) % 1
        arrow(c, x, 1150 - 120 * u, x, 1090 - 120 * u, "#ffd59a", 8, math.sin(u * math.pi) * 0.8, 20)
    cloud(c, 540, 860 + bob, 1.9, 0.97)
    for (dx, dy, ph) in SPARK:
        circ(c, 540 + dx * 1.3, 860 + bob + dy * 1.3, 5, "#6ec6f0", 0.5 + 0.5 * math.sin(t * 3 + ph))
def i1(c, t, d):
    cloud(c, 230, 600, 0.9, 0.95)
    k = ss(0.6, 1.4, t)
    line(c, 300, 640, lerp(300, 560, k), lerp(640, 760, k), "#ffffff", 6, 0.8 * k)
    if k > 0:
        circ(c, 700, 830, 240 * eout(k), "#ffffff", 0.12); circ(c, 700, 830, 240 * eout(k), "#ffffff", 0.9, sw=8)
        rr = np.random.default_rng(9)
        for _ in range(40):
            a = rr.uniform(0, 6.28); r = 210 * math.sqrt(rr.uniform(0, 1))
            x = 700 + r * math.cos(a) * eout(k); y = 830 + r * math.sin(a) * eout(k) + 4 * math.sin(t * 2 + a)
            circ(c, x, y, 9, "#6ec6f0", ss(1.2, 1.8, t))
    tag(c, "milyarlarca damlacık", 700, 1120, THEME["accent"], ss(1.8, 2.3, t), 40, "c", "Bold")
    q = ss(3.8, 4.4, t)
    rrect(c, 120, 900, 40, 220, 20, "#c99a6a", q); tag(c, "saç teli", 140, 1170, None, q, 32, "c")
    circ(c, 280, 1010, 5, "#6ec6f0", q); tag(c, "damlacık", 280, 1060, None, q, 30, "c")
def i2(c, t, d):
    y = 740 + 20 * ss(0, d, t)
    circ(c, 540, y, 70, "#6ec6f0"); circ(c, 515, y - 22, 18, "#ffffff", 0.6)
    a = ss(1.0, 1.6, t)
    for dx in (-110, 0, 110):
        u = (t * 0.8 + dx * 0.002) % 1
        arrow(c, 540 + dx, y + 240 - 60 * u, 540 + dx, y + 150 - 60 * u, "#ffffff", 9, a * 0.85, 24)
    tag(c, "hava direnci", 540, y + 275, "#ffffff", a, 38, "c", "Bold")
    b = ss(0.6, 1.0, t); arrow(c, 540, y - 200, 540, y - 110, GOLD, 9, b, 24)
    tag(c, "ağırlık: çok az", 540, y - 225, GOLD, b, 36, "c", "Bold")
    tag(c, "saatte birkaç on metre", 540, 1170, THEME["accent"], ss(3.2, 3.7, t), 40, "c", "Bold")
def i3(c, t, d):
    rrect(c, 60, 1105, 960, 60, 20, "#2e7d4f")
    sun(c, 900, 1010, 40, t, 0.9)
    a = ss(0.6, 1.2, t)
    for k in range(4):
        x = 200 + k * 180
        for j in range(2):
            u = (t * 0.45 + k * 0.19 + j * 0.5) % 1; yy = 1090 - 170 * u
            p = skia.Path()
            for s_ in range(0, 101, 5):
                py = yy - s_; px = x + 14 * math.sin(s_ / 18 + t * 2)
                p.moveTo(px, py) if s_ == 0 else p.lineTo(px, py)
            c.drawPath(p, stroke("#ffb36b", 8, a * math.sin(u * math.pi)))
    tag(c, "sıcak hava yükselir", 540, 1147, "#ffffff", ss(1.0, 1.5, t), 34, "c", "Bold")
    cloud(c, 540, 600, 1.6, 0.95)
    for k in range(7):
        x = 330 + k * 70; y = 700 + 10 * math.sin(t * 2.2 + k)
        circ(c, x, y, 9, "#6ec6f0", ss(2.4, 2.9, t))
    tag(c, "damlacıklar havada kalır", 540, 790, THEME["accent"], ss(3.0, 3.5, t), 36, "c", "Bold")
def i4(c, t, d):
    k = ss(0.5, 1.3, t)
    c.save(); c.translate(0, 0)
    poly(c, [(380, 560), (700, 560), (800, 500), (480, 500)], "#ffffff", 0.25 * k)
    poly(c, [(700, 560), (800, 500), (800, 780), (700, 840)], "#ffffff", 0.15 * k)
    rrect(c, 380, 560, 320, 280, 4, "#ffffff", 0.10 * k)
    rrect(c, 380, 560, 320, 280, 4, "#ffffff", 0.8 * k, sw=5)
    rr = np.random.default_rng(3)
    for _ in range(26): circ(c, rr.uniform(400, 680), rr.uniform(580, 820), 6, "#6ec6f0", k)
    c.restore()
    tag(c, "1 km³ bulut", 540, 470, "#ffffff", k, 38, "c", "Bold")
    p = ss(3.6, 4.4, t)
    tag(c, "su: ~1 milyon kg", 100, 940, "#9fdcff", ss(3.4, 3.8, t), 36, "l", "Bold")
    rrect(c, 100, 960, max(6, 6 * p), 44, 3, "#6ec6f0", ss(3.4, 3.8, t))
    q = ss(6.2, 7.4, t)
    tag(c, "hava: ~1 milyar kg", 100, 1060, "#ffffff", ss(6.0, 6.4, t), 36, "l", "Bold")
    rrect(c, 100, 1080, 880 * q, 44, 12, "#ffffff", 0.85 * ss(6.0, 6.4, t))
    tag(c, "hava bin kat ağır!", 540, 1175, GOLD, ss(7.6, 8.1, t), 40, "c", "Bold")
SCENES = [
 title_scene("Bulutlar", "neden düşmez?", "Tonlarca su gökyüzünde", hero),
 reason_scene("NEDEN 1", "Minicik damlacıklar", ["Bulut, milyarlarca minicik", "su damlacığından oluşur."], i1),
 reason_scene("NEDEN 2", "Hava direnci frenler", ["Damlacık çok küçük olduğu için", "saatte yalnızca birkaç on metre düşer."], i2),
 reason_scene("NEDEN 3", "Yükselen sıcak hava", ["Yukarı akım, yavaşça düşen", "damlacıkları havada tutar."], i3),
 reason_scene("NEDEN 4", "Su geniş alana yayılır", ["Buluttaki su, kendisinden bin kat", "ağır havanın içine dağılmıştır."], i4),
 cards_scene("BONUS", "Yağmur ne zaman yağar?", [("Damlacıklar birleşir", "Çarpışıp büyürler"), ("Büyük damla hızlı düşer", "Hava artık frenleyemez"), ("Yağmur başlar", "Yukarı akım taşıyamaz")]),
 end_scene("Bulutlar uçmuyor;", "çok yavaş düşüyor.", hero),
]
if __name__ == "__main__":
    nb.main(SLUG, NARRATION, SCENES)
