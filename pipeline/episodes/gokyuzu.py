import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import numpy as np, skia
from nb import *
import nb

SLUG = "gokyuzu-neden-mavi"
nb.THEME.update(bg=["#1d4e89", "#12305a", "#0a1a33"], accent="#7fd0ff")
NARRATION = [
 "Gökyüzü neden mavi? İşte ışığın kısa hikâyesi.",
 "Güneş ışığı beyaz görünür, ama aslında bütün renklerin karışımıdır.",
 "Her rengin dalga boyu farklıdır. Kırmızı uzun, mavi ise kısa dalgalıdır.",
 "Işık atmosfere girince hava molekülleriyle çarpışır. Kısa dalgalı mavi ışık, her yöne çok daha fazla saçılır.",
 "Bu yüzden nereye bakarsak bakalım, gözümüze mavi ışık ulaşır.",
 "Peki gün batımı neden kızıl? Işık daha uzun yol kat eder; mavi saçılıp kaybolur, geriye kızıl tonlar kalır.",
 "Gökyüzü boyalı değil; sadece ışığı saçıyor. Neden böyle? Artık biliyorsunuz.",
]
RAIN = ["#ff5d5d", "#ff9a3c", "#ffe066", "#6fd08c", "#6ec6f0", "#5b7bff", "#b07cff"]
def hero(c, t):
    sun(c, 540, 860, 120, t)
    cloud(c, 320 + 12 * math.sin(t), 1010, 1.1, 0.95); cloud(c, 770 - 10 * math.sin(t * 0.8), 740, 0.8, 0.9)
def i1(c, t, d):
    sun(c, 180, 800, 62, t)
    p = ss(0.6, 1.6, t); line(c, 285, 800, 285 + 190 * p, 800, "#ffffff", 14)
    q = ss(1.6, 2.8, t)
    if q > 0:
        for k, cl in enumerate(RAIN):
            ang = math.radians(-27 + k * 9); line(c, 560, 800, 560 + 400 * q * math.cos(ang), 800 + 400 * q * math.sin(ang), cl, 13)
    poly(c, [(520, 680), (640, 900), (400, 900)], "#cfe8ff", 0.35); poly(c, [(520, 680), (640, 900), (400, 900)], "#ffffff", 0.95, sw=6)
    tag(c, "beyaz ışık", 380, 750, "#ffffff", ss(1.0, 1.5, t), 34, "c")
    tag(c, "bütün renkler", 800, 1075, THEME["accent"], ss(2.8, 3.3, t), 38, "c", "Bold")
def wave(c, y, wl, color, t, amp=48):
    p = skia.Path()
    for k in range(0, 861, 6):
        x = 110 + k; yy = y + amp * math.sin(k / wl * 2 * math.pi - t * 3)
        p.moveTo(x, yy) if k == 0 else p.lineTo(x, yy)
    c.drawPath(p, stroke(color, 10))
def i2(c, t, d):
    wave(c, 630, 300, "#ff5d5d", t); tag(c, "kırmızı: uzun dalga", 540, 760, "#ff9a9a", ss(1.6, 2.1, t), 40, "c", "Bold")
    wave(c, 930, 95, "#5b9bff", t); tag(c, "mavi: kısa dalga", 540, 1060, "#9cc6ff", ss(2.8, 3.3, t), 40, "c", "Bold")
_r = np.random.default_rng(2)
MOL = [(float(_r.uniform(180, 900)), float(_r.uniform(700, 1090))) for _ in range(16)]
def i3(c, t, d):
    for (x, y) in MOL: circ(c, x, y, 12, "#ffffff", 0.45)
    p = ss(0.8, 2.0, t); line(c, 90, 590, 90 + 900 * p, 590, "#ff5d5d", 10)
    tag(c, "kırmızı: dümdüz geçer", 540, 550, "#ff9a9a", ss(1.8, 2.3, t), 34, "c")
    q = ss(2.4, 3.3, t); line(c, 90, 880, 90 + 430 * q, 880, "#5b9bff", 10)
    circ(c, 540, 880, 20, "#ffffff")
    if t > 3.3:
        for k in range(12):
            ang = k * math.pi / 6 + 0.26; L = ((t - 3.3) * 170 + k * 37) % 210; a = 1 - L / 210
            line(c, 540 + math.cos(ang) * (34 + L), 880 + math.sin(ang) * (34 + L), 540 + math.cos(ang) * (70 + L), 880 + math.sin(ang) * (70 + L), "#6fb0ff", 8, a)
    tag(c, "mavi: her yöne saçılır", 540, 1150, "#9cc6ff", ss(3.6, 4.1, t), 34, "c")
def i4(c, t, d):
    rrect(c, 60, 1085, 960, 70, 20, "#2e7d4f")
    circ(c, 540, 975, 36, "#ffd7b0"); rrect(c, 506, 1012, 68, 80, 26, GOLD)
    sun(c, 860, 590, 50, t)
    for k in range(9):
        ang = math.radians(200 + k * 17.5); sx = 540 + 430 * math.cos(ang); sy = 960 + 430 * math.sin(ang)
        u = (t * 0.45 + k * 0.137) % 1; x0 = lerp(sx, 540, u * 0.78); y0 = lerp(sy, 960, u * 0.78)
        arrow(c, x0, y0, lerp(sx, 540, u * 0.78 + 0.11), lerp(sy, 960, u * 0.78 + 0.11), "#7fd0ff", 8, ss(0, 0.15, u) * (1 - ss(0.8, 1, u)), 20)
SCENES = [
 title_scene("Gökyüzü", "neden mavi?", "Işığın kısa hikâyesi", hero),
 reason_scene("NEDEN 1", "Beyaz ışık, tüm renkler", ["Güneş ışığı beyaz görünür;", "aslında bütün renklerin karışımıdır."], i1),
 reason_scene("NEDEN 2", "Her rengin dalgası farklı", ["Kırmızı ışık uzun dalgalıdır,", "mavi ışık ise kısa dalgalı."], i2),
 reason_scene("NEDEN 3", "Mavi daha çok saçılır", ["Işık hava molekülleriyle çarpışır;", "kısa dalgalı mavi her yöne saçılır."], i3),
 reason_scene("NEDEN 4", "Mavi her yönden gelir", ["Nereye bakarsak bakalım,", "gözümüze saçılan mavi ışık ulaşır."], i4),
 cards_scene("BONUS", "Gün batımı neden kızıl?", [("Işık uzun yol kat eder", "Güneş ufka yakınken"), ("Mavi saçılıp kaybolur", "Yol boyunca dağılır"), ("Geriye kızıl kalır", "Turuncu ve kırmızı tonlar")]),
 end_scene("Gökyüzü boyalı değil;", "ışığı saçıyor.", hero),
]
if __name__ == "__main__":
    nb.main(SLUG, NARRATION, SCENES)
