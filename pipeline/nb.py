"""Neden Böyle video kitaplığı: çizim yardımcıları, seslendirme, 8-bit müzik, render ve birleştirme.
Kullanım için pipeline/README.md ve episodes/sogan.py dosyasına bakın."""
import sys, os, json, math, subprocess, hashlib
import numpy as np, skia

W, H, FPS = 1080, 1920, 30
ROOT = os.path.dirname(os.path.abspath(__file__))
CACHE = os.path.expanduser("~/.cache/nedenboyle")
VOICE = "tr_TR-fahrettin-medium"
VOICE_DIR = f"{CACHE}/vits-piper-{VOICE}"
F = "/usr/share/fonts/truetype/google-fonts/"
def _tf(k):
    p = F + f"Poppins-{k}.ttf"
    if not os.path.exists(p): p = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if k == "Bold" else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
    return skia.Typeface.MakeFromFile(p)
TF = {k: _tf(k) for k in ("Bold", "Medium", "Regular")}

CREAM, PINK, GOLD, BLUE, GREEN, MINT, RED = "#f6e7c8", "#ff7fb6", "#f5b942", "#6ec6f0", "#6fd08c", "#c9f5d9", "#ff5d5d"
# Bölüm bu sözlüğü değiştirerek renk temasını ayarlayabilir (arka plan 3 renk + vurgu rengi)
THEME = dict(bg=["#3a1c4d", "#22112f", "#150b1d"], accent=PINK, text=CREAM)
def col(h, a=1.0):
    h = h.lstrip("#")
    return skia.Color(int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16), int(max(0, min(1, a)) * 255))
def fill(h, a=1.0): return skia.Paint(AntiAlias=True, Color=col(h, a))
def stroke(h, w, a=1.0, cap=True):
    p = skia.Paint(AntiAlias=True, Color=col(h, a), Style=skia.Paint.kStroke_Style, StrokeWidth=w)
    if cap: p.setStrokeCap(skia.Paint.kRound_Cap); p.setStrokeJoin(skia.Paint.kRound_Join)
    return p
def clamp(x, a=0.0, b=1.0): return max(a, min(b, x))
def ss(a, b, x):
    t = clamp((x - a) / (b - a)); return t * t * (3 - 2 * t)
def eout(x): x = clamp(x); return 1 - (1 - x) ** 3
def eback(x):
    x = clamp(x); c1 = 1.70158; c3 = c1 + 1
    return 1 + c3 * (x - 1) ** 3 + c1 * (x - 1) ** 2
def lerp(a, b, t): return a + (b - a) * t
def qbez(p0, p1, p2, t):
    return ((1 - t) ** 2 * p0[0] + 2 * (1 - t) * t * p1[0] + t * t * p2[0],
            (1 - t) ** 2 * p0[1] + 2 * (1 - t) * t * p1[1] + t * t * p2[1])

def text(c, s, x, y, size, color=CREAM, a=1.0, w="Bold", align="c", spacing=0.0):
    if a <= 0.003: return
    f = skia.Font(TF[w], size); f.setSubpixel(True); p = fill(color, a)
    if spacing:
        widths = [f.measureText(ch) + spacing for ch in s]; tw = sum(widths) - spacing
        x0 = x - tw / 2 if align == "c" else x
        for ch, cw in zip(s, widths):
            c.drawString(ch, x0, y, f, p); x0 += cw
        return
    tw = f.measureText(s)
    x0 = x - tw / 2 if align == "c" else (x - tw if align == "r" else x)
    c.drawString(s, x0, y, f, p)

def background(c):
    c.clear(col(THEME["bg"][2]))
    p = skia.Paint(AntiAlias=True)
    p.setShader(skia.GradientShader.MakeRadial(center=(W / 2, 820), radius=1050,
                colors=[col(x) for x in THEME["bg"]], positions=[0, 0.55, 1]))
    c.drawRect(skia.Rect.MakeWH(W, H), p)

N_SCENES = [7]
def progress(c, idx, frac):
    n = N_SCENES[0]; x0, x1, y = 60, 1020, 108; gap = 14; seg = (x1 - x0 - gap * (n - 1)) / n
    for i in range(n):
        xa = x0 + i * (seg + gap)
        c.drawLine(xa, y, xa + seg, y, stroke(CREAM, 6, 0.16))
        f = 1 if i < idx else (frac if i == idx else 0)
        if f > 0: c.drawLine(xa, y, xa + seg * f, y, stroke(THEME["accent"], 6, 0.95))

def header(c, label, title, t):
    a = ss(0.0, 0.45, t); dy = (1 - eout(t / 0.5)) * 24
    text(c, label, W / 2, 222 + dy, 30, THEME["accent"], a, "Bold", spacing=7)
    text(c, title, W / 2, 312 + dy, 70, CREAM, a)

def caption(c, lines, t, t0=0.6, y=1270):
    for i, ln in enumerate(lines):
        a = ss(t0 + i * 0.25, t0 + 0.5 + i * 0.25, t)
        text(c, ln, W / 2, y + i * 60 + (1 - a) * 14, 41, CREAM, 0.88 * a, "Medium")

# ---------- hazır şekiller ----------
def drop(c, x, y, r, a=1.0, color=BLUE):
    if a <= 0.01: return
    p = skia.Path(); p.moveTo(0, -1.8 * r); p.cubicTo(0.35 * r, -1.0 * r, r, -0.45 * r, r, 0.1 * r)
    p.cubicTo(r, 1.25 * r, -r, 1.25 * r, -r, 0.1 * r); p.cubicTo(-r, -0.45 * r, -0.35 * r, -1.0 * r, 0, -1.8 * r); p.close()
    c.save(); c.translate(x, y); c.drawPath(p, fill(color, a))
    c.drawCircle(-0.35 * r, 0.25 * r, 0.22 * r, fill("#ffffff", 0.55 * a)); c.restore()

def puff(c, x, y, r, a):
    if a <= 0.01: return
    c.drawCircle(x, y, r * 1.7, fill(MINT, 0.10 * a))
    c.drawCircle(x, y, r, fill(MINT, 0.55 * a))
    c.drawCircle(x - r * 0.3, y - r * 0.3, r * 0.35, fill("#ffffff", 0.5 * a))

def check(c, x, y, r, a=1.0, ok=True):
    c.drawCircle(x, y, r, fill(GREEN if ok else RED, a))
    p = skia.Path(); p.moveTo(x - r * 0.45, y + r * 0.02); p.lineTo(x - r * 0.12, y + r * 0.36); p.lineTo(x + r * 0.48, y - r * 0.32)
    c.drawPath(p, stroke("#143021", r * 0.24, a))

def eye(c, x, y, w, h, red=0.0, wet=0.0, look=(0, 0)):
    ep = skia.Path(); ep.moveTo(-w, 0); ep.quadTo(0, -h * 1.55, w, 0); ep.quadTo(0, h * 1.45, -w, 0); ep.close()
    c.save(); c.translate(x, y)
    sc = (255, int(lerp(250, 196, red)), int(lerp(245, 196, red)))
    c.drawPath(ep, skia.Paint(AntiAlias=True, Color=skia.Color(*sc)))
    c.save(); c.clipPath(ep, True)
    if red > 0.02:
        rng = np.random.default_rng(3)
        for side in (-1, 1):
            for k in range(5):
                yy = rng.uniform(-h * 0.5, h * 0.5); ln = rng.uniform(0.35, 0.6) * w
                vp = skia.Path(); vp.moveTo(side * w, yy * 0.3)
                vp.quadTo(side * (w - ln * 0.5), yy + rng.uniform(-18, 18), side * (w - ln), yy * 1.1)
                c.drawPath(vp, stroke("#e0383f", 3.5, 0.75 * red))
    ix, iy, ir = look[0], look[1], h * 0.78
    p = skia.Paint(AntiAlias=True)
    p.setShader(skia.GradientShader.MakeRadial(center=(ix, iy), radius=ir, colors=[col("#c98a3f"), col("#8a5422"), col("#4b2a0f")], positions=[0.25, 0.75, 1]))
    c.drawCircle(ix, iy, ir, p); c.drawCircle(ix, iy, ir * 0.45, fill("#120a06"))
    c.drawCircle(ix - ir * 0.3, iy - ir * 0.32, ir * 0.17, fill("#ffffff", 0.9))
    if wet > 0.01:
        wp = skia.Paint(AntiAlias=True); wp.setShader(skia.GradientShader.MakeLinear(points=[(0, h * (0.9 - 0.9 * wet)), (0, h)], colors=[col(BLUE, 0.0), col(BLUE, 0.75)]))
        c.drawRect(skia.Rect.MakeLTRB(-w, -h, w, h * 1.5), wp)
    c.restore()
    up = skia.Path(); up.moveTo(-w, 0); up.quadTo(0, -h * 1.55, w, 0); c.drawPath(up, stroke("#f0c9a8", 14))
    lo = skia.Path(); lo.moveTo(-w, 0); lo.quadTo(0, h * 1.45, w, 0); c.drawPath(lo, stroke("#f0c9a8", 8, 0.9))
    for k in range(7):
        tt = 0.14 + k * 0.12; px, py = qbez((-w, 0), (0, -h * 1.55), (w, 0), tt)
        dx = (tt - 0.5) * 60; c.drawLine(px, py - 6, px + dx, py - 44, stroke("#f0c9a8", 7))
    c.restore()

def node(c, x, y, label, a=1.0, color=GOLD, pulse=0.0):
    f = skia.Font(TF["Bold"], 38); tw = f.measureText(label); w = tw + 64; h = 78
    if pulse > 0: c.drawRoundRect(skia.Rect.MakeXYWH(x - w / 2 - 14 * pulse, y - h / 2 - 14 * pulse, w + 28 * pulse, h + 28 * pulse), 50, 50, stroke(color, 4, 0.5 * (1 - pulse) * a))
    c.drawRoundRect(skia.Rect.MakeXYWH(x - w / 2, y - h / 2, w, h), 39, 39, fill("#2b1739", a))
    c.drawRoundRect(skia.Rect.MakeXYWH(x - w / 2, y - h / 2, w, h), 39, 39, stroke(color, 4, a))
    text(c, label, x, y + 13, 38, color, a)

def shield(c, x, y, s, a=1.0):
    p = skia.Path(); p.moveTo(0, -1); p.lineTo(0.85, -0.65); p.lineTo(0.85, 0.1); p.cubicTo(0.85, 0.7, 0.3, 1.0, 0, 1.15)
    p.cubicTo(-0.3, 1.0, -0.85, 0.7, -0.85, 0.1); p.lineTo(-0.85, -0.65); p.close()
    c.save(); c.translate(x, y); c.scale(s, s)
    c.drawPath(p, fill(GOLD, a)); c.drawPath(p, skia.Paint(AntiAlias=True, Color=col("#2b1739", a), Style=skia.Paint.kStroke_Style, StrokeWidth=0.09))
    ck = skia.Path(); ck.moveTo(-0.38, 0.05); ck.lineTo(-0.1, 0.36); ck.lineTo(0.42, -0.25)
    q = stroke("#2b1739", 0.17, a); c.drawPath(ck, q); c.restore()


# ---------- seslendirme ----------
def tts(work, narration, tails=None, length_scale=0.97):
    """Her sahne için bir cümle grubu seslendirir; sahne süresi = ses süresi + pay. info listesini döndürür."""
    import soundfile as sf
    os.makedirs(work, exist_ok=True); ip = f"{work}/info.json"
    if os.path.exists(ip):
        info = json.load(open(ip))
        if [x["text"] for x in info] == list(narration): return info
    info = []; t = 0.0
    for i, s in enumerate(narration):
        p = f"{work}/seg{i}.wav"
        subprocess.run([sys.executable, "-m", "piper", "-m", f"{VOICE_DIR}/{VOICE}.onnx", "-f", p, "--length-scale", str(length_scale),
                        "--sentence-silence", "0.25"], input=s.encode(), check=True, capture_output=True)
        x, sr = sf.read(p, dtype="float32"); idx = np.where(np.abs(x) > 0.01)[0]
        x = x[max(0, idx[0] - int(0.02 * sr)): idx[-1] + int(0.08 * sr)]; sf.write(p, x, sr)
        dur = len(x) / sr; tail = (tails[i] if tails else (1.8 if i == len(narration) - 1 else 1.0))
        scene = round((dur + tail) * FPS) / FPS
        info.append(dict(i=i, text=s, vo_start=round(t + 0.35, 3), vo_dur=round(dur, 2), scene_start=round(t, 3), scene_dur=scene)); t += scene
    json.dump(info, open(ip, "w"), ensure_ascii=False)
    return info

# ---------- render ----------
_surface = skia.Surface(W, H)
def frame(scenes, info, i, t):
    c = _surface.getCanvas(); d = info[i]["scene_dur"]; last = i == len(scenes) - 1
    N_SCENES[0] = len(scenes); background(c); progress(c, i, clamp(t / d))
    fade = (1 - ss(d - 0.6, d - 0.1, t)) if last else (1 - ss(d - 0.25, d - 0.02, t))
    c.saveLayerAlpha(None, int(255 * fade)); scenes[i](c, t, d); c.restore()
    return _surface.makeImageSnapshot()

def preview(work, scenes, info, specs):
    """specs: ["0:3.5", "2:4.0"] -> tam boy PNG kareler + küçültülmüş tek kontrol görseli (sheet.jpg)."""
    from PIL import Image
    ims = []
    for spec in specs:
        i, t = spec.split(":"); p = f"{work}/prev_{i}_{t}.png"; frame(scenes, info, int(i), float(t)).save(p, skia.kPNG)
        ims.append(Image.open(p).convert("RGB").resize((432, 768)))
    cols = min(4, len(ims)); rows = (len(ims) + cols - 1) // cols; s = Image.new("RGB", (432 * cols, 768 * rows))
    for k, im in enumerate(ims): s.paste(im, ((k % cols) * 432, (k // cols) * 768))
    s.save(f"{work}/sheet.jpg", quality=88); print("preview:", f"{work}/sheet.jpg")

def render(work, scenes, info):
    os.makedirs(f"{work}/scenes", exist_ok=True); files = []
    for i in range(len(scenes)):
        n = round(info[i]["scene_dur"] * FPS); tmp = f"{work}/scenes/tmp_s{i}.mp4"; out = f"{work}/scenes/s{i}.mp4"
        ff = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgba", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                               "-c:v", "libx264", "-crf", "18", "-preset", "veryfast", "-pix_fmt", "yuv420p", tmp], stdin=subprocess.PIPE)
        for k in range(n):
            ff.stdin.write(frame(scenes, info, i, k / FPS).toarray(colorType=skia.kRGBA_8888_ColorType).tobytes())
        ff.stdin.close()
        if ff.wait() != 0: sys.exit(f"scene {i} failed")
        os.replace(tmp, out); files.append(out); print("scene", i, n, "frames", flush=True)
    with open(f"{work}/list.txt", "w") as f:
        for p in files: f.write(f"file '{p}'\n")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", f"{work}/list.txt", "-c", "copy", f"{work}/video.mp4"], check=True)

# ---------- 8-bit müzik + miks ----------
def mix(work, info, seed):
    """Seed'e göre her bölümde farklı bir chiptune üretir, seslendirmenin altına kısarak karıştırır."""
    import soundfile as sf
    from scipy.signal import resample_poly, butter, sosfilt
    SR = 44100; DUR = info[-1]["scene_start"] + info[-1]["scene_dur"]; N = int(SR * DUR)
    rng = np.random.default_rng(seed)
    BARS = max(8, 4 * round(DUR / rng.uniform(2.05, 2.35) / 4)); bar = DUR / BARS; s16 = bar / 16; tr = int(rng.integers(-3, 4))
    mf = lambda m: 440 * 2 ** ((m + tr - 69) / 12)
    def pulse(f, n, duty): t = np.arange(n) / SR; return np.where((t * f) % 1 < duty, 1.0, -1.0)
    def tri(f, n): t = np.arange(n) / SR; x = 2 * np.abs(2 * ((t * f) % 1) - 1) - 1; return np.round(x * 7.5) / 7.5
    def env(n, a=0.004, r=0.03, decay=0.0):
        e = np.ones(n); na = min(n, int(a * SR)); nr = min(n, int(r * SR)); e[:na] = np.linspace(0, 1, na); e[-nr:] *= np.linspace(1, 0, nr)
        if decay: e *= np.exp(-np.arange(n) / SR * decay)
        return e
    def add(buf, t0, x, g):
        i = int(t0 * SR); x = x[:max(0, N - i)]; buf[i:i + len(x)] += x * g
    lead = np.zeros(N); arp = np.zeros(N); bass = np.zeros(N); drums = np.zeros(N)
    ch = {'C': [48, 52, 55], 'Am': [57, 60, 64], 'F': [53, 57, 60], 'G': [55, 59, 62], 'Dm': [50, 53, 57], 'Em': [52, 55, 59]}
    progs = [['C', 'Am', 'F', 'G'], ['Am', 'F', 'C', 'G'], ['C', 'G', 'Am', 'F'], ['F', 'G', 'Em', 'Am'], ['Dm', 'G', 'C', 'Am'], ['C', 'Em', 'F', 'G']]
    pa, pb = rng.choice(len(progs), 2, replace=False)
    prog = [(progs[pa] if (b // 4) % 2 == 0 else progs[pb])[b % 4] for b in range(BARS)]; prog[-2:] = ['G', 'C']
    scale = [60, 62, 64, 67, 69, 72, 74, 76, 79, 81, 84]   # do majör pentatonik
    rhythms = [[(0, 4), (4, 2), (6, 2), (8, 6), (14, 2)], [(0, 2), (2, 2), (4, 4), (8, 2), (10, 2), (12, 4)], [(0, 4), (4, 4), (8, 8)],
               [(0, 6), (6, 2), (8, 4), (12, 4)], [(0, 2), (2, 2), (4, 2), (6, 2), (8, 8)], [(0, 4), (4, 4), (8, 4), (12, 4)]]
    phrases = {}
    def phrase(key, chord):
        if key not in phrases:
            r = rhythms[int(rng.integers(len(rhythms)))]; pos = int(rng.integers(3, 8)); notes = []
            for k, (s, l) in enumerate(r):
                if k == 0 or l >= 6:   # güçlü zamanlarda akor sesi
                    tones = [m for m in scale if (m - chord[0]) % 12 in [(x - chord[0]) % 12 for x in chord]] or scale
                    m = min(tones, key=lambda x: abs(scale.index(x) - pos) + rng.uniform(0, 1.5)); pos = scale.index(m)
                else:
                    pos = int(clamp(pos + int(rng.choice([-2, -1, -1, 1, 1, 2])), 0, len(scale) - 1)); m = scale[pos]
                notes.append((s, l, m))
            phrases[key] = notes
        return phrases[key]
    for b in range(BARS):
        t0 = b * bar; c = ch[prog[b]]; last = b == BARS - 1
        if 2 <= b < BARS - 1:
            for (s, l, m) in phrase((b % 8, prog[b]), c):
                n = int(l * s16 * SR * 0.92); t = np.arange(n) / SR; ph = np.cumsum(mf(m) * (1 + 0.004 * np.sin(2 * np.pi * 5.5 * t) * (t > 0.18))) / SR
                add(lead, t0 + s * s16, np.where(ph % 1 < 0.25, 1.0, -1.0) * env(n, decay=1.2), 0.19)
        if last:
            for m in (48, 60, 64, 67, 72):
                n = int(bar * SR); add(lead, t0, pulse(mf(m), n, 0.5) * env(n, decay=1.5, r=0.6), 0.08)
            continue
        for k in range(16):
            m = c[[0, 2, 1, 2][k % 4]] + 12 + (12 if k % 8 >= 4 else 0); n = int(s16 * SR * 0.8)
            add(arp, t0 + k * s16, pulse(mf(m), n, 0.125) * env(n, decay=9), 0.09)
        root = c[0] - 12 if c[0] - 12 >= 40 else c[0]
        for k, (off, l) in enumerate([(0, 2), (4, 2), (6, 2), (8, 2), (12, 2), (14, 2)]):
            n = int(l * s16 * SR * 0.9); add(bass, t0 + off * s16, tri(mf(root + (7 if k in (2, 5) else 0)), n) * env(n), 0.30)
        if b >= 2:
            for k in range(16):
                if k % 8 == 0:
                    n = int(0.11 * SR); t = np.arange(n) / SR; f = 150 * np.exp(-t * 28) + 45
                    add(drums, t0 + k * s16, np.sign(np.sin(2 * np.pi * np.cumsum(f) / SR)) * env(n, decay=22), 0.22)
                if k % 8 == 4:
                    n = int(0.10 * SR); add(drums, t0 + k * s16, np.repeat(rng.choice([-1.0, 1.0], n // 6 + 1), 6)[:n] * env(n, decay=30), 0.12)
                if k % 2 == 0:
                    n = int(0.03 * SR); add(drums, t0 + k * s16, rng.choice([-1.0, 1.0], n) * env(n, decay=90), 0.04)
    music = sosfilt(butter(2, 9000, 'lp', fs=SR, output='sos'), lead + arp + bass + drums)
    f = int(0.4 * SR); music[:f] *= np.linspace(0, 1, f); music[-int(0.8 * SR):] *= np.linspace(1, 0, int(0.8 * SR))
    voice = np.zeros(N)
    for s in info:
        x, sr = sf.read(f"{work}/seg{s['i']}.wav", dtype="float32"); x = resample_poly(x, SR, sr); x = x / np.max(np.abs(x)) * 0.9
        add(voice, s["vo_start"], x, 1.0)
    win = int(0.25 * SR); e = np.convolve(np.abs(voice), np.ones(win) / win, 'same'); act = np.convolve(np.clip(e / 0.03, 0, 1), np.ones(win) / win, 'same')
    m = voice * 0.95 + music * (1 - 0.55 * act) * 0.42; m = m / max(1.0, np.max(np.abs(m)) / 0.97)
    sf.write(f"{work}/mix.wav", np.stack([m, m], 1), SR)

def build(slug, scenes, info, work):
    render(work, scenes, info)
    mix(work, info, int(hashlib.sha1(slug.encode()).hexdigest()[:8], 16))
    out = f"{work}/{slug}.mp4"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", f"{work}/video.mp4", "-i", f"{work}/mix.wav", "-map", "0:v", "-map", "1:a", "-c:v", "copy",
                    "-af", "loudnorm=I=-15:TP=-1.5:LRA=11", "-c:a", "aac", "-b:a", "192k", "-ar", "44100", "-movflags", "+faststart", out], check=True)
    print("OK", out, round(info[-1]["scene_start"] + info[-1]["scene_dur"], 2), "sn"); return out

def main(slug, narration, scenes, tails=None):
    """Bölüm dosyasının sonunda çağrılır:  python3 episodes/x.py preview 0:3.5 1:4.0   |   python3 episodes/x.py build"""
    work = os.path.join(ROOT, "build", slug); info = tts(work, narration, tails)
    for s in info: print(s["i"], "başlangıç", s["scene_start"], "süre", s["scene_dur"], "|", s["text"])
    cmd = sys.argv[1] if len(sys.argv) > 1 else "info"
    if cmd == "preview": preview(work, scenes, info, sys.argv[2:])
    elif cmd == "build": build(slug, scenes, info, work)
