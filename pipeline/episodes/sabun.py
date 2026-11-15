import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import numpy as np, skia
from nb import *
import nb

SLUG = "sabun-nasil-temizler"
nb.THEME.update(bg=["#2b5d6e", "#1a3a47", "#0d1f27"], accent="#9ff0e0")
NARRATION = [
 "Sabun kiri nasıl söker? İşte köpüğün kısa kimyası.",
 "Kirin çoğu yağlıdır. Yağ ve su ise birbirine karışmaz; su tek başına yağı sökemez.",
 "Sabun molekülünün iki ucu vardır: bir ucu suyu sever, diğer ucu yağı.",
 "Yağı seven uçlar kire saplanır ve onu her yandan sarar.",
 "Böylece kir, minik bir topun içine hapsolur. Su da bu topu alıp götürür.",
 "İyi bir temizlik için: ellerinizi en az yirmi saniye ovun, iyice köpürtün ve bol suyla durulayın.",
 "Sabun kiri yok etmiyor; paketleyip suya teslim ediyor. Neden böyle? Artık biliyorsunuz.",
]
def smol(c, x, y, ang, L=70, a=1.0, hr=15, w=6, amp=8):
    p = skia.Path(); p.moveTo(x, y); n = 6
    for k in range(1, n + 1):
        dd = L * k / n; off = amp if k % 2 else -amp
        p.lineTo(x + math.cos(ang) * dd - math.sin(ang) * off, y + math.sin(ang) * dd + math.cos(ang) * off)
    c.drawPath(p, stroke(GOLD, w, a)); circ(c, x, y, hr, BLUE, a)
def hero(c, t):
    rrect(c, 340, 850, 400, 190, 70, "#ffb3d1"); rrect(c, 372, 882, 336, 126, 46, "#ff8fbc", 1, 6)
    for k in range(8):
        u = (t * 0.28 + k * 0.13) % 1; x = 380 + (k * 97) % 330; r = 16 + (k % 3) * 9
        circ(c, x + 10 * math.sin(t * 2 + k), 850 - u * 250, r, "#ffffff", 0.9 * (1 - u), 5)
def i1(c, t, d):
    rrect(c, 100, 1050, 880, 26, 13, "#8aa0aa")
    c.drawOval(skia.Rect.MakeLTRB(380, 960, 700, 1056), fill(GOLD)); tag(c, "yağ", 540, 1022, "#6b4a00", 1, 36, "c", "Bold")
    for k in range(5):
        u = (t * 0.5 + k * 0.2) % 1; xk = 440 + k * 50; sg = -1 if k < 2 else 1
        if u < 0.6: x = xk; y = 540 + u / 0.6 * 390
        else: x = xk + sg * (u - 0.6) / 0.4 * 260; y = 930 + (u - 0.6) / 0.4 * 95
        drop(c, x, y, 19, ss(0, 0.1, u) * (1 - ss(0.9, 1, u)))
    tag(c, "su", 760, 620, BLUE, ss(0.8, 1.3, t), 38, "c", "Bold")
def i2(c, t, d):
    w = 4 * math.sin(t * 2)
    smol(c, 300, 780 + w, 0.0, 560, 1, 78, 18, 42)
    tag(c, "suyu sever", 300, 950, BLUE, ss(2.6, 3.1, t), 40, "c", "Bold"); tag(c, "yağı sever", 690, 950, GOLD, ss(3.9, 4.4, t), 40, "c", "Bold")
def i3(c, t, d):
    circ(c, 540, 810, 115, GOLD, 0.95); tag(c, "kir", 540, 824, "#6b4a00", 1, 40, "c", "Bold")
    for k in range(14):
        ang = k * 2 * math.pi / 14; dist = lerp(400, 182, ss(0.8 + k * 0.1, 2.4 + k * 0.1, t))
        smol(c, 540 + math.cos(ang) * dist, 810 + math.sin(ang) * dist, ang + math.pi, 78, 1, 17, 7)
def i4(c, t, d):
    for k, yy in enumerate((600, 740, 900, 1040)):
        p = skia.Path()
        for j in range(0, 901, 12):
            x = 90 + j; y = yy + 14 * math.sin(j / 70 - t * 4 + k); p.moveTo(x, y) if j == 0 else p.lineTo(x, y)
        c.drawPath(p, stroke(BLUE, 7, 0.55))
    cx = lerp(330, 760, ss(1.6, d - 0.6, t)); cy = 820 + 18 * math.sin(t * 2)
    circ(c, cx, cy, 72, GOLD, 0.95)
    for k in range(12):
        ang = k * math.pi / 6 + t * 0.4; smol(c, cx + math.cos(ang) * 128, cy + math.sin(ang) * 128, ang + math.pi, 54, 1, 14, 6, 6)
    tag(c, "misel", cx, cy - 170, THEME["accent"], ss(1.0, 1.5, t), 38, "c", "Bold")
SCENES = [
 title_scene("Sabun kiri", "nasıl söker?", "Köpüğün kısa kimyası", hero),
 reason_scene("NEDEN 1", "Yağ ve su karışmaz", ["Kirin çoğu yağlıdır.", "Su tek başına yağı sökemez."], i1),
 reason_scene("NEDEN 2", "Sabunun iki ucu var", ["Molekülün bir ucu suyu sever,", "diğer ucu yağı."], i2),
 reason_scene("NEDEN 3", "Sabun kiri sarar", ["Yağı seven uçlar kire saplanır", "ve onu her yandan sarar."], i3),
 reason_scene("NEDEN 4", "Su, topu alıp götürür", ["Kir minik bir topa hapsolur;", "su da bu topu alıp götürür."], i4),
 cards_scene("İPUÇLARI", "İyi temizlik için", [("En az 20 saniye ov", "Sabunun kiri sarması zaman alır"), ("İyice köpürt", "Sabun her yere ulaşsın"), ("Bol suyla durula", "Kir, suyla birlikte akar")]),
 end_scene("Sabun kiri yok etmiyor;", "paketleyip götürüyor.", hero),
]
if __name__ == "__main__":
    nb.main(SLUG, NARRATION, SCENES)
