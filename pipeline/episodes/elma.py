import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import numpy as np, skia
from nb import *
import nb

SLUG = "elma-neden-kararir"
nb.THEME.update(bg=["#2f6b3a", "#1c4526", "#0e2615"], accent="#ffd166")
NARRATION = [
 "Kesilen elma neden kararır? İşte dakikalar içinde olan kimya.",
 "Elmayı kesince dokusu zedelenir ve havadaki oksijen içeri girer.",
 "Oksijen, elmadaki bir enzimi harekete geçirir. Adı polifenol oksidaz.",
 "Bu enzim, elmanın içindeki fenolik maddeleri oksijenle tepkimeye sokar.",
 "Ortaya çıkan yeni maddeler birleşir ve kahverengi pigmentlere dönüşür.",
 "Kararmayı yavaşlatan üç şey var. Limon suyu; asidi enzimi yavaşlatır. Buzdolabı; soğukta tepkime ağırlaşır. Bal ya da şerbet; yüzeyi kaplar, oksijeni azaltır.",
 "Elmayı karartan şey oksijen ve bir enzim. Neden böyle? Artık biliyorsunuz.",
]
SKIN, FLESH, BROWN, O2C, PHEN, QUIN = "#d8343a", "#fff3d1", "#9a6a3a", "#8fd3ff", "#8fe08a", "#ff9a3c"

def _apple_path():
    p = skia.Path(); p.moveTo(0, -0.72); p.cubicTo(0.45, -1.05, 1.1, -0.75, 1.05, -0.05); p.cubicTo(1.0, 0.75, 0.45, 1.1, 0, 0.92)
    p.cubicTo(-0.45, 1.1, -1.0, 0.75, -1.05, -0.05); p.cubicTo(-1.1, -0.75, -0.45, -1.05, 0, -0.72); p.close(); return p
AP = _apple_path()
def apple(c, x, y, s, brown=0.0, cut=True, a=1.0):
    """Elma: cut=True ise kesik yüzü (çekirdekli), brown 0..1 kararma."""
    c.save(); c.translate(x, y); c.scale(s, s)
    c.drawLine(0, -0.72, 0.09, -1.08, stroke("#6b4423", 0.07, a))
    lp = skia.Path(); lp.moveTo(0.09, -0.98); lp.quadTo(0.32, -1.3, 0.6, -1.08); lp.quadTo(0.32, -0.9, 0.09, -0.98); c.drawPath(lp, fill("#6fd08c", a))
    c.drawPath(AP, fill(SKIN, a))
    if cut:
        c.save(); c.scale(0.9, 0.9); c.translate(0, 0.01); c.drawPath(AP, fill(mixcol(FLESH, BROWN, brown), a)); c.restore()
        c.drawOval(skia.Rect.MakeLTRB(-0.27, -0.33, 0.27, 0.42), fill(mixcol("#f3e2ae", "#7d522a", brown), a))
        for sx in (-1, 1):
            sp = skia.Path(); sp.moveTo(sx * 0.11, -0.12); sp.quadTo(sx * 0.24, 0.08, sx * 0.11, 0.2); sp.quadTo(sx * 0.02, 0.06, sx * 0.11, -0.12)
            c.drawPath(sp, fill("#4b2a0f", a))
    else:
        c.drawOval(skia.Rect.MakeLTRB(-0.72, -0.55, -0.42, 0.05), fill("#ffffff", 0.28 * a))
    c.restore()
def o2(c, x, y, r=17, a=1.0):
    circ(c, x - r * 0.8, y, r, O2C, a); circ(c, x + r * 0.8, y, r, O2C, a)
    circ(c, x - r * 1.1, y - r * 0.3, r * 0.3, "#ffffff", 0.7 * a)
def enzyme(c, x, y, r, mouth, color=GOLD, a=1.0, ang=0.0):
    """Enzim: ağzı açılıp kapanan yuvarlak (mouth: derece)."""
    if a <= 0.01: return
    p = skia.Path(); p.moveTo(x, y); p.arcTo(skia.Rect.MakeLTRB(x - r, y - r, x + r, y + r), ang + mouth / 2, 360 - mouth, False); p.close()
    c.drawPath(p, fill(color, a))
    ex = x + r * 0.2 * math.cos(math.radians(ang - 70)); ey = y + r * 0.55 * math.sin(math.radians(ang - 70))
    circ(c, ex, ey, r * 0.13, "#2b1739", a)

def hero(c, t):
    b = 0.75 * ss(1.4, 4.2, t)
    apple(c, 540, 900, 250, b)
    for k in range(5):
        ang = math.radians(200 + k * 35); u = 0.5 + 0.5 * math.sin(t * 1.6 + k)
        o2(c, 540 + (330 + 22 * u) * math.cos(ang), 880 + (310 + 22 * u) * math.sin(ang), 15, 0.9)

def i1(c, t, d):
    k = ss(1.1, 1.9, t)                                  # elma ikiye ayrılır
    if k < 0.02:
        apple(c, 540, 830, 230, cut=False)
    else:
        apple(c, 540 - 225 * k, 830, 200, cut=False); apple(c, 540 + 225 * k, 830, 200, 0.0)
    kn = ss(0.5, 1.1, t) * (1 - ss(1.5, 2.0, t))         # bıçak
    if kn > 0.01:
        y = lerp(430, 640, ss(0.5, 1.1, t))
        poly(c, [(528, y - 150), (552, y - 150), (552, y + 150), (540, y + 190), (528, y + 150)], "#dfe6ee", kn)
        rrect(c, 522, y - 250, 36, 104, 12, "#6b4423", kn)
    for j in range(6):                                   # oksijen kesik yüze gelir
        if t < 2.3: break
        u = ((t - 2.3) * 0.42 + j * 0.167) % 1; ang = math.radians(-80 + j * 32)
        x = 755 + (1 - u) * 270 * math.cos(ang); y = 830 + (1 - u) * 300 * math.sin(ang)
        o2(c, min(x, 985), y, 15, ss(0, 0.15, u) * (1 - ss(0.8, 1, u)))
    tag(c, "kesik yüz", 755, 1110, "#ffffff", ss(1.9, 2.4, t), 34, "c")
    tag(c, "oksijen", 870, 520, O2C, ss(2.6, 3.1, t), 40, "c", "Bold")

_r = np.random.default_rng(7)
CELLS = [(float(_r.uniform(150, 930)), float(_r.uniform(600, 1070))) for _ in range(26)]
def panel(c, brown=0.0):
    rrect(c, 100, 540, 880, 580, 46, mixcol(FLESH, BROWN, brown), 0.95); rrect(c, 100, 540, 880, 580, 46, SKIN, 1, sw=10)
    for (x, y) in CELLS: circ(c, x, y, 26, mixcol("#f1dfa6", "#7d522a", brown), 0.55, sw=4)
def i2(c, t, d):
    panel(c)
    tag(c, "elmanın içi", 540, 512, "#ffffff", ss(0.4, 0.9, t), 32, "c")
    u = ss(0.7, 2.2, t); o2(c, lerp(960, 690, u), lerp(600, 800, u), 20)
    wake = ss(2.0, 2.6, t); m = 8 + wake * (32 + 22 * math.sin(t * 7))
    enzyme(c, 500, 830, 105, m, mixcol("#b9a26a", GOLD, wake))
    if wake > 0.05:
        for k in range(8):
            ang = k * math.pi / 4 + t; L = 132 + 14 * math.sin(t * 6 + k)
            line(c, 500 + math.cos(ang) * L, 830 + math.sin(ang) * L, 500 + math.cos(ang) * (L + 26), 830 + math.sin(ang) * (L + 26), GOLD, 7, wake)
    tag(c, "enzim", 240, 845, "#5a3a12", ss(1.4, 1.9, t), 44, "c", "Bold")
    node(c, 540, 1085, "polifenol oksidaz", ss(4.2, 4.7, t), GOLD)

def i3(c, t, d):
    panel(c)
    cyc = 2.4
    for j in range(3):                                   # fenolik + oksijen girer, kinon çıkar
        tt = t - 1.0 - j * 0.8
        if tt < 0: continue
        u = (tt % cyc) / cyc
        if u < 0.5:
            v = ss(0, 0.5, u); a = 1 - ss(0.42, 0.5, u)
            circ(c, lerp(180, 430, v), lerp(660 + j * 30, 815, v), 26, PHEN, a)
            o2(c, lerp(200, 430, v), lerp(1010 - j * 30, 850, v), 15, a)
        else:
            v = ss(0.5, 1, u)
            poly(c, [(lerp(610, 890, v), lerp(830, 700 + j * 110, v) - 30), (lerp(610, 890, v) + 30, lerp(830, 700 + j * 110, v)),
                     (lerp(610, 890, v), lerp(830, 700 + j * 110, v) + 30), (lerp(610, 890, v) - 30, lerp(830, 700 + j * 110, v))], QUIN, ss(0.5, 0.58, u))
    enzyme(c, 520, 830, 100, 30 + 24 * math.sin(t * 8), GOLD, 1, 180)
    tag(c, "fenolik madde", 250, 600, "#2d6b2a", ss(1.0, 1.5, t), 32, "c", "Bold")
    tag(c, "oksijen", 230, 1085, "#2a6c96", ss(1.4, 1.9, t), 32, "c", "Bold")
    tag(c, "yeni madde", 820, 600, "#b85a10", ss(2.4, 2.9, t), 32, "c", "Bold")

QP = [(float(_r.uniform(170, 910)), float(_r.uniform(520, 760))) for _ in range(14)]
def i4(c, t, d):
    g = ss(1.0, 3.2, t)                                  # parçacıklar birleşip kahverengileşir
    for k, (x, y) in enumerate(QP):
        tx = 540 + ((k % 5) - 2) * 46; ty = 640 + ((k // 5) - 1) * 46
        xx = lerp(x, tx, g) + 5 * math.sin(t * 2 + k); yy = lerp(y, ty, g) + 5 * math.cos(t * 2.3 + k)
        cl = mixcol(QUIN, "#7a4a22", ss(0.5, 1, g))
        poly(c, [(xx, yy - 28), (xx + 28, yy), (xx, yy + 28), (xx - 28, yy)], cl)
    tag(c, "kahverengi pigment", 540, 790, THEME["accent"], ss(3.0, 3.5, t), 40, "c", "Bold")
    arrow(c, 540, 815, 540, 868, THEME["accent"], 8, ss(3.3, 3.8, t), 20)
    apple(c, 540, 1010, 128, 0.85 * ss(2.4, 4.6, t))

SCENES = [
 title_scene("Kesilen elma", "neden kararır?", "Dakikalar içinde olan kimya", hero),
 reason_scene("ADIM 1", "Oksijen içeri girer", ["Kesilen elmanın dokusu zedelenir;", "havadaki oksijen içeri girer."], i1),
 reason_scene("ADIM 2", "Enzim harekete geçer", ["Oksijen, elmadaki bir enzimi", "harekete geçirir."], i2),
 reason_scene("ADIM 3", "Tepkime başlar", ["Enzim, fenolik maddeleri", "oksijenle tepkimeye sokar."], i3),
 reason_scene("ADIM 4", "Kahverengi pigment", ["Yeni maddeler birleşir,", "kahverengi pigmentlere dönüşür."], i4),
 cards_scene("İPUCU", "Kararmayı ne yavaşlatır?", [("Limon suyu", "Asidi enzimi yavaşlatır"), ("Buzdolabı", "Soğukta tepkime ağırlaşır"), ("Bal ya da şerbet", "Yüzeyi kaplar, oksijeni azaltır")]),
 end_scene("Elmayı karartan:", "oksijen ve bir enzim", hero),
]
if __name__ == "__main__":
    nb.main(SLUG, NARRATION, SCENES)
