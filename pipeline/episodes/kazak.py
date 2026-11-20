import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import numpy as np, skia
from nb import *
import nb

SLUG = "kazak-neden-citirdar"
nb.THEME.update(bg=["#2b2d6e", "#1a1b4a", "#0d0e2a"], accent="#ffd84a")
ZAP = "#ffe866"
WOOL = "#e05a6a"
NEG = "#6ec6f0"
POS = "#ff8a5c"
NARRATION = [
 "Kazağı çıkarınca neden çıtırdar? Cevap: statik elektrik.",
 "Kazak çıkarken saçımıza ve tişörtümüze sürtünür. Bu sırada eksi yüklü minik elektronlar, bir yüzeyden ötekine geçer.",
 "Elektron kazanan taraf eksi, elektron kaybeden taraf artı yüklü olur. Bu yük, yüzeylerde birikir.",
 "Nemli havada su, yükün yavaşça kaçmasını sağlar. Kışın ise hava kurudur; yük kaçamaz ve birikmeye devam eder.",
 "Yük yeterince artınca elektronlar havadan sıçrar. Bu minik kıvılcımlar havayı ısıtır; duyduğumuz çıtırtı budur.",
 "Peki saçlar neden havaya kalkar? Saç tellerinin hepsi aynı yükü alır. Aynı yükler birbirini iter, teller birbirinden uzaklaşır.",
 "Kazaktaki çıtırtı, minik kıvılcımların sesidir. Neden böyle? Artık biliyorsunuz.",
]

def sweater(c, x, y, s=1.0, color=WOOL, a=1.0):
    # gövde + kollar + yaka + örgü çizgileri
    body = [(x - 150 * s, y - 150 * s), (x + 150 * s, y - 150 * s), (x + 150 * s, y + 170 * s), (x - 150 * s, y + 170 * s)]
    poly(c, [(x - 150 * s, y - 150 * s), (x - 260 * s, y + 120 * s), (x - 200 * s, y + 145 * s), (x - 140 * s, y)], color, a)
    poly(c, [(x + 150 * s, y - 150 * s), (x + 260 * s, y + 120 * s), (x + 200 * s, y + 145 * s), (x + 140 * s, y)], color, a)
    poly(c, body, color, a)
    rrect(c, x - 150 * s, y + 140 * s, 300 * s, 34 * s, 10 * s, mixcol(color, "#000000", 0.25), a)
    p = skia.Path(); p.moveTo(x - 60 * s, y - 150 * s); p.quadTo(x, y - 90 * s, x + 60 * s, y - 150 * s); p.close()
    c.drawPath(p, fill(mixcol(color, "#000000", 0.3), a))
    for k in range(4):
        yy = y - 70 * s + k * 52 * s
        for j in range(5):
            xx = x - 100 * s + j * 50 * s
            line(c, xx - 14 * s, yy, xx, yy + 14 * s, "#ffffff", 4 * s, 0.25 * a); line(c, xx, yy + 14 * s, xx + 14 * s, yy, "#ffffff", 4 * s, 0.25 * a)

def spark(c, x, y, L, ang, t, seed=0, a=1.0, w=7):
    if a <= 0.01: return
    rng = np.random.default_rng(seed + int(t * 14))
    p = skia.Path(); p.moveTo(x, y); n = 5
    for k in range(1, n + 1):
        f = k / n; jx = 0 if k == n else float(rng.uniform(-1, 1)) * L * 0.18
        px = x + math.cos(ang) * L * f - math.sin(ang) * jx; py = y + math.sin(ang) * L * f + math.cos(ang) * jx
        p.lineTo(px, py)
    c.drawPath(p, stroke(ZAP, w * 2.6, 0.25 * a)); c.drawPath(p, stroke(ZAP, w, a)); c.drawPath(p, stroke("#ffffff", w * 0.4, a))

def charge(c, x, y, sign, a=1.0, r=26):
    if a <= 0.01: return
    col_ = NEG if sign < 0 else POS
    circ(c, x, y, r, col_, a); line(c, x - r * 0.5, y, x + r * 0.5, y, "#10123a", r * 0.22, a)
    if sign > 0: line(c, x, y - r * 0.5, x, y + r * 0.5, "#10123a", r * 0.22, a)

def head(c, x, y, s=1.0, hair=0.0, t=0.0, a=1.0):
    # hair: 0 düz, 1 tamamen kabarık
    for k in range(13):
        ang0 = math.radians(-160 + k * 11.7)
        up = math.radians(-90 + (k - 6) * 13)
        ang = lerp(ang0 if abs(ang0 + math.pi / 2) < 1.2 else ang0, up, hair) if hair else ang0
        L = (70 + 8 * math.sin(k * 2.1)) * s * (1 + 0.9 * hair) + 4 * hair * math.sin(t * 6 + k)
        sx = x + math.cos(ang0) * 78 * s; sy = y + math.sin(ang0) * 78 * s
        if hair:
            ex = sx + math.cos(ang) * L * 0.9; ey = sy + math.sin(ang) * L * 0.9
        else:
            ex = sx + math.cos(ang0 + 1.3 * (1 if k < 6 else -1)) * 20 * s; ey = sy + 30 * s
        line(c, sx, sy, ex, ey, "#5a3a22", 9 * s, a)
    circ(c, x, y, 82 * s, "#5a3a22", a)
    circ(c, x, y + 14 * s, 74 * s, "#ffd7b0", a)
    circ(c, x - 26 * s, y + 10 * s, 7 * s, "#2b2d6e", a); circ(c, x + 26 * s, y + 10 * s, 7 * s, "#2b2d6e", a)
    p = skia.Path(); p.moveTo(x - 20 * s, y + 44 * s); p.quadTo(x, y + 58 * s, x + 20 * s, y + 44 * s)
    c.drawPath(p, stroke("#a8505a", 5 * s, a))

def hero(c, t):
    sweater(c, 540, 930, 1.15)
    for k, (x, y, ang) in enumerate([(330, 700, -2.4), (760, 690, -0.7), (250, 1010, 3.0), (830, 1020, 0.1), (540, 640, -1.57)]):
        on = (math.sin(t * 5 + k * 1.9) > 0.1)
        spark(c, x, y, 110, ang, t, k * 7, 1.0 if on else 0.55)

def i1(c, t, d):
    head(c, 540, 620, 1.0)
    # kazak başın üstünden yukarı çıkıyor
    yk = 890 + 30 * math.sin(t * 3)
    sweater(c, 540, yk, 0.95)
    tag(c, "sürtünme", 540, 515, ZAP, ss(0.8, 1.3, t), 40, "c", "Bold")
    # elektronlar saçtan kazağa geçer
    for k in range(6):
        u = ((t - 2.0) * 0.55 + k / 6) % 1 if t > 2.0 else -1
        if u < 0: continue
        x0 = 420 + k * 48; y0 = 690; y1 = yk - 40
        charge(c, x0, lerp(y0, y1, eout(u)), -1, ss(0, 0.15, u) * (1 - ss(0.85, 1, u)), 20)
    tag(c, "elektronlar geçer", 540, 1170, NEG, ss(2.6, 3.1, t), 38, "c", "Bold")

def i2(c, t, d):
    # sol: kazak (eksi), sağ: saç/tişört (artı)
    sweater(c, 300, 840, 0.62)
    rrect(c, 640, 680, 300, 330, 40, "#f6e7c8", 0.9)
    tag(c, "kazak", 300, 1110, THEME["text"], ss(0.6, 1.0, t), 38, "c", "Bold")
    tag(c, "tişört / saç", 790, 1110, THEME["text"], ss(0.6, 1.0, t), 38, "c", "Bold")
    for k in range(8):
        cx = 300 + ((k % 4) - 1.5) * 64; cy = 790 + (k // 4) * 80
        charge(c, cx, cy, -1, pop(t, 1.4 + k * 0.12), 22)
        px = 790 + ((k % 4) - 1.5) * 64; py = 790 + (k // 4) * 80
        charge(c, px, py, 1, pop(t, 2.9 + k * 0.12), 22)
    tag(c, "eksi yük", 300, 620, NEG, ss(2.0, 2.5, t), 40, "c", "Bold")
    tag(c, "artı yük", 790, 620, POS, ss(3.4, 3.9, t), 40, "c", "Bold")

def i3(c, t, d):
    # sol: nemli hava (damlalar yükü taşır), sağ: kuru hava (yük kalır)
    line(c, 540, 560, 540, 1120, THEME["text"], 3, 0.3)
    tag(c, "nemli", 300, 600, NEG, ss(0.6, 1.0, t), 44, "c", "Bold")
    tag(c, "kuru", 780, 600, ZAP, ss(3.0, 3.5, t), 44, "c", "Bold")
    sweater(c, 300, 930, 0.5); sweater(c, 780, 930, 0.5)
    for k in range(6):
        u = (t * 0.5 + k / 6) % 1
        ang = k * math.pi / 3 + 0.4; r = 80 + 120 * u
        dx = 300 + math.cos(ang) * r; dy = 900 + math.sin(ang) * r * 0.8
        drop(c, dx, dy, 18, 0.8 * (1 - u))
        charge(c, dx, dy + 34, -1, 0.9 * (1 - u) * ss(1.0, 1.5, t), 13)
    nk = int(clamp((t - 3.4) / 0.35, 0, 9))
    for k in range(nk):
        charge(c, 780 + ((k % 3) - 1) * 52, 870 + (k // 3) * 52, -1, 1, 20)
    tag(c, "yük kaçar", 300, 1160, THEME["text"], ss(2.0, 2.5, t), 36, "c")
    tag(c, "yük birikir", 780, 1160, THEME["text"], ss(4.2, 4.7, t), 36, "c")

def i4(c, t, d):
    head(c, 540, 1000, 0.9)
    yk = lerp(860, 700, ss(0.3, 1.6, t))
    sweater(c, 540, yk, 0.8)
    for k in range(5):
        charge(c, 450 + k * 45, yk + 60, -1, 0.9, 16)
    if t > 2.0:
        for k, (x, ang) in enumerate([(430, 1.9), (540, 1.57), (650, 1.2)]):
            on = math.sin(t * 7 + k * 2.3) > -0.2
            spark(c, x, yk + 150, 130, ang, t, 40 + k, 1.0 if on else 0.2, 6)
    tag(c, "kıvılcım", 230, 760, ZAP, ss(2.2, 2.7, t), 42, "c", "Bold")
    if t > 4.0:
        for k in range(3):
            r = ((t - 4.0) * 120 + k * 60) % 180
            p = skia.Path(); p.addArc(skia.Rect.MakeXYWH(850 - r, 860 - r, 2 * r, 2 * r), -50, 100)
            c.drawPath(p, stroke(THEME["text"], 6, 0.7 * (1 - r / 180)))
        tag(c, "çıt çıt!", 850, 1070, THEME["text"], ss(4.0, 4.5, t), 42, "c", "Bold")

def s5(c, t, d):
    header(c, "BONUS", "Saçlar neden kabarır?", t)
    hair = ss(1.5, 4.0, t)
    c.saveLayerAlpha(None, int(255 * ss(0.2, 0.7, t)))
    head(c, 540, 900, 1.6, hair, t)
    for k in range(5):
        ang = math.radians(-160 + k * 35); r = 250 + 30 * hair
        charge(c, 540 + math.cos(ang) * r, 900 + math.sin(ang) * r, 1, ss(2.4 + k * 0.15, 2.8 + k * 0.15, t), 22)
    c.restore()
    caption(c, ["Teller aynı yükü alır;", "aynı yükler birbirini iter."], t, 0.9, 1262)

SCENES = [
 title_scene("Kazak neden", "çıtırdar?", "Statik elektriğin sırrı", hero),
 reason_scene("NEDEN 1", "Sürtünme elektron taşır", ["Kazak saça ve tişörte sürtünür;", "elektronlar bir yüzeyden ötekine geçer."], i1),
 reason_scene("NEDEN 2", "Bir taraf eksi, biri artı", ["Elektron kazanan eksi, kaybeden", "artı yüklü olur; yük birikir."], i2),
 reason_scene("NEDEN 3", "Kuru hava yükü tutar", ["Nemli havada yük su ile kaçar;", "kışın hava kuru, yük birikir."], i3),
 reason_scene("NEDEN 4", "Kıvılcım ve çıtırtı", ["Elektronlar havadan sıçrar;", "minik kıvılcımlar çıtırdar."], i4),
 s5,
 end_scene("Kazaktaki çıtırtı,", "minik kıvılcımların sesi.", hero),
]
if __name__ == "__main__":
    nb.main(SLUG, NARRATION, SCENES)
