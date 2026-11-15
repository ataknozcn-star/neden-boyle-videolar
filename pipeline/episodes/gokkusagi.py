import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import numpy as np, skia
from nb import *
import nb

SLUG = "gokkusagi-nasil-olusur"
nb.THEME.update(bg=["#2b5876", "#1b3a52", "#0e1f2e"], accent="#ffd166")
NARRATION = [
 "Gökkuşağı nasıl oluşur? İşte ışıkla yağmurun oyunu.",
 "Güneş ışığı beyaz görünür, ama aslında bütün renklerin karışımıdır.",
 "Işık bir yağmur damlasına girerken kırılır. Her renk farklı miktarda büküldüğü için renkler birbirinden ayrılır.",
 "Işık damlanın arka yüzeyinden yansır ve çıkarken bir kez daha kırılır. Kırmızı yaklaşık kırk iki, mor ise kırk derecelik açıyla çıkar.",
 "Bu yüzden gökkuşağını, güneş arkamızda, yağmur önümüzdeyken görürüz.",
 "Üç bilgi daha. Kırmızı hep dışta, mor içtedir. Gökkuşağı aslında tam bir çemberdir. Uçaktan bakınca bütünü görülebilir.",
 "Gökkuşağı boya değil; ışığın oyunu. Neden böyle? Artık biliyorsunuz.",
]
RAIN = ["#ff5d5d", "#ff9a3c", "#ffe066", "#6fd08c", "#6ec6f0", "#5b7bff", "#b07cff"]

def bow(c, cx, cy, r_out, band, p=1.0, a=1.0):
    """Kırmızı dışta, mor içte yedi bantlı yay (üst yarım çember); p: soldan sağa çizilme oranı."""
    if p <= 0: return
    for k, cl in enumerate(RAIN):
        r = r_out - k * band
        c.drawArc(skia.Rect.MakeLTRB(cx - r, cy - r, cx + r, cy + r), 180, 180 * p, False, stroke(cl, band + 1, a, cap=False))

def hero(c, t):
    bow(c, 540, 1040, 350, 22, ss(0.4, 1.6, t))
    cloud(c, 215 + 8 * math.sin(t), 1030, 1.0, 0.97); cloud(c, 850 - 8 * math.sin(t * 0.8), 1030, 1.0, 0.97)

def i1(c, t, d):
    sun(c, 540, 640, 80, t)
    p = ss(0.6, 1.5, t); line(c, 540, 780, 540, 780 + 110 * p, "#ffffff", 16)
    tag(c, "beyaz ışık", 590, 850, "#ffffff", ss(1.0, 1.5, t), 36, "l")
    for k, cl in enumerate(RAIN):
        q = pop(t, 2.2 + k * 0.22, 0.4); x = 150 + k * 130
        if q > 0:
            line(c, 540, 895, x, 1000, cl, 6, 0.55 * min(q, 1)); circ(c, x, 1040, 44 * q, cl)
    tag(c, "bütün renkler bir arada", 540, 1150, THEME["accent"], ss(3.9, 4.4, t), 40, "c", "Bold")

CX, CY, R = 560, 800, 235
def on(deg): return (CX + R * math.cos(math.radians(deg)), CY + R * math.sin(math.radians(deg)))
P_IN = on(212)
BACK = [on(4 + k * 3.5) for k in range(7)]       # kırmızı üstte, mor altta (mor daha çok bükülür)
EXIT = [on(104 + k * 4) for k in range(7)]       # yansıyan ışınlar kesişir: kırmızı altta çıkar
OUTA = [math.radians(120 + k * 5) for k in range(7)]  # kırmızı daha dik çıkar (şematik)

def big_drop(c):
    circ(c, CX, CY, R, "#8fd3ff", 0.22); circ(c, CX, CY, R, "#cfeaff", 0.9, sw=6)
    c.drawArc(skia.Rect.MakeLTRB(CX - R + 34, CY - R + 34, CX + R - 34, CY + R - 34), 200, 50, False, stroke("#ffffff", 10, 0.5))

def seg(c, a_, b_, p, cl, w=8):
    if p > 0: line(c, a_[0], a_[1], lerp(a_[0], b_[0], p), lerp(a_[1], b_[1], p), cl, w)

def enter(c, t, t0=0.6):
    seg(c, (70, P_IN[1]), P_IN, ss(t0, t0 + 1.0, t), "#ffffff", 14)
    for k, cl in enumerate(RAIN): seg(c, P_IN, BACK[k], ss(t0 + 1.0, t0 + 2.2, t), cl)

def i2(c, t, d):
    big_drop(c); enter(c, t, 1.2)
    tag(c, "güneş ışığı", 80, P_IN[1] - 34, "#ffffff", ss(1.2, 1.7, t), 34, "l")
    tag(c, "yağmur damlası", CX, CY - R - 28, "#cfeaff", ss(0.6, 1.1, t), 36, "c")
    tag(c, "renkler ayrılır", CX, CY + R + 70, THEME["accent"], ss(4.6, 5.1, t), 40, "c", "Bold")

def i3(c, t, d):
    c.save(); c.translate(0, -70); big_drop(c); enter(c, t, -5)
    for k, cl in enumerate(RAIN):
        seg(c, BACK[k], EXIT[k], ss(0.7, 1.9, t), cl)
        e = EXIT[k]; L = 170
        seg(c, e, (e[0] + L * math.cos(OUTA[k]), e[1] + L * math.sin(OUTA[k])), ss(3.0, 4.2, t), cl)
    circ(c, CX + R + 4, CY + 50, 22 * pop(t, 1.0), "#ffffff", 0.9, sw=6)
    c.restore()
    tag(c, "yansıma", CX + R + 36, CY - 8, "#ffffff", ss(1.2, 1.7, t), 34, "l")
    tag(c, "kırmızı ≈ 42°", 450, 1150, "#ff9a9a", ss(5.4, 5.9, t), 38, "l", "Bold")
    tag(c, "mor ≈ 40°", 90, 1075, "#c9a6ff", ss(7.0, 7.5, t), 38, "l", "Bold")

_r = np.random.default_rng(7)
DROPS = [(float(_r.uniform(480, 990)), float(_r.uniform(0, 1))) for _ in range(34)]
def i4(c, t, d):
    cloud(c, 760, 610, 1.2, 0.85, "#c5d3df")
    for (x, ph) in DROPS:
        u = (t * 0.9 + ph) % 1; y = 690 + u * 380
        line(c, x, y, x - 6, y + 26, "#9fd4ff", 5, 0.55 * (1 - ss(0.85, 1, u)))
    bow(c, 730, 1085, 265, 16, ss(1.6, 3.0, t), 0.95)
    rrect(c, 60, 1085, 960, 70, 20, "#2e7d4f")
    sun(c, 170, 610, 56, t)
    for k in range(3):
        u = (t * 0.5 + k / 3) % 1
        arrow(c, lerp(280, 430, u), lerp(630, 730, u), lerp(280, 430, u) + 50, lerp(630, 730, u) + 33, GOLD, 7, ss(0, 0.2, u) * (1 - ss(0.75, 1, u)), 18)
    circ(c, 300, 965, 38, "#ffd7b0"); rrect(c, 264, 1004, 72, 86, 28, THEME["accent"]); circ(c, 318, 960, 6, "#3a2a20")
    tag(c, "güneş arkada", 80, 760, GOLD, ss(2.6, 3.1, t), 32, "l", "Bold")
    tag(c, "yağmur önde", 760, 482, "#cfeaff", ss(3.6, 4.1, t), 32, "c", "Bold")

SCENES = [
 title_scene("Gökkuşağı", "nasıl oluşur?", "Işıkla yağmurun oyunu", hero),
 reason_scene("ADIM 1", "Beyaz ışıkta her renk", ["Güneş ışığı beyaz görünür;", "aslında bütün renklerin karışımıdır."], i1),
 reason_scene("ADIM 2", "Damla ışığı kırar", ["Işık damlaya girerken bükülür;", "her renk farklı büküldüğü için ayrılır."], i2),
 reason_scene("ADIM 3", "Yansır ve geri çıkar", ["Arka yüzeyden yansır, çıkarken", "yeniden kırılır: her renge ayrı açı."], i3),
 reason_scene("ADIM 4", "Güneş arkada olmalı", ["Gökkuşağını güneş arkamızda,", "yağmur önümüzdeyken görürüz."], i4),
 cards_scene("ÜÇ BİLGİ", "Bunları biliyor muydunuz?", [("Kırmızı dışta, mor içte", "Renklerin sırası hep aynıdır"), ("Aslında tam bir çember", "Biz çoğu zaman yayını görürüz"), ("Uçaktan bütünü görülebilir", "Yukarıdan bakınca çember tamamlanır")]),
 end_scene("Gökkuşağı boya değil;", "ışığın oyunu.", hero),
]
if __name__ == "__main__":
    nb.main(SLUG, NARRATION, SCENES)
