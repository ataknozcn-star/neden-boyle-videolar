import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import numpy as np, skia
from nb import *
import nb

SLUG = "misir-neden-patlar"
nb.THEME.update(bg=["#7a2e1f", "#4a1a12", "#260d09"], accent="#ffd54a")
NARRATION = [
 "Mısır neden patlar? İşte tanenin içindeki küçük patlama.",
 "Her mısır tanesinin içinde bir damla su ve bolca nişasta vardır.",
 "Tane ısınınca içindeki su buhara dönüşür. Sert kabuk ise buharın çıkmasına izin vermez.",
 "Basınç yükselir, yükselir. Yaklaşık yüz seksen derecede kabuk dayanamaz ve yarılır.",
 "Buhar bir anda genleşir; yumuşamış nişasta köpürüp dışarı fırlar ve hemen katılaşır. İşte patlamış mısır!",
 "Peki bazıları neden patlamaz? Kabuğu çatlaksa buhar kaçar; tane kuruysa yeterli basınç oluşmaz.",
 "Mısır kendiliğinden patlamıyor; içindeki su kaçmaya çalışıyor. Neden böyle? Artık biliyorsunuz.",
]
def kpath(s):
    p = skia.Path(); p.moveTo(0, -115 * s); p.cubicTo(125 * s, -95 * s, 135 * s, 95 * s, 0, 125 * s); p.cubicTo(-135 * s, 95 * s, -125 * s, -95 * s, 0, -115 * s); p.close(); return p
def kernel(c, cx, cy, s=1.0, rot=0.0, cut=False):
    c.save(); c.translate(cx, cy); c.rotate(rot); p = kpath(s)
    c.drawPath(p, fill("#fbeecb" if cut else "#f5b942")); c.drawPath(p, stroke("#d6951f" if cut else "#b9781a", (24 if cut else 9) * s, 1, False))
    if not cut: circ(c, 0, 100 * s, 24 * s, "#fff1c9"); line(c, -45 * s, -50 * s, -60 * s, 20 * s, "#ffffff", 12 * s, 0.35)
    c.restore()
def popcorn(c, cx, cy, s=1.0, a=1.0):
    for dx, dy, r in ((-85, -30, 72), (80, -45, 76), (-55, 72, 66), (68, 66, 72), (0, -98, 64), (0, 0, 92)):
        circ(c, cx + dx * s, cy + dy * s, r * s, "#e9dcc0", a); circ(c, cx + dx * s - 5 * s, cy + dy * s - 6 * s, r * s * 0.93, "#fff8e6", a)
    circ(c, cx + 8 * s, cy + 28 * s, 30 * s, "#f5b942", a)
def hero(c, t):
    popcorn(c, 540, 860, 1.25); kernel(c, 300, 1070, 0.42, -25); kernel(c, 780, 1080, 0.38, 30)
def i1(c, t, d):
    kernel(c, 540, 800, 2.3, 0, True); drop(c, 540, 815, 36)
    for (lbl, tx, ty, x1, y1, col_, t0, al) in (("kabuk", 860, 560, 720, 640, "#ffd54a", 1.0, "c"), ("nişasta", 190, 690, 400, 760, "#fbeecb", 2.6, "c"), ("su", 880, 1010, 590, 840, BLUE, 1.8, "c")):
        a = ss(t0, t0 + 0.5, t); line(c, tx - (40 if tx > 540 else -60), ty + 14, x1, y1, col_, 4, 0.8 * a); tag(c, lbl, tx, ty, col_, a, 38, al, "Bold")
def i2(c, t, d):
    flames(c, 540, 1130, 8, t); rrect(c, 250, 1130, 580, 16, 8, "#8a8f99")
    kernel(c, 540, 790, 1.9, 0, True)
    drop(c, 540, 800, 30, 1 - ss(1.2, 2.2, t)); s_ = ss(1.6, 2.6, t)
    for k in range(6):
        ang = k * math.pi / 3 + t * 0.6; puff(c, 540 + math.cos(ang) * 62 * s_, 795 + math.sin(ang) * 62 * s_, 24, s_)
    a = ss(3.2, 3.8, t)
    for k in range(6):
        ang = k * math.pi / 3 + 0.5; L = 118 + 14 * math.sin(t * 6)
        arrow(c, 540 + math.cos(ang) * 95, 795 + math.sin(ang) * 95, 540 + math.cos(ang) * L * 1.25, 795 + math.sin(ang) * L * 1.25, "#ffffff", 7, a, 18)
    tag(c, "buhar", 860, 600, MINT, ss(2.2, 2.7, t), 38, "c", "Bold")
def i3(c, t, d):
    k = ss(0.6, d - 2.2, t); sh = 7 * math.sin(t * 45) * k
    kernel(c, 360 + sh, 810, 1.45, 0)
    ca = ss(d - 2.0, d - 1.6, t)
    for pts in ([(330, 700), (372, 760), (340, 815), (392, 880)], [(372, 760), (430, 742)], [(340, 815), (290, 850)]):
        poly(c, pts, "#4a1a12", ca, 9, False)
    rrect(c, 760, 520, 56, 500, 28, "#ffffff", 0.9, 6); h = 440 * k
    rrect(c, 770, 1010 - h, 36, h, 18, RED); circ(c, 788, 1040, 46, RED)
    text(c, f"{int(lerp(20, 180, k))} °C", 788, 1160, 56, THEME["accent"], 1)
    tag(c, "basınç artıyor", 360, 1080, "#ffffff", ss(1.0, 1.5, t), 38, "c", "Bold")
def i4(c, t, d):
    T0 = 1.0
    if t < T0: kernel(c, 540 + 8 * math.sin(t * 50), 820, 1.4); return
    u = t - T0
    for k in range(14):
        ang = k * 2 * math.pi / 14; r0 = 150 + u * 520; a = 1 - ss(0.1, 0.6, u)
        line(c, 540 + math.cos(ang) * r0, 810 + math.sin(ang) * r0, 540 + math.cos(ang) * (r0 + 60), 810 + math.sin(ang) * (r0 + 60), "#ffffff", 9, a)
    for k in range(5):
        v = (u * 0.35 + k * 0.2) % 1; puff(c, 380 + k * 80 + 12 * math.sin(t * 2 + k), 620 - v * 120, 26, (1 - v) * ss(0.2, 0.6, u))
    popcorn(c, 540, 830, 1.45 * pop(t, T0, 0.5))
    tag(c, "patlamış mısır!", 540, 1150, THEME["accent"], ss(T0 + 2.8, T0 + 3.3, t), 44, "c", "Bold")
SCENES = [
 title_scene("Mısır neden", "patlar?", "Tanenin içindeki küçük patlama", hero),
 reason_scene("NEDEN 1", "İçinde bir damla su", ["Her tanenin içinde bir damla su", "ve bolca nişasta vardır."], i1),
 reason_scene("NEDEN 2", "Su buhara dönüşür", ["Isınan su buhara dönüşür;", "sert kabuk buharı dışarı bırakmaz."], i2),
 reason_scene("NEDEN 3", "Basınç yükselir", ["Basınç yükselir; yaklaşık 180 °C'de", "kabuk dayanamaz ve yarılır."], i3),
 reason_scene("NEDEN 4", "Nişasta köpürüp fırlar", ["Buhar genleşir, nişasta köpürüp", "dışarı fırlar ve hemen katılaşır."], i4),
 cards_scene("PEKİ YA", "Neden bazıları patlamaz?", [("Kabuk çatlaksa", "Buhar kaçar, basınç birikmez"), ("Tane kuruysa", "İçinde yeterli su yoktur"), ("Kapalı kapta sakla", "Nemini koruyan mısır iyi patlar")]),
 end_scene("Mısır patlamıyor;", "içindeki su kaçıyor.", hero),
]
if __name__ == "__main__":
    nb.main(SLUG, NARRATION, SCENES)
