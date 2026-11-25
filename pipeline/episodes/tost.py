import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import numpy as np, skia
from nb import *
import nb

SLUG = "ekmek-neden-kizarir"
nb.THEME.update(bg=["#7a4520", "#4a2812", "#26140a"], accent="#ffb35c")
NARRATION = [
 "Kızarmış ekmek neden kahverengi olur? Cevap, küçük bir mutfak kimyasında.",
 "Ekmeğin içinde iki önemli malzeme var: şekerler ve proteinlerin yapı taşları olan amino asitler.",
 "Isı önce ekmeğin yüzeyindeki suyu buharlaştırır. Yüzey kurur ve kıtırlaşır.",
 "Kuru yüzey yaklaşık yüz kırk dereceye ulaşınca, şekerler ile amino asitler tepkimeye girer. Buna Mayyar tepkimesi denir.",
 "Bu tepkime yüzlerce yeni koku ve tat molekülü üretir. Kahverengi rengi ise melanoidin denen pigmentler verir.",
 "Peki ekmek neden yanar? Isı çok artarsa şekerler ve nişasta parçalanır, yüzey kömürleşip kararır.",
 "Kahverengi renk, aslında lezzetin işareti. Neden böyle? Artık biliyorsunuz.",
]
PALE, GOLDEN, BROWN, DARK, BURNT = "#f3dcae", "#e7b45f", "#b8702e", "#7a431a", "#2a1a12"

def slice_path(x, y, s):
    p = skia.Path(); w = 150 * s; h = 160 * s
    p.moveTo(x - w * 0.82, y + h); p.lineTo(x - w * 0.82, y - h * 0.35)
    p.cubicTo(x - w * 1.25, y - h * 0.55, x - w * 1.1, y - h * 1.25, x - w * 0.45, y - h * 1.05)
    p.cubicTo(x - w * 0.2, y - h * 1.3, x + w * 0.2, y - h * 1.3, x + w * 0.45, y - h * 1.05)
    p.cubicTo(x + w * 1.1, y - h * 1.25, x + w * 1.25, y - h * 0.55, x + w * 0.82, y - h * 0.35)
    p.lineTo(x + w * 0.82, y + h); p.close(); return p
def toast(c, x, y, s, inner, crust="#8a4a1c", a=1.0):
    c.drawPath(slice_path(x, y, s * 1.08), fill(crust, a))
    c.drawPath(slice_path(x, y + 4 * s, s * 0.92), fill(inner, a))
    for k, (dx, dy) in enumerate(((-50, -40), (35, -70), (60, 40), (-30, 70), (5, 5), (-70, 20))):
        circ(c, x + dx * s, y + dy * s, 7 * s, mixcol(inner, "#000000", 0.18), a)
def toaster(c, x, y, s=1.0):
    rrect(c, x - 210 * s, y - 120 * s, 420 * s, 260 * s, 70 * s, "#d9dde3")
    rrect(c, x - 210 * s, y + 60 * s, 420 * s, 80 * s, 40 * s, "#aeb5bf")
    for dx in (-80, 80): rrect(c, x + (dx - 55) * s, y - 128 * s, 110 * s, 26 * s, 13 * s, "#4b525c")
    rrect(c, x + 205 * s, y - 40 * s, 40 * s, 22 * s, 10 * s, "#4b525c")
    for k in range(3): line(c, x - 150 * s + k * 26 * s, y + 10 * s, x - 150 * s + k * 26 * s, y + 40 * s, "#aeb5bf", 8 * s)

def hero(c, t):
    up = eout(ss(0.9, 1.5, t)) * 190
    for dx in (-100, 100):
        c.save(); c.clipRect(skia.Rect.MakeLTRB(0, 0, W, 940 - 150)); toast(c, 540 + dx, 900 - up, 0.68, BROWN, DARK); c.restore()
    toaster(c, 540, 940, 1.25)
    for k in range(4):
        u = (t * 0.5 + k * 0.25) % 1; xx = 450 + k * 60 + 20 * math.sin(u * 6 + k)
        circ(c, xx, 530 - u * 60, 14 + u * 14, "#ffffff", 0.25 * (1 - u) * ss(1.3, 1.8, t))

def hexagon(c, x, y, r, color, a=1.0, sw=0):
    pts = [(x + r * math.cos(k * math.pi / 3 + math.pi / 6), y + r * math.sin(k * math.pi / 3 + math.pi / 6)) for k in range(6)]
    poly(c, pts, color, a, sw)
def amino(c, x, y, s, color, a=1.0):
    for k in range(3):
        line(c, x + (k - 1) * 46 * s, y, x + k * 46 * s, y, color, 8 * s, a) if k < 2 else None
        circ(c, x + (k - 1) * 46 * s, y + (8 if k == 1 else 0) * s, 20 * s, color, a)
def i1(c, t, d):
    toast(c, 540, 860, 1.15, PALE, "#c98f4a")
    a1 = ss(1.2, 1.8, t); a2 = ss(3.0, 3.6, t)
    for k, (x, y) in enumerate(((400, 760), (470, 930), (360, 1010))):
        hexagon(c, x, y, 34 * pop(t, 1.2 + k * 0.15), "#ffffff", 0.95 * a1)
    for k, (x, y) in enumerate(((680, 760), (640, 960), (730, 1040))):
        amino(c, x, y, 1.0 * pop(t, 3.0 + k * 0.15), "#ff8a5c", a2)
    tag(c, "şeker", 300, 620, "#ffffff", a1, 44, "c", "Bold")
    tag(c, "amino asit", 760, 620, "#ffb39a", a2, 44, "c", "Bold")
def i2(c, t, d):
    k = ss(0.8, 3.6, t)
    toast(c, 540, 900, 1.15, mixcol(PALE, "#efcf92", k), mixcol("#c98f4a", "#b9772f", k))
    for j in range(9):
        u = (t * 0.55 + j * 0.111) % 1; x = 360 + (j % 5) * 90 + 25 * math.sin(u * 7 + j)
        circ(c, x, 700 - u * 210, 14 + 22 * u, "#ffffff", 0.45 * (1 - u) * ss(0.6, 1.2, t))
    for j in range(5): drop(c, 420 + j * 60, 840 + (j % 2) * 70, 14, 0.8 * (1 - k), BLUE)
    tag(c, "su buharlaşır", 540, 520, "#ffffff", ss(1.0, 1.5, t), 42, "c", "Bold")
    tag(c, "yüzey kurur, kıtırlaşır", 540, 1140, THEME["accent"], ss(3.0, 3.5, t), 38, "c", "Bold")
def i3(c, t, d):
    # termometre
    rrect(c, 130, 560, 56, 470, 28, "#ffffff", 0.9); circ(c, 158, 1050, 52, "#ffffff", 0.9)
    lv = ss(0.8, 3.2, t); circ(c, 158, 1050, 40, RED); rrect(c, 144, 1010 - 420 * lv, 28, 430 * lv, 14, RED)
    tag(c, "~140 °C", 158, 525, "#ffffff", ss(2.8, 3.3, t), 40, "c", "Bold")
    m = eout(ss(3.6, 5.2, t))
    hx = lerp(380, 520, m); ax = lerp(800, 610, m)
    hexagon(c, hx, 790, 50, "#ffffff"); amino(c, ax, 790, 1.15, "#ff8a5c")
    if t > 5.2:
        q = pop(t, 5.2, 0.5)
        for k in range(10):
            ang = k * math.pi / 5; r = 80 + 30 * q
            line(c, 565 + math.cos(ang) * r * 0.7, 790 + math.sin(ang) * r * 0.7, 565 + math.cos(ang) * r, 790 + math.sin(ang) * r, GOLD, 8, ss(5.2, 5.6, t))
    tag(c, "şeker + amino asit", 600, 640, "#ffffff", ss(3.6, 4.1, t), 36, "c")
    rrect(c, 320, 960, 560, 110, 55, THEME["accent"], 0.95 * ss(5.6, 6.2, t))
    tag(c, "Maillard tepkimesi", 600, 1030, "#3b2010", ss(5.6, 6.2, t), 44, "c", "Bold")
def i4(c, t, d):
    k = ss(3.2, 5.6, t)
    toast(c, 540, 930, 1.05, mixcol("#efcf92", BROWN, k), mixcol("#b9772f", DARK, k))
    for j in range(8):
        u = (t * 0.4 + j * 0.125) % 1; x = 300 + j * 68
        p = skia.Path(); p.moveTo(x, 700)
        for s_ in range(1, 9): p.lineTo(x + 22 * math.sin(s_ * 0.9 + t * 3 + j), 700 - s_ * 22)
        c.save(); c.translate(0, -u * 60); c.drawPath(p, stroke(GOLD, 6, 0.6 * (1 - u) * ss(0.6, 1.2, t))); c.restore()
        circ(c, x + 10, 560 - u * 80, 9, "#ffd7a0", 0.8 * (1 - u) * ss(0.6, 1.2, t))
    tag(c, "yüzlerce koku ve tat molekülü", 540, 500, "#ffffff", ss(1.0, 1.5, t), 38, "c", "Bold")
    tag(c, "melanoidin: kahverengi pigment", 540, 1150, THEME["accent"], ss(4.0, 4.5, t), 38, "c", "Bold")

SCENES = [
 title_scene("Kızarmış ekmek", "neden kahverengi?", "Küçük bir mutfak kimyası", hero),
 reason_scene("ADIM 1", "İki gizli malzeme", ["Ekmekte şekerler ve proteinlerin", "yapı taşı amino asitler bulunur."], i1),
 reason_scene("ADIM 2", "Önce su gider", ["Isı yüzeydeki suyu buharlaştırır;", "yüzey kurur ve kıtırlaşır."], i2),
 reason_scene("ADIM 3", "Maillard tepkimesi", ["Yaklaşık 140 °C'de şekerler ile", "amino asitler tepkimeye girer."], i3),
 reason_scene("ADIM 4", "Koku ve renk doğar", ["Yüzlerce yeni koku ve tat oluşur;", "rengi melanoidin pigmentleri verir."], i4),
 cards_scene("BONUS", "Ekmek neden yanar?", [("Kısa süre: altın sarısı", "Maillard yeni başlar"), ("Biraz daha: kahverengi", "Daha çok pigment ve koku"), ("Fazla ısı: simsiyah", "Şeker ve nişasta kömürleşir")]),
 end_scene("Kahverengi renk,", "lezzetin işareti.", hero),
]
if __name__ == "__main__":
    nb.main(SLUG, NARRATION, SCENES)
