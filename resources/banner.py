"""Generates the banner, panels and link buttons next to this file.  Usage: python3 resources/banner.py"""
import os
import random
import re
from xml.sax.saxutils import escape as e

os.chdir(os.path.dirname(os.path.abspath(__file__)))      # outputs always land in resources/, wherever this is run from

# Vintage cherry blossom over smoke
BG, SURFACE, OVERLAY, SUB, FG = "#1b1618", "#3b2e33", "#86737a", "#bba9a8", "#ecdfd2"
BLOSSOM, SAKURA, ROSE = "#f7dbe1", "#e9a9b9", "#c9788d"      # pale petal, dusty pink, deep rose
GOLD, SAGE, BRANCH = "#d6b583", "#a9b48c", "#5a4540"          # faded gold, sage leaf, bark
USER = "jonathan@gammill"
FONT = "ui-monospace, SFMono-Regular, 'SF Mono', Menlo, Consolas, 'Liberation Mono', 'DejaVu Sans Mono', monospace"

# figlet "ANSI Shadow" — the classic rice header. Regenerate with: figlet -f "ANSI Shadow" -w 300 "JONATHAN GAMMILL"
NAME_ART = [
 "     ██╗ ██████╗ ███╗   ██╗ █████╗ ████████╗██╗  ██╗ █████╗ ███╗   ██╗     ██████╗  █████╗ ███╗   ███╗███╗   ███╗██╗██╗     ██╗",
 "     ██║██╔═══██╗████╗  ██║██╔══██╗╚══██╔══╝██║  ██║██╔══██╗████╗  ██║    ██╔════╝ ██╔══██╗████╗ ████║████╗ ████║██║██║     ██║",
 "     ██║██║   ██║██╔██╗ ██║███████║   ██║   ███████║███████║██╔██╗ ██║    ██║  ███╗███████║██╔████╔██║██╔████╔██║██║██║     ██║",
 "██   ██║██║   ██║██║╚██╗██║██╔══██║   ██║   ██╔══██║██╔══██║██║╚██╗██║    ██║   ██║██╔══██║██║╚██╔╝██║██║╚██╔╝██║██║██║     ██║",
 "╚█████╔╝╚██████╔╝██║ ╚████║██║  ██║   ██║   ██║  ██║██║  ██║██║ ╚████║    ╚██████╔╝██║  ██║██║ ╚═╝ ██║██║ ╚═╝ ██║██║███████╗███████╗",
 " ╚════╝  ╚═════╝ ╚═╝  ╚═══╝╚═╝  ╚═╝   ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝     ╚═════╝ ╚═╝  ╚═╝╚═╝     ╚═╝╚═╝     ╚═╝╚═╝╚══════╝╚══════╝",
]

PETAL = "M0 0C-6 -5 -7.5 -13 -2 -16.5L0 -14.5L2 -16.5C7.5 -13 6 -5 0 0Z"   # notched sakura petal, base at origin

def defs(w, h, seed):
    return f'''<defs>
<linearGradient id="name" gradientUnits="userSpaceOnUse" x1="30" y1="0" x2="742" y2="0"><stop offset="0" stop-color="{BLOSSOM}"/><stop offset=".55" stop-color="{SAKURA}"/><stop offset="1" stop-color="{ROSE}"/></linearGradient>
<linearGradient id="petal" x1=".5" y1="1" x2=".5" y2="0"><stop offset="0" stop-color="{ROSE}"/><stop offset=".45" stop-color="{SAKURA}"/><stop offset="1" stop-color="{BLOSSOM}"/></linearGradient>
<radialGradient id="vignette" cx=".5" cy=".5" r=".75"><stop offset=".55" stop-color="#000" stop-opacity="0"/><stop offset="1" stop-color="#000" stop-opacity=".55"/></radialGradient>
<filter id="smoke" x="0" y="0" width="100%" height="100%"><feTurbulence type="fractalNoise" baseFrequency="0.004 0.011" numOctaves="4" seed="{seed}"/><feColorMatrix values="0 0 0 0 .74  0 0 0 0 .62  0 0 0 0 .68  1.9 0 0 0 -.8"/><feGaussianBlur stdDeviation="5"/></filter>
<filter id="grain" x="0" y="0" width="100%" height="100%"><feTurbulence type="fractalNoise" baseFrequency=".85" numOctaves="2" seed="3"/><feColorMatrix values="0 0 0 0 1  0 0 0 0 .92  0 0 0 0 .85  0 0 0 .55 -.2"/></filter>
<filter id="glow" x="-5%" y="-30%" width="110%" height="160%"><feGaussianBlur stdDeviation="2.2"/></filter>
<g id="blossom">{"".join(f'<path d="{PETAL}" fill="url(#petal)" transform="rotate({a})"/>' for a in range(0, 360, 72))}{"".join(f'<path d="M0 0L0 -6.5" stroke="{GOLD}" stroke-width=".6" transform="rotate({a})"/><circle cx="0" cy="-6.5" r=".9" fill="{GOLD}" transform="rotate({a})"/>' for a in range(18, 360, 45))}<circle r="1.8" fill="{ROSE}"/></g>
<path id="loose" d="{PETAL}" fill="url(#petal)"/>
</defs>
<rect width="{w}" height="{h}" fill="{BG}"/>
<rect width="{w}" height="{h}" fill="{BG}" filter="url(#smoke)" opacity=".5"/>
<rect width="{w}" height="{h}" fill="url(#vignette)"/>'''

class Svg:
    def __init__(self, w, h, label, seed=7):
        self.w, self.h = w, h
        self.o = [f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 {w} {h}" width="{w}" height="{h}" font-family="{FONT}" role="img" aria-label="{e(label)}">',
                  defs(w, h, seed)]
    def t(self, x, y, s, fill=FG, size=15, weight=400, anchor="start", opacity=1):
        self.o.append(f'<text x="{x}" y="{y}" fill="{fill}" font-size="{size}" font-weight="{weight}" text-anchor="{anchor}" opacity="{opacity}">{e(s)}</text>')
    def box(self, x, y, w, h):
        self.o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" fill="{BG}" fill-opacity=".35" stroke="{ROSE}" stroke-opacity=".7" stroke-width="1.5"/>')
    def prompt(self, x, y, cmd, size=15, path="/", cursor=False):
        # one <text> with tspans, so spacing holds whatever monospace font the viewer has
        cur = f'<tspan fill="{SAKURA}"> \u2588<animate attributeName="opacity" values="1;1;0;0" dur="1.2s" repeatCount="indefinite"/></tspan>' if cursor else ""
        self.o.append(f'<text x="{x}" y="{y}" font-size="{size}" fill="{FG}" xml:space="preserve"><tspan fill="{SAGE}" font-weight="700">{USER}</tspan>:'
                      f'<tspan fill="{SAKURA}" font-weight="700">{e(path)}</tspan>$ {e(cmd)}{cur}</text>')
    def branch(self, paths):
        """paths: (d, stroke-width) pairs."""
        self.o.append(f'<g fill="none" stroke="{BRANCH}" stroke-linecap="round">' + "".join(f'<path d="{d}" stroke-width="{w}"/>' for d, w in paths) + "</g>")
    def blossoms(self, items):
        """items: (x, y, scale, rotation) — scale under 0.5 draws a closed bud."""
        for x, y, sc, rot in items:
            if sc < 0.5:
                self.o.append(f'<circle cx="{x}" cy="{y}" r="3.2" fill="{ROSE}"/><circle cx="{x}" cy="{y - 1}" r="1.8" fill="{SAKURA}"/>')
            else:
                self.o.append(f'<use xlink:href="#blossom" href="#blossom" transform="translate({x} {y}) rotate({rot}) scale({sc})"/>')
    def sway(self, px, py, dur=7):
        """Open a group that rocks gently about (px, py), like a branch in a breeze. Close with end()."""
        self.o.append(f'<g><animateTransform attributeName="transform" type="rotate" dur="{dur}s" repeatCount="indefinite" calcMode="spline" '
                      f'keyTimes="0;.3;.65;1" keySplines=".4 0 .6 1;.4 0 .6 1;.4 0 .6 1" values="0 {px} {py};1.3 {px} {py};-.9 {px} {py};0 {px} {py}"/>')
    def end(self): self.o.append("</g>")
    def petals(self, items):
        """items: (x, y, scale, rotation, opacity) — loose petals that flutter down, fade out and loop.
        Each is offset in time so they never fall in step; without animation they sit still."""
        for i, (x, y, sc, rot, op) in enumerate(items):
            dur = 7 + (i * 1.7) % 5
            self.o.append(f'<g><animateTransform attributeName="transform" type="translate" dur="{dur:.1f}s" begin="-{(i * 2.3) % dur:.1f}s" repeatCount="indefinite" '
                          f'values="-22 -52;-4 -26;-14 2;10 28;0 54;26 82"/>'
                          f'<animate attributeName="opacity" dur="{dur:.1f}s" begin="-{(i * 2.3) % dur:.1f}s" repeatCount="indefinite" keyTimes="0;.15;.75;1" values="0;1;1;0"/>'
                          f'<g><animateTransform attributeName="transform" type="rotate" dur="{dur * .6:.1f}s" repeatCount="indefinite" values="-25 {x} {y};35 {x} {y};-25 {x} {y}"/>'
                          f'<use xlink:href="#loose" href="#loose" opacity="{op}" transform="translate({x} {y}) rotate({rot}) scale({sc})"/></g></g>')
    def raw(self, s): self.o.append(s)
    def save(self, path):
        grain = f'<rect width="{self.w}" height="{self.h}" filter="url(#grain)" opacity=".5" pointer-events="none"/>'
        open(path, "w").write("\n".join(self.o + [grain, "</svg>"]))

def ascii_art(s, lines, x, y, cw, ch, slant=12):
    """ANSI Shadow block art drawn as shapes, not font glyphs, so it is crisp on every machine.
    The letters are hollow: only the outline of the block cells is stroked. The font's
    box-drawing shadow is kept as faint linework behind it."""
    rows, cols = len(lines), max(map(len, lines))
    on = lambda r, c: 0 <= r < rows and 0 <= c < len(lines[r]) and lines[r][c] == "█"
    shadow, edge = [], []
    for r, line in enumerate(lines):
        top = y + r * ch
        for c, glyph in enumerate(line):
            l, mx, rt, my, bot = x + c * cw, x + (c + .5) * cw, x + (c + 1) * cw, top + ch / 2, top + ch
            d = {"═": f"M{l:.1f} {my:.1f}H{rt:.1f}", "║": f"M{mx:.1f} {top:.1f}V{bot:.1f}",
                 "╗": f"M{l:.1f} {my:.1f}H{mx:.1f}V{bot:.1f}", "╔": f"M{rt:.1f} {my:.1f}H{mx:.1f}V{bot:.1f}",
                 "╝": f"M{l:.1f} {my:.1f}H{mx:.1f}V{top:.1f}", "╚": f"M{rt:.1f} {my:.1f}H{mx:.1f}V{top:.1f}"}.get(glyph)
            if d: shadow.append(d)
    # outline = every cell edge with a block on exactly one side, merged into long runs
    for r in range(rows + 1):                      # horizontal edges
        start = None
        for c in range(cols + 1):
            hit = c < cols and on(r - 1, c) != on(r, c)
            if hit and start is None: start = c
            if not hit and start is not None:
                edge.append(f"M{x + start * cw:.1f} {y + r * ch:.1f}H{x + c * cw:.1f}"); start = None
    for c in range(cols + 1):                      # vertical edges
        start = None
        for r in range(rows + 1):
            hit = r < rows and on(r, c - 1) != on(r, c)
            if hit and start is None: start = r
            if not hit and start is not None:
                edge.append(f"M{x + c * cw:.1f} {y + start * ch:.1f}V{y + r * ch:.1f}"); start = None
    outline = "".join(edge)
    base = y + rows * ch                           # italic: lean the whole name about its baseline
    s.raw(f'<g transform="translate({x} {base:.1f}) skewX({-slant}) translate({-x} {-base:.1f})">')
    s.raw(f'<path d="{"".join(shadow)}" fill="none" stroke="{ROSE}" stroke-width="1" stroke-linejoin="round" opacity=".4"/>')
    s.raw(f'<path d="{outline}" fill="none" stroke="{ROSE}" stroke-width="4" stroke-linecap="square" opacity=".45" filter="url(#glow)"/>')
    s.raw(f'<path d="{outline}" fill="none" stroke="url(#name)" stroke-width="1.7" stroke-linecap="square"/>')
    s.raw('</g>')

# ---------------------------------------------------------------- hero banner
W, H = 1200, 446
s = Svg(W, H, "Jonathan Gammill — IT Automation Specialist and Application Developer at Asurepoint LLC")

# cherry branch reaching in from the lower left, behind the terminal text
s.raw('<g transform="translate(0 46)">')
s.sway(-10, 392)
s.branch([("M-10 392C90 376 170 340 280 342S440 374 548 352", 5),
          ("M150 354C176 328 208 320 236 308", 3),
          ("M330 345C370 324 408 324 442 314", 2.6),
          ("M420 364C460 382 498 386 532 390", 2.2),
          ("M60 380C70 360 86 350 104 344", 2.2)])
s.blossoms([(236, 308, 1.15, 10), (198, 324, 0.9, 40), (280, 342, 1.3, 25), (150, 354, 1.0, 60),
            (442, 314, 1.1, 5), (392, 327, 0.85, 50), (548, 352, 1.25, 30), (478, 364, 0.95, 15),
            (532, 390, 0.9, 70), (104, 344, 1.05, 20), (40, 384, 1.2, 45),
            (252, 300, 0.3, 0), (458, 306, 0.3, 0), (320, 336, 0.3, 0), (566, 344, 0.3, 0), (118, 334, 0.3, 0)])
s.end()
s.petals([(612, 318, 0.9, 130, .85), (668, 356, 0.75, 215, .7), (718, 300, 0.7, 60, .6), (640, 388, 0.8, 300, .75),
          (742, 368, 0.6, 160, .5), (690, 262, 0.55, 20, .4), (590, 372, 0.6, 250, .6)])
s.raw('</g>')

s.box(8, 8, W - 16, 38)
s.raw(f'<rect x="18" y="16" width="38" height="22" rx="5" fill="{SAKURA}"/>')
s.t(37, 32, "[0]", BG, 14, 700, "middle"); s.t(74, 32, f"{USER}: /", SUB)
s.raw(f'<text x="{W / 2}" y="32" font-size="15" text-anchor="middle"><tspan fill="{SAGE}">AUTOMATION</tspan><tspan fill="{OVERLAY}"> | </tspan><tspan fill="{GOLD}">APP DEV</tspan><tspan fill="{OVERLAY}"> | </tspan><tspan fill="{SAKURA}">DIGITAL FORENSICS</tspan></text>')
s.t(W - 26, 32, "Plano, TX", SUB, anchor="end")

s.prompt(30, 88, "whoami")
ascii_art(s, NAME_ART, 30, 108, 5.35, 11.5)

# who-am-i laid out as an NTFS MFT record: attribute type, attribute name, value
# (":degree" / ":school" are named $DATA streams, i.e. alternate data streams)
y = 218
for tid, attr, stream, val, col in (("0x10", "$STANDARD_INFORMATION", "", "IT Automation Specialist / Application Developer", FG),
                                    ("0x30", "$FILE_NAME", "", "Asurepoint LLC", FG),
                                    ("0x80", "$DATA", ":degree", "B.S. Information Technology, Digital Forensics", SUB),
                                    ("0x80", "$DATA", ":school", "University of South Alabama", SUB)):
    s.t(30, y, tid, OVERLAY, 14)
    s.raw(f'<text x="74" y="{y}" font-size="14" fill="{GOLD}">{e(attr)}<tspan fill="{ROSE}">{stream}</tspan></text>')
    s.t(272, y, val, col, 14)
    y += 21
s.prompt(30, 326, "cd /home/jonathan", cursor=True)

s.raw(f'<path d="M772 60V{H - 16}" stroke="{ROSE}" stroke-opacity=".35"/>')
s.t(800, 88, "$", SAGE, 15, 700); s.t(818, 88, "tree -L 2 /")
# (depth, name, note)
tree = [(0, "/", ""),
        (1, "home/jonathan/", ""),
        (1, "proc/", "2 roles running"),
        (1, "opt/", "projects"),
        (2, "multi-agent-ai/", ""),
        (2, "cyber-carver/", ""),
        (2, "portal-resilience/", ""),
        (1, "usr/bin/", "languages"),
        (1, "usr/lib/forensics/", ""),
        (1, "mnt/cloud/", ""),
        (1, "mnt/c/", "ntfs volume"),
        (1, "etc/education/", ""),
        (1, "var/log/", "experience")]
RH, y0, ind, lines, py = 21, 122, 26, [], {}
for i, (d, name, note) in enumerate(tree):
    y = y0 + i * RH
    py[d] = y
    x = 800 + d * ind
    if d:
        lines.append(f"M{x - ind + 5} {py[d - 1] + 6}V{y - 5}h13")
    s.t(x, y, name, SAKURA, 14, 700)
    if note: s.t(1000, y, "# " + note, OVERLAY, 13)
s.raw(f'<path d="{"".join(lines)}" fill="none" stroke="{OVERLAY}" stroke-width="1.2"/>')

# the NTFS boot sector's OEM ID, as xxd would show it on the mounted volume
s.t(800, 402, "$", SAGE, 14, 700); s.t(817, 402, "xxd -s 3 -l 8 /dev/sdb1", FG, 14)
s.raw(f'<text x="800" y="423" font-size="13" fill="{OVERLAY}" xml:space="preserve">00000003: <tspan fill="{ROSE}">4e54 4653 2020 2020</tspan>  <tspan fill="{GOLD}" font-weight="700">NTFS</tspan></text>')

# hex strip: an endless carve through a byte stream, hunting for file headers and footers.
# It opens with the bytes that spell the name, then real file signatures separated by filler.
SIGNATURES = [("ff d8 ff e0", "ff d9"),                 # JPEG  SOI / EOI
              ("89 50 4e 47", "ae 42 60 82"),           # PNG   magic / end of IEND
              ("25 50 44 46", "25 25 45 4f 46"),        # PDF   %PDF / %%EOF
              ("50 4b 03 04", "50 4b 05 06"),           # ZIP   local file header / end of central directory
              ("47 49 46 38", "00 3b")]                 # GIF   GIF8 / trailer
rng = random.Random(1010)
filler = lambda n: [(f"{rng.randrange(256):02x}", OVERLAY, 400) for _ in range(n)]
stream = [(f"{ord(ch):02x}", ROSE, 400) for ch in "Jonathan Gammill"] + filler(2)
for head, foot in SIGNATURES:
    stream += [(b, GOLD, 700) for b in head.split()] + filler(5) + [(b, SAGE, 700) for b in foot.split()] + filler(3)

ROW, TOP, BOT, SPEED = 19, 62, 432, 2.0                 # row height, visible window, rows per second
visible = (BOT - TOP) // ROW + 2
cells = "".join(f'<text x="{W - 26}" y="{TOP + 16 + i * ROW}" fill="{col}" font-size="12" font-weight="{wt}" text-anchor="end">{b}</text>'
                for i, (b, col, wt) in enumerate(stream + stream[:visible]))     # repeat the start so the loop is seamless
s.raw(f'<defs><linearGradient id="hexfade" gradientUnits="userSpaceOnUse" x1="0" y1="{TOP}" x2="0" y2="{BOT}"><stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset=".12" stop-color="#fff"/><stop offset=".85" stop-color="#fff"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>'
      f'<mask id="hexmask" maskUnits="userSpaceOnUse" x="{W - 60}" y="{TOP}" width="60" height="{BOT - TOP}"><rect x="{W - 60}" y="{TOP}" width="60" height="{BOT - TOP}" fill="url(#hexfade)"/></mask></defs>')
s.raw(f'<g mask="url(#hexmask)"><g>{cells}<animateTransform attributeName="transform" type="translate" from="0 0" to="0 {-len(stream) * ROW}" dur="{len(stream) / SPEED:.1f}s" repeatCount="indefinite"/></g></g>')
# the scan head: bytes pass through this fixed window as they are examined
scan_y = TOP + 16 + 9 * ROW
s.raw(f'<rect x="{W - 46}" y="{scan_y - 13}" width="26" height="18" rx="3" fill="none" stroke="{SAKURA}" stroke-width="1.2"><animate attributeName="stroke-opacity" values=".95;.35;.95" dur="1s" repeatCount="indefinite"/></rect>')
s.save("github-banner.svg")

# ---------------------------------------------------------------- lower panels
W, H = 1200, 236
s = Svg(W, H, "Experience log and skills directory listing", seed=11)
s.box(8, 8, 586, H - 16); s.box(606, 8, 586, H - 16)

# sprig reaching in from the right edge of the skills panel
s.sway(1196, 206, 8)
s.branch([("M1196 206C1160 196 1128 168 1100 128", 3.6), ("M1142 180C1118 184 1096 180 1076 190", 2.2), ("M1118 150C1128 124 1146 104 1162 84", 2.2)])
s.blossoms([(1100, 128, 1.2, 15), (1076, 190, 1.0, 50), (1162, 84, 1.05, 30), (1140, 118, 0.85, 5), (1150, 178, 0.9, 65),
            (1092, 112, 0.3, 0), (1170, 70, 0.3, 0), (1062, 196, 0.3, 0)])
s.end()
s.petals([(1040, 150, 0.7, 140, .6), (1010, 204, 0.6, 250, .45), (540, 196, 0.75, 120, .6), (562, 96, 0.6, 30, .4), (500, 150, 0.55, 220, .35)])

s.prompt(28, 40, "cat experience.log", 14, "/var/log")
y = 76
for when, org, role in (("2026.06 - now", "Asurepoint LLC", "IT Automation Specialist"),
                        ("2026.06 - now", "Asurepoint LLC", "Application Developer"),
                        ("2024 summer", "MS Dept. of Marine Resources", "IT Data Management Intern")):
    now = when.endswith("now")
    s.t(28, y, when, GOLD, 14); s.t(170, y, org, FG, 14, 700); s.t(170, y + 22, role, SAGE, 14)
    y += 50

s.prompt(626, 40, "ls bin lib/forensics /mnt/cloud", 14, "/usr")
y = 76
for d, items, col in (("bin:", "python  bash  powershell  c#  java  javascript", SAGE),
                      ("lib/forensics:", "autopsy  ftk-imager  encase  wireshark  kali", FG),
                      ("/mnt/cloud:", "aws  gcp  postgresql  mongodb", GOLD)):
    s.t(626, y, d, SAKURA, 14, 700); s.t(626, y + 22, items, col, 14)
    y += 50
s.save("github-panels.svg")

# ---------------------------------------------------------------- link buttons
# README images cannot contain links, so each button is its own small SVG that the README wraps in <a>.
def button(path, key, label, accent):
    cw, h = 9.6, 44                                   # 16px monospace advance, button height
    tag_w = 40
    w = round(tag_w + 16 + len(label) * cw + 18)
    open(path, "w").write(
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" font-family="{FONT}" role="img" aria-label="{e(label)}">'
        f'<rect x=".75" y=".75" width="{w - 1.5}" height="{h - 1.5}" rx="8" fill="{BG}" stroke="{accent}" stroke-width="1.5"/>'
        f'<rect x="6" y="6" width="{tag_w}" height="{h - 12}" rx="5" fill="{accent}"/>'
        f'<text x="{6 + tag_w / 2}" y="28" font-size="15" font-weight="700" fill="{BG}" text-anchor="middle">[{key}]</text>'
        f'<text x="{tag_w + 18}" y="28" font-size="16" fill="{FG}">{e(label)}</text></svg>')

# Neutral file names on purpose: ad and tracker blockers hide images whose names mention
# things like "linkedin" or "contact", which made those two buttons vanish for some viewers.
button("link-1.svg", 1, "resume.pdf", GOLD)
button("link-2.svg", 2, "linkedin", SAGE)
button("link-3.svg", 3, "contact", SAKURA)
button("link-4.svg", 4, "rice site", ROSE)

# ---------------------------------------------------------------- site copy
# The site paints this same smoke across the whole page (site/bg.svg), so its copy of the banner
# drops the full-size background, smoke, vignette and grain layers and sits on the page seamlessly.
if os.path.isdir("../site"):
    hero = open("github-banner.svg").read()
    open("../site/github-banner.svg", "w").write(re.sub(r'<rect width="1200" height="446"[^>]*/>\n?', "", hero))
