import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import numpy as np, skia
from nb import *
import nb

SLUG = "kasik-neden-kirik-gorunur"
AQ = "#5fe0d0"; WATER = "#3aa0d8"; SPOON = "#d9e2ec"
nb.THEME.update(bg=["#1b4a5a", "#11303c", "#081820"], accent=AQ)
NARRATION = [
 "Bardaktaki kaşık neden kırık görünür? Sebebi, ışığın sudaki yolculuğu.",
 "Bir şeyi görebilmemiz için, ondan gelen ışığın gözümüze ulaşması gerekir.",
 "Işık suda, havadakinden daha yavaş ilerler. Hızı, yaklaşık dörtte üçüne düşer.",
 "Işık sudan havaya eğik geçerken, hızı değiştiği için yön değiştirir. Buna kırılma denir.",
 "Beynimiz ise ışığın dümdüz geldiğini varsayar. Bu yüzden kaşığın sudaki kısmını, olduğundan daha yukarıda görürüz.",
 "Aynı nedenle havuzlar olduğundan sığ, sudaki balıklar da olduklarından daha yakında görünür.",
 "Kaşık kırılmadı; kırılan ışık. Neden böyle? Artık biliyorsunuz.",
]

def spoon_seg(c, x0, y0, x1, y1, a=1.0, bowl=False, w=18):
    line(c, x0, y0, x1, y1, SPOON, w, a)
    if bowl:
        ang = math.degrees(math.atan2(y1 - y0, x1 - x0))
        c.save(); c.translate(x1, y1); c.rotate(ang)
        c.drawOval(skia.Rect.MakeXYWH(-10, -30, 92, 60), fill(SPOON, a)); c.restore()

def glass(c, t, x=540, top=620, bot=1150, w=360, lvl=820):
    hw = w / 2
    rrect(c, x - hw, lvl, w, bot - lvl, 26, WATER, 0.55)
    yy = lvl + 4 * math.sin(t * 2)
    line(c, x - hw + 8, yy, x + hw - 8, yy, "#bfe9ff", 6, 0.9)
    # kaşık: su üstü sap, su altı kaymış parça
    spoon_seg(c, 760, 560, x + 20, lvl)
    c.save(); c.clipRect(skia.Rect.MakeLTRB(x - hw + 6, lvl + 6, x + hw - 6, bot - 6))
    spoon_seg(c, x - 34, lvl + 6, x - 105, bot - 160, 0.95, bowl=True)
    c.restore()
    rrect(c, x - hw, top, w, bot - top, 26, "#e8f6ff", 0.9, sw=7)
    line(c, x - hw + 30, top + 40, x - hw + 30, bot - 60, "#ffffff", 6, 0.25)

def hero(c, t):
    glass(c, t)
    for k in range(3):
        y = 1120 - ((t * 60 + k * 90) % 280)
        circ(c, 470 + k * 50, y, 7, "#e6f7ff", 0.5)

def i1(c, t, d):
    sun(c, 180, 620, 60, t)
    circ(c, 300, 1010, 70, "#ff7a5c"); circ(c, 300, 1010, 70, "#ffffff", 0.25, sw=4)
    line(c, 305, 942, 320, 905, "#7a5c3e", 8)
    eye(c, 840, 760, 200, 110)
    p = ss(0.5, 1.5, t)
    arrow(c, 210, 690, lerp(210, 280, p), lerp(690, 920, p), GOLD, 8, ss(0.4, 0.6, t), 22)
    q = ss(1.8, 3.0, t)
    if q > 0: arrow(c, 380, 975, lerp(380, 720, q), lerp(975, 800, q), AQ, 9, 1, 24)
    tag(c, "ışık cisme çarpar", 520, 640, THEME["text"], ss(1.0, 1.5, t), 36, "c")
    tag(c, "gözümüze yansır", 640, 1050, AQ, ss(3.0, 3.5, t), 40, "c", "Bold")

def i2(c, t, d):
    rrect(c, 80, 620, 920, 170, 30, "#ffffff", 0.08); rrect(c, 80, 900, 920, 170, 30, WATER, 0.5)
    tag(c, "HAVA", 110, 660, THEME["text"], 0.9, 32, "l", "Bold"); tag(c, "SU", 110, 940, "#dff4ff", 0.9, 32, "l", "Bold")
    u = ss(0.6, 2.6, t)
    x1 = lerp(150, 940, u); x2 = lerp(150, 940, u * 0.75)
    line(c, 150, 720, x1, 720, GOLD, 10, 0.5); circ(c, x1, 720, 20, GOLD)
    line(c, 150, 1000, x2, 1000, AQ, 10, 0.5); circ(c, x2, 1000, 20, AQ)
    tag(c, "hızlı", 940, 660, GOLD, ss(2.6, 3.0, t), 36, "r", "Bold")
    tag(c, "yavaş: yaklaşık ¾", 940, 940, AQ, ss(3.0, 3.5, t), 36, "r", "Bold")

# kırılma geometrisi (n≈1,33): yüzey noktası (540, 820)
SX, SY = 540, 820
def i3(c, t, d):
    rrect(c, 80, SY, 920, 330, 20, WATER, 0.5)
    line(c, 80, SY, 1000, SY, "#bfe9ff", 6)
    for y in range(560, 1140, 34): line(c, SX, y, SX, y + 18, "#ffffff", 4, 0.35)
    tag(c, "hava", 110, 790, THEME["text"], 0.8, 32); tag(c, "su", 110, 870, "#dff4ff", 0.8, 32)
    p = ss(0.5, 1.6, t); circ(c, 420, 1080, 16, GOLD)
    line(c, 420, 1080, lerp(420, SX, p), lerp(1080, SY, p), GOLD, 10)
    q = ss(1.8, 2.8, t)
    if q > 0:
        # düz devam etseydi
        for k in range(6):
            u0, u1 = k / 6, k / 6 + 0.09
            if u0 < q: line(c, lerp(SX, 641, u0), lerp(SY, 600, u0), lerp(SX, 641, min(u1, q)), lerp(SY, 600, min(u1, q)), "#ffffff", 5, 0.4)
        arrow(c, SX, SY, lerp(SX, 700, q), lerp(SY, 582, q), GOLD, 10, 1, 26)
    tag(c, "yön değişir!", 850, 720, GOLD, ss(3.0, 3.5, t), 42, "c", "Bold")
    tag(c, "KIRILMA", 760, 1000, "#ffffff", ss(3.6, 4.1, t), 50, "c", "Bold")

def i4(c, t, d):
    rrect(c, 80, SY, 920, 330, 20, WATER, 0.5)
    line(c, 80, SY, 1000, SY, "#bfe9ff", 6)
    eye(c, 790, 560, 150, 84, look=(-0.6, 0.6))
    circ(c, 420, 1080, 22, SPOON)
    tag(c, "gerçek yer", 300, 1095, THEME["text"], ss(0.6, 1.1, t), 34, "c")
    p = ss(0.8, 2.0, t)
    line(c, 420, 1080, lerp(420, SX, min(1, p * 2)), lerp(1080, SY, min(1, p * 2)), GOLD, 9)
    if p > 0.5: arrow(c, SX, SY, lerp(SX, 700, (p - 0.5) * 2), lerp(SY, 582, (p - 0.5) * 2), GOLD, 9, 1, 24)
    q = ss(2.6, 3.6, t)
    for k in range(5):
        u0 = k / 5
        if u0 < q: line(c, lerp(SX, 432, u0), lerp(SY, 980, u0), lerp(SX, 432, min(u0 + 0.12, q)), lerp(SY, 980, min(u0 + 0.12, q)), AQ, 6, 0.9)
    g = ss(3.6, 4.1, t)
    circ(c, 432, 975, 22, AQ, 0.45 * g); circ(c, 432, 975, 22, AQ, g, sw=4)
    tag(c, "görünen yer", 270, 975, AQ, g, 34, "c", "Bold")
    tag(c, "beyin düz çizgi varsayar", 330, 640, THEME["text"], ss(2.4, 2.9, t), 36, "c")

SCENES = [
 title_scene("Bardaktaki kaşık", "neden kırık görünür?", "Işığın sudaki yolculuğu", hero),
 reason_scene("NEDEN 1", "Görmek = ışık", ["Bir cismi görmek için ondan gelen", "ışığın gözümüze ulaşması gerekir."], i1),
 reason_scene("NEDEN 2", "Suda ışık yavaşlar", ["Işık suda havadakinden yavaştır;", "hızı yaklaşık dörtte üçüne iner."], i2),
 reason_scene("NEDEN 3", "Işık yön değiştirir", ["Sudan havaya eğik geçen ışık", "kırılır, yani yön değiştirir."], i3),
 reason_scene("NEDEN 4", "Beyin düz çizgi sanır", ["Beyin ışığı düz izler; kaşığın", "ucunu daha yukarıda görürüz."], i4),
 cards_scene("BONUS", "Su hep yanıltır", [("Havuz sığ görünür", "Dibi daha yakında sanılır"), ("Balık daha yakında görünür", "Göründüğünden biraz derindedir"), ("Kaşık sapasağlam", "Kırılan yalnızca ışık")]),
 end_scene("Kaşık kırılmadı;", "kırılan ışık.", hero),
]
if __name__ == "__main__":
    nb.main(SLUG, NARRATION, SCENES)
