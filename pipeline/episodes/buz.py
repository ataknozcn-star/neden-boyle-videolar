import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import numpy as np, skia
from nb import *
import nb

SLUG = "buz-neden-yuzer"
nb.THEME.update(bg=["#1f5f7a", "#123a52", "#0a2030"], accent="#8fe3ff")
NARRATION = [
 "Buz neden suda yüzer? İşte suyun tuhaf sırrı.",
 "Çoğu madde donunca sıkışır ve ağırlaşır. Su ise tam tersini yapar.",
 "Sıvı suda moleküller birbirine yakın durur ve serbestçe kayar.",
 "Su donarken moleküller altıgen bir kafes kurar. Bu kafesin içinde boşluklar kalır.",
 "Aynı miktar su, buz olunca yaklaşık yüzde dokuz genişler. Yani buz, sudan daha hafiftir.",
 "İyi ki öyle. Buz yüzdüğü için göller üstten donar; alttaki su sıvı kalır ve balıklar kışı atlatır.",
 "Buz batmıyor; çünkü içi boşluk dolu. Neden böyle? Artık biliyorsunuz.",
]
def mol(c, x, y, r=20, a=1.0, rot=0.0):
    for s_ in (-1, 1):
        ang = rot + s_ * 0.9 + math.pi / 2; circ(c, x + math.cos(ang) * r * 1.05, y + math.sin(ang) * r * 1.05, r * 0.52, "#ffffff", a)
    circ(c, x, y, r, "#4fb3ff", a)
def glass(c, cx, cy, t, s=1.0):
    w = 320 * s; h = 400 * s; x = cx - w / 2; y = cy - h / 2; wl = y + 120 * s
    rrect(c, x + 8, wl, w - 16, h - 120 * s - 8, 26, "#3fa0e0", 0.8)
    ic = 130 * s; iy = wl - ic * 0.12 + 6 * math.sin(t * 2)
    rrect(c, cx - ic / 2, iy, ic, ic, 18, "#e8f8ff", 0.96); rrect(c, cx - ic / 2, iy, ic, ic, 18, "#ffffff", 1, sw=5)
    line(c, cx - ic * 0.28, iy + ic * 0.25, cx - ic * 0.28, iy + ic * 0.6, "#ffffff", 8, 0.8)
    rrect(c, x, y, w, h, 34, "#ffffff", 0.9, sw=8)
def hero(c, t): glass(c, 540, 900, t, 1.1)
def i1(c, t, d):
    k = ss(1.2, 2.6, t)
    tag(c, "çoğu madde", 300, 580, None, 1, 38, "c", "Bold"); tag(c, "su", 780, 580, THEME["accent"], 1, 38, "c", "Bold")
    sl = 210 * (1 - 0.16 * k); rrect(c, 300 - sl / 2, 800 - sl / 2, sl, sl, 20, "#c9a36b")
    sr = 210 * (1 + 0.14 * ss(2.6, 4.0, t)); rrect(c, 780 - sr / 2, 800 - sr / 2, sr, sr, 20, "#bfeaff")
    tag(c, "donunca küçülür", 300, 1010, None, ss(2.2, 2.7, t), 32, "c"); tag(c, "donunca büyür", 780, 1010, THEME["accent"], ss(3.6, 4.1, t), 32, "c")
_r = np.random.default_rng(8)
LIQ = [(210 + (i % 7) * 110 + float(_r.uniform(-22, 22)), 590 + (i // 7) * 92 + float(_r.uniform(-18, 18)), float(_r.uniform(0, 6.28))) for i in range(42)]
def i2(c, t, d):
    rrect(c, 130, 510, 820, 620, 40, "#3fa0e0", 0.22); rrect(c, 130, 510, 820, 620, 40, "#ffffff", 0.8, sw=6)
    for i, (x, y, ph) in enumerate(LIQ):
        mol(c, x + 14 * math.sin(t * 2.2 + ph), y + 12 * math.cos(t * 1.9 + ph * 1.3), 21, 1, ph + t * 0.8)
L_ = 88; VERT = {}
for r in (-1, 0, 1):
    for q in (-1, 0, 1):
        hx = 540 + q * L_ * math.sqrt(3) + (abs(r) % 2) * L_ * math.sqrt(3) / 2 - L_ * math.sqrt(3) / 4; hy = 810 + r * L_ * 1.5
        for k in range(6):
            vx = hx + L_ * math.cos(math.radians(60 * k + 30)); vy = hy + L_ * math.sin(math.radians(60 * k + 30)); VERT[(round(vx / 6), round(vy / 6))] = (vx, vy)
VERT = list(VERT.values()); START = [(float(_r.uniform(200, 880)), float(_r.uniform(560, 1080))) for _ in VERT]
BONDS = [(i, j) for i in range(len(VERT)) for j in range(i + 1, len(VERT)) if abs(math.hypot(VERT[i][0] - VERT[j][0], VERT[i][1] - VERT[j][1]) - L_) < 6]
def i3(c, t, d):
    m = ss(1.0, 3.2, t); ba = ss(2.8, 3.6, t)
    P = [(lerp(sx, vx, m) + (1 - m) * 10 * math.sin(t * 2 + i), lerp(sy, vy, m) + (1 - m) * 10 * math.cos(t * 2.3 + i)) for i, ((sx, sy), (vx, vy)) in enumerate(zip(START, VERT))]
    for i, j in BONDS: line(c, P[i][0], P[i][1], P[j][0], P[j][1], "#bfeaff", 6, 0.8 * ba)
    for i, (x, y) in enumerate(P): mol(c, x, y, 17, 1, i)
    tag(c, "boşluk", 540 - L_ * math.sqrt(3) / 4 + 0, 822, "#ffffff", ss(3.8, 4.3, t), 30, "c", "Bold")
def i4(c, t, d):
    glass(c, 440, 810, t, 1.25)
    a = ss(1.6, 2.1, t); arrow(c, 742, 634, 590, 622, THEME["accent"], 6, a)
    tag(c, "hacim +%9", 870, 650, THEME["accent"], a, 40, "c", "Bold"); tag(c, "buz, sudan hafif", 860, 1000, None, ss(3.6, 4.1, t), 32, "c")
SCENES = [
 title_scene("Buz neden", "suda yüzer?", "Suyun tuhaf sırrı", hero),
 reason_scene("NEDEN 1", "Su kurala uymaz", ["Çoğu madde donunca sıkışır.", "Su ise tam tersini yapar."], i1),
 reason_scene("NEDEN 2", "Sıvı su sıkışıktır", ["Sıvı suda moleküller birbirine", "yakın durur ve serbestçe kayar."], i2),
 reason_scene("NEDEN 3", "Buz, altıgen bir kafes", ["Donarken moleküller altıgen kafes", "kurar; içinde boşluklar kalır."], i3),
 reason_scene("NEDEN 4", "Buz sudan hafiftir", ["Su, buz olunca yaklaşık %9 genişler.", "Bu yüzden buz suyun üstünde kalır."], i4),
 cards_scene("İYİ Kİ ÖYLE", "Buz yüzmeseydi?", [("Göller üstten donar", "Buz yüzeyde kalır"), ("Buz, yorgan gibi örter", "Alttaki suyu soğuktan korur"), ("Canlılar kışı atlatır", "Dipte su sıvı kalır")]),
 end_scene("Buz batmıyor;", "içi boşluk dolu.", hero),
]
if __name__ == "__main__":
    nb.main(SLUG, NARRATION, SCENES)
