import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import numpy as np, skia
from nb import *
import nb

SLUG = "ekmek-neden-bayatlar"
nb.THEME.update(bg=["#5a3418", "#3a200e", "#1f1108"], accent="#ffb86b")
NARRATION = [
 "Ekmek neden bayatlar? Cevap, kurumaktan ibaret değil.",
 "Ekmeğin içi nişastayla doludur. Fırında nişasta su çeker, şişer ve yumuşar.",
 "Ekmek soğuyunca nişasta molekülleri yeniden dizilip kristalleşir.",
 "Bu sırada su, ekmeğin içinden kabuğa doğru göç eder. İç sertleşir, kabuk ise yumuşar.",
 "Şaşırtıcı ama buzdolabı bu süreci hızlandırır. Ekmek dolapta daha çabuk bayatlar.",
 "Ekmek taze kalsın diye: oda sıcaklığında saklayın, uzun süre için dondurun ve yemeden önce ısıtın.",
 "Bayat ekmek kurumuş değil; kristalleşmiş. Neden böyle? Artık biliyorsunuz.",
]
def loaf(c, cx, cy, s=1.0):
    p = skia.Path(); p.moveTo(cx - 240 * s, cy + 95 * s); p.cubicTo(cx - 290 * s, cy - 170 * s, cx + 290 * s, cy - 170 * s, cx + 240 * s, cy + 95 * s); p.close()
    c.drawPath(p, fill("#d99a4e")); c.drawPath(p, stroke("#a8662a", 10 * s))
    for k in (-1, 0, 1): line(c, cx + k * 115 * s - 28 * s, cy - 75 * s, cx + k * 115 * s + 28 * s, cy - 15 * s, "#f6dcae", 13 * s)
def hero(c, t): loaf(c, 540, 930, 1.15)
def i1(c, t, d):
    r = 95 + 70 * ss(1.4, 3.6, t)
    circ(c, 540, 810, r, "#f3e2c0"); circ(c, 540, 810, r, "#c9a36b", 1, 8)
    for k in range(6):
        ang = k * math.pi / 3 + 0.4; u = ss(1.0 + k * 0.25, 2.6 + k * 0.25, t); dist = lerp(360, r * 0.5, u)
        drop(c, 540 + math.cos(ang) * dist, 810 + math.sin(ang) * dist, 17, 1 - 0.35 * u)
    tag(c, "nişasta", 540, 822, "#7a4a1a", 1, 38, "c", "Bold"); tag(c, "su", 860, 560, BLUE, ss(1.0, 1.5, t), 38, "c", "Bold")
_r = np.random.default_rng(6)
OFF = [[(float(_r.uniform(-48, 48)), float(_r.uniform(-48, 48))) for j in range(9)] for i in range(6)]
def i2(c, t, d):
    m = ss(1.2, 3.4, t)
    for i in range(6):
        p = skia.Path()
        for j in range(9):
            x = 180 + j * 90 + OFF[i][j][0] * (1 - m); y = 600 + i * 82 + OFF[i][j][1] * (1 - m) + (1 - m) * 8 * math.sin(t * 2 + i + j)
            p.moveTo(x, y) if j == 0 else p.lineTo(x, y)
        c.drawPath(p, stroke(mixcol("#f6dcae", "#ffffff", m), 11))
    tag(c, "düzensiz", 540, 1130, None, (1 - ss(1.2, 2.2, t)), 36, "c"); tag(c, "düzenli: kristal", 540, 1130, THEME["accent"], ss(3.0, 3.6, t), 38, "c", "Bold")
def i3(c, t, d):
    rrect(c, 280, 540, 520, 500, 130, "#b8742f"); rrect(c, 318, 578, 444, 424, 100, "#f3dfb5")
    for k in range(8):
        ang = k * math.pi / 4 + 0.2; u = (t * 0.3 + k / 8) % 1; dist = 40 + u * 185
        drop(c, 540 + math.cos(ang) * dist, 800 + math.sin(ang) * dist * 0.95, 14, math.sin(math.pi * u))
    tag(c, "iç: sertleşir", 540, 812, "#7a4a1a", ss(2.6, 3.1, t), 36, "c", "Bold"); tag(c, "kabuk: yumuşar", 540, 1110, THEME["accent"], ss(3.8, 4.3, t), 36, "c", "Bold")
def i4(c, t, d):
    rrect(c, 350, 480, 380, 660, 34, "#dfe9f2"); line(c, 350, 720, 730, 720, "#9fb3c6", 8)
    line(c, 690, 560, 690, 660, "#9fb3c6", 12); line(c, 690, 780, 690, 900, "#9fb3c6", 12)
    loaf(c, 520, 990, 0.42)
    for k in range(3):
        yy = 560 + k * 60; p = skia.Path()
        for j in range(0, 221, 10):
            x = 400 + j; y = yy + 10 * math.sin(j / 30 + t * 4 + k); p.moveTo(x, y) if j == 0 else p.lineTo(x, y)
        c.drawPath(p, stroke(BLUE, 7))
    k = pop(t, 2.2, 0.4)
    if k > 0:
        c.save(); c.translate(760, 500); c.scale(k, k); circ(c, 0, 0, 46, RED); text(c, "!", 0, 24, 66, "#ffffff"); c.restore()
SCENES = [
 title_scene("Ekmek neden", "bayatlar?", "Kurumaktan ibaret değil", hero),
 reason_scene("NEDEN 1", "Nişasta su çeker", ["Fırında nişasta su çeker,", "şişer ve yumuşar."], i1),
 reason_scene("NEDEN 2", "Nişasta kristalleşir", ["Ekmek soğuyunca nişasta molekülleri", "yeniden dizilip kristalleşir."], i2),
 reason_scene("NEDEN 3", "Su kabuğa göç eder", ["Su içten kabuğa doğru göç eder.", "İç sertleşir, kabuk yumuşar."], i3),
 reason_scene("NEDEN 4", "Dolap hızlandırır", ["Buzdolabı bu süreci hızlandırır;", "ekmek dolapta daha çabuk bayatlar."], i4, 0.9),
 cards_scene("İPUÇLARI", "Ekmek taze kalsın", [("Oda sıcaklığında sakla", "Bez torba ya da ekmek kutusunda"), ("Uzun süre için dondur", "Dondurucu, bayatlamayı durdurur"), ("Yemeden önce ısıt", "Isı, nişastayı yeniden yumuşatır")]),
 end_scene("Bayat ekmek kuru değil;", "kristalleşmiş.", hero),
]
if __name__ == "__main__":
    nb.main(SLUG, NARRATION, SCENES)
