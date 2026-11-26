import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import numpy as np, skia
from nb import *
import nb

SLUG = "sabun-kopugu-neden-yuvarlak"
nb.THEME.update(bg=["#0f5a63", "#0a3b45", "#06222b"], accent="#7ff0e0")
NARRATION = [
 "Sabun köpüğü neden hep yuvarlak? Cevap, suyun gizli gücünde.",
 "Sabun köpüğü, havayı saran çok ince bir zardır. Bu zar, iki sabun katmanının arasında kalan ince bir su tabakasıdır.",
 "Sudaki moleküller birbirini çeker. Bu yüzey gerilimi, zarı bir lastik gibi hep küçülmeye zorlar.",
 "Ama içerideki hava da dışarı doğru iter. Zarın çekmesiyle havanın itmesi dengelenir.",
 "Aynı miktarda havayı saran şekiller arasında, en az yüzeye sahip olan küredir. Zar en küçük hâlini alınca köpük yuvarlak olur.",
 "Peki renkler nereden geliyor? Işık zarın iç ve dış yüzünden yansıyıp karışır. Zar inceldikçe renkler değişir, sonunda köpük patlar.",
 "Köpük, en az yüzeyli şekli seçer. Neden böyle? Artık biliyorsunuz.",
]
IRI = ["#ff7fb6", "#ffd36e", "#7ff0e0", "#7fb0ff", "#c99bff"]
WATER = "#6ec6f0"

def bubble(c, x, y, r, t=0.0, a=1.0):
    if r <= 1 or a <= 0.01: return
    circ(c, x, y, r, "#bff6ff", 0.10 * a)
    n = 5
    for k in range(n):
        st = (t * 40 + k * 72) % 360
        p = skia.Path(); p.addArc(skia.Rect.MakeXYWH(x - r, y - r, 2 * r, 2 * r), st, 80)
        c.drawPath(p, stroke(IRI[k], max(3, r * 0.05), 0.75 * a))
    circ(c, x, y, r, "#ffffff", 0.35 * a, sw=max(2, r * 0.015))
    p = skia.Path(); p.addArc(skia.Rect.MakeXYWH(x - r * 0.72, y - r * 0.72, 1.44 * r, 1.44 * r), 200, 50)
    c.drawPath(p, stroke("#ffffff", max(4, r * 0.07), 0.8 * a))
    circ(c, x + r * 0.42, y - r * 0.45, r * 0.07, "#ffffff", 0.8 * a)

def wand(c, x, y, a=1.0):
    line(c, x, y + 95, x - 70, y + 330, "#f5b942", 16, a)
    circ(c, x, y, 95, "#f5b942", a, sw=14)

def hero(c, t):
    wand(c, 300, 1000)
    bubble(c, 610, 830 - 10 * math.sin(t * 1.3), 190, t)
    bubble(c, 330 + 8 * math.sin(t), 690, 70, t + 1)
    bubble(c, 840, 1050 + 10 * math.sin(t * 1.1), 85, t + 2)
    for j in range(4):
        u = (t * 0.25 + j * 0.25) % 1
        bubble(c, 420 + j * 90 + 20 * math.sin(t + j), 1100 - u * 520, 22 + 8 * j % 3, t, 0.9 * (1 - u) * ss(0, 0.1, u))

def i1(c, t, d):
    bubble(c, 300, 820, 190 * pop(t, 0.4, 0.7), t)
    z = ss(1.6, 2.4, t)
    if z > 0:
        line(c, 440, 700, 640, 640, "#ffffff", 4, 0.7 * z); line(c, 440, 940, 640, 1000, "#ffffff", 4, 0.7 * z)
        rrect(c, 640, 620, 340, 400, 30, "#ffffff", 0.06 * z); rrect(c, 640, 620, 340, 400, 30, "#ffffff", 0.4 * z, sw=3)
        s1 = ss(4.0, 4.5, t); s2 = ss(5.0, 5.5, t)
        for k in range(7):
            yy = 660 + k * 52
            circ(c, 690, yy, 15, IRI[0], s1); line(c, 705, yy, 725, yy, IRI[0], 5, s1)
            circ(c, 930, yy, 15, IRI[0], s1); line(c, 895, yy, 915, yy, IRI[0], 5, s1)
        rrect(c, 735, 640, 150, 360, 20, WATER, 0.55 * s2)
        for k in range(6): circ(c, 770 + (k % 2) * 80, 690 + k * 55, 11, "#ffffff", 0.8 * s2)
    tag(c, "sabun", 690, 1075, "#ffb3d4", ss(4.2, 4.7, t), 34, "c", "Bold")
    tag(c, "su", 810, 1075, "#bfe8ff", ss(5.2, 5.7, t), 34, "c", "Bold")
    tag(c, "sabun", 930, 1075, "#ffb3d4", ss(4.2, 4.7, t), 34, "c", "Bold")
    tag(c, "ince zar", 300, 1075, THEME["accent"], ss(1.0, 1.5, t), 40, "c", "Bold")

def i2(c, t, d):
    xs = [160 + k * 152 for k in range(6)]
    sq = 1 - 0.18 * ss(3.0, 4.6, t)
    xs = [540 + (x - 540) * sq for x in xs]
    for row, y in enumerate((700, 860, 1020)):
        for k in range(5):
            line(c, xs[k], y, xs[k + 1], y, "#bfe8ff", 6, 0.8 * ss(1.0, 1.5, t))
        if row < 2:
            for k in range(6): line(c, xs[k], y, xs[k], y + 160, "#bfe8ff", 6, 0.8 * ss(1.0, 1.5, t))
        for k in range(6):
            wob = 4 * math.sin(t * 6 + k + row)
            circ(c, xs[k] + wob, y, 30 * pop(t, 0.4 + 0.05 * k + 0.1 * row), WATER)
    a = ss(2.4, 2.9, t)
    arrow(c, 70, 860, 160, 860, "#ffffff", 9, a, 26); arrow(c, 1010, 860, 920, 860, "#ffffff", 9, a, 26)
    tag(c, "moleküller birbirini çeker", 540, 600, "#bfe8ff", ss(1.2, 1.7, t), 38, "c", "Bold")
    tag(c, "yüzey gerilimi: hep küçül!", 540, 1150, THEME["accent"], ss(3.2, 3.7, t), 40, "c", "Bold")

def i3(c, t, d):
    br = 230 + 8 * math.sin(t * 2.2)
    bubble(c, 540, 840, br, t)
    ain = ss(0.6, 1.2, t); aout = ss(2.0, 2.6, t)
    for k in range(8):
        ang = k * math.pi / 4 + math.pi / 8; cs, sn = math.cos(ang), math.sin(ang)
        arrow(c, 540 + cs * (br + 70), 840 + sn * (br + 70), 540 + cs * (br + 12), 840 + sn * (br + 12), IRI[0], 9, ain, 22)
    for k in range(8):
        ang = k * math.pi / 4; cs, sn = math.cos(ang), math.sin(ang)
        arrow(c, 540 + cs * 135, 840 + sn * 105, 540 + cs * (br - 30), 840 + sn * (br - 30), "#bfe8ff", 9, aout, 22)
    tag(c, "zar çeker", 540, 560, "#ffb3d4", ain, 40, "c", "Bold")
    rrect(c, 420, 805, 240, 66, 33, "#0a3b45", 0.9 * aout)
    tag(c, "hava iter", 540, 852, "#ffffff", aout, 40, "c", "Bold")
    tag(c, "DENGE", 540, 1150, THEME["accent"], ss(3.6, 4.1, t), 52, "c", "Bold")

def i4(c, t, d):
    k = eout(ss(4.2, 5.8, t))
    cx, cy, s = 540, 880, 175
    # küpten küreye: köşeleri yuvarlanan kare
    r = lerp(20, s, k)
    rrect(c, cx - s, cy - s, 2 * s, 2 * s, r, "#bff6ff", 0.12 * (1 - k))
    rrect(c, cx - s, cy - s, 2 * s, 2 * s, r, "#ffffff", 0.7 * (1 - k), sw=6)
    if k < 0.98:
        a = 0.6 * (1 - k)
        poly(c, [(cx - s, cy - s), (cx - s + 70, cy - s - 60), (cx + s + 70, cy - s - 60), (cx + s, cy - s)], "#ffffff", a, sw=5, close=False)
        line(c, cx + s + 70, cy - s - 60, cx + s + 70, cy + s - 60, "#ffffff", 5, a); line(c, cx + s + 70, cy + s - 60, cx + s, cy + s, "#ffffff", 5, a)
    bubble(c, cx, cy, s * 1.08, t, k)
    tag(c, "küp: daha çok yüzey", 540, 575, "#ffffff", ss(1.0, 1.5, t) * (1 - ss(4.0, 4.4, t)), 40, "c", "Bold")
    tag(c, "küre: en az yüzey", 540, 575, THEME["accent"], ss(5.6, 6.1, t), 44, "c", "Bold")
    tag(c, "aynı miktarda hava", 540, 1135, "#bfe8ff", ss(1.8, 2.3, t), 38, "c")

SCENES = [
 title_scene("Sabun köpüğü", "neden yuvarlak?", "Suyun gizli gücü", hero),
 reason_scene("NEDEN 1", "İnce bir su zarı", ["Köpük, havayı saran ince bir zardır:", "iki sabun katmanı arasında su."], i1),
 reason_scene("NEDEN 2", "Zar hep küçülmek ister", ["Su molekülleri birbirini çeker;", "yüzey gerilimi zarı daraltır."], i2),
 reason_scene("NEDEN 3", "İçerideki hava iter", ["Zarın çekmesiyle havanın itmesi", "birbirini dengeler."], i3),
 reason_scene("NEDEN 4", "Küre en az yüzeyli", ["Aynı hacmi saran en küçük yüzey", "küredir; köpük yuvarlak olur."], i4),
 cards_scene("BONUS", "Renkler nereden geliyor?", [("Işık iki kez yansır", "Zarın iç ve dış yüzünden"), ("Yansımalar karışır", "Zarın kalınlığı rengi belirler"), ("Zar incelir, patlar", "Renkler değişir, köpük söner")]),
 end_scene("Köpük, en az yüzeyli", "şekli seçer.", hero),
]
if __name__ == "__main__":
    nb.main(SLUG, NARRATION, SCENES)
