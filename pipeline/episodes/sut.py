import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import numpy as np, skia
from nb import *
import nb

SLUG = "sut-neden-tasar"
nb.THEME.update(bg=["#7a3f2a", "#472318", "#22100a"], accent="#ffb05c")
NARRATION = [
 "Süt neden taşar? Su kaynar ama taşmaz; süt ise bir anda yükselir.",
 "Süt yalnızca su değildir. İçinde yağ ve protein de vardır.",
 "Süt ısınınca yağ ve proteinler yüzeyde toplanır; ince bir kaymak tabakası oluşur.",
 "Dipte oluşan su buharı yukarı çıkar, ama bu tabakayı kolayca geçemez. Altında hapsolur.",
 "Biriken buhar tabakayı yukarı iter ve süt taşar. Suda böyle bir tabaka olmadığı için buhar rahatça çıkar.",
 "Taşmayı önlemek için üç ipucu. Ara sıra karıştırın; tabaka dağılır. Ateşi kısın; buhar daha yavaş oluşur. Derin bir tencere seçin; yükselecek yer kalır.",
 "Sütü taşıran şey, yüzeydeki tabakanın altında sıkışan buhar. Neden böyle? Artık biliyorsunuz.",
]
MILK, SKINC, STEEL, FATC, PROC, WATERC = "#fff6e2", "#f0c66b", "#cfd6de", "#f5b942", "#ff7fb6", "#6ec6f0"

def pot(c, cx, top, w, h, level, t, skin=0.0, color=MILK, lift=0.0, fire=4, a=1.0):
    """Kesit tencere: level 0..1 doluluk, skin 0..1 kaymak tabakası, lift tabakanın yükselmesi (px)."""
    x0 = cx - w / 2; ys = top + h * (1 - level) - lift
    rrect(c, x0, ys, w, top + h - ys, 6, color, a)
    if skin > 0.01: line(c, x0 + 14, ys, x0 + w - 14, ys, SKINC, 18, skin * a)
    p = skia.Path(); p.moveTo(x0, top - 6); p.lineTo(x0, top + h); p.lineTo(x0 + w, top + h); p.lineTo(x0 + w, top - 6)
    c.drawPath(p, stroke(STEEL, 18, a))
    for s_ in (-1, 1): line(c, cx + s_ * (w / 2 + 6), top + 34, cx + s_ * (w / 2 + 62), top + 34, STEEL, 20, a)
    if fire:
        rrect(c, cx - w * 0.36, top + h + 78, w * 0.72, 16, 8, "#3a2a26", a)
        flames(c, cx, top + h + 80, fire, t, a, gap=w * 0.6 / max(1, fire - 1))
    return ys
def bubble(c, x, y, r, a=1.0):
    circ(c, x, y, r, "#ffffff", 0.28 * a); circ(c, x, y, r, "#5aa2d6", 0.95 * a, sw=5)
    circ(c, x - r * 0.35, y - r * 0.35, r * 0.2, "#ffffff", 0.9 * a)
def steam(c, x, y, t, k, a=1.0):
    u = (t * 0.5 + k * 0.37) % 1
    p = skia.Path(); yy = y - 90 * u; p.moveTo(x, yy); p.cubicTo(x + 26, yy - 28, x - 26, yy - 56, x, yy - 84)
    c.drawPath(p, stroke("#ffffff", 9, 0.6 * a * ss(0, 0.2, u) * (1 - ss(0.65, 1, u))))

def hero(c, t):
    k = ss(1.0, 2.6, t); wob = 6 * math.sin(t * 5)
    ys = pot(c, 540, 720, 480, 380, 0.55 + 0.45 * k, t, skin=0.0, lift=30 * k + wob * k, fire=5)
    for i in range(9):                                   # köpük
        x = 320 + i * 55; r = 44 + 12 * math.sin(t * 4 + i * 1.3)
        circ(c, x, ys - 6 + 8 * math.sin(t * 3 + i), r * (0.35 + 0.65 * k), "#fffdf5")
    for s_ in (-1, 1):                                   # kenardan akan süt
        q = ss(2.4, 3.6, t)
        if q > 0:
            xx = 540 + s_ * 262; line(c, xx, 700, xx, 700 + 300 * q, "#fffdf5", 34)
            circ(c, xx, 700 + 300 * q, 22, "#fffdf5")
    for i in range(3): steam(c, 420 + i * 120, 655, t, i, 0.9)

_r = np.random.default_rng(7)
PART = [(float(_r.uniform(330, 750)), float(_r.uniform(700, 900)), int(k % 3)) for k in range(18)]
def particle(c, x, y, kind, a=1.0, s=1.0):
    if kind == 0: drop(c, x, y, 17 * s, a, WATERC)
    elif kind == 1: circ(c, x, y, 20 * s, FATC, a); circ(c, x - 6 * s, y - 6 * s, 6 * s, "#ffffff", 0.6 * a)
    else:
        p = skia.Path(); p.moveTo(x - 24 * s, y); p.cubicTo(x - 12 * s, y - 22 * s, x - 4 * s, y + 22 * s, x + 8 * s, y); p.quadTo(x + 16 * s, y - 14 * s, x + 24 * s, y)
        c.drawPath(p, stroke(PROC, 9 * s, a))
def i1(c, t, d):
    pot(c, 540, 580, 520, 370, 0.78, t, fire=0)
    for n, (x, y, kind) in enumerate(PART):
        a = ss(0.8 + kind * 1.1, 1.3 + kind * 1.1, t)
        particle(c, x + 8 * math.sin(t * 1.3 + n), y + 6 * math.cos(t * 1.1 + n * 2), kind, a)
    for kind, (lab, cl, x) in enumerate((("su", WATERC, 230), ("yağ", FATC, 540), ("protein", PROC, 850))):
        a = ss(1.0 + kind * 1.1, 1.5 + kind * 1.1, t)
        particle(c, x - 75 if kind < 2 else x - 115, 1082, kind, a, 1.1)
        tag(c, lab, x - 35 if kind < 2 else x - 70, 1098, cl, a, 46, "l", "Bold")
def i2(c, t, d):
    k = ss(1.2, 4.2, t)
    ys = pot(c, 540, 600, 520, 370, 0.78, t, skin=ss(2.6, 4.4, t))
    for n, (x, y, kind) in enumerate(PART):
        if kind == 0: continue
        u = clamp(k * 1.25 - (n % 5) * 0.06); yy = lerp(y + 40, ys + 22, eout(u))
        particle(c, x + 6 * math.sin(t * 1.5 + n), yy, kind, 1 - 0.75 * ss(2.8, 4.4, t), 0.9)
    a = ss(3.6, 4.2, t)
    arrow(c, 830, 545, 760, ys - 20, THEME["accent"], 7, a)
    tag(c, "kaymak tabakası", 700, 525, THEME["accent"], a, 42, "c", "Bold")
    for i in range(3): arrow(c, 380 + i * 160, 900, 380 + i * 160, 800, "#ffffff", 7, 0.5 * ss(1.0, 1.5, t) * (1 - ss(3.2, 4.0, t)), 20)
def i3(c, t, d):
    ys = pot(c, 540, 600, 520, 370, 0.78, t, skin=1.0)
    for n in range(14):
        x = 325 + (n * 97) % 430; t0 = 0.8 + n * 0.33
        if t < t0: continue
        u = clamp((t - t0) / 1.4); r = 16 + (n % 3) * 5
        stop = ys + 16 + r + (n % 3) * 20
        y = lerp(950, stop, eout(u)) + (2.5 * math.sin(t * 6 + n) if u >= 1 else 0)
        bubble(c, x + 5 * math.sin(t * 3 + n), y, r)
    a = ss(3.2, 3.8, t)
    for i in range(3):
        x = 400 + i * 140; check_x = 16
        line(c, x - check_x, ys - 62, x + check_x, ys - 30, RED, 9, a); line(c, x + check_x, ys - 62, x - check_x, ys - 30, RED, 9, a)
    tag(c, "buhar geçemiyor", 540, 505, THEME["accent"], a, 42, "c", "Bold")
def i4(c, t, d):
    # sol: süt taşıyor
    k = ss(0.8, 3.0, t)
    ys = pot(c, 290, 640, 340, 330, 0.62 + 0.38 * k, t, skin=1.0, lift=26 * k, fire=3)
    for n in range(6): bubble(c, 180 + n * 44, ys + 40 + (n % 2) * 34, 15 + (n % 3) * 3)
    q = ss(2.8, 4.0, t)
    for s_ in (-1, 1):
        if q > 0:
            xx = 290 + s_ * 190; line(c, xx, 628, xx, 628 + 220 * q, "#fffdf5", 26); circ(c, xx, 628 + 220 * q, 17, "#fffdf5")
    if q > 0:
        for n in range(6): circ(c, 180 + n * 44, ys - 4, 30 * q, "#fffdf5")
    tag(c, "süt", 290, 560, MILK, ss(0.4, 0.9, t), 50, "c", "Bold")
    if t > 3.4:
        r = 40 * pop(t, 3.4); circ(c, 290, 1110, r, RED)
        for s_ in (-1, 1): line(c, 290 - r * 0.38, 1110 - s_ * r * 0.38, 290 + r * 0.38, 1110 + s_ * r * 0.38, "#3a0f12", r * 0.24)
    # sağ: su kaynıyor, buhar çıkıyor
    a = ss(3.6, 4.2, t)
    yw = pot(c, 790, 640, 340, 330, 0.62, t, color="#5bb8ee", fire=3, a=max(0.35, a))
    if a > 0:
        for n in range(7):
            u = (t * 0.7 + n * 0.19) % 1; bubble(c, 680 + (n * 71) % 220, lerp(950, yw + 8, u), 13 + (n % 3) * 3, a * (1 - ss(0.85, 1, u)))
        for n in range(3): steam(c, 710 + n * 80, yw - 10, t, n, a)
    tag(c, "su", 790, 560, WATERC, max(0.35, a), 50, "c", "Bold")
    if t > 5.0: check(c, 790, 1110, 40 * pop(t, 5.0))
SCENES = [
 title_scene("Süt", "neden taşar?", "Su taşmaz, süt taşar!", hero),
 reason_scene("NEDEN 1", "Süt yalnızca su değil", ["Sütün içinde suyla birlikte", "yağ ve protein de vardır."], i1),
 reason_scene("NEDEN 2", "Yüzeyde tabaka oluşur", ["Isınınca yağ ve proteinler üstte", "toplanır; ince bir kaymak oluşur."], i2),
 reason_scene("NEDEN 3", "Buhar altta hapsolur", ["Dipte oluşan su buharı yükselir,", "ama tabakayı kolayca geçemez."], i3),
 reason_scene("NEDEN 4", "Buhar tabakayı iter", ["Biriken buhar tabakayı kaldırır.", "Suda tabaka yok; buhar rahat çıkar."], i4),
 cards_scene("İPUÇLARI", "Taşmayı önlemek için", [("Ara sıra karıştırın", "Tabaka dağılır, buhar çıkar"), ("Ateşi kısın", "Buhar daha yavaş oluşur"), ("Derin tencere seçin", "Yükselecek yer kalır")]),
 end_scene("Sütü taşıran şey:", "sıkışan buhar.", hero),
]
if __name__ == "__main__":
    nb.main(SLUG, NARRATION, SCENES)
