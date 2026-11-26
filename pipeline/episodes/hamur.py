import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import numpy as np, skia
from nb import *
import nb

SLUG = "hamur-neden-kabarir"
nb.THEME.update(bg=["#7a4a22", "#4e2e15", "#2a180b"], accent="#ffcf7a")
NARRATION = [
 "Hamur neden kabarır? Sırrı, gözle görülmeyen minicik canlılarda.",
 "Maya, aslında tek hücreli canlı bir mantardır. Hamurun içinde beslenir ve çoğalır.",
 "Undaki nişastanın bir kısmı enzimlerle şekere dönüşür. Maya bu şekeri yer; karbondioksit gazı ve biraz alkol çıkarır.",
 "Yoğurmak, unun proteinlerinden esnek bir gluten ağı oluşturur. Bu ağ, gazı minik kabarcıkların içinde hapseder.",
 "Kabarcıklar büyüdükçe hamur şişer. Fırında ısı gazı genleştirir ve hamur son bir kez hızla kabarır.",
 "Özetle: maya gaz üretir, gluten bu gazı tutar, fırının ısısı da süngerimsi yapıyı sabitler.",
 "Ekmeğin içindeki delikler, mayanın bıraktığı gaz izleri. Neden böyle? Artık biliyorsunuz.",
]
DOUGH, DOUGH2, BOWL = "#f3dcae", "#e2c088", "#c8553d"

def bowl(c, x, y, w):
    p = skia.Path(); p.moveTo(x - w / 2, y)
    p.cubicTo(x - w / 2, y + w * 0.42, x + w / 2, y + w * 0.42, x + w / 2, y); p.close()
    c.drawPath(p, fill(BOWL)); rrect(c, x - w / 2 - 14, y - 12, w + 28, 26, 13, "#e0705a")
def dough(c, x, y, w, h, holes=0, seed=1, t=0.0):
    p = skia.Path(); p.moveTo(x - w / 2, y)
    p.cubicTo(x - w / 2, y - h * 1.3, x + w / 2, y - h * 1.3, x + w / 2, y); p.close()
    c.drawPath(p, fill(DOUGH)); c.drawPath(p, stroke(DOUGH2, 6))
    r = np.random.default_rng(seed)
    for _ in range(holes):
        u = float(r.uniform(-0.38, 0.38)); v = float(r.uniform(0.15, 0.8)); rr = float(r.uniform(6, 14))
        circ(c, x + u * w, y - v * h * 0.95, rr * (0.6 + 0.4 * min(1, h / 200)), DOUGH2, 0.9)
def yeast(c, x, y, s, t, a=1.0, bud=0.0):
    c.save(); c.translate(x, y); c.rotate(8 * math.sin(t * 2 + x));
    r = skia.Rect.MakeXYWH(-46 * s, -36 * s, 92 * s, 72 * s)
    c.drawOval(r, fill("#e9d27a", a)); c.drawOval(r, stroke("#8a6b1f", 5 * s, a))
    circ(c, -8 * s, -4 * s, 13 * s, "#8a6b1f", 0.7 * a)
    if bud > 0:
        circ(c, 50 * s, -22 * s, 22 * s * bud, "#e9d27a", a); circ(c, 50 * s, -22 * s, 22 * s * bud, "#8a6b1f", a, sw=4 * s)
    c.restore()
def bubble(c, x, y, r, a=1.0):
    circ(c, x, y, r, "#ffffff", 0.18 * a); circ(c, x, y, r, "#ffffff", 0.85 * a, sw=4)
    circ(c, x - r * 0.35, y - r * 0.35, r * 0.18, "#ffffff", 0.8 * a)

def hero(c, t):
    h = 150 + 40 * (0.5 + 0.5 * math.sin(t * 1.3))
    dough(c, 540, 990, 470, h, holes=9, seed=3)
    bowl(c, 540, 990, 520)
    for k in range(4):
        u = (t * 0.35 + k * 0.25) % 1
        bubble(c, 420 + k * 80, 990 - h * 1.05 - 40 - u * 150, 12 + 8 * u, 1 - u)

def i1(c, t, d):
    circ(c, 540, 820, 300, "#ffffff", 0.06); circ(c, 540, 820, 300, "#ffffff", 0.35, sw=5)
    pos = [(430, 720), (650, 760), (500, 900), (690, 930), (380, 870), (560, 650)]
    for k, (x, y) in enumerate(pos):
        a = ss(0.5 + k * 0.25, 0.9 + k * 0.25, t)
        yeast(c, x, y, 0.95, t, a, bud=ss(3.0 + k * 0.3, 3.8 + k * 0.3, t))
    tag(c, "maya hücreleri", 540, 1180, THEME["accent"], ss(1.6, 2.1, t), 40, "c", "Bold")

def hexa(c, x, y, r, color, a=1.0):
    poly(c, [(x + r * math.cos(k * math.pi / 3), y + r * math.sin(k * math.pi / 3)) for k in range(6)], color, a)
    poly(c, [(x + r * math.cos(k * math.pi / 3), y + r * math.sin(k * math.pi / 3)) for k in range(6)], "#ffffff", 0.7 * a, sw=4)
def i2(c, t, d):
    # nişasta zinciri -> şeker parçaları
    sp = ss(1.0, 2.4, t)
    for k in range(6):
        x0 = 190 + k * 58; y0 = 600
        x1 = 160 + (k % 3) * 120 + 20; y1 = 760 + (k // 3) * 110
        x = lerp(x0, x1, sp); y = lerp(y0, y1, sp)
        if k < 5 and sp < 0.2: line(c, x0 + 26, y0, x0 + 32, y0, "#ffffff", 6, 1 - sp * 5)
        eaten = ss(4.4 + k * 0.3, 4.8 + k * 0.3, t) if k < 4 else 0.0
        hexa(c, lerp(x, 640, eaten), lerp(y, 820, eaten), 26 * (1 - eaten * 0.9), "#fff3c4", 1 - eaten)
    tag(c, "nişasta", 330, 535, THEME["text"], ss(0.5, 1.0, t) * (1 - ss(1.8, 2.3, t)), 34, "c")
    tag(c, "şeker", 330, 1010, "#fff3c4", ss(2.2, 2.7, t), 38, "c", "Bold")
    arrow(c, 500, 820, 590, 820, THEME["text"], 8, ss(3.4, 3.9, t))
    yeast(c, 700, 820, 1.25, t, ss(3.5, 4.0, t))
    for k in range(5):
        if t < 4.6: break
        u = ((t - 4.6) * 0.5 + k * 0.2) % 1
        x = 760 + 60 * math.sin(k * 2.1 + u * 4); y = 760 - u * 250
        bubble(c, x + 40, y, 16 + 10 * u, 1 - u)
    tag(c, "CO2 gazı", 830, 520, "#ffffff", ss(5.0, 5.5, t), 40, "c", "Bold")
    tag(c, "+ biraz alkol", 720, 1010, THEME["accent"], ss(6.0, 6.5, t), 34, "c")

def i3(c, t, d):
    k = ss(0.6, 2.4, t)
    for j in range(7):
        p = skia.Path(); y = 560 + j * 85
        for s_ in range(0, 841, 10):
            x = 120 + s_; yy = y + 18 * math.sin(s_ / 70 + j + t * 1.2)
            if s_ > 840 * k: break
            p.moveTo(x, yy) if s_ == 0 else p.lineTo(x, yy)
        c.drawPath(p, stroke(DOUGH, 7, 0.85))
    for j in range(8):
        p = skia.Path(); x = 140 + j * 115
        for s_ in range(0, 541, 10):
            y = 540 + s_; xx = x + 16 * math.sin(s_ / 60 + j * 1.3 + t)
            if s_ > 540 * k: break
            p.moveTo(xx, y) if s_ == 0 else p.lineTo(xx, y)
        c.drawPath(p, stroke(DOUGH2, 5, 0.7))
    g = ss(3.2, 6.5, t)
    for (x, y, r0) in ((400, 760, 30), (660, 880, 24), (560, 680, 18)):
        bubble(c, x, y, r0 + 55 * g * (r0 / 30), ss(3.0, 3.5, t))
    tag(c, "gluten ağı", 540, 1170, THEME["accent"], ss(1.8, 2.3, t), 40, "c", "Bold")

def oven(c, x, y, w, h, t, a=1.0):
    rrect(c, x, y, w, h, 30, "#3b3f47", a); rrect(c, x + 30, y + 30, w - 60, h - 60, 20, "#1c1e22", a)
    rrect(c, x + 30, y + 30, w - 60, h - 60, 20, "#ff8a3c", 0.12 * a)
    flames(c, x + w / 2, y + h - 42, 6, t, a * 0.9, 60)
def i4(c, t, d):
    # 1) kasede kabarma
    a1 = 1 - ss(3.6, 4.2, t)
    if a1 > 0:
        c.saveLayerAlpha(None, int(255 * a1))
        h = 70 + 170 * ss(0.6, 3.2, t)
        dough(c, 540, 1000, 470, h, holes=int(4 + 10 * ss(0.6, 3.2, t)), seed=5)
        bowl(c, 540, 1000, 520)
        tag(c, "hamur şişer", 540, 560, THEME["accent"], ss(1.2, 1.7, t), 40, "c", "Bold")
        c.restore()
    # 2) fırında son kabarma
    a2 = ss(3.8, 4.4, t)
    if a2 > 0:
        c.saveLayerAlpha(None, int(255 * a2))
        oven(c, 150, 560, 780, 560, t)
        hh = 90 + 70 * ss(4.4, 6.0, t)
        col_ = mixcol(DOUGH, "#c9823f", ss(4.8, 6.3, t))
        p = skia.Path(); x0 = 540; y0 = 980; w = 430
        p.moveTo(x0 - w / 2, y0); p.cubicTo(x0 - w / 2, y0 - hh * 1.3, x0 + w / 2, y0 - hh * 1.3, x0 + w / 2, y0); p.close()
        c.drawPath(p, fill(col_)); c.drawPath(p, stroke("#8a4f1f", 6))
        rrect(c, 260, 980, 560, 16, 8, "#9aa0a8")
        for k in range(3):
            u = (t * 0.6 + k * 0.33) % 1
            line(c, 420 + k * 120, 900 - hh - 20 - u * 60, 420 + k * 120 + 10 * math.sin(u * 6), 870 - hh - 20 - u * 60, "#ffffff", 6, 0.6 * (1 - u))
        tag(c, "ısı gazı genleştirir", 540, 1180, THEME["accent"], ss(4.6, 5.1, t), 40, "c", "Bold")
        c.restore()

def sliced(c, t):
    p = skia.Path(); p.moveTo(290, 1060); p.cubicTo(290, 720, 790, 720, 790, 1060); p.close()
    c.drawPath(p, fill("#b8702f"))
    p2 = skia.Path(); p2.moveTo(320, 1050); p2.cubicTo(320, 760, 760, 760, 760, 1050); p2.close()
    c.drawPath(p2, fill(DOUGH))
    r = np.random.default_rng(8)
    for _ in range(26):
        x = float(r.uniform(350, 730)); y = float(r.uniform(880, 1030)); rr = float(r.uniform(6, 16))
        circ(c, x, y, rr, DOUGH2)
    for _ in range(8):
        x = float(r.uniform(430, 650)); y = float(r.uniform(830, 880)); circ(c, x, y, float(r.uniform(5, 11)), DOUGH2)
    rrect(c, 260, 1060, 560, 20, 10, "#8a5a33")

SCENES = [
 title_scene("Hamur", "neden kabarır?", "Mayanın gizli işi", hero),
 reason_scene("NEDEN 1", "Maya canlıdır", ["Maya, tek hücreli bir mantardır;", "hamurda beslenir ve çoğalır."], i1),
 reason_scene("NEDEN 2", "Maya şekeri yer", ["Nişasta kısmen şekere dönüşür;", "maya onu yer, CO2 gazı çıkarır."], i2),
 reason_scene("NEDEN 3", "Gluten gazı tutar", ["Yoğurmak esnek bir ağ oluşturur;", "gaz minik kabarcıklarda kalır."], i3),
 reason_scene("NEDEN 4", "Kabarcıklar büyür", ["Hamur şişer; fırında ısı gazı", "genleştirir, son kez kabarır."], i4),
 cards_scene("ÖZET", "Kabarmanın üç adımı", [("Maya gaz üretir", "Şekeri yer, CO2 çıkarır"), ("Gluten gazı tutar", "Esnek ağ, minik kabarcıklar"), ("Fırın yapıyı sabitler", "Süngerimsi doku oluşur")]),
 end_scene("Ekmekteki delikler,", "gaz izleridir.", sliced),
]
if __name__ == "__main__":
    nb.main(SLUG, NARRATION, SCENES)
