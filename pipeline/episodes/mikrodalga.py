import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import numpy as np, skia
from nb import *
import nb

SLUG = "mikrodalga-nasil-isitir"
nb.THEME.update(bg=["#4a2412", "#2c160c", "#170b06"], accent="#ffb347")
NARRATION = [
 "Mikrodalga fırın yemeği nasıl ısıtır? Ateş yok, alev yok; ama yemek ısınıyor.",
 "Fırının içindeki bir parça, mikrodalga denen görünmez dalgalar üretir. Metal duvarlar bu dalgaları içeride yansıtır.",
 "Yemeklerin içinde bol su vardır. Su molekülünün bir ucu hafif artı, öbür ucu hafif eksi yüklüdür.",
 "Mikrodalganın elektrik alanı, saniyede milyarlarca kez yön değiştirir. Su molekülleri ona uymak için durmadan ileri geri döner.",
 "Dönen moleküller komşularına sürtünür ve çarpar; bu hareket ısıya dönüşür. Isı, dış katmanlardan yemeğin içine doğru yayılır.",
 "Bu yüzden tabla döner, böylece ısı daha eşit dağılır. Arada karıştırmak da işe yarar. Metal kaplar ise kıvılcım çıkarabilir.",
 "Mikrodalga, yemeğin içindeki suyu dans ettirerek ısıtır. Neden böyle? Artık biliyorsunuz.",
]
METAL, STEEL, GLOW = "#c9cdd6", "#8a909c", "#ffd36b"
WAVE = "#7fe0ff"

def mol(c, x, y, s, ang, a=1.0, signs=False):
    """Su molekülü: O (kırmızı) + iki H (beyaz). ang: H'lerin baktığı yön (radyan)."""
    for sg in (-1, 1):
        hx = x + 40 * s * math.cos(ang + sg * 0.92); hy = y + 40 * s * math.sin(ang + sg * 0.92)
        line(c, x, y, hx, hy, "#ffffff", 7 * s, a)
        circ(c, hx, hy, 17 * s, "#f4f4f4", a)
        if signs: text(c, "+", hx, hy + 11 * s, 30 * s, "#d0452f", a)
    circ(c, x, y, 28 * s, "#ff5d4a", a)
    if signs: text(c, "−", x, y + 12 * s, 40 * s, "#ffffff", a)

def oven(c, t, x=540, y=900, s=1.0, glow=1.0):
    w, h = 640 * s, 420 * s; x0, y0 = x - w / 2, y - h / 2
    rrect(c, x0, y0, w, h, 34 * s, METAL)
    rrect(c, x0 + 30 * s, y0 + 36 * s, 420 * s, h - 72 * s, 20 * s, "#1e1410")
    rrect(c, x0 + 30 * s, y0 + 36 * s, 420 * s, h - 72 * s, 20 * s, GLOW, 0.22 * glow * (0.8 + 0.2 * math.sin(t * 5)))
    # tabak ve kase
    bx = x0 + 240 * s; by = y0 + h - 90 * s
    c.drawOval(skia.Rect.MakeXYWH(bx - 150 * s, by - 10 * s, 300 * s, 34 * s), fill("#e8e2d4"))
    p = skia.Path(); p.moveTo(bx - 95 * s, by - 60 * s); p.quadTo(bx, by + 50 * s, bx + 95 * s, by - 60 * s); p.close()
    c.drawPath(p, fill("#ff8a3c"))
    rrect(c, bx - 100 * s, by - 68 * s, 200 * s, 14 * s, 7 * s, "#ffb347")
    for k in range(3):
        ph = (t * 0.7 + k / 3) % 1
        sx = bx + (k - 1) * 45 * s + 10 * s * math.sin(t * 3 + k)
        line(c, sx, by - 80 * s - 70 * s * ph, sx + 8 * s, by - 105 * s - 70 * s * ph, "#ffffff", 7 * s, 0.6 * (1 - ph) * glow)
    # kontrol paneli
    px = x0 + 480 * s
    rrect(c, px, y0 + 40 * s, 130 * s, 70 * s, 12 * s, "#1e1410"); text(c, "0:30", px + 65 * s, y0 + 88 * s, 38 * s, "#7dffb0")
    for r_ in range(3):
        for c_ in range(2): rrect(c, px + 12 * s + c_ * 58 * s, y0 + 140 * s + r_ * 56 * s, 46 * s, 40 * s, 10 * s, STEEL)
    rrect(c, px + 8 * s, y0 + h - 80 * s, 114 * s, 40 * s, 14 * s, "#2f6f4f")

def hero(c, t): oven(c, t)

def zig(c, pts, color, t, a=1.0, wl=40, amp=12):
    """Kırık çizgi boyunca dalgalı ışın."""
    for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
        L = math.hypot(x1 - x0, y1 - y0); ux, uy = (x1 - x0) / L, (y1 - y0) / L; nx, ny = -uy, ux
        p = skia.Path(); n = max(2, int(L / 6))
        for i in range(n + 1):
            d = L * i / n; off = amp * math.sin(d / wl * 2 * math.pi - t * 8)
            xx, yy = x0 + ux * d + nx * off, y0 + uy * d + ny * off
            p.moveTo(xx, yy) if i == 0 else p.lineTo(xx, yy)
        c.drawPath(p, stroke(color, 7, a))

def i1(c, t, d):
    rrect(c, 120, 560, 840, 520, 30, METAL, 1, sw=18)
    rrect(c, 129, 569, 822, 502, 24, "#1e1410")
    rrect(c, 150, 600, 150, 110, 16, STEEL)
    for j in range(3): zig(c, [(172, 630 + j * 25), (278, 630 + j * 25)], WAVE, t, 1, 26, 6)
    tag(c, "dalga üreteci", 225, 535, "#ffffff", ss(0.9, 1.4, t), 32, "c", "Bold")
    pts = [(300, 655), (950, 830), (560, 1070), (130, 900), (420, 570), (950, 760)]
    p = ss(1.0, 4.5, t); segs = len(pts) - 1; k = p * segs; n = int(k)
    if p > 0:
        part = pts[:n + 1]
        if n < segs: part = part + [(lerp(pts[n][0], pts[n + 1][0], k - n), lerp(pts[n][1], pts[n + 1][1], k - n))]
        if len(part) >= 2: zig(c, part, WAVE, t)
    for (x, y) in pts[1:-1]:
        circ(c, x, y, 16, "#ffffff", 0.5 * ss(2.5, 3.5, t))
    tag(c, "metal duvar yansıtır", 540, 1140, THEME["accent"], ss(3.8, 4.3, t), 40, "c", "Bold")

def i2(c, t, d):
    k = pop(t, 0.4, 0.6)
    if k > 0:
        c.save(); c.translate(540, 830); c.scale(3.4 * k, 3.4 * k); c.translate(-540, -830)
        mol(c, 540, 830, 1.0, math.pi / 2 + 0.12 * math.sin(t * 2), signs=False)
        c.restore()
    a = ss(2.8, 3.3, t)
    tag(c, "−", 540, 870, "#ffffff", a, 110, "c", "Bold")
    for sg in (-1, 1):
        hx = 540 + 136 * math.cos(math.pi / 2 + sg * 0.92); hy = 830 + 136 * math.sin(math.pi / 2 + sg * 0.92)
        tag(c, "+", hx, hy + 30, "#d0452f", a, 90, "c", "Bold")
    tag(c, "oksijen", 540, 640, "#ff9a8a", ss(1.4, 1.9, t), 36, "c", "Bold")
    tag(c, "hidrojen", 400, 1030, "#ffffff", ss(1.8, 2.3, t), 34, "c")
    tag(c, "hidrojen", 680, 1030, "#ffffff", ss(1.8, 2.3, t), 34, "c")

def i3(c, t, d):
    ph = math.sin(t * 4.0)
    # alan oku
    a = ss(0.5, 1.0, t)
    if ph >= 0: arrow(c, 200, 560, 880, 560, WAVE, 12, a, 34)
    else: arrow(c, 880, 560, 200, 560, WAVE, 12, a, 34)
    tag(c, "elektrik alanı", 540, 520, WAVE, a, 34, "c", "Bold")
    sw = ss(1.6, 2.6, t)
    for r_ in range(3):
        for c_ in range(4):
            x = 225 + c_ * 210; y = 700 + r_ * 160
            base = (r_ * 4 + c_) * 1.3
            ang = lerp(base, (0 if ph >= 0 else math.pi) + 0.35 * math.sin(t * 9 + base), sw)
            mol(c, x, y, 1.25, ang)
    tag(c, "ileri geri döner", 540, 1150, THEME["accent"], ss(3.0, 3.5, t), 40, "c", "Bold")

def i4(c, t, d):
    # yemek kesiti: dıştan içe ısınma
    heat = ss(1.0, d - 0.5, t)
    cx, cy = 540, 850
    for i in range(8, 0, -1):
        r = 260 * i / 8
        inner = 1 - i / 8
        k = clamp(heat * 1.6 - inner * 1.2)
        circ(c, cx, cy, r, mixcol("#5b7bff", "#ff5d3a", k))
    _r = np.random.default_rng(5)
    for j in range(14):
        ang = j * 2 * math.pi / 14; rr = 215 + 18 * math.sin(j)
        jx = 9 * math.sin(t * 23 + j * 2.1) * ss(0.4, 1.0, t); jy = 9 * math.cos(t * 19 + j)
        mol(c, cx + rr * math.cos(ang) + jx, cy + rr * math.sin(ang) + jy, 0.7, t * 6 + j)
    for j in range(6):
        ang = j * math.pi / 3 + 0.5; u = (t * 0.5 + j / 6) % 1
        r0 = lerp(250, 110, u)
        arrow(c, cx + r0 * math.cos(ang), cy + r0 * math.sin(ang), cx + (r0 - 60) * math.cos(ang), cy + (r0 - 60) * math.sin(ang), "#ffffff", 7, 0.8 * ss(2.4, 3.0, t) * (1 - u), 18)
    tag(c, "önce dış katman", 540, 520, "#ffb08a", ss(1.4, 1.9, t), 38, "c", "Bold")
    tag(c, "ısı içe yayılır", 540, 1175, "#ffffff", ss(3.6, 4.1, t), 38, "c", "Bold")

SCENES = [
 title_scene("Mikrodalga", "nasıl ısıtır?", "Ateş yok, alev yok", hero),
 reason_scene("ADIM 1", "Görünmez dalgalar", ["Fırın mikrodalga üretir;", "metal duvarlar onu içeride tutar."], i1),
 reason_scene("ADIM 2", "Yemekteki su", ["Su molekülünün bir ucu artı,", "öbür ucu eksi yüklüdür."], i2),
 reason_scene("ADIM 3", "Moleküller döner", ["Alan saniyede milyarlarca kez", "yön değiştirir; su da döner."], i3),
 reason_scene("ADIM 4", "Hareket ısıya dönüşür", ["Moleküller çarpışır ve ısınır;", "ısı dıştan içe doğru yayılır."], i4),
 cards_scene("İPUÇLARI", "Eşit ısıtmak için", [("Tabla döner", "Isı daha eşit dağılır"), ("Arada karıştırın", "Soğuk noktalar kalmaz"), ("Metal koymayın", "Kıvılcım çıkarabilir")]),
 end_scene("Ateş değil;", "su molekülleri dans ediyor.", hero),
]
if __name__ == "__main__":
    nb.main(SLUG, NARRATION, SCENES)
