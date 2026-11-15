import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import numpy as np, skia
from nb import *
import nb

SLUG = "yapraklar-neden-sararir"
nb.THEME.update(bg=["#6b3a12", "#40220c", "#1f1106"], accent="#ffa94d")
NARRATION = [
 "Yapraklar sonbaharda neden sararır? İşte renklerin sırrı.",
 "Yaprağı yeşil yapan şey klorofildir. Klorofil, güneş ışığını besine çevirir.",
 "Yaprağın içinde aslında sarı ve turuncu pigmentler de vardır. Ama yeşil o kadar baskındır ki onları göremeyiz.",
 "Sonbaharda günler kısalır ve hava soğur. Ağaç klorofil üretmeyi bırakır; yeşil yavaş yavaş kaybolur.",
 "Yeşil gidince, altta saklanan sarı ve turuncu ortaya çıkar. Bazı ağaçlar bir de kırmızı pigment üretir.",
 "Sonunda ağaç, yaprağın sapını kapatır ve yaprak düşer. Böylece kışı su kaybetmeden geçirir.",
 "Yapraklar boyanmıyor; yeşil perde kalkıyor. Neden böyle? Artık biliyorsunuz.",
]
GRN, YLW, ORG, RDL = "#4caf50", "#f2c230", "#f08a24", "#d6453d"
def lpath(s):
    p = skia.Path(); p.moveTo(0, -175 * s); p.cubicTo(160 * s, -115 * s, 160 * s, 95 * s, 0, 175 * s); p.cubicTo(-160 * s, 95 * s, -160 * s, -115 * s, 0, -175 * s); p.close(); return p
def leaf(c, cx, cy, s=1.0, color=GRN, rot=0.0, a=1.0):
    c.save(); c.translate(cx, cy); c.rotate(rot); c.drawPath(lpath(s), fill(color, a)); v = mixcol(color, "#000000", 0.45)
    line(c, 0, -150 * s, 0, 225 * s, v, 8 * s, a)
    for k in (-80, -10, 60):
        for sg in (-1, 1): line(c, 0, k * s, sg * 88 * s, (k - 52) * s, v, 5 * s, a)
    c.restore()
def hero(c, t): leaf(c, 540, 890, 1.3, mixcol(GRN, ORG, ss(1.2, 3.6, t)), 8 * math.sin(t * 1.5))
_r = np.random.default_rng(12)
DOTS = [(float(_r.uniform(-85, 85)), float(_r.uniform(-130, 130))) for _ in range(12)]
def i1(c, t, d):
    sun(c, 210, 600, 62, t)
    for k in range(3):
        u = (t * 0.6 + k / 3) % 1; x0 = lerp(290, 520, u); y0 = lerp(650, 760, u)
        arrow(c, x0, y0, x0 + 46, y0 + 22, GOLD, 8, ss(0, 0.15, u) * (1 - ss(0.8, 1, u)), 18)
    leaf(c, 640, 840, 1.35, GRN)
    for (dx, dy) in DOTS[:9]: circ(c, 640 + dx, 840 + dy, 13, "#1f6b2a")
    a = ss(1.4, 1.9, t); line(c, 850, 640, 720, 760, "#b9f0bd", 4, 0.8 * a); tag(c, "klorofil", 880, 625, "#b9f0bd", a, 38, "c", "Bold")
def i2(c, t, d):
    k = ss(2.0, 3.4, t)
    leaf(c, 540, 770, 1.35, YLW); leaf(c, 540, 770, 1.35, GRN, 0, 1 - 0.55 * k)
    for i, (dx, dy) in enumerate(DOTS): circ(c, 540 + dx * 1.2, 770 + dy * 1.2, 15, YLW if i % 2 else ORG, k)
    a = ss(3.0, 3.5, t)
    circ(c, 330, 1160, 15, YLW, a); tag(c, "sarı", 358, 1173, YLW, a, 36, "l", "Bold"); circ(c, 580, 1160, 15, ORG, a); tag(c, "turuncu", 608, 1173, ORG, a, 36, "l", "Bold")
def i3(c, t, d):
    k = ss(1.0, d - 1.4, t)
    sun(c, 830, lerp(560, 690, k), lerp(64, 44, k), t, 1 - 0.35 * k)
    leaf(c, 480, 760, 1.3, mixcol(GRN, YLW, k))
    tag(c, "gün uzunluğu", 200, 1105, None, 0.85, 30, "l")
    rrect(c, 200, 1125, 680, 22, 11, "#ffffff", 0.2); rrect(c, 200, 1125, 680 * (1 - 0.55 * k), 22, 11, GOLD)
def i4(c, t, d):
    for (x, y, s_, cl, rot, t0) in ((260, 810, 0.85, YLW, -16, 0.7), (540, 790, 0.98, ORG, 0, 1.9), (820, 810, 0.85, RDL, 16, max(3.6, d - 2.8))):
        k = pop(t, t0, 0.5)
        if k > 0: leaf(c, x, y + 6 * math.sin(t * 2 + x), s_ * k, cl, rot + 4 * math.sin(t * 1.6 + x))
    for (x, lbl, cl, t0) in ((260, "sarı", YLW, 0.9), (540, "turuncu", ORG, 2.1), (820, "kırmızı", RDL, max(3.8, d - 2.6))):
        tag(c, lbl, x, 1100, cl, ss(t0, t0 + 0.5, t), 38, "c", "Bold")
SCENES = [
 title_scene("Yapraklar neden", "sararır?", "Sonbahar renklerinin sırrı", hero),
 reason_scene("NEDEN 1", "Yeşilin adı klorofil", ["Yaprağı yeşil yapan klorofildir;", "güneş ışığını besine çevirir."], i1),
 reason_scene("NEDEN 2", "Sarı zaten oradadır", ["Yaprakta sarı ve turuncu pigmentler", "de vardır; yeşil onları gizler."], i2),
 reason_scene("NEDEN 3", "Klorofil üretimi durur", ["Günler kısalıp hava soğuyunca", "yeşil yavaş yavaş kaybolur."], i3),
 reason_scene("NEDEN 4", "Saklı renkler ortaya çıkar", ["Sarı ve turuncu görünür olur;", "bazı ağaçlar kırmızı pigment üretir."], i4),
 cards_scene("VE SONRA", "Yaprak neden dökülür?", [("Ağaç sapı kapatır", "Yaprağa su gitmez olur"), ("Yaprak kurur ve düşer", "Rüzgâr gerisini halleder"), ("Ağaç suyunu korur", "Kışı böyle atlatır")]),
 end_scene("Yapraklar boyanmıyor;", "yeşil perde kalkıyor.", hero),
]
if __name__ == "__main__":
    nb.main(SLUG, NARRATION, SCENES)
