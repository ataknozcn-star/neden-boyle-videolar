import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import numpy as np, skia
from nb import *
import nb

SLUG = "kuslar-neden-carpilmaz"
YEL = "#ffd23f"
nb.THEME.update(bg=["#26375a", "#162038", "#0b1020"], accent=YEL)
NARRATION = [
 "Kuşlar elektrik telinde neden çarpılmaz? Cevap, elektriğin nasıl aktığında.",
 "Elektrik akımı, akabileceği tam bir yol ister. Yüksek gerilimden, daha düşük gerilime doğru akar.",
 "Kuş tek bir tele konduğunda, iki ayağı da aynı teldedir. Yani ikisi de aynı gerilimdedir.",
 "Ayakları arasında gerilim farkı olmayınca, akım kuşun bedenine sapmaz. Teldeki yoluna devam eder.",
 "Ama kuş kanadıyla ikinci bir tele ya da direğe dokunursa, yol tamamlanır. Akım bedeninden geçer.",
 "Kısacası, tehlikeli olan gerilimin kendisi değil, gerilim farkıdır. Bu yüzden teller birbirinden aralıklı çekilir.",
 "Kuşların sırrı, tek bir tele basmak. Neden böyle? Artık biliyorsunuz.",
]
BIRD = "#6ec6f0"; WIRE = "#9aa7bd"

def bird(c, x, y, s=1.0, t=0.0, wing=0.0, color=BIRD, a=1.0):
    """(x, y) ayakların tele değdiği nokta. wing: 0 kapalı, 1 açık (sağa uzanır)."""
    c.save(); c.translate(x, y); c.scale(s, s)
    line(c, -14, -6, -18, 0, "#ff9a3c", 5, a); line(c, 14, -6, 18, 0, "#ff9a3c", 5, a)
    poly(c, [(-38, -40), (-82, -22), (-70, -48)], mixcol(color, "#000000", 0.25), a)
    c.drawOval(skia.Rect.MakeXYWH(-46, -82, 92, 78), fill(color, a))
    c.drawOval(skia.Rect.MakeXYWH(-22, -50, 52, 40), fill("#e9f6ff", a))
    bob = 2 * math.sin(t * 4)
    circ(c, 30, -92 + bob, 27, color, a)
    poly(c, [(52, -98 + bob), (76, -90 + bob), (52, -84 + bob)], GOLD, a)
    circ(c, 38, -98 + bob, 5, "#10182a", a)
    wc = mixcol(color, "#000000", 0.18)
    if wing <= 0.01:
        c.drawOval(skia.Rect.MakeXYWH(-40, -68, 58, 34), fill(wc, a))
    else:
        ang = lerp(0.3, -0.5, wing); L = lerp(55, 125, wing)
        tx, ty = -10 + L * math.cos(ang), -60 + L * math.sin(ang)
        p = skia.Path(); p.moveTo(-18, -62); p.quadTo((-18 + tx) / 2 - 10, (-62 + ty) / 2 - 25, tx, ty)
        p.quadTo((25 + tx) / 2 + 15, (-42 + ty) / 2 + 10, 25, -42); p.close(); c.drawPath(p, fill(wc, a))
    c.restore()

def wire(c, x0, x1, y, sag=14, color=WIRE, w=8, a=1.0):
    p = skia.Path(); p.moveTo(x0, y); p.quadTo((x0 + x1) / 2, y + sag * 2, x1, y); c.drawPath(p, stroke(color, w, a))
def wy(x, x0, x1, y, sag=14):
    u = (x - x0) / (x1 - x0); return y + sag * 4 * u * (1 - u) * 1.0
def flow(c, x0, x1, y, t, sag=14, color=YEL, n=9, speed=160, a=1.0):
    L = x1 - x0
    for k in range(n):
        x = x0 + ((t * speed + k * L / n) % L)
        circ(c, x, wy(x, x0, x1, y, sag), 9, color, a * 0.95)
def bolt(c, x, y, s, color=YEL, a=1.0):
    pts = [(0.15, -1), (-0.45, 0.1), (-0.02, 0.1), (-0.2, 1), (0.45, -0.15), (0.02, -0.15)]
    poly(c, [(x + px * s, y + py * s) for px, py in pts], color, a)
def pole(c, x, y0, y1):
    rrect(c, x - 16, y0, 32, y1 - y0, 8, "#8a6a4a"); rrect(c, x - 120, y0 + 20, 240, 22, 8, "#7a5c3e")
    for dx in (-90, 90): rrect(c, x + dx - 10, y0 - 4, 20, 28, 6, "#e8eef7")

def hero(c, t):
    wire(c, 60, 1020, 820, 18); wire(c, 60, 1020, 1010, 18)
    flow(c, 60, 1020, 820, t, 18); flow(c, 60, 1020, 1010, t + 0.7, 18)
    bird(c, 430, wy(430, 60, 1020, 820, 18) - 4, 1.25, t)
    bird(c, 700, wy(700, 60, 1020, 1010, 18) - 4, 1.0, t + 1, color=PINK)
    bolt(c, 860, 620, 70, YEL, 0.6 + 0.4 * math.sin(t * 5))

def i1(c, t, d):
    rrect(c, 80, 690, 230, 230, 34, "#ff5d5d", 0.85); rrect(c, 770, 690, 230, 230, 34, "#5b9bff", 0.85)
    text(c, "YÜKSEK", 195, 812, 40, "#ffffff"); text(c, "gerilim", 195, 862, 32, "#ffffff", 0.85, "Medium")
    text(c, "DÜŞÜK", 885, 812, 40, "#ffffff"); text(c, "gerilim", 885, 862, 32, "#ffffff", 0.85, "Medium")
    p = ss(0.6, 1.6, t); line(c, 310, 805, 310 + 460 * p, 805, WIRE, 10)
    if t > 1.6: flow(c, 318, 762, 795, t, 0, YEL, 7, 140)
    arrow(c, 430, 990, 650, 990, YEL, 9, ss(3.4, 3.9, t), 26)
    tag(c, "akım bu yöne akar", 540, 1070, YEL, ss(3.6, 4.1, t), 38, "c", "Bold")
    tag(c, "tam bir yol gerekir", 540, 640, THEME["text"], ss(1.6, 2.1, t), 36, "c")

def i2(c, t, d):
    wire(c, 60, 1020, 900, 0, WIRE, 14); flow(c, 60, 1020, 900, t, 0, YEL, 10, 150, 0.5)
    k = pop(t, 0.4, 0.6)
    if k > 0:
        c.save(); c.translate(540, 893); c.scale(k, k); c.translate(-540, -893); bird(c, 540, 893, 2.3, t); c.restore()
    for dx in (-41, 41):
        r = ss(1.8, 2.3, t); circ(c, 540 + dx, 900, 26, YEL, r * 0.9, sw=6)
    r = ss(2.0, 2.5, t)
    line(c, 499, 930, 430, 985, YEL, 4, r); line(c, 581, 930, 650, 985, YEL, 4, r)
    tag(c, "sol ayak", 400, 1020, THEME["text"], r, 36, "c")
    tag(c, "sağ ayak", 680, 1020, THEME["text"], r, 36, "c")
    tag(c, "aynı gerilim", 540, 1110, YEL, ss(3.5, 4.0, t), 46, "c", "Bold")

def i3(c, t, d):
    wire(c, 60, 1020, 900, 0, WIRE, 14); flow(c, 60, 1020, 900, t, 0, YEL, 12, 220)
    bird(c, 540, 893, 2.3, t)
    a = ss(1.2, 1.7, t)
    arrow(c, 880, 880, 880, 700, "#ff5d5d", 8, a * 0.8, 22)
    line(c, 840, 760, 920, 820, "#ff5d5d", 10, a); line(c, 920, 760, 840, 820, "#ff5d5d", 10, a)
    tag(c, "bedene akım yok", 870, 655, "#ff9a9a", ss(1.4, 1.9, t), 34, "c")
    tag(c, "fark = 0", 260, 720, YEL, ss(1.6, 2.1, t), 54, "c", "Bold")
    arrow(c, 180, 980, 900, 980, YEL, 9, ss(3.0, 3.5, t), 26)
    tag(c, "akım telde devam eder", 540, 1060, THEME["text"], ss(3.2, 3.7, t), 38, "c")

def i4(c, t, d):
    wire(c, 60, 1020, 760, 0, WIRE, 12); wire(c, 60, 1020, 1000, 0, "#c4a1ff", 12)
    tag(c, "1. tel", 90, 735, THEME["text"], 0.8, 30); tag(c, "2. tel", 90, 975, THEME["text"], 0.8, 30)
    w = ss(1.0, 2.6, t)
    bird(c, 470, 994, 2.0, t, wing=w, color=PINK)
    touch = t > 2.7
    if touch:
        fl = 0.5 + 0.5 * math.sin(t * 22)
        circ(c, 670, 760, 34, YEL, 0.35 + 0.4 * fl)
        bolt(c, 760, 690, 60, "#ff5d5d", fl); bolt(c, 330, 860, 50, YEL, 1 - fl)
    tag(c, "iki tel = tehlike", 540, 1120, "#ff8080", ss(3.0, 3.5, t), 46, "c", "Bold")

SCENES = [
 title_scene("Kuşlar elektrik telinde", "neden çarpılmaz?", "Elektriğin gizli kuralı", hero),
 reason_scene("NEDEN 1", "Akım bir yol ister", ["Elektrik yüksek gerilimden", "düşük gerilime doğru akar."], i1),
 reason_scene("NEDEN 2", "İki ayak, aynı tel", ["Tek tele konan kuşun", "iki ayağı da aynı gerilimde."], i2),
 reason_scene("NEDEN 3", "Fark yoksa akım yok", ["Akım kuşun bedenine sapmaz,", "teldeki yoluna devam eder."], i3),
 reason_scene("NEDEN 4", "İkinci tel tehlikeli", ["Kanat ikinci tele ya da direğe", "değerse akım bedenden geçer."], i4),
 cards_scene("ÖZET", "Önemli olan fark", [("Gerilim farkı öldürür", "Gerilimin kendisi değil"), ("Tek tel: güvenli", "İki ayak aynı gerilimde"), ("Teller aralıklı çekilir", "Kanatlar ikisine yetişmesin")]),
 end_scene("Kuşların sırrı:", "tek tele basmak.", hero),
]
if __name__ == "__main__":
    nb.main(SLUG, NARRATION, SCENES)
