import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import numpy as np, skia
from nb import *
import nb

SLUG = "ay-neden-sekil-degistirir"
nb.THEME.update(bg=["#1c2350", "#111634", "#080b1e"], accent="#ffe9a8")
NARRATION = [
 "Ay neden şekil değiştirir? Bir gece ince bir hilal, bir gece kocaman bir dolunay.",
 "Ay kendi ışığını üretmez. Gördüğümüz ay ışığı, aslında Güneş'ten yansıyan ışıktır.",
 "Güneş, Ay'ın her zaman yarısını aydınlatır. Öbür yarısı ise karanlıkta kalır.",
 "Ay, Dünya'nın çevresinde dolanır. Bu sırada Güneş, Ay ve Dünya arasındaki açı sürekli değişir.",
 "Açı değiştikçe, aydınlık yarının ne kadarını gördüğümüz de değişir. Hilal, yarım ay, dolunay. Döngü yaklaşık yirmi dokuz buçuk günde tamamlanır.",
 "Peki bu, Dünya'nın gölgesi mi? Hayır. Dünya'nın gölgesi Ay'a çok nadir düşer; o zaman ay tutulması olur. Evreler, yalnızca bakış açımızdan doğar.",
 "Ay küçülmüyor; biz onu farklı açılardan görüyoruz. Neden böyle? Artık biliyorsunuz.",
]
MOON, DARK = "#fff1c4", "#2a3160"

def moon(c, x, y, r, p, a=1.0, glow=True):
    """p: evre (0 yeni ay, 0.25 ilk dördün, 0.5 dolunay, 0.75 son dördün). Kuzey yarımküreden görünüş."""
    p %= 1.0
    circ(c, x, y, r, DARK, a)
    k = math.cos(2 * math.pi * p); side = 1 if p < 0.5 else -1
    lit = 1 - abs(p - 0.5) * 2  # 0 yeni, 1 dolunay
    if glow and lit > 0.05: circ(c, x, y, r * 1.18, MOON, 0.10 * a * lit)
    if lit > 0.005:
        path = skia.Path(); n = 48
        for i in range(n + 1):  # dış kenar: üstten alta, aydınlık taraftan
            ang = -math.pi / 2 + math.pi * i / n
            px, py = x + side * r * math.cos(ang), y + r * math.sin(ang)
            path.moveTo(px, py) if i == 0 else path.lineTo(px, py)
        for i in range(n + 1):  # sınır çizgisi (elips): alttan üste
            ang = math.pi / 2 - math.pi * i / n
            path.lineTo(x + side * k * r * math.cos(ang), y + r * math.sin(ang))
        path.close(); c.drawPath(path, fill(MOON, a))
    circ(c, x, y, r, "#ffffff", 0.25 * a, sw=3)

_r = np.random.default_rng(11)
STARS = [(float(_r.uniform(70, 1010)), float(_r.uniform(560, 1200)), float(_r.uniform(2.5, 5.5)), float(_r.uniform(0, 6))) for _ in range(40)]
def stars(c, t, a=1.0, ymin=0, ymax=2000):
    for (x, y, r, ph) in STARS:
        if ymin <= y <= ymax: circ(c, x, y, r, "#ffffff", a * (0.45 + 0.35 * math.sin(t * 2 + ph)))

def hero(c, t):
    stars(c, t)
    moon(c, 540, 880, 230, 0.06 + t * 0.09)

def i1(c, t, d):
    stars(c, t, 0.6)
    sun(c, 170, 640, 80, t)
    moon(c, 780, 640, 95, 0.5)
    circ(c, 300, 1050, 85, "#3f7fd0"); circ(c, 280, 1030, 30, GREEN, 0.9); circ(c, 330, 1075, 22, GREEN, 0.9)
    for k in range(3):
        u = ss(0.8 + k * 0.25, 1.8 + k * 0.25, t)
        y0 = 610 + k * 30
        if u > 0: arrow(c, 270, y0, lerp(270, 670, u), y0, GOLD, 9, 1, 20 if u > 0.95 else 0.01)
    for k in range(3):
        u = ss(2.4 + k * 0.25, 3.4 + k * 0.25, t)
        x0, y0 = 720 - k * 25, 720 + k * 20; x1, y1 = 400 - k * 25, 990 + k * 20
        if u > 0: arrow(c, x0, y0, lerp(x0, x1, u), lerp(y0, y1, u), MOON, 9, 1, 20 if u > 0.95 else 0.01)
    tag(c, "Güneş", 170, 815, GOLD, ss(0.4, 0.9, t), 38, "c", "Bold")
    tag(c, "Ay", 780, 815, MOON, ss(0.4, 0.9, t), 38, "c", "Bold")
    tag(c, "yansıyan ışık", 760, 960, THEME["accent"], ss(3.2, 3.7, t), 42, "c", "Bold")

def i2(c, t, d):
    stars(c, t, 0.5)
    sun(c, 150, 820, 70, t)
    for k in range(5):
        y = 640 + k * 90; u = ss(0.4 + k * 0.1, 1.4 + k * 0.1, t)
        if u > 0: line(c, 250, y, lerp(250, 430, u), y, GOLD, 8, 0.8)
    r = 230; x, y = 680, 820
    circ(c, x, y, r, DARK)
    w = ss(1.4, 2.2, t)
    path = skia.Path(); path.addArc(skia.Rect.MakeXYWH(x - r, y - r, 2 * r, 2 * r), 90, 180); path.close()
    c.drawPath(path, fill(MOON, w))
    circ(c, x, y, r, "#ffffff", 0.3, sw=3)
    line(c, x, y - r - 20, x, y + r + 20, "#ffffff", 4, 0.5 * w)
    tag(c, "aydınlık", 560, 830, "#5a4a20", ss(2.0, 2.5, t), 40, "c", "Bold")
    tag(c, "karanlık", 800, 830, "#c8d0ff", ss(3.4, 3.9, t), 40, "c", "Bold")
    tag(c, "her zaman yarısı", 680, 1115, THEME["accent"], ss(2.4, 2.9, t), 42, "c", "Bold")

def lit_half_moon(c, x, y, r, a=1.0):
    """Üstten görünüş: Güneş solda, Ay'ın sol yarısı aydınlık."""
    circ(c, x, y, r, DARK, a)
    path = skia.Path(); path.addArc(skia.Rect.MakeXYWH(x - r, y - r, 2 * r, 2 * r), 90, 180); path.close()
    c.drawPath(path, fill(MOON, a)); circ(c, x, y, r, "#ffffff", 0.3 * a, sw=2)

def i3(c, t, d):
    cx, cy, R = 600, 830, 250
    for k in range(6):
        y = 600 + k * 92; line(c, 70, y, 160, y, GOLD, 7, 0.7)
    tag(c, "Güneş ışığı", 120, 545, GOLD, ss(0.4, 0.9, t), 34, "c", "Bold")
    circ(c, cx, cy, R, "#ffffff", 0.25, sw=3)
    circ(c, cx, cy, 70, "#3f7fd0"); circ(c, cx - 20, cy - 18, 24, GREEN, 0.9); circ(c, cx + 25, cy + 22, 18, GREEN, 0.9)
    tag(c, "Dünya", cx, cy + 115, "#9cc6ff", ss(0.6, 1.1, t), 34, "c", "Bold")
    ang = math.pi + t * 0.55
    mx, my = cx + R * math.cos(ang), cy + R * math.sin(ang)
    lit_half_moon(c, mx, my, 48)
    for k in range(1, 8):
        a2 = ang - k * 0.12
        circ(c, cx + R * math.cos(a2), cy + R * math.sin(a2), 6, MOON, 0.5 * (1 - k / 8))
    q = ss(2.6, 3.2, t)
    tag(c, "açı sürekli değişir", 600, 1150, THEME["accent"], q, 42, "c", "Bold")

PH = [0.0, 0.125, 0.25, 0.375, 0.5, 0.625, 0.75, 0.875]
NAMES = ["yeni ay", "hilal", "ilk dördün", "şişkin", "dolunay", "şişkin", "son dördün", "hilal"]
def i4(c, t, d):
    for i, p in enumerate(PH):
        row, col_ = divmod(i, 4); x = 180 + col_ * 240; y = 610 + row * 270
        k = pop(t, 0.6 + i * 0.45)
        if k <= 0: continue
        moon(c, x, y, 78 * k, p, 1.0, glow=False)
        tag(c, NAMES[i], x, y + 130, THEME["text"], ss(0.8 + i * 0.45, 1.2 + i * 0.45, t), 30, "c", "Medium")
    arrow(c, 120, 1150, lerp(120, 960, ss(4.5, 6.0, t)), 1150, THEME["accent"], 6, ss(4.5, 4.8, t), 18)
    tag(c, "≈ 29,5 gün", 540, 1115, THEME["accent"], ss(6.0, 6.5, t), 38, "c", "Bold")

SCENES = [
 title_scene("Ay neden", "şekil değiştirir?", "Işık ve açı meselesi", hero),
 reason_scene("NEDEN 1", "Ay kendisi parlamaz", ["Ay ışık üretmez; gördüğümüz", "Güneş'ten yansıyan ışıktır."], i1),
 reason_scene("NEDEN 2", "Yarısı hep aydınlık", ["Güneş, Ay'ın hep yarısını aydınlatır;", "öbür yarısı karanlıkta kalır."], i2),
 reason_scene("NEDEN 3", "Ay, Dünya'yı dolanır", ["Ay dolandıkça Güneş, Ay ve Dünya", "arasındaki açı değişir."], i3),
 reason_scene("NEDEN 4", "Görünen kısım değişir", ["Aydınlık yarının ne kadarını", "gördüğümüz açıya bağlıdır."], i4),
 cards_scene("BONUS", "Dünya'nın gölgesi mi?", [("Hayır, gölge değil", "Gölge Ay'a çok nadir düşer"), ("Düşerse: ay tutulması", "Evrelerle karıştırılmamalı"), ("Evreler açıdan doğar", "Sadece bakış açımız değişir")]),
 end_scene("Ay küçülmüyor;", "sadece açı değişiyor.", hero),
]
if __name__ == "__main__":
    nb.main(SLUG, NARRATION, SCENES)
