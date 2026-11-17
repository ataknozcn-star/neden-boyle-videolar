import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import numpy as np, skia
from nb import *
import nb

SLUG = "ayna-neden-bugulanir"
nb.THEME.update(bg=["#1f6470", "#123f48", "#08232a"], accent="#8ff0e6")
NARRATION = [
 "Banyo aynası neden buğulanır? Sıcak bir duştan sonra ayna bembeyaz olur.",
 "Sıcak duş suyu buharlaşır. Banyonun havası, gözle göremediğimiz su buharıyla dolar.",
 "Sıcak hava çok su buharı taşıyabilir. Ama hava soğudukça taşıyabileceği buhar azalır.",
 "Ayna, banyodaki havadan daha soğuktur. Ona değen nemli hava soğur ve buharın bir kısmı suya dönüşür.",
 "Aynada milyonlarca minicik damla oluşur. Bu damlalar ışığı her yöne saçar; bu yüzden yansımamızı net göremeyiz.",
 "Buğuyu azaltmak için üç ipucu. Banyoyu havalandırın; nemli hava dışarı çıkar. Daha ılık su kullanın; daha az buhar oluşur. Aynayı ısıtın; ılık yüzeyde buhar yoğuşmaz.",
 "Aynayı buğulandıran şey, soğuk yüzeyde suya dönüşen buhar. Neden böyle? Artık biliyorsunuz.",
]
GLASS, FRAME, SKIN, VAP, WARM, COLD = "#bfe6ee", "#e9eef2", "#5d8f9b", "#d9fbff", "#ff8a6a", "#6ec6f0"
_r = np.random.default_rng(11)
FOGD = [(float(_r.uniform(0.04, 0.96)), float(_r.uniform(0.04, 0.96)), float(_r.uniform(3, 8))) for _ in range(90)]

def mirror(c, cx, cy, w, h, fog, t, a=1.0):
    x0, y0 = cx - w / 2, cy - h / 2
    rrect(c, x0 - 18, y0 - 18, w + 36, h + 36, 46, "#8fa6b1", a)
    rrect(c, x0, y0, w, h, 32, GLASS, a)
    for k in range(2):                                   # parlama çizgileri
        line(c, x0 + w * (0.62 + k * 0.14), y0 + 40, x0 + w * (0.36 + k * 0.14), y0 + h * 0.42, "#ffffff", 14 - k * 6, 0.55 * a * (1 - fog))
    circ(c, cx, cy - h * 0.08, w * 0.17, SKIN, a * (1 - 0.85 * fog))  # yansıyan yüz
    rrect(c, cx - w * 0.3, cy + h * 0.14, w * 0.6, h * 0.4, w * 0.22, SKIN, a * (1 - 0.85 * fog))
    if fog > 0.01:
        rrect(c, x0, y0, w, h, 32, "#f4fbfd", 0.82 * fog * a)
        for (u, v, r) in FOGD: circ(c, x0 + u * w, y0 + v * h, r * w / 400, "#ffffff", 0.9 * fog * a)
def steam(c, x, y, t, k, a=1.0, hgt=160):
    u = (t * 0.45 + k * 0.37) % 1
    p = skia.Path(); yy = y - hgt * u; p.moveTo(x, yy); p.cubicTo(x + 30, yy - 32, x - 30, yy - 64, x, yy - 96)
    c.drawPath(p, stroke("#ffffff", 10, 0.55 * a * ss(0, 0.2, u) * (1 - ss(0.65, 1, u))))

def hero(c, t):
    mirror(c, 540, 850, 400, 500, ss(0.8, 2.6, t), t)
    rrect(c, 280, 1150, 520, 46, 22, FRAME); rrect(c, 520, 1112, 40, 40, 10, "#9fb3bd")
    for i in range(4): steam(c, 330 + i * 140, 1140, t, i, 0.9 * ss(0.4, 1.2, t), 260)

VAPD = [(float(_r.uniform(150, 930)), float(_r.uniform(740, 1040)), float(_r.uniform(0, 1))) for _ in range(46)]
def i1(c, t, d):
    line(c, 110, 530, 300, 530, "#9fb3bd", 18); line(c, 300, 530, 300, 580, "#9fb3bd", 18)
    poly(c, [(240, 580), (360, 580), (340, 620), (260, 620)], FRAME)
    rrect(c, 120, 1060, 840, 70, 30, FRAME)
    for n in range(14):                                  # duş damlaları
        u = (t * 1.3 + n * 0.071) % 1; x = 262 + (n * 37) % 80 + u * (n % 5 - 2) * 18
        drop(c, x, lerp(640, 1050, u), 9, 0.9 * ss(0.3, 0.8, t))
    k = ss(1.2, 4.5, t)                                  # oda buharla dolar
    for n, (x, y, ph) in enumerate(VAPD):
        if ph > k: continue
        yy = y - 30 * ((t * 0.3 + ph) % 1)
        circ(c, x + 10 * math.sin(t * 1.5 + n), yy, 8, VAP, 0.7 * ss(ph, ph + 0.1, k))
    for i in range(4): steam(c, 420 + i * 130, 1050, t, i, 0.8 * ss(0.8, 1.4, t), 220)
    tag(c, "görünmez su buharı", 680, 690, THEME["accent"], ss(2.6, 3.1, t), 40, "c", "Bold")

BOXW = [(float(_r.uniform(130, 470)), float(_r.uniform(660, 1030)), float(_r.uniform(0, 6.28))) for _ in range(26)]
BOXC = [(float(_r.uniform(610, 950)), float(_r.uniform(660, 1030)), float(_r.uniform(0, 6.28))) for _ in range(7)]
def i2(c, t, d):
    for (x0, colr, dots, lab, sub, t0) in ((100, WARM, BOXW, "sıcak hava", "çok buhar", 0.5), (580, COLD, BOXC, "soğuk hava", "az buhar", 2.6)):
        a = ss(t0, t0 + 0.5, t)
        rrect(c, x0, 630, 400, 430, 34, colr, 0.12 * a); rrect(c, x0, 630, 400, 430, 34, colr, 0.9 * a, sw=6)
        for n, (x, y, ph) in enumerate(dots):
            circ(c, x + 14 * math.sin(t * 2.2 + ph), y + 12 * math.cos(t * 1.8 + ph * 1.3), 11, VAP, 0.85 * a)
        tag(c, lab, x0 + 200, 600, colr, a, 42, "c", "Bold")
        tag(c, sub, x0 + 200, 1120, THEME["text"], ss(t0 + 0.6, t0 + 1.1, t), 38, "c", "Medium")

_r3 = np.random.default_rng(5)
FLOW = [(float(_r3.uniform(600, 1100)), float(_r3.uniform(0, 1))) for _ in range(30)]
def i3(c, t, d):
    mx = 780
    rrect(c, mx, 560, 60, 560, 16, GLASS); rrect(c, mx + 60, 560, 26, 560, 10, FRAME)
    tag(c, "soğuk ayna", mx + 30, 540, COLD, ss(0.6, 1.1, t), 40, "c", "Bold")
    tag(c, "nemli sıcak hava", 380, 600, WARM, ss(1.0, 1.5, t), 40, "c", "Bold")
    for n, (y, ph) in enumerate(FLOW):
        yy = 640 + (y - 600) * 0.9
        u = ((t - 1.0) * 0.45 + ph) % 1
        if t > 1.0 + 0.3 * ph: circ(c, lerp(130, mx - 30, u), yy + 8 * math.sin(t * 3 + n), 10, VAP, 0.85 * ss(0, 0.1, u) * (1 - ss(0.9, 1, u)))
        t0 = 2.0 + ph * 3.0
        if t > t0: drop(c, mx - 12, yy, 11, ss(t0, t0 + 0.3, t), "#6fd6ff")
    tag(c, "buhar suya dönüşür", 380, 1160, THEME["accent"], ss(4.0, 4.5, t), 42, "c", "Bold")
def i4(c, t, d):
    rrect(c, 90, 980, 900, 50, 14, GLASS); rrect(c, 90, 1030, 900, 22, 8, FRAME)
    line(c, 540, 600, 540, 1050, THEME["text"], 4, 0.3)
    k = ss(0.6, 1.8, t)                                  # sol: düz cam, net yansıma
    arrow(c, 170, 640, lerp(170, 310, k), lerp(640, 975, k), "#ffe066", 9, ss(0.5, 0.7, t))
    q = ss(1.8, 2.8, t)
    if q > 0: arrow(c, 310, 975, lerp(310, 450, q), lerp(975, 640, q), "#ffe066", 9)
    tag(c, "düz cam: net", 315, 1110, THEME["text"], ss(2.6, 3.1, t), 38, "c", "Bold")
    for n in range(9):                                   # sağ: damlalar
        x = 590 + n * 46; r = 17 + (n % 3) * 4; a = ss(2.6 + n * 0.08, 3.0 + n * 0.08, t)
        p = skia.Path(); p.addCircle(x, 980, r); c.save(); c.clipRect(skia.Rect.MakeLTRB(0, 0, W, 980)); c.drawPath(p, fill("#6fd6ff", 0.9 * a)); c.restore()
    k2 = ss(3.2, 4.0, t)
    arrow(c, 640, 640, lerp(640, 770, k2), lerp(640, 960, k2), "#ffe066", 9, ss(3.1, 3.3, t))
    if t > 4.0:
        for m in range(7):
            ang = math.radians(-160 + m * 23); L = 60 + 110 * ss(4.0, 4.8, t)
            arrow(c, 770 + math.cos(ang) * 30, 958 + math.sin(ang) * 30, 770 + math.cos(ang) * L, 958 + math.sin(ang) * L, "#ffe066", 6, 0.9, 16)
    tag(c, "damlalar: saçılır", 765, 1110, THEME["accent"], ss(4.6, 5.1, t), 38, "c", "Bold")
SCENES = [
 title_scene("Banyo aynası", "neden buğulanır?", "Sıcak duştan sonra ayna bembeyaz!", hero),
 reason_scene("NEDEN 1", "Sıcak su buharlaşır", ["Duş suyu buharlaşır; banyonun havası", "görünmez su buharıyla dolar."], i1),
 reason_scene("NEDEN 2", "Sıcak hava nem taşır", ["Sıcak hava çok buhar taşıyabilir;", "hava soğudukça bu kapasite azalır."], i2),
 reason_scene("NEDEN 3", "Ayna daha soğuktur", ["Aynaya değen nemli hava soğur;", "buharın bir kısmı suya dönüşür."], i3),
 reason_scene("NEDEN 4", "Damlalar ışığı saçar", ["Minicik damlalar ışığı her yöne", "saçar; yansıma net görünmez."], i4),
 cards_scene("İPUÇLARI", "Buğuyu azaltmak için", [("Banyoyu havalandırın", "Nemli hava dışarı çıkar"), ("Daha ılık su kullanın", "Daha az buhar oluşur"), ("Aynayı ısıtın", "Ilık yüzeyde buhar yoğuşmaz")]),
 end_scene("Buğu, soğuk aynada", "suya dönen buhar.", hero),
]
if __name__ == "__main__":
    nb.main(SLUG, NARRATION, SCENES)
