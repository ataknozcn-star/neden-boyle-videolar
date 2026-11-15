import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import numpy as np, skia
from nb import *
import nb

SLUG = "deniz-neden-tuzlu"
nb.THEME.update(bg=["#0f6e8c", "#0a4a63", "#06283a"], accent="#ffe08a")
NARRATION = [
 "Deniz neden tuzlu? İşte tuzun uzun yolculuğu.",
 "Yağmur suyu hafif asitlidir. Kayalara düştükçe onları yavaşça aşındırır ve içlerindeki mineralleri çözer.",
 "Nehirler, çözünen bu mineralleri denize taşır.",
 "Güneş deniz suyunu buharlaştırır. Su göğe yükselir, ama tuz denizde kalır.",
 "Bu döngü milyonlarca yıl boyunca sürdü ve tuz denizde azar azar birikti.",
 "Üç bilgi daha. Bir litre deniz suyunda yaklaşık otuz beş gram tuz vardır. Nehirlerde de tuz bulunur, ama çok azdır. Deniz tabanındaki sıcak su bacaları da mineral ekler.",
 "Denizin tuzu kayalardan geliyor. Neden böyle? Artık biliyorsunuz.",
]
SEA, FOAM, ROCK = "#2f8fd0", "#bfe6ff", "#8d8580"

def sea(c, x0, x1, ytop, ybot, t, a=1.0):
    p = skia.Path(); p.moveTo(x0, ybot)
    for x in range(int(x0), int(x1) + 1, 8): p.lineTo(x, ytop + 10 * math.sin(x / 55 + t * 2.2))
    p.lineTo(x1, ybot); p.close(); c.drawPath(p, fill(SEA, a))
    q = skia.Path()
    for k, x in enumerate(range(int(x0), int(x1) + 1, 8)):
        y = ytop + 10 * math.sin(x / 55 + t * 2.2); q.moveTo(x, y) if k == 0 else q.lineTo(x, y)
    c.drawPath(q, stroke(FOAM, 8, a))

def salt(c, x, y, s=14, a=1.0):
    if a > 0.01 and s > 0: poly(c, [(x, y - s), (x + s, y), (x, y + s), (x - s, y)], "#ffffff", a)

_r = np.random.default_rng(11)
PTS = [(float(_r.uniform(0.04, 0.96)), float(_r.uniform(0.22, 0.88))) for _ in range(44)]
def salts(c, x0, x1, ytop, ybot, n, t, s=13):
    for k, (u, v) in enumerate(PTS[:n]):
        salt(c, lerp(x0, x1, u), lerp(ytop, ybot, v) + 4 * math.sin(t * 1.5 + k), s, 0.95)

def hero(c, t):
    sun(c, 540, 700, 84, t)
    sea(c, 150, 930, 900, 1130, t); salts(c, 150, 930, 900, 1130, 14, t, 16)

RAINX = [float(_r.uniform(330, 750)) for _ in range(16)]
MNT = [(150, 1085), (420, 790), (540, 930), (660, 820), (930, 1085)]
def i1(c, t, d):
    cloud(c, 540, 600, 1.0, 0.9, "#c5d3df")
    tag(c, "hafif asitli yağmur", 540, 490, "#cfeaff", ss(0.8, 1.3, t), 34, "c")
    for k, x in enumerate(RAINX):
        u = (t * 1.1 + k * 0.173) % 1; y = 670 + u * 150
        line(c, x, y, x - 5, y + 24, "#9fd4ff", 5, 0.7 * (1 - ss(0.8, 1, u)))
    poly(c, MNT, ROCK); poly(c, [(420, 790), (372, 842), (420, 830), (455, 832)], "#d9d4cf")
    poly(c, [(660, 820), (622, 864), (662, 852), (698, 862)], "#d9d4cf")
    for k in range(8):
        left = k % 2 == 0; u = ss(0, 1, ((t - 2.6) * 0.3 + k * 0.125) % 1) if t > 2.6 else -1
        if u < 0: continue
        a_, b_ = ((420, 800), (190, 1050)) if left else ((660, 830), (890, 1050))
        salt(c, lerp(a_[0], b_[0], u), lerp(a_[1], b_[1], u) - 14, 12, ss(0, 0.15, u) * (1 - ss(0.85, 1, u)))
    tag(c, "mineraller çözünür", 540, 1150, THEME["accent"], ss(5.0, 5.5, t), 40, "c", "Bold")

R0, R1, R2 = (300, 742), (430, 950), (640, 1016)
def i2(c, t, d):
    poly(c, [(80, 1140), (80, 820), (640, 1010), (640, 1140)], "#4f7a52")
    poly(c, [(80, 820), (240, 560), (430, 942)], ROCK); poly(c, [(240, 560), (200, 625), (242, 610), (275, 630)], "#d9d4cf")
    sea(c, 610, 1000, 1010, 1140, t)
    p = skia.Path(); p.moveTo(*R0); p.quadTo(R1[0], R1[1], R2[0], R2[1]); c.drawPath(p, stroke(SEA, 36)); c.drawPath(p, stroke(FOAM, 6, 0.5))
    for k in range(6):
        u = (t * 0.32 + k / 6) % 1; x, y = qbez(R0, R1, R2, u); salt(c, x, y, 11, ss(0, 0.1, u) * (1 - ss(0.9, 1, u)))
    n = int(clamp((t - 0.8) / max(d - 1.6, 1)) * 12)
    for k, (u, v) in enumerate(PTS[:n]): salt(c, lerp(650, 990, u), lerp(1030, 1135, v), 11, 0.95)
    tag(c, "nehir", 560, 880, FOAM, ss(0.9, 1.4, t), 36, "l", "Bold")
    tag(c, "deniz", 820, 970, FOAM, ss(1.8, 2.3, t), 36, "c", "Bold")

def i3(c, t, d):
    sun(c, 840, 610, 62, t)
    sea(c, 80, 1000, 900, 1090, t); salts(c, 80, 1000, 900, 1090, 18, t)
    for k, x in enumerate((230, 430, 630)):
        u = (t * 0.4 + k / 3) % 1; y = 870 - 210 * u
        if t > 1.0: arrow(c, x, y, x, y - 60, "#ffffff", 9, 0.85 * ss(0, 0.15, u) * (1 - ss(0.75, 1, u)), 22)
    tag(c, "su buharlaşır", 110, 560, "#ffffff", ss(1.2, 1.7, t), 36, "l")
    tag(c, "tuz denizde kalır", 540, 1150, THEME["accent"], ss(3.6, 4.1, t), 40, "c", "Bold")

def i4(c, t, d):
    k = ss(0.8, d - 1.3, t)
    tag(c, "milyonlarca yıl", 540, 560, THEME["text"], ss(0.5, 1.0, t), 38, "c", "Bold")
    rrect(c, 140, 592, 800, 24, 12, THEME["text"], 0.2); rrect(c, 140, 592, max(24, 800 * k), 24, 12, THEME["accent"])
    sea(c, 80, 1000, 740, 1090, t); salts(c, 80, 1000, 740, 1090, int(lerp(4, 44, k)), t)
    tag(c, "tuz azar azar birikir", 540, 1150, THEME["accent"], ss(2.6, 3.1, t), 40, "c", "Bold")

SCENES = [
 title_scene("Deniz", "neden tuzlu?", "Tuzun uzun yolculuğu", hero),
 reason_scene("ADIM 1", "Yağmur kayaları aşındırır", ["Hafif asitli yağmur kayaları aşındırır,", "içlerindeki mineralleri çözer."], i1),
 reason_scene("ADIM 2", "Nehirler tuzu taşır", ["Nehirler, çözünen mineralleri", "denize kadar taşır."], i2),
 reason_scene("ADIM 3", "Su gider, tuz kalır", ["Güneş suyu buharlaştırır;", "tuz ise denizde kalır."], i3),
 reason_scene("ADIM 4", "Tuz zamanla birikir", ["Bu döngü milyonlarca yıl sürdü;", "tuz denizde azar azar birikti."], i4),
 cards_scene("ÜÇ BİLGİ", "Bunları biliyor muydunuz?", [("Litrede yaklaşık 35 gram tuz", "Deniz suyunun ortalaması"), ("Nehirlerde de tuz var", "Ama tadı alınmayacak kadar az"), ("Deniz tabanı da katkı yapar", "Sıcak su bacaları mineral ekler")]),
 end_scene("Denizin tuzu", "kayalardan geliyor.", hero),
]
if __name__ == "__main__":
    nb.main(SLUG, NARRATION, SCENES)
