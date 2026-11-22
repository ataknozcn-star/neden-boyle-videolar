import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import numpy as np, skia
from nb import *
import nb

SLUG = "dagda-su-neden-erken-kaynar"
nb.THEME.update(bg=["#2c4566", "#1b2c45", "#0e1828"], accent="#ffb36b")
NARRATION = [
 "Yüksek dağda su neden daha erken kaynar? Cevap, başımızın üstündeki havada.",
 "Su ısındıkça molekülleri hızlanır. Bazıları yüzeyden kaçıp buhara dönüşür.",
 "Ama üstümüzdeki hava, suyun yüzeyine sürekli bastırır. Buna hava basıncı denir.",
 "Suyun içindeki buharın itişi, hava basıncını yendiğinde kabarcıklar oluşur ve su kaynar. Deniz kıyısında bu, yüz derecede olur.",
 "Yukarı çıktıkça hava incelir, basınç düşer. Dünyanın en yüksek dağının tepesinde su, yaklaşık yetmiş derecede kaynar.",
 "Peki sonuç ne? Dağda kaynayan su daha az sıcaktır, yemek geç pişer. Düdüklü tencere ise tersini yapar: basıncı artırır, su yüz yirmi derece civarında kaynar.",
 "Kaynamak yalnızca ısı değil, basınç meselesi. Neden böyle? Artık biliyorsunuz.",
]
WATER = "#4fa3e0"
SNOW = "#eef6ff"

def pot(c, x, y, s, t, boil=1.0, fire=True, a=1.0):
    """Tencere: (x, y) su yüzeyinin ortası."""
    if fire: flames(c, x, y + 150 * s, 4, t, a, gap=38 * s)
    rrect(c, x - 125 * s, y - 20 * s, 250 * s, 160 * s, 26 * s, "#9aa7b8", a)
    rrect(c, x - 112 * s, y - 6 * s, 224 * s, 134 * s, 20 * s, WATER, a)
    rrect(c, x - 160 * s, y - 8 * s, 40 * s, 16 * s, 8 * s, "#7c8899", a)
    rrect(c, x + 120 * s, y - 8 * s, 40 * s, 16 * s, 8 * s, "#7c8899", a)
    rrect(c, x - 140 * s, y - 34 * s, 280 * s, 18 * s, 9 * s, "#b9c4d3", a)
    if boil > 0:
        for k in range(7):
            u = (t * 0.9 + k * 0.143) % 1
            bx = x + (k - 3) * 28 * s + 6 * s * math.sin(t * 5 + k)
            circ(c, bx, y + 115 * s - 110 * s * u, (5 + 7 * u) * s, "#ffffff", 0.75 * a * boil * (1 - u * 0.4))
        for k in range(3):
            u = (t * 0.5 + k * 0.33) % 1
            puff(c, x + (k - 1) * 60 * s, y - 60 * s - 130 * s * u, (22 + 26 * u) * s, 0.55 * a * boil * (1 - u))

def mountain(c, cx, base, w, h, a=1.0):
    poly(c, [(cx - w / 2, base), (cx, base - h), (cx + w / 2, base)], "#53657f", a)
    poly(c, [(cx, base - h), (cx + w / 2, base), (cx + w * 0.12, base)], "#3f4f66", a)
    k = 0.26
    pts = [(cx - w / 2 * k, base - h * (1 - k)), (cx, base - h), (cx + w / 2 * k, base - h * (1 - k)),
           (cx + w * 0.06, base - h * (1 - k) + 26), (cx - w * 0.02, base - h * (1 - k) + 6), (cx - w * 0.08, base - h * (1 - k) + 30)]
    poly(c, pts, SNOW, a)

def thermo(c, x, y, frac, color, a=1.0, h=300):
    rrect(c, x - 22, y - h, 44, h, 22, "#ffffff", 0.25 * a)
    rrect(c, x - 22, y - h, 44, h, 22, "#ffffff", 0.7 * a, sw=4)
    hh = (h - 30) * clamp(frac); rrect(c, x - 11, y - 12 - hh, 22, hh + 14, 11, color, a)
    circ(c, x, y + 18, 36, color, a); circ(c, x, y + 18, 36, "#ffffff", 0.7 * a, sw=4)

def hero(c, t):
    mountain(c, 640, 1110, 760, 470)
    pot(c, 640, 690, 0.38, t, fire=True)
    tag(c, "~70 °C", 640, 590, THEME["accent"], 1, 44, "c", "Bold")
    pot(c, 230, 1000, 0.42, t, fire=True)
    tag(c, "100 °C", 230, 900, "#ffffff", 1, 44, "c", "Bold")
    rrect(c, 60, 1108, 960, 16, 8, "#2f6fa8")

_r = np.random.default_rng(5)
MOLS = [(float(_r.uniform(-1, 1)), float(_r.uniform(-1, 1)), float(_r.uniform(0, 6.28))) for _ in range(18)]
def i1(c, t, d):
    heat = ss(0.5, 3.0, t)
    flames(c, 540, 1075, 7, t, heat, gap=60)
    rrect(c, 250, 700, 580, 340, 40, "#9aa7b8")
    rrect(c, 270, 720, 540, 300, 30, WATER)
    sp = 0.6 + 4.5 * heat
    for (u, v, ph) in MOLS:
        x = 540 + u * 230 + 30 * math.sin(t * sp + ph); y = 870 + v * 110 + 30 * math.cos(t * sp * 1.3 + ph)
        circ(c, x, y, 16, "#ffffff", 0.85)
        line(c, x, y, x - 22 * math.sin(t * sp + ph + 1), y - 22 * math.cos(t * sp + ph + 1), "#ffffff", 5, 0.3 * heat)
    if t > 2.6:
        for k in range(5):
            u = ((t - 2.6) * 0.55 + k * 0.2) % 1
            x = 330 + k * 105 + 20 * math.sin(t * 3 + k); y = 710 - 200 * u
            circ(c, x, y, 14, "#ffffff", 0.9 * (1 - u))
            puff(c, x, y - 10, 24 * u + 6, 0.35 * (1 - u))
    tag(c, "ısındıkça hızlanır", 540, 1170, THEME["accent"], ss(1.2, 1.7, t), 38, "c", "Bold")
    tag(c, "buhar olur", 540, 500, "#ffffff", ss(3.0, 3.5, t), 40, "c", "Bold")

_r2 = np.random.default_rng(9)
AIR = [(float(_r2.uniform(110, 970)), float(_r2.uniform(500, 820))) for _ in range(34)]
def i2(c, t, d):
    for (x, y) in AIR:
        circ(c, x, y + 8 * math.sin(t * 2 + x), 10, "#c9dcf2", 0.55)
    rrect(c, 100, 930, 880, 220, 30, WATER)
    rrect(c, 100, 930, 880, 18, 9, "#9fd1f5")
    p = ss(1.6, 2.6, t)
    for k in range(6):
        x = 170 + k * 148; push = 18 * (0.5 + 0.5 * math.sin(t * 4 + k))
        arrow(c, x, 690 + push, x, 690 + push + 190 * p, THEME["accent"], 12, p, 30)
    tag(c, "hava", 540, 470 + 20, "#ffffff", ss(0.8, 1.3, t), 40, "c", "Bold")
    tag(c, "su", 540, 1060, "#ffffff", ss(3.2, 3.7, t), 48, "c", "Bold")

def i3(c, t, d):
    rrect(c, 90, 760, 640, 390, 36, WATER)
    rrect(c, 90, 760, 640, 18, 9, "#9fd1f5")
    for k in range(5):
        x = 150 + k * 130
        arrow(c, x, 560, x, 735, "#c9dcf2", 10, ss(0.5, 1.2, t), 26)
    tag(c, "hava basıncı", 410, 525, "#c9dcf2", ss(0.6, 1.1, t), 36, "c", "Bold")
    g = ss(1.2, 4.6, t)
    r = 30 + 55 * g; bx, by = 410, 990 - 120 * ss(4.6, 6.0, t)
    circ(c, bx, by, r, "#ffffff", 0.25); circ(c, bx, by, r, "#ffffff", 0.9, sw=5)
    for k in range(8):
        ang = k * math.pi / 4
        arrow(c, bx + math.cos(ang) * (r - 26), by + math.sin(ang) * (r - 26), bx + math.cos(ang) * (r + 22), by + math.sin(ang) * (r + 22), THEME["accent"], 7, ss(1.4, 2.0, t), 14)
    tag(c, "buharın itişi", 410, 1115, THEME["accent"], ss(1.8, 2.3, t), 36, "c", "Bold")
    thermo(c, 880, 1080, 0.25 + 0.7 * ss(1.0, 6.0, t), "#ff6b5b", 1, 400)
    tag(c, "100 °C", 880, 600, "#ffffff", ss(5.6, 6.2, t), 46, "c", "Bold")

def i4(c, t, d):
    mountain(c, 560, 1160, 820, 600)
    rrect(c, 60, 1160, 960, 14, 7, "#2f6fa8")
    _r3 = np.random.default_rng(3)
    for k in range(90):
        x = float(_r3.uniform(70, 1010)); yy = float(_r3.uniform(0, 1)) ** 2.2
        y = 1150 - (1 - yy) * 640
        circ(c, x + 6 * math.sin(t * 1.5 + k), y, 7, "#c9dcf2", 0.5 * ss(0.3, 1.2, t))
    pop1 = pop(t, 1.0); pop2 = pop(t, 5.6)
    if pop1 > 0:
        rrect(c, 70, 1060, 270 * pop1, 74, 22, "#0e1828", 0.8); tag(c, "deniz: 100 °C", 205, 1110, "#ffffff", pop1, 38, "c", "Bold")
    if pop2 > 0:
        rrect(c, 680, 520, 330, 80, 22, "#0e1828", 0.85 * pop2); tag(c, "zirve: ~70 °C", 845, 574, THEME["accent"], pop2, 40, "c", "Bold")
    arrow(c, 980, 1080, 980, 720, "#ffffff", 8, ss(2.0, 2.8, t), 26)
    tag(c, "basınç düşer", 960, 690, "#ffffff", ss(2.6, 3.1, t), 32, "r", "Medium")

SCENES = [
 title_scene("Dağda su", "neden erken kaynar?", "Cevap havada saklı", hero),
 reason_scene("NEDEN 1", "Moleküller hızlanır", ["Su ısındıkça molekülleri hızlanır;", "bazıları kaçıp buhara dönüşür."], i1),
 reason_scene("NEDEN 2", "Hava suya bastırır", ["Üstümüzdeki hava suyun yüzeyine", "sürekli bastırır: hava basıncı."], i2),
 reason_scene("NEDEN 3", "Buhar havayı yenince", ["Buharın itişi hava basıncını yenince", "kabarcıklar oluşur; su kaynar."], i3),
 reason_scene("NEDEN 4", "Yukarıda hava incedir", ["Basınç düşer; en yüksek zirvede su", "yaklaşık yetmiş derecede kaynar."], i4),
 cards_scene("SONUÇ", "Hepsi basınçla ilgili", [("Dağda yemek geç pişer", "Kaynayan su daha az sıcaktır"), ("Düdüklü tencere tersi", "Basıncı artırır"), ("Su ~120 °C'de kaynar", "Yemek çok daha hızlı pişer")]),
 end_scene("Kaynamak yalnızca ısı değil;", "basınç meselesi.", hero),
]
if __name__ == "__main__":
    nb.main(SLUG, NARRATION, SCENES)
