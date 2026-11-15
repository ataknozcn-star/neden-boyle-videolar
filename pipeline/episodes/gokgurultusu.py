import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import numpy as np, skia
from nb import *
import nb

SLUG = "gok-gurultusu-neden-sonra-gelir"
nb.THEME.update(bg=["#3b3f63", "#23264a", "#11132a"], accent="#ffe066")
NARRATION = [
 "Gök gürültüsü neden şimşekten sonra gelir? İşte gecikmenin sırrı.",
 "Şimşek, bulutlarda biriken elektriğin bir anda boşalmasıdır.",
 "Şimşek, çevresindeki havayı bir anda binlerce dereceye ısıtır. Hava hızla genleşir ve patlama gibi bir ses çıkarır.",
 "Işık saniyede üç yüz bin kilometre yol alır. Ses ise yalnızca üç yüz kırk metre.",
 "Bu yüzden önce şimşeği görür, sonra gürültüyü duyarız. Aradaki her üç saniye, yaklaşık bir kilometre demektir.",
 "Siz de deneyin: şimşeği görünce saymaya başlayın, gürültüyü duyunca durun ve saniyeyi üçe bölün.",
 "Gök gürültüsü geç kalmıyor; ses yavaş yürüyor. Neden böyle? Artık biliyorsunuz.",
]
YEL = "#ffe066"; CL = "#b9bfdf"
def bolt(c, x, y, s=1.0, a=1.0, color=YEL):
    pts = [(10, 0), (-55, 120), (-8, 120), (-62, 260), (70, 85), (20, 85), (62, 0)]
    poly(c, [(x + px * s, y + py * s) for px, py in pts], color, a)
def hero(c, t):
    f = 1.0 if (t % 1.7) < 0.28 else 0.5
    bolt(c, 545, 900, 1.15, f); cloud(c, 530, 840, 1.9, 1, CL)
def i1(c, t, d):
    rrect(c, 100, 1110, 880, 22, 11, "#5a6190")
    if (t % 2.0) < 0.32 and t > 1.0:
        circ(c, 540, 820, 330, YEL, 0.10); bolt(c, 545, 770, 1.3)
    cloud(c, 530, 660, 2.3, 1, CL)
    for k, x in enumerate((370, 470, 570, 670)):
        text(c, "+", x, 640, 54, RED, ss(0.6 + k * 0.1, 1.0 + k * 0.1, t)); text(c, "−", x + 30, 760, 60, "#3d5cff", ss(0.9 + k * 0.1, 1.3 + k * 0.1, t))
def i2(c, t, d):
    for k in range(3):
        u = (t * 0.6 + k / 3) % 1; circ(c, 530, 800, 70 + u * 330, "#ff9a3c", (1 - u) * 0.9, 9)
    circ(c, 530, 800, 150, "#ff9a3c", 0.18 + 0.08 * math.sin(t * 8))
    bolt(c, 545, 560, 1.75)
def i3(c, t, d):
    for yy in (700, 960): line(c, 140, yy, 940, yy, "#ffffff", 4, 0.25)
    line(c, 940, 600, 940, 1040, "#ffffff", 6, 0.6)
    tag(c, "ışık", 140, 640, YEL, 1, 40, "l", "Bold"); tag(c, "300.000 km/sn", 920, 640, YEL, ss(1.2, 1.7, t), 38, "r", "Bold")
    tag(c, "ses", 140, 900, BLUE, 1, 40, "l", "Bold"); tag(c, "340 m/sn", 920, 900, BLUE, ss(4.2, 4.7, t), 38, "r", "Bold")
    u = ss(1.0, 1.25, t); x = lerp(140, 940, u)
    if u > 0: line(c, 140, 700, x, 700, YEL, 10, 0.5); circ(c, x, 700, 34, YEL, 0.3); circ(c, x, 700, 18, YEL)
    xs = 160 + max(0, t - 1.0) * 42
    for k in range(3):
        c.drawArc(skia.Rect.MakeLTRB(xs - 60 - k * 34, 960 - 60 - k * 12, xs + 20 - k * 34 + 40, 960 + 60 + k * 12), -55, 110, False, stroke(BLUE, 9, 1 - k * 0.28))
def i4(c, t, d):
    rrect(c, 60, 1090, 960, 26, 13, "#5a6190")
    rrect(c, 790, 980, 130, 110, 12, "#e8d9b8"); poly(c, [(770, 985), (855, 905), (940, 985)], "#c25b4a"); rrect(c, 838, 1030, 36, 60, 6, "#7a4a2a")
    if 0.8 < t < 1.15: circ(c, 270, 800, 260, YEL, 0.12); bolt(c, 275, 690, 1.2)
    cloud(c, 260, 600, 1.7, 1, CL)
    r = max(0, t - 1.1) * 165
    for k in range(3):
        rr = r - k * 46
        if rr > 30: c.drawArc(skia.Rect.MakeLTRB(270 - rr, 860 - rr, 270 + rr, 860 + rr), -18, 54, False, stroke(BLUE, 9, (1 - k * 0.3) * (1 - ss(520, 640, rr))))
    n = int(clamp((t - 1.1), 0, 3.01))
    if t > 1.1: text(c, f"{min(3, n + 1) if t < 4.1 else 3} sn", 620, 640, 84, "#ffffff", 1)
    tag(c, "3 sn ≈ 1 km", 620, 740, YEL, ss(4.3, 4.8, t), 50, "c", "Bold")
SCENES = [
 title_scene("Gök gürültüsü neden", "sonra gelir?", "Gecikmenin sırrı", hero),
 reason_scene("NEDEN 1", "Şimşek bir boşalmadır", ["Şimşek, bulutlarda biriken elektriğin", "bir anda boşalmasıdır."], i1),
 reason_scene("NEDEN 2", "Hava ısınır ve patlar", ["Şimşek havayı binlerce dereceye ısıtır;", "hızla genleşen hava gürler."], i2),
 reason_scene("NEDEN 3", "Işık hızlı, ses yavaş", ["Işık göz açıp kapayana dek ulaşır;", "ses ise yolda oyalanır."], i3),
 reason_scene("NEDEN 4", "Önce görür, sonra duyarız", ["Önce şimşeği görür, sonra gürültüyü", "duyarız. Her 3 saniye ≈ 1 kilometre."], i4),
 cards_scene("SİZ DE DENEYİN", "Fırtına ne kadar uzakta?", [("Şimşeği gör, saymaya başla", "Bin bir, bin iki, bin üç…"), ("Gürültüyü duyunca dur", "Kaç saniye geçti?"), ("Saniyeyi üçe böl", "Sonuç: yaklaşık kilometre")]),
 end_scene("Gürültü geç kalmıyor;", "ses yavaş yürüyor.", hero),
]
if __name__ == "__main__":
    nb.main(SLUG, NARRATION, SCENES)
