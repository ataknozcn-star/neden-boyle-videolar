import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import numpy as np, skia
from nb import *
import nb

SLUG = "mum-nasil-yanar"
nb.THEME.update(bg=["#3b2412", "#24150b", "#120a05"], accent="#ffb347")
NARRATION = [
 "Mum nasıl yanar? Asıl yanan şey, sandığınız şey değil.",
 "Fitil tutuşunca alevin sıcaklığı, fitilin dibindeki mumu eritir.",
 "Eriyen sıvı mum, kılcal etkiyle fitilden yukarı tırmanır. Tıpkı peçetenin suyu emmesi gibi.",
 "Alevin sıcaklığı bu sıvıyı buharlaştırır. Aslında yanan şey katı mum değil, mum buharıdır.",
 "Mum buharı havadaki oksijenle tepkimeye girer. Isı, ışık, su buharı ve karbondioksit açığa çıkar.",
 "Peki alev neden sarı? Alevdeki minicik kurum parçacıkları ısınıp parlar. Alevin dibindeki mavi bölgede ise oksijen boldur.",
 "Mum, kendi yakıtını taşıyan küçük bir fabrikadır. Neden böyle? Artık biliyorsunuz.",
]
WAX, WAXD, WICK, LIQ = "#f3e6cf", "#d9c6a5", "#3a2a1e", "#ffe9a8"

def flame(c, x, y, s, t, a=1.0, blue=True):
    """Alev tabanı (x, y); s ölçek."""
    fl = 1 + 0.06 * math.sin(t * 11) + 0.04 * math.sin(t * 17.3); sway = 6 * s * math.sin(t * 5.3)
    for wd, hh, cl, al in ((95, 330, "#ff8a3c", 0.25), (58, 250, "#ff9a3c", 1.0), (40, 190, "#ffd34d", 1.0), (22, 110, "#fff4c8", 1.0)):
        w_, h_ = wd * s, hh * s * fl
        p = skia.Path(); p.moveTo(x, y + 18 * s); p.cubicTo(x - w_ * 1.3, y - h_ * 0.15, x - w_ * 0.5, y - h_ * 0.7, x + sway, y - h_)
        p.cubicTo(x + w_ * 0.5, y - h_ * 0.7, x + w_ * 1.3, y - h_ * 0.15, x, y + 18 * s); p.close(); c.drawPath(p, fill(cl, a * al))
    if blue: c.drawOval(skia.Rect.MakeXYWH(x - 30 * s, y - 6 * s, 60 * s, 30 * s), fill("#5b8cff", a * 0.85))

def candle(c, x, top, w, h, t, a=1.0, lit=True, s=1.0, pool=0.0):
    rrect(c, x - w / 2, top, w, h, 14, WAX, a); rrect(c, x - w / 2 + w * 0.68, top, w * 0.32, h, 14, WAXD, a * 0.6)
    if pool > 0: c.drawOval(skia.Rect.MakeXYWH(x - w * 0.42 * pool, top - 10, w * 0.84 * pool, 26), fill(LIQ, a))
    line(c, x, top + 6, x, top - 50 * s, WICK, 10 * s, a)
    if lit: flame(c, x, top - 52 * s, s, t, a)

def hero(c, t):
    c.drawCircle(540, 820, 300, skia.Paint(AntiAlias=True, Shader=skia.GradientShader.MakeRadial((540, 820), 300, [col("#ffb347", 0.35), col("#ffb347", 0)])))
    candle(c, 540, 930, 210, 260, t, pool=1.0)
    rrect(c, 380, 1180, 320, 34, 17, "#7a4a28")

def i1(c, t, d):
    k = ss(0.6, 3.0, t)
    candle(c, 540, 860, 300, 300, t, s=1.0, pool=k)
    for j, (x0, x1) in enumerate([(330, 430), (750, 650)]):
        u = (t * 0.8 + j * 0.5) % 1
        arrow(c, x0, 640 + 40 * u, x1, 760 + 40 * u, "#ff7a3c", 8, ss(0.8, 1.3, t) * math.sin(u * math.pi), 20)
    tag(c, "ısı", 300, 610, "#ffb07a", ss(1.0, 1.5, t), 44, "c", "Bold")
    tag(c, "eriyen mum", 860, 1020, LIQ, ss(2.6, 3.1, t), 40, "c", "Bold")
    arrow(c, 800, 980, 650, 875, LIQ, 6, ss(2.6, 3.1, t), 18)

def i2(c, t, d):
    # büyütülmüş fitil kesiti
    rrect(c, 440, 520, 200, 600, 30, "#4a3626");
    for k in range(9): line(c, 455 + k * 21, 530, 455 + k * 21, 1110, "#2c1f15", 5)
    rrect(c, 120, 1030, 840, 110, 30, LIQ, 0.9); tag(c, "sıvı mum", 230, 1100, "#5a3d1e", ss(0.5, 1.0, t), 38, "c", "Bold")
    for k in range(10):
        u = (t * 0.35 + k * 0.1) % 1; y = lerp(1060, 560, u); x = 470 + (k % 5) * 35
        circ(c, x, y, 13, LIQ, ss(0.8, 1.4, t) * (1 - ss(0.85, 1, u)))
    arrow(c, 700, 1000, 700, 640, "#ffb347", 9, ss(1.5, 2.0, t), 28)
    tag(c, "kılcal etki", 860, 600, "#ffb347", ss(1.7, 2.2, t), 40, "c", "Bold")
    tag(c, "yukarı tırmanır", 860, 830, THEME["text"], ss(2.3, 2.8, t), 34, "c")

def i3(c, t, d):
    line(c, 300, 1150, 300, 790, WICK, 14)
    for k in range(4): circ(c, 300, 1110 - k * 90, 12, LIQ, ss(0.5, 1.0, t))
    flame(c, 300, 780, 1.0, t, ss(0.3, 0.8, t))
    for k in range(7):
        u = (t * 0.45 + k / 7) % 1; side = -1 if k % 2 else 1
        x = 300 + side * (40 + u * 70); y = 800 - u * 260
        circ(c, x, y, 14 + 10 * u, "#ffffff", 0.75 * ss(1.2, 1.8, t) * math.sin(u * math.pi))
    tag(c, "mum buharı", 165, 900, "#ffffff", ss(1.6, 2.1, t), 32, "c", "Bold")
    arrow(c, 190, 860, 255, 815, "#ffffff", 5, ss(1.6, 2.1, t), 16)
    # sağ: katı mum yanmaz / buhar yanar
    rrect(c, 620, 860, 140, 160, 16, WAX, ss(2.6, 3.0, t)); r_ = 38 * pop(t, 3.0); circ(c, 690, 1080, r_, RED)
    if r_ > 0: line(c, 690 - r_ * 0.4, 1080 - r_ * 0.4, 690 + r_ * 0.4, 1080 + r_ * 0.4, "#3a0f0f", r_ * 0.24); line(c, 690 + r_ * 0.4, 1080 - r_ * 0.4, 690 - r_ * 0.4, 1080 + r_ * 0.4, "#3a0f0f", r_ * 0.24)
    tag(c, "katı mum", 690, 820, THEME["text"], ss(2.6, 3.0, t), 32, "c")
    for k in range(5): circ(c, 860 + (k % 3) * 34, 900 + (k // 3) * 40 + 8 * math.sin(t * 3 + k), 16, "#ffffff", 0.7 * ss(3.4, 3.8, t))
    check(c, 895, 1080, 38 * pop(t, 3.9), ok=True); tag(c, "buhar", 895, 820, THEME["text"], ss(3.4, 3.8, t), 32, "c")

def mol(c, x, y, parts, a):
    for dx, dy, r, cl in parts: circ(c, x + dx, y + dy, r, cl, a)
O2 = [(-18, 0, 20, "#ff6b6b"), (18, 0, 20, "#ff6b6b")]
CO2 = [(-36, 0, 18, "#ff6b6b"), (0, 0, 22, "#555555"), (36, 0, 18, "#ff6b6b")]
H2O = [(0, 0, 22, "#ff6b6b"), (-26, 18, 13, "#e8f4ff"), (26, 18, 13, "#e8f4ff")]
def i4(c, t, d):
    flame(c, 540, 1000, 1.25, t)
    for k, (sx, sy) in enumerate([(150, 1080), (930, 1080), (150, 900), (930, 900)]):
        u = ss(0.4 + k * 0.15, 2.0 + k * 0.15, t); x = lerp(sx, 540 + (-60 if sx < 540 else 60), u); y = lerp(sy, 960, u)
        mol(c, x, y, O2, (1 - ss(1.8, 2.3, t)) * ss(0.3, 0.6, t))
    tag(c, "oksijen", 200, 1150, "#ff9a9a", ss(0.6, 1.1, t) * (1 - ss(2.0, 2.4, t)), 36, "c", "Bold")
    for k, (ex, ey, m, lb) in enumerate([(230, 600, CO2, "karbondioksit"), (850, 600, H2O, "su buharı")]):
        u = ss(2.6 + k * 0.4, 3.8 + k * 0.4, t); x = lerp(540, ex, u); y = lerp(700, ey, u)
        mol(c, x, y, m, ss(2.6 + k * 0.4, 2.9 + k * 0.4, t)); tag(c, lb, ex, ey + 70, THEME["text"], ss(3.6 + k * 0.4, 4.0 + k * 0.4, t), 34, "c", "Bold")
    tag(c, "ısı + ışık", 540, 1140, "#ffd34d", ss(4.6, 5.1, t), 42, "c", "Bold")

SCENES = [
 title_scene("Mum", "nasıl yanar?", "Asıl yanan şey sürpriz", hero),
 reason_scene("ADIM 1", "Isı mumu eritir", ["Alevin sıcaklığı, fitilin", "dibindeki mumu eritir."], i1),
 reason_scene("ADIM 2", "Sıvı fitile tırmanır", ["Eriyen mum, kılcal etkiyle", "fitilden yukarı çekilir."], i2),
 reason_scene("ADIM 3", "Mum buharlaşır", ["Yanan şey katı mum değil,", "sıcakta oluşan mum buharıdır."], i3),
 reason_scene("ADIM 4", "Buhar oksijenle yanar", ["Isı ve ışık çıkar; geriye", "su buharı ve karbondioksit kalır."], i4),
 cards_scene("BONUS", "Alev neden sarı?", [("Kurum parçacıkları", "Minicik karbon taneleri"), ("Isınıp sarı parlar", "Alevin aydınlık kısmı"), ("Dipte mavi bölge", "Orada oksijen boldur")]),
 end_scene("Mum, kendi yakıtını", "taşıyan bir fabrika.", hero),
]
if __name__ == "__main__":
    nb.main(SLUG, NARRATION, SCENES)
