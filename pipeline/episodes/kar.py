import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import numpy as np, skia
from nb import *
import nb

SLUG = "kar-neden-beyaz"
nb.THEME.update(bg=["#35577a", "#1f3a57", "#0f1f33"], accent="#bfe9ff")
NARRATION = [
 "Kar neden beyaz? Oysa buz, cam gibi şeffaftır.",
 "Kar taneleri, şeffaf buz kristallerinden oluşur. Tek bir buz parçası, ışığın büyük kısmını geçirir.",
 "Ama bir avuç karda sayısız minik kristal ve aralarında hava boşlukları vardır.",
 "Işık her kristal yüzeyine çarptığında yön değiştirir. Kristalden kristale sekerek her yöne saçılır ve geri döner.",
 "Bu saçılma bütün renklere neredeyse eşit davranır. Renklerin hepsi birlikte gözümüze ulaşınca, beyaz görürüz.",
 "Peki buzul neden mavi? Işık buzun derinlerine iner. Buz, kırmızı ışığı biraz daha çok soğurur. Geriye mavi tonlar kalır.",
 "Kar boyalı değil; ışığı geri saçıyor. Neden böyle? Artık biliyorsunuz.",
]
ICE, SNOW = "#d8f1ff", "#f4fbff"
RAIN = ["#ff5d5d", "#ff9a3c", "#ffe066", "#6fd08c", "#6ec6f0", "#5b7bff", "#b07cff"]

def flake(c, x, y, r, rot=0.0, a=1.0, color="#ffffff", w=None):
    w = w or max(3, r * 0.12)
    for k in range(6):
        ang = rot + k * math.pi / 3; ca, sa = math.cos(ang), math.sin(ang)
        line(c, x, y, x + ca * r, y + sa * r, color, w, a)
        for f in (0.45, 0.72):
            bx, by = x + ca * r * f, y + sa * r * f; L = r * (0.32 if f < 0.6 else 0.22)
            for s_ in (-1, 1):
                b = ang + s_ * 0.8; line(c, bx, by, bx + math.cos(b) * L, by + math.sin(b) * L, color, w * 0.8, a)
    circ(c, x, y, w * 0.9, color, a)

_r = np.random.default_rng(5)
FALL = [(float(_r.uniform(120, 960)), float(_r.uniform(0, 1)), float(_r.uniform(14, 26)), float(_r.uniform(0, 6))) for _ in range(14)]
def hero(c, t):
    for (x, ph, r, rt) in FALL:
        y = 600 + ((ph + t * 0.12) % 1) * 520
        flake(c, x + 18 * math.sin(t * 1.3 + rt), y, r, rt + t * 0.6, 0.75)
    p = skia.Path(); p.moveTo(90, 1160); p.quadTo(300, 1000, 540, 1080); p.quadTo(780, 990, 990, 1160); p.close()
    c.drawPath(p, fill(SNOW))
    flake(c, 540, 860, 150, t * 0.25, 1.0, "#ffffff", 14)

def i1(c, t, d):
    k = pop(t, 0.3)
    c.save(); c.translate(540, 820); c.scale(k, k)
    rrect(c, -170, -170, 340, 340, 46, ICE, 0.28); rrect(c, -170, -170, 340, 340, 46, "#ffffff", 0.9, sw=7)
    line(c, -110, -120, -40, -120, "#ffffff", 10, 0.7); line(c, -125, -90, -105, -90, "#ffffff", 10, 0.6)
    c.restore()
    p = ss(1.2, 2.6, t)
    if p > 0:
        x1 = lerp(90, 990, p); line(c, 90, 820, x1, 820, GOLD, 12)
        if p > 0.95: arrow(c, 900, 820, 990, 820, GOLD, 12)
    tag(c, "şeffaf buz", 540, 590, THEME["accent"], ss(0.8, 1.3, t), 44, "c", "Bold")
    tag(c, "ışık içinden geçer", 540, 1080, GOLD, ss(2.6, 3.1, t), 40, "c", "Bold")

_r2 = np.random.default_rng(9)
CRY = []
for _ in range(60):
    x, y = float(_r2.uniform(250, 830)), float(_r2.uniform(600, 1040))
    if math.hypot(x - 540, y - 820) < 250: CRY.append((x, y, float(_r2.uniform(14, 30)), float(_r2.uniform(0, 3))))
def hexa(c, x, y, r, rot, a=1.0):
    pts = [(x + r * math.cos(rot + k * math.pi / 3), y + r * math.sin(rot + k * math.pi / 3)) for k in range(6)]
    poly(c, pts, ICE, 0.55 * a); poly(c, pts, "#ffffff", 0.95 * a, sw=3)
def i2(c, t, d):
    circ(c, 540, 820, 285, "#0b1828", 0.55); circ(c, 540, 820, 285, "#ffffff", 0.9, sw=8)
    for i, (x, y, r, rot) in enumerate(CRY):
        hexa(c, x, y, r * eback((t - 0.4 - i * 0.03) / 0.4) if t > 0.4 + i * 0.03 else 0, rot, 1)
    tag(c, "minik kristaller", 540, 500, THEME["accent"], ss(1.6, 2.1, t), 42, "c", "Bold")
    tag(c, "aralarında hava", 540, 1170, "#ffffff", ss(2.8, 3.3, t), 40, "c", "Bold")

BOUNCE = [(300, 470), (440, 760), (330, 900), (560, 980), (700, 820), (620, 700), (800, 560), (960, 470)]
def i3(c, t, d):
    for (x, y, r, rot) in CRY: hexa(c, x, y + 0, r, rot, 0.85)
    p = ss(0.8, 4.2, t) * (len(BOUNCE) - 1)
    for k in range(len(BOUNCE) - 1):
        q = clamp(p - k)
        if q <= 0: break
        (x0, y0), (x1, y1) = BOUNCE[k], BOUNCE[k + 1]
        if q >= 1 and k == len(BOUNCE) - 2: arrow(c, x0, y0, x1, y1, GOLD, 10, 1, 28)
        else: line(c, x0, y0, lerp(x0, x1, q), lerp(y0, y1, q), GOLD, 10)
        if 0 < k and q > 0: circ(c, x0, y0, 12, "#ffffff", 0.9)
    if t > 4.6:
        for k in range(10):
            ang = k * math.pi / 5 + 0.3; L = ((t - 4.6) * 160 + k * 31) % 150; a = 1 - L / 150
            line(c, 540 + math.cos(ang) * (300 + L), 820 + math.sin(ang) * (300 + L) * 0.85, 540 + math.cos(ang) * (330 + L), 820 + math.sin(ang) * (330 + L) * 0.85, GOLD, 7, a * 0.8)
    tag(c, "ışık seker, geri döner", 540, 1180, GOLD, ss(3.4, 3.9, t), 40, "c", "Bold")

def i4(c, t, d):
    p = skia.Path(); p.moveTo(80, 1120); p.quadTo(300, 980, 520, 1060); p.lineTo(520, 1120); p.close()
    c.drawPath(p, fill(SNOW))
    for k in range(3): flake(c, 150 + k * 130, 1010 - (k % 2) * 40, 26, t * 0.4 + k, 0.8)
    eye(c, 830, 640, 120, 62, look=(-30, 10))
    for k, cl in enumerate(RAIN):
        u = ss(0.8 + k * 0.25, 1.6 + k * 0.25, t)
        x0, y0 = 200 + k * 42, 1000 - k * 8; x1, y1 = 700, 690
        if u > 0: line(c, x0, y0, lerp(x0, x1, u), lerp(y0, y1, u), cl, 10)
    w = ss(3.4, 4.0, t)
    circ(c, 830, 640, 190, "#ffffff", 0.18 * w); circ(c, 830, 640, 150, "#ffffff", 0.9 * w, sw=6)
    tag(c, "tüm renkler", 330, 820, "#ffffff", ss(2.2, 2.7, t), 40, "c", "Bold")
    tag(c, "birlikte = beyaz", 820, 900, THEME["accent"], w, 44, "c", "Bold")

SCENES = [
 title_scene("Kar", "neden beyaz?", "Oysa buz şeffaftır", hero),
 reason_scene("NEDEN 1", "Buz aslında şeffaf", ["Kar taneleri şeffaf buz kristalidir;", "tek bir buz ışığı çoğunlukla geçirir."], i1),
 reason_scene("NEDEN 2", "Sayısız minik kristal", ["Bir avuç karda sayısız kristal", "ve aralarında hava boşlukları var."], i2),
 reason_scene("NEDEN 3", "Işık seker ve saçılır", ["Her yüzeyde yön değiştirir;", "kristalden kristale sekip geri döner."], i3),
 reason_scene("NEDEN 4", "Tüm renkler: beyaz", ["Saçılma her renge neredeyse eşit;", "hepsi birlikte beyaz görünür."], i4),
 cards_scene("BONUS", "Buzul neden mavi?", [("Işık derine iner", "Kalın, yoğun buz katmanları"), ("Kırmızı soğurulur", "Buz kırmızıyı biraz daha çok emer"), ("Geriye mavi kalır", "Derin buz mavi görünür")]),
 end_scene("Kar boyalı değil;", "ışığı geri saçıyor.", hero),
]
if __name__ == "__main__":
    nb.main(SLUG, NARRATION, SCENES)
