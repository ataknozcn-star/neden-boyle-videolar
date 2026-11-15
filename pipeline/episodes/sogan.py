"""Örnek bölüm: Soğan doğrarken neden ağlarız?  Yeni bölümler bu dosya örnek alınarak yazılır."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import numpy as np, skia
from nb import *
import nb

SLUG = "sogan-neden-aglatir"
NARRATION = [
 "Soğan doğrarken neden ağlarız? İşte gözyaşının kısa kimyası.",
 "Bıçak soğanı kestiğinde hücreler parçalanır. Normalde ayrı duran bir enzim ile kükürtlü bileşikler birbirine karışır.",
 "Bu karışım, saniyeler içinde uçucu bir gaza dönüşür. Gaz havaya karışır ve gözlerinize doğru yükselir.",
 "Gaz göze ulaşınca sinir uçlarını tahriş eder. Sinirler de beyne alarm verir.",
 "Beyin, gözyaşı bezlerine emir gönderir: Yıka! Yani gözyaşı, gözün kendini koruma yoludur.",
 "Daha az gözyaşı için: soğanı önce soğutun, keskin bir bıçak kullanın ve mutfağı havalandırın.",
 "Soğan sizi üzmüyor; sadece kendini savunuyor. Neden böyle? Artık biliyorsunuz.",
]
ONION1, ONION2, SKIN = "#c2538f", "#7a2a5c", "#4a1838"

def bulb_path(R):
    p = skia.Path(); p.moveTo(0, -R * 1.08)
    p.cubicTo(R * 0.95, -R * 0.95, R * 1.3, R * 0.25, 0, R)
    p.cubicTo(-R * 1.3, R * 0.25, -R * 0.95, -R * 0.95, 0, -R * 1.08); p.close(); return p

def onion(c, x, y, R, rot=0.0, scale=1.0, a=1.0):
    if scale <= 0.01: return
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(scale, scale)
    # shadow
    sh = fill("#000000", 0.28 * a); sh.setMaskFilter(skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 18))
    c.drawOval(skia.Rect.MakeLTRB(-R * 0.8, R * 0.98, R * 0.8, R * 1.14), sh)
    # roots
    for i in range(-3, 4):
        c.drawLine(i * R * 0.05, R * 0.97, i * R * 0.11, R * 1.13, stroke("#e8cfa6", 5, a))
    # sprout
    sp = skia.Path(); sp.moveTo(-R * 0.13, -R * 0.98); sp.quadTo(-R * 0.05, -R * 1.25, -R * 0.2, -R * 1.48)
    sp.quadTo(R * 0.06, -R * 1.3, R * 0.02, -R * 1.62); sp.quadTo(R * 0.2, -R * 1.3, R * 0.13, -R * 0.98); sp.close()
    c.drawPath(sp, fill("#b98a4e", a))
    bp = bulb_path(R); p = skia.Paint(AntiAlias=True)
    p.setShader(skia.GradientShader.MakeRadial(center=(-R * 0.35, -R * 0.35), radius=R * 1.7,
                colors=[col("#e07ab0", a), col(ONION1, a), col(ONION2, a)], positions=[0, 0.45, 1]))
    c.drawPath(bp, p)
    c.save(); c.clipPath(bp, True)
    for k in (0.62, 0.28):
        lp = skia.Path(); lp.moveTo(0, -R * 1.08); lp.cubicTo(R * 0.95 * k, -R * 0.95, R * 1.3 * k, R * 0.25, 0, R)
        c.drawPath(lp, stroke(SKIN, 5, 0.55 * a))
        lp = skia.Path(); lp.moveTo(0, -R * 1.08); lp.cubicTo(-R * 0.95 * k, -R * 0.95, -R * 1.3 * k, R * 0.25, 0, R)
        c.drawPath(lp, stroke(SKIN, 5, 0.55 * a))
    hl = skia.Path(); hl.moveTo(-R * 0.55, -R * 0.55); hl.quadTo(-R * 0.82, -R * 0.1, -R * 0.62, R * 0.3)
    c.drawPath(hl, stroke("#ffffff", 16, 0.22 * a))
    c.restore(); c.restore()

# ---------- scenes ----------
def s0(c, t, d):
    a1 = ss(0.05, 0.5, t); a2 = ss(0.35, 0.85, t)
    text(c, "Soğan doğrarken", W / 2, 330 + (1 - a1) * 20, 80, CREAM, a1)
    text(c, "neden ağlarız?", W / 2, 452 + (1 - a2) * 20, 108, PINK, a2)
    sc = eback((t - 0.3) / 0.7) if t > 0.3 else 0
    onion(c, W / 2, 900, 230, rot=4 * math.sin(t * 2.2), scale=sc)
    rng = np.random.default_rng(11)
    for i in range(8):
        x = W / 2 + rng.choice([-1, 1]) * rng.uniform(300, 430); ph = rng.uniform(0, 1.6); sp = rng.uniform(1.5, 2.1)
        tt = (t - 1.3 - ph * 0.6)
        if tt < 0: continue
        u = (tt % sp) / sp
        drop(c, x, 640 + u * u * 560, 20 + (i % 3) * 5, a=ss(0, 0.12, u) * (1 - ss(0.8, 1, u)))
    text(c, "Gözyaşının kısa kimyası", W / 2, 1340, 42, CREAM, 0.8 * ss(2.3, 2.9, t), "Medium")

_rng1 = np.random.default_rng(5)
CW, CH, GAP, GX, GY = 190, 150, 16, 136, 540
CUT_A, CUT_B = (70, 560), (1010, 1010)
CELLS = []
for r in range(3):
    for q in range(4):
        cx = GX + q * (CW + GAP) + CW / 2; cy = GY + r * (CH + GAP) + CH / 2
        ax, ay = CUT_A; bx, by = CUT_B; L = math.hypot(bx - ax, by - ay)
        u = ((cx - ax) * (bx - ax) + (cy - ay) * (by - ay)) / L ** 2
        dist = ((cx - ax) * (by - ay) - (cy - ay) * (bx - ax)) / L
        dots = []
        for k in range(3): dots.append(("e", cx - 48 + _rng1.uniform(-17, 17), cy + _rng1.uniform(-17, 17)))
        for k in range(4): dots.append(("s", cx + 46 + _rng1.uniform(-26, 26), cy + _rng1.uniform(-44, 44)))
        tg = []
        for k in range(7):
            uu = clamp(u + _rng1.uniform(-0.2, 0.2), 0.05, 0.95); off = _rng1.uniform(-62, 62)
            tg.append((ax + (bx - ax) * uu - (by - ay) / L * off, ay + (by - ay) * uu + (bx - ax) / L * off))
        CELLS.append(dict(cx=cx, cy=cy, u=u, dist=dist, broken=abs(dist) < 95, dots=dots, tg=tg))

def s1(c, t, d):
    header(c, "NEDEN 1", "Hücreler parçalanır", t)
    ga = ss(0.2, 0.7, t)
    T0, TD = 1.7, 0.9; prog = eout((t - T0) / TD) if t > T0 else 0
    for ce in CELLS:
        tc = T0 + ce["u"] * TD * 0.75; k = ss(tc, tc + 0.5, t) if ce["broken"] else 0
        sgn = 1 if ce["dist"] > 0 else -1; L = math.hypot(CUT_B[0] - CUT_A[0], CUT_B[1] - CUT_A[1])
        ox = -(CUT_B[1] - CUT_A[1]) / L * 9 * k * -sgn; oy = (CUT_B[0] - CUT_A[0]) / L * 9 * k * -sgn
        r = skia.Rect.MakeXYWH(ce["cx"] - CW / 2 + ox, ce["cy"] - CH / 2 + oy, CW, CH)
        c.drawRoundRect(r, 30, 30, fill(CREAM, 0.07 * ga))
        sp = stroke("#e9b9d3", 5, (0.8 - 0.45 * k) * ga)
        if k > 0.3: sp.setPathEffect(skia.DashPathEffect.Make([22, 16], 0))
        c.drawRoundRect(r, 30, 30, sp)
        c.drawCircle(ce["cx"] - 48 + ox, ce["cy"] + oy, 40, stroke(GOLD, 4, 0.75 * ga * (1 - k)))
        for (kind, x, y), (tx, ty) in zip(ce["dots"], ce["tg"]):
            m = eout((t - tc - 0.1) / 1.6) if (ce["broken"] and t > tc) else 0
            jx = math.sin(t * 3 + x) * 5 * m; jy = math.cos(t * 2.6 + y) * 5 * m
            c.drawCircle(lerp(x + ox, tx, m) + jx, lerp(y + oy, ty, m) + jy, 11, fill(GOLD if kind == "e" else PINK, ga))
    if prog > 0:
        ax, ay = CUT_A; bx, by = CUT_B; px, py = lerp(ax, bx, prog), lerp(ay, by, prog)
        fa = 1 - ss(T0 + TD + 0.2, T0 + TD + 1.2, t)
        g = stroke("#ffffff", 22, 0.25 * fa); g.setMaskFilter(skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 12))
        c.drawLine(ax, ay, px, py, g); c.drawLine(ax, ay, px, py, stroke("#ffffff", 6, 0.95 * fa))
        if prog < 1:  # blade
            ang = math.degrees(math.atan2(by - ay, bx - ax))
            c.save(); c.translate(px, py); c.rotate(ang)
            bl = skia.Path(); bl.moveTo(20, 0); bl.lineTo(-250, -70); bl.lineTo(-330, -70); bl.lineTo(-330, 0); bl.close()
            c.drawPath(bl, fill("#dfe6ee", 0.95)); c.drawRoundRect(skia.Rect.MakeXYWH(-520, -62, 195, 50), 20, 20, fill("#8a5a34")); c.restore()
    la = ss(3.2, 3.8, t); y = 1130
    c.drawCircle(250, y - 13, 13, fill(GOLD, la)); text(c, "enzim", 276, y, 36, GOLD, la, "Medium", align="l")
    c.drawCircle(470, y - 13, 13, fill(PINK, la)); text(c, "kükürtlü bileşikler", 496, y, 36, PINK, la, "Medium", align="l")
    caption(c, ["Bıçak hücreleri parçalar. Ayrı duran enzim", "ve kükürtlü bileşikler birbirine karışır."], t, 1.0, 1262)

def half_onion(c, x, y, R, a=1.0):
    c.save(); c.translate(x, y)
    sh = fill("#000000", 0.28 * a); sh.setMaskFilter(skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 18))
    c.drawOval(skia.Rect.MakeLTRB(-R * 0.8, R * 0.95, R * 0.8, R * 1.1), sh)
    hw0 = R * 1.085
    bp = skia.Path(); bp.moveTo(-hw0, 0); bp.cubicTo(-hw0, R * 1.35, hw0, R * 1.35, hw0, 0); bp.close(); p = skia.Paint(AntiAlias=True)
    p.setShader(skia.GradientShader.MakeRadial(center=(-R * 0.35, 0), radius=R * 1.6, colors=[col("#e07ab0", a), col(ONION1, a), col(ONION2, a)], positions=[0, 0.45, 1]))
    c.drawPath(bp, p)
    hw = R * 1.085; hh = R * 0.3
    c.drawOval(skia.Rect.MakeLTRB(-hw, -hh, hw, hh), fill("#f7e6f0", a))
    for k in (0.8, 0.6, 0.4, 0.2):
        c.drawOval(skia.Rect.MakeLTRB(-hw * k, -hh * k, hw * k, hh * k), stroke("#d07aa8", 5, 0.8 * a))
    c.drawOval(skia.Rect.MakeLTRB(-hw, -hh, hw, hh), stroke(ONION2, 7, a))
    c.restore()

_rng2 = np.random.default_rng(9)
GAS = [dict(b=0.4 + i * 0.2 + _rng2.uniform(0, 0.12), x=540 + _rng2.uniform(-170, 170), ph=_rng2.uniform(0, 6.28),
            sp=_rng2.uniform(105, 140), r=_rng2.uniform(15, 25)) for i in range(30)]

def s2(c, t, d):
    header(c, "NEDEN 2", "Bir gaz doğar", t)
    a = ss(0.2, 0.7, t); OY = 985
    half_onion(c, W / 2, OY, 200, a)
    for g in GAS:
        age = t - g["b"]
        if age < 0: continue
        oy = OY - 15
        if age < 0.55:
            m = eout(age / 0.55)
            c.drawCircle(lerp(g["x"] - 70, g["x"], m), lerp(oy + 34, oy, m), 11, fill(GOLD, a))
            c.drawCircle(lerp(g["x"] + 70, g["x"], m), lerp(oy + 34, oy, m), 11, fill(PINK, a))
        else:
            ag = age - 0.55
            if ag < 0.25: c.drawCircle(g["x"], oy, 14 + ag * 150, stroke("#ffffff", 4, (1 - ag / 0.25) * 0.8))
            y = oy - g["sp"] * ag ** 1.08; x = g["x"] + 34 * math.sin(ag * 1.9 + g["ph"])
            al = ss(0, 0.2, ag) * (1 - ss(520, 430, y) if False else ss(430, 540, y))
            puff(c, x, y, g["r"] * (0.7 + 0.12 * ag), al * a)
    la = ss(2.4, 3.0, t)
    c.drawLine(668, 650, 722, 606, stroke(MINT, 3, 0.8 * la))
    text(c, "uçucu gaz", 736, 600, 40, MINT, la, "Bold", align="l")
    text(c, "syn-propanetiyal-S-oksit", 736, 638, 22, MINT, 0.65 * la, "Regular", align="l")
    caption(c, ["Karışım saniyeler içinde uçucu bir gaza", "dönüşür ve gözlere doğru yükselir."], t, 0.9, 1262)

EX, EY, EW, EH = 500, 850, 290, 135
BRAIN = (800, 520); GLAND = (250, 700)
_rng3 = np.random.default_rng(21)
DRIFT = [dict(b=_rng3.uniform(0, 2.2), sx=_rng3.uniform(40, 420), sy=_rng3.uniform(1130, 1200), tx=EX + _rng3.uniform(-210, 210),
              ty=EY + _rng3.uniform(-40, 60), r=_rng3.uniform(15, 24), ph=_rng3.uniform(0, 6)) for i in range(16)]
NERVE = ((EX + EW, EY), (EX + EW + 90, 640), BRAIN)

def nerve(c, a):
    p = skia.Path(); p.moveTo(*NERVE[0]); p.quadTo(NERVE[1][0], NERVE[1][1], NERVE[2][0], NERVE[2][1] + 40)
    c.drawPath(p, stroke("#b79ad0", 7, 0.55 * a))

def s3(c, t, d):
    header(c, "NEDEN 3", "Göz alarm verir", t)
    a = ss(0.2, 0.7, t); red = ss(1.3, 3.2, t)
    nerve(c, a)
    c.save(); c.saveLayerAlpha(None, int(255 * a)); eye(c, EX, EY, EW, EH, red=red, look=(-18 * (1 - red), 14 * (1 - red))); c.restore(); c.restore()
    for g in DRIFT:
        age = t - g["b"]
        if age < 0: continue
        m = eout(age / 1.9); x = lerp(g["sx"], g["tx"], m) + 16 * math.sin(age * 2.4 + g["ph"]); y = lerp(g["sy"], g["ty"], m)
        puff(c, x, y, g["r"], ss(0, 0.25, age) * (1 - ss(1.7, 2.6, age)) * a)
    for k in range(6):
        tp = t - 2.5 - k * 0.5
        if 0 < tp < 0.8:
            x, y = qbez(NERVE[0], NERVE[1], (NERVE[2][0], NERVE[2][1] + 40), tp / 0.8)
            c.drawCircle(x, y, 26, fill(GOLD, 0.25)); c.drawCircle(x, y, 13, fill(GOLD))
    al = ss(3.1, 3.4, t); pl = ((t - 3.1) % 0.7) / 0.7 if t > 3.1 else 0
    node(c, BRAIN[0], BRAIN[1], "beyin", a, RED if al > 0.5 else GOLD, pulse=pl if al > 0 else 0)
    if al > 0:
        s = eback((t - 3.1) / 0.4); c.save(); c.translate(BRAIN[0] + 130, BRAIN[1] - 62); c.scale(s, s)
        c.drawCircle(0, 0, 36, fill(RED)); text(c, "!", 0, 19, 52, "#ffffff"); c.restore()
    text(c, "sinir", NERVE[1][0] + 34, 690, 30, "#b79ad0", 0.9 * a, "Medium", align="l")
    caption(c, ["Gaz, sinir uçlarını tahriş eder;", "sinirler beyne alarm verir."], t, 0.9, 1262)

def s4(c, t, d):
    header(c, "NEDEN 4", "Gözyaşı savunmadır", t)
    a = ss(0.2, 0.7, t); red = 1 - 0.75 * ss(3.2, 6.2, t); wet = ss(2.2, 3.4, t)
    nerve(c, a * 0.6)
    P0, P1, P2 = (BRAIN[0] - 70, BRAIN[1]), (470, 470), (GLAND[0] + 62, GLAND[1] - 12)
    p = skia.Path(); p.moveTo(*P0); p.quadTo(P1[0], P1[1], P2[0], P2[1]); c.drawPath(p, stroke(BLUE, 7, 0.45 * a))
    for k in range(5):
        tp = t - 0.5 - k * 0.45
        if 0 < tp < 0.9:
            x, y = qbez(P0, P1, P2, tp / 0.9); c.drawCircle(x, y, 26, fill(BLUE, 0.25)); c.drawCircle(x, y, 13, fill(BLUE))
    gp = ss(1.3, 1.7, t); gs = 1 + 0.12 * math.sin(t * 7) * ss(1.4, 2.0, t)
    c.save(); c.translate(*GLAND); c.scale(gs, gs)
    c.drawOval(skia.Rect.MakeLTRB(-62, -44, 62, 44), fill("#3f7fa6", a)); c.drawOval(skia.Rect.MakeLTRB(-62, -44, 62, 44), stroke(BLUE, 5, a * (0.5 + 0.5 * gp))); c.restore()
    text(c, "gözyaşı bezi", GLAND[0] + 50, GLAND[1] - 72, 32, BLUE, a, "Medium", align="r")
    c.save(); c.saveLayerAlpha(None, int(255 * a)); eye(c, EX, EY, EW, EH, red=red, wet=wet); c.restore(); c.restore()
    rng = np.random.default_rng(4)
    for i in range(9):  # lingering gas washed away
        x = EX + rng.uniform(-230, 230); y = EY + rng.uniform(-70, 70); r = rng.uniform(14, 22)
        k = ss(2.6 + i * 0.12, 4.2 + i * 0.12, t)
        puff(c, x, y + k * 260, r, (1 - k) * a)
    for i, dx in enumerate((-150, -20, 120)):
        tt = t - 2.7 - i * 0.35
        if tt < 0: continue
        u = (tt % 1.25) / 1.25; x = EX + dx; y0 = EY + EH * 0.95 - abs(dx) * 0.28
        drop(c, x, y0 + 20 + u * u * 250, 24, a=ss(0, 0.15, u) * (1 - ss(0.82, 1, u)))
    node(c, BRAIN[0], BRAIN[1], "beyin", a, GOLD)
    ya = ss(2.4, 2.7, t) * (1 - ss(4.6, 5.0, t))
    if ya > 0:
        s = eback((t - 2.4) / 0.4); c.save(); c.translate(BRAIN[0] + 20, BRAIN[1] - 108); c.scale(s, s)
        c.drawRoundRect(skia.Rect.MakeXYWH(-105, -44, 210, 82), 41, 41, fill(BLUE, ya)); text(c, "Yıka!", 0, 14, 46, "#10202b", ya); c.restore()
    caption(c, ["Beyin, gözyaşı bezlerine emir gönderir.", "Gözyaşı, gözü yıkayıp korur."], t, 0.9, 1262)

TIPS = [("Soğanı soğut", "Soğuk, tepkimeyi yavaşlatır", 1.9), ("Keskin bıçak kullan", "Daha az hücre ezilir", 3.0), ("Mutfağı havalandır", "Gaz, göze ulaşmadan dağılır", 4.2)]
def s5(c, t, d):
    header(c, "İPUÇLARI", "Daha az gözyaşı için", t)
    for i, (a_, b_, t0) in enumerate(TIPS):
        k = eout((t - t0) / 0.45) if t > t0 else 0
        if k <= 0: continue
        y = 560 + i * 200; x = 90 + (1 - k) * 60
        c.save(); c.saveLayerAlpha(None, int(255 * k))
        c.drawRoundRect(skia.Rect.MakeXYWH(x, y, 900, 168), 34, 34, fill(CREAM, 0.09))
        c.drawRoundRect(skia.Rect.MakeXYWH(x, y, 900, 168), 34, 34, stroke(CREAM, 2, 0.18))
        check(c, x + 92, y + 84, 42 * eback((t - t0 - 0.1) / 0.4))
        text(c, a_, x + 170, y + 78, 50, CREAM, 1, "Bold", align="l")
        text(c, b_, x + 170, y + 128, 33, CREAM, 0.7, "Regular", align="l")
        c.restore(); c.restore()

def s6(c, t, d):
    a1 = ss(0.1, 0.55, t); a2 = ss(1.0, 1.5, t)
    text(c, "Soğan sizi üzmüyor;", W / 2, 320 + (1 - a1) * 20, 70, CREAM, a1)
    text(c, "kendini savunuyor.", W / 2, 420 + (1 - a2) * 20, 84, PINK, a2)
    onion(c, W / 2, 840, 205, rot=3 * math.sin(t * 2), scale=eback((t - 0.2) / 0.6) if t > 0.2 else 0)
    if t > 1.5: shield(c, W / 2 + 175, 960, 92 * eback((t - 1.5) / 0.5))
    a3 = ss(3.3, 3.8, t); a4 = ss(4.4, 4.9, t)
    text(c, "Neden böyle?", W / 2, 1290 + (1 - a3) * 20, 96, GOLD, a3)
    text(c, "Artık biliyorsunuz.", W / 2, 1372 + (1 - a4) * 14, 46, CREAM, 0.9 * a4, "Medium")


if __name__ == "__main__":
    nb.main(SLUG, NARRATION, [s0, s1, s2, s3, s4, s5, s6])
