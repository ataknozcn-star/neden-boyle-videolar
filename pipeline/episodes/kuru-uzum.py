import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import numpy as np, skia
from nb import *
import nb

SLUG = "kuru-uzum-neden-siser"
nb.THEME.update(bg=["#4a2a6b", "#2c1745", "#170b26"], accent="#d2a8ff")
NARRATION = [
 "Kuru üzüm suda neden şişer? Cevap, ozmoz denen sessiz bir yolculukta.",
 "Kuru üzüm, suyunu kaybetmiş bir üzümdür. Ama şekeri içinde kalmıştır, yani içi çok şekerlidir.",
 "Üzümün kabuğu ve hücre zarları yarı geçirgendir. Küçük su moleküllerini geçirir, büyük şeker moleküllerini tutar.",
 "Su, şekerin az olduğu taraftan çok olduğu tarafa geçme eğilimindedir. Üzümün içi daha şekerli olduğu için su içeri akar. Buna ozmoz denir.",
 "İçeri giren su hücreleri doldurur. Üzüm yavaş yavaş şişer, kırışıkları açılır.",
 "Ozmoz tersine de çalışır. Tuzlanan salatalık ve şekerlenen çilek, suyunu dışarı bırakır.",
 "Su, şekerin peşinden gider. Neden böyle? Artık biliyorsunuz.",
]
RAISIN, GRAPE, WATER = "#5a2a44", "#8e4fc4", "#6ec6f0"

def berry(c, x, y, r, k, a=1.0):
    """k=0 kuru üzüm (kırışık, koyu, küçük), k=1 dolgun üzüm."""
    k = clamp(k); rr = r * lerp(0.72, 1.0, k); p = skia.Path()
    for j in range(73):
        th = j / 72 * 2 * math.pi
        wob = 1 + (1 - k) * (0.09 * math.sin(7 * th + 0.6) + 0.05 * math.sin(11 * th))
        px = x + rr * 1.0 * wob * math.cos(th); py = y + rr * lerp(0.82, 0.94, k) * wob * math.sin(th)
        p.moveTo(px, py) if j == 0 else p.lineTo(px, py)
    p.close(); c.drawPath(p, fill(mixcol(RAISIN, GRAPE, k), a))
    wa = a * (1 - k) * 0.8
    if wa > 0.01:
        for (dx, dy, s0) in ((-0.35, -0.2, 0.0), (0.1, -0.35, 1.0), (0.25, 0.15, 2.0), (-0.2, 0.3, 3.0)):
            q = skia.Path(); cx, cy = x + dx * rr, y + dy * rr
            q.moveTo(cx - 0.28 * rr, cy); q.quadTo(cx, cy - 0.16 * rr * (1 if s0 % 2 else -1), cx + 0.28 * rr, cy + 0.04 * rr)
            c.drawPath(q, stroke("#2a1020", max(3, rr * 0.06), wa))
    circ(c, x - rr * 0.35, y - rr * 0.35, rr * 0.18, "#ffffff", a * (0.15 + 0.3 * k))
    line(c, x + rr * 0.05, y - rr * 0.8, x + rr * 0.2, y - rr * 1.05, "#7a5a2a", max(4, rr * 0.07), a)

def glass(c, x, y, w, h, lvl=0.8, a=1.0):
    top = y - h / 2; bot = y + h / 2; wl = bot - h * lvl
    poly(c, [(x - w / 2 + 6, wl), (x + w / 2 - 6, wl), (x + w / 2 - 22, bot - 6), (x - w / 2 + 22, bot - 6)], WATER, 0.35 * a)
    line(c, x - w / 2 + 6, wl, x + w / 2 - 6, wl, "#bfe8ff", 5, 0.8 * a)
    poly(c, [(x - w / 2, top), (x - w / 2 + 18, bot), (x + w / 2 - 18, bot), (x + w / 2, top)], "#ffffff", 0.9 * a, sw=8, close=False)

def wdot(c, x, y, a=1.0): circ(c, x, y, 13, WATER, a)
def sugar(c, x, y, r, a=1.0):
    pts = [(x + r * math.cos(j * math.pi / 3 + math.pi / 6), y + r * math.sin(j * math.pi / 3 + math.pi / 6)) for j in range(6)]
    poly(c, pts, "#ffffff", 0.95 * a)

def hero(c, t):
    k = 0.5 + 0.5 * math.sin(t * 1.1 - 1.4)
    glass(c, 540, 900, 520, 560, 0.78)
    berry(c, 540, 980, 150, k)
    for j in range(5):
        u = (t * 0.45 + j * 0.2) % 1
        circ(c, 380 + j * 80, 1120 - u * 380, 7 + 4 * u, "#ffffff", 0.35 * (1 - u))

def i1(c, t, d):
    k = 1 - eout(ss(0.6, 3.0, t))
    berry(c, 540, 830, 190, k)
    for j in range(8):
        ang = j * math.pi / 4 + 0.3; u = ss(0.8, 3.2, t)
        dist = 220 + 140 * ((u * 1.6 + j * 0.13) % 1)
        drop(c, 540 + math.cos(ang) * dist, 830 + math.sin(ang) * dist * 0.8, 16, 0.85 * ss(0.8, 1.2, t) * (1 - ss(3.0, 3.6, t)), BLUE)
    tag(c, "su gider", 540, 540, "#bfe8ff", ss(1.2, 1.7, t) * (1 - ss(3.4, 3.8, t)), 44, "c", "Bold")
    s = ss(3.8, 4.4, t)
    for j, (dx, dy) in enumerate(((-60, -30), (40, -50), (10, 40), (-40, 50), (70, 20))):
        sugar(c, 540 + dx, 830 + dy, 24 * pop(t, 3.8 + j * 0.12), s)
    tag(c, "şeker içeride kalır", 540, 1100, THEME["accent"], ss(4.2, 4.7, t), 42, "c", "Bold")

_r = np.random.default_rng(4)
WL = [(float(_r.uniform(120, 480)), float(_r.uniform(620, 1060)), float(_r.uniform(0, 1))) for _ in range(9)]
def i2(c, t, d):
    # zar: ortada delikli dikey çizgi
    for y in range(600, 1040, 70): rrect(c, 528, y, 24, 44, 12, "#e8d6ff", 0.9)
    for j, (x0, y0, ph) in enumerate(WL):
        u = ((t * 0.28 + ph) % 1)
        x = lerp(140, 940, u); y = 640 + ((j * 53) % 420)
        y = 600 + 70 * min(5, round((y - 600) / 70)) + 57  # deliklerden geç
        wdot(c, x, y, ss(0.8, 1.3, t))
    for j, (sx, sy) in enumerate(((760, 700), (850, 880), (720, 1010))):
        b = abs(math.sin(t * 1.6 + j)) * 50
        sugar(c, sx - b * 0.0 + (40 - b), sy, 42, ss(2.6, 3.1, t))
    tag(c, "su geçer", 300, 560, "#bfe8ff", ss(1.2, 1.7, t), 40, "c", "Bold")
    tag(c, "şeker geçemez", 800, 560, "#ffffff", ss(3.0, 3.5, t), 40, "c", "Bold")
    tag(c, "yarı geçirgen zar", 540, 1165, THEME["accent"], ss(4.2, 4.7, t), 40, "c", "Bold")

def i3(c, t, d):
    rrect(c, 90, 620, 900, 440, 40, "#ffffff", 0.08); rrect(c, 90, 620, 900, 440, 40, "#ffffff", 0.3, sw=3)
    for y in range(640, 1040, 60): rrect(c, 530, y, 20, 36, 10, "#e8d6ff", 0.9)
    tag(c, "dış: az şeker", 300, 590, "#bfe8ff", ss(0.8, 1.3, t), 38, "c", "Bold")
    tag(c, "üzüm içi: çok şeker", 780, 590, THEME["accent"], ss(1.6, 2.1, t), 38, "c", "Bold")
    sugar(c, 300, 840, 34, ss(0.8, 1.3, t))
    for j, (x, y) in enumerate(((680, 720), (820, 760), (720, 880), (880, 900), (660, 990), (800, 1000))):
        sugar(c, x, y, 30, ss(1.6, 2.1, t))
    m = ss(3.4, 4.0, t)
    for j in range(6):
        u = (t * 0.5 + j / 6) % 1; y = 690 + j * 62
        x = lerp(160, 900, u); a = m * ss(0, 0.1, u) * (1 - ss(0.85, 1, u))
        wdot(c, x, y, a)
    arrow(c, 380, 1110, 700, 1110, "#bfe8ff", 10, m, 28)
    a2 = ss(6.0, 6.6, t)
    rrect(c, 380, 790, 320, 100, 50, THEME["accent"], 0.95 * a2)
    tag(c, "OZMOZ", 540, 862, "#2c1745", a2, 56, "c", "Bold")

def i4(c, t, d):
    k = eout(ss(0.6, 4.2, t))
    glass(c, 540, 830, 520, 540, 0.8)
    berry(c, 540, 890, 160, k)
    for j in range(8):
        ang = j * math.pi / 4 + 0.2; u = (t * 0.6 + j * 0.125) % 1
        dist = lerp(250, 150, u)
        circ(c, 540 + math.cos(ang) * dist, 890 + math.sin(ang) * dist * 0.85, 10, WATER, 0.9 * (1 - u) * ss(0.5, 1.0, t) * (1 - ss(4.2, 4.8, t)))
    tag(c, "kırışıklar açılır", 540, 1180, THEME["accent"], ss(3.2, 3.7, t), 40, "c", "Bold")

SCENES = [
 title_scene("Kuru üzüm suda", "neden şişer?", "Ozmozun sessiz yolculuğu", hero),
 reason_scene("ADIM 1", "Su gitti, şeker kaldı", ["Kuru üzüm suyunu kaybetmiştir;", "içi bu yüzden çok şekerlidir."], i1),
 reason_scene("ADIM 2", "Seçici bir kapı", ["Kabuk ve hücre zarları suyu geçirir,", "büyük şeker moleküllerini tutar."], i2),
 reason_scene("ADIM 3", "Su şekere koşar", ["Su, az şekerli taraftan", "çok şekerli tarafa geçer: ozmoz."], i3),
 reason_scene("ADIM 4", "Üzüm dolgunlaşır", ["İçeri giren su hücreleri doldurur;", "üzüm şişer, kırışıklar açılır."], i4),
 cards_scene("BONUS", "Ozmoz tersine de işler", [("Kuru üzüm suda", "Su içeri girer, şişer"), ("Tuzlanan salatalık", "Suyunu dışarı bırakır"), ("Şekerlenen çilek", "Kendi şerbetini salar")]),
 end_scene("Su, şekerin", "peşinden gider.", hero),
]
if __name__ == "__main__":
    nb.main(SLUG, NARRATION, SCENES)
