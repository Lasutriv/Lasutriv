#!/usr/bin/env python3
"""Generate the profile banner + footer SVGs (dossier / CRT theme).

Edit LINES / colours below, then run:  python3 assets/generate.py
Writes header.svg and footer.svg next to this script (stdlib only).
"""
import math
import sys
from pathlib import Path

OUT = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parent
OUT.mkdir(parents=True, exist_ok=True)

W, H = 1200, 400
AMBER = "#f5a524"
RED = "#f85149"
FG = "#e6edf3"
MUTED = "#8b949e"
DIM = "#6e7681"
LINE = "#30363d"
MONO = ("ui-monospace, SFMono-Regular, 'SF Mono', Menlo, Consolas, "
        "'Liberation Mono', 'DejaVu Sans Mono', monospace")


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def f(x):
    return f"{x:.2f}".rstrip("0").rstrip(".")


def tl(text, fs, ls=0):
    """textLength attrs pinning a monospace label to 0.6em + letter-spacing."""
    return f'textLength="{f(len(text) * (0.6 * fs + ls))}" lengthAdjust="spacing"'


BOTTOM = "CLEARANCE PUBLIC  ·  STATUS ACTIVE  ·  LOCATION"
BOTTOM_W = len(BOTTOM) * (0.6 * 13 + 3)


# ---------------------------------------------------------------- typing
LINES = [
    ("ROLE", "Game developer · autonomous AI agents"),
    ("LATEST OPS", "Monarchy · New Roots"),
    ("FIELD ASSET", "AIA-Evolve, an AI agent that ships code 24/7"),
]
TX = 56            # left margin of typed block
TY0 = 262          # first baseline
TDY = 34           # line spacing
ADV = 11.6         # forced per-character advance (via textLength)
FS = 19
KEYW = 13          # key column width in chars
CHAR_DT = 0.030    # seconds per char
T_START = 1.25     # typing begins after the stamp lands
LINE_GAP = 0.30


def typed_block():
    out_defs, out_body = [], []
    t = T_START
    for i, (key, val) in enumerate(LINES):
        y = TY0 + i * TDY
        key_txt = key.ljust(KEYW)
        full = "› " + key_txt + val
        n = len(full)
        dur = n * CHAR_DT
        widths = ";".join(f(k * ADV) for k in range(n + 1))
        xs = ";".join(f(TX + k * ADV) for k in range(n + 1))
        cid = f"type{i}"
        out_defs.append(
            f'<clipPath id="{cid}"><rect x="{TX - 2}" y="{y - FS - 2}" '
            f'width="0" height="{FS + 10}">'
            f'<animate attributeName="width" values="{widths}" '
            f'begin="{f(t)}s" dur="{f(dur)}s" calcMode="discrete" '
            f'fill="freeze"/></rect></clipPath>'
        )
        out_body.append(
            f'<text clip-path="url(#{cid})" x="{TX}" y="{y}" '
            f'textLength="{f(n * ADV)}" lengthAdjust="spacing" '
            f'font-size="{FS}">'
            f'<tspan fill="{AMBER}">› </tspan>'
            f'<tspan fill="{MUTED}">{esc(key_txt)}</tspan>'
            f'<tspan fill="{FG}">{esc(val)}</tspan></text>'
        )
        # block cursor that rides the typing head
        last = i == len(LINES) - 1
        vis = "visible" if i == 0 else "hidden"
        anims = [
            f'<animate attributeName="x" values="{xs}" begin="{f(t)}s" '
            f'dur="{f(dur)}s" calcMode="discrete" fill="freeze"/>'
        ]
        if i > 0:
            anims.append(f'<set attributeName="visibility" to="visible" '
                         f'begin="{f(t)}s"/>')
        if not last:
            nxt = t + dur + LINE_GAP
            anims.append(f'<set attributeName="visibility" to="hidden" '
                         f'begin="{f(nxt)}s"/>')
        out_body.append(
            f'<rect class="cursor" x="{TX}" y="{y - FS + 3}" width="{f(ADV - 1)}" '
            f'height="{FS + 2}" fill="{AMBER}" visibility="{vis}">'
            + "".join(anims) + "</rect>"
        )
        t += dur + LINE_GAP
    return "\n    ".join(out_defs), "\n  ".join(out_body)


# ---------------------------------------------------------------- sonar
# Full-bleed background sonar: range rings radiate from an origin on the
# right and the beam sweeps the whole banner, behind all the text.
RCX, RCY = 1004, 206
SR = 1060          # beam length, long enough to reach the far corners
SWEEP_T = 6.0      # seconds per revolution
RING_STEP = 120
BEAM_SPAN = 56     # degrees of fading trail behind the beam
BEAM_MAX = .22     # trail opacity right behind the beam
# contacts sit in open space so they never light up under text
BLIPS = [(905, 104), (1094, 122), (1126, 284), (932, 304),
         (818, 318), (702, 226), (436, 98)]


def polar(r, deg):
    a = math.radians(deg)
    return RCX + r * math.cos(a), RCY + r * math.sin(a)


def wedge(r, a0, a1):
    x0, y0 = r * math.cos(math.radians(a0)), r * math.sin(math.radians(a0))
    x1, y1 = r * math.cos(math.radians(a1)), r * math.sin(math.radians(a1))
    return f"M0 0L{f(x0)} {f(y0)}A{r} {r} 0 0 1 {f(x1)} {f(y1)}Z"


def sonar():
    p = []
    # range rings, fading with distance
    for i, r in enumerate(range(RING_STEP, SR, RING_STEP)):
        op = max(.05, .17 - i * .017)
        p.append(f'<circle cx="{RCX}" cy="{RCY}" r="{r}" fill="none" '
                 f'stroke="{AMBER}" stroke-opacity="{f(op)}"/>')
    # short crosshair and bearing ticks around the origin
    c = RING_STEP * 1.5
    p.append(f'<path d="M{f(RCX - c)} {RCY}H{f(RCX + c)}M{RCX} {f(RCY - c)}V{f(RCY + c)}" '
             f'stroke="{AMBER}" stroke-opacity=".12"/>')
    ticks = []
    for d in range(0, 360, 10):
        L = 9 if d % 30 == 0 else 4
        x0, y0 = polar(RING_STEP, d)
        x1, y1 = polar(RING_STEP - L, d)
        ticks.append(f"M{f(x0)} {f(y0)}L{f(x1)} {f(y1)}")
    p.append(f'<path d="{"".join(ticks)}" stroke="{AMBER}" stroke-opacity=".35"/>')
    # beam: nested wedges that all end at the leading edge, so opacity builds
    # toward the beam with no seams between slices
    sw = [f'<circle r="{SR}" fill="none"/>']  # keeps the fill-box centred
    steps, prev = 18, 0.0
    for k in range(steps):
        target = BEAM_MAX * ((k + 1) / steps) ** 1.7
        a = 1 - (1 - target) / (1 - prev)
        prev = target
        a0 = -BEAM_SPAN * (1 - k / steps)
        sw.append(f'<path d="{wedge(SR, a0, 0)}" fill="{AMBER}" '
                  f'fill-opacity="{a:.4f}"/>')
    sw.append(f'<path d="M0 0H{SR}" stroke="{AMBER}" stroke-opacity=".14" '
              f'stroke-width="7"/>')
    sw.append(f'<path d="M0 0H{SR}" stroke="{AMBER}" stroke-opacity=".6" '
              f'stroke-width="1.5"/>')
    p.append(f'<g transform="translate({RCX} {RCY})"><g class="sweep">'
             + "".join(sw) + "</g></g>")
    # contacts light up as the beam passes over them
    for x, y in BLIPS:
        deg = math.degrees(math.atan2(y - RCY, x - RCX)) % 360
        delay = f(deg / 360 * SWEEP_T)
        p.append(
            f'<g style="animation-delay:{delay}s" class="blip">'
            f'<circle class="ping" cx="{x}" cy="{y}" r="5" fill="none" '
            f'stroke="{AMBER}" style="animation-delay:{delay}s"/>'
            f'<circle cx="{x}" cy="{y}" r="3.5" fill="{AMBER}"/></g>'
        )
    p.append(f'<circle cx="{RCX}" cy="{RCY}" r="9" fill="none" stroke="{AMBER}" '
             f'stroke-opacity=".5"/>')
    p.append(f'<circle cx="{RCX}" cy="{RCY}" r="3.5" fill="{AMBER}"/>')
    return "\n  ".join(p)


def hud_corners(x0, y0, x1, y1, L=18, inset=14, op=".6"):
    i = inset
    d = (f"M{x0 + i} {y0 + i + L}V{y0 + i}H{x0 + i + L}"
         f"M{x1 - i - L} {y0 + i}H{x1 - i}V{y0 + i + L}"
         f"M{x1 - i} {y1 - i - L}V{y1 - i}H{x1 - i - L}"
         f"M{x0 + i + L} {y1 - i}H{x0 + i}V{y1 - i - L}")
    return (f'<path d="{d}" fill="none" stroke="{AMBER}" stroke-opacity="{op}" '
            f'stroke-width="2"/>')


COMMON_DEFS = f"""
    <linearGradient id="bg" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#0b1016"/>
      <stop offset="1" stop-color="#0d1117"/>
    </linearGradient>
    <pattern id="grid" width="40" height="40" patternUnits="userSpaceOnUse">
      <path d="M40 0H0V40" fill="none" stroke="{FG}" stroke-opacity=".035"/>
    </pattern>
    <pattern id="scan" width="4" height="4" patternUnits="userSpaceOnUse">
      <rect width="4" height="1" fill="#000" fill-opacity=".2"/>
    </pattern>
    <linearGradient id="band" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="{AMBER}" stop-opacity="0"/>
      <stop offset=".5" stop-color="{AMBER}" stop-opacity=".045"/>
      <stop offset="1" stop-color="{AMBER}" stop-opacity="0"/>
    </linearGradient>
    <pattern id="hatch" width="6" height="6" patternUnits="userSpaceOnUse"
             patternTransform="rotate(45)">
      <rect width="6" height="6" fill="#020304"/>
      <rect width="2" height="6" fill="#ffffff" fill-opacity=".04"/>
    </pattern>"""

COMMON_CSS = f"""
    text {{ font-family: {MONO}; white-space: pre; }}
    .blink {{ animation: blink 1.1s steps(1, end) infinite; }}
    .cursor {{ animation: blink 1s steps(1, end) infinite; }}
    .band {{ animation: band 7s linear infinite; }}
    @keyframes blink {{ 0% {{ opacity: 1; }} 50% {{ opacity: 0; }} }}
    @keyframes band {{ from {{ transform: translateY(-140px); }}
                      to {{ transform: translateY({H + 20}px); }} }}"""


def header():
    tdefs, tbody = typed_block()
    css = COMMON_CSS + f"""
    .name {{ animation: flicker .9s linear both; }}
    .glitch {{ opacity: 0; animation: glitch 6.5s steps(1, end) 2.2s infinite; }}
    .glitch.b {{ animation-name: glitch-b; }}
    .stamp {{ transform-box: fill-box; transform-origin: center;
              animation: stamp .45s cubic-bezier(.2, .9, .3, 1.2) .55s both; }}
    .sweep {{ transform-box: fill-box; transform-origin: center;
              animation: spin {f(SWEEP_T)}s linear infinite; }}
    .blip {{ opacity: .1; animation: blip {f(SWEEP_T)}s ease-out infinite; }}
    .ping {{ transform-box: fill-box; transform-origin: center; opacity: 0;
             animation: ping {f(SWEEP_T)}s ease-out infinite; }}
    @keyframes flicker {{
      0% {{ opacity: 0; }} 12% {{ opacity: .9; }} 18% {{ opacity: .15; }}
      30% {{ opacity: 1; }} 36% {{ opacity: .45; }} 48%, 100% {{ opacity: 1; }} }}
    @keyframes glitch {{
      0% {{ opacity: 0; transform: none; }}
      90% {{ opacity: .75; transform: translate(-5px, 0); }}
      92% {{ opacity: .75; transform: translate(4px, 1px); }}
      94% {{ opacity: 0; transform: none; }} }}
    @keyframes glitch-b {{
      0% {{ opacity: 0; transform: none; }}
      90% {{ opacity: .75; transform: translate(5px, 0); }}
      92% {{ opacity: .75; transform: translate(-3px, -1px); }}
      94% {{ opacity: 0; transform: none; }} }}
    @keyframes stamp {{
      0% {{ opacity: 0; transform: scale(2.2); }}
      70% {{ opacity: 1; transform: scale(.95); }}
      100% {{ opacity: 1; transform: scale(1); }} }}
    @keyframes spin {{ to {{ transform: rotate(360deg); }} }}
    @keyframes blip {{ 0% {{ opacity: .95; }} 65%, 100% {{ opacity: .1; }} }}
    @keyframes ping {{ 0% {{ opacity: .9; transform: scale(.6); }}
                      45%, 100% {{ opacity: 0; transform: scale(3.2); }} }}
    @media (prefers-reduced-motion: reduce) {{
      * {{ animation: none !important; }}
      .blip {{ opacity: .5; }}
    }}"""

    name = "LASUTRIV"
    name_len = 508
    name_attrs = (f'x="56" y="200" font-size="86" font-weight="800" '
                  f'textLength="{name_len}" lengthAdjust="spacing"')

    return f"""<svg xmlns="http://www.w3.org/2000/svg" xml:space="preserve" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-labelledby="t d">
  <title id="t">LASUTRIV — personnel file</title>
  <desc id="d">Codename Lasutriv. Role: game developer working with autonomous AI agents. Latest ops: Monarchy and New Roots. Field asset: AIA-Evolve, an AI agent that ships code around the clock. Studio: Summit Tec. Status: declassified.</desc>
  <defs>{COMMON_DEFS}
    <radialGradient id="glow" cx=".5" cy=".5" r=".5">
      <stop offset="0" stop-color="{AMBER}" stop-opacity=".10"/>
      <stop offset="1" stop-color="{AMBER}" stop-opacity="0"/>
    </radialGradient>
    <clipPath id="panel"><rect width="{W}" height="{H}" rx="16"/></clipPath>
    <filter id="ink" x="-10%" y="-30%" width="120%" height="160%">
      <feTurbulence type="fractalNoise" baseFrequency=".85" numOctaves="2" seed="7"/>
      <feColorMatrix values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0 0 0 -9 6.1"/>
      <feComposite in="SourceGraphic" operator="in"/>
    </filter>
    <filter id="phosphor" x="-20%" y="-50%" width="140%" height="200%">
      <feGaussianBlur stdDeviation="3" result="b"/>
      <feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
    {tdefs}
  </defs>
  <style>{css}
  </style>

  <g clip-path="url(#panel)">
  <rect width="{W}" height="{H}" fill="url(#bg)"/>
  <rect width="{W}" height="{H}" fill="url(#grid)"/>
  <circle cx="{RCX}" cy="{RCY}" r="260" fill="url(#glow)"/>
  <rect width="{W}" height="62" fill="#11161d"/>
  <rect y="{H - 50}" width="{W}" height="50" fill="#11161d"/>

  <!-- background sonar -->
  {sonar()}

  <!-- top bar -->
  <path d="M0 62H{W}" stroke="{LINE}"/>
  <circle class="blink" cx="62" cy="36" r="5" fill="{AMBER}"/>
  <text x="80" y="41" font-size="14" letter-spacing="3" fill="{MUTED}" {tl("SUMMIT TEC  //  PERSONNEL FILE", 14, 3)}>SUMMIT TEC  //  PERSONNEL FILE</text>
  <text x="{W - 56}" y="41" font-size="14" letter-spacing="3" fill="{MUTED}" text-anchor="end" {tl("FILE 2054-LSV-001", 14, 3)}>FILE 2054-LSV-001</text>

  <!-- codename -->
  <text x="58" y="118" font-size="15" letter-spacing="6" fill="{AMBER}" {tl("CODENAME", 15, 6)} filter="url(#phosphor)">CODENAME</text>
  <g class="name">
    <text class="glitch" {name_attrs} fill="#ff3b5c">{name}</text>
    <text class="glitch b" {name_attrs} fill="#00e1ff">{name}</text>
    <text {name_attrs} fill="{FG}">{name}</text>
  </g>
  <rect x="58" y="216" width="72" height="3" fill="{AMBER}"/>
  <rect x="136" y="216" width="18" height="3" fill="{AMBER}" fill-opacity=".5"/>
  <rect x="160" y="216" width="8" height="3" fill="{AMBER}" fill-opacity=".25"/>

  <!-- declassified stamp -->
  <g transform="translate(726 142) rotate(-9)">
    <g class="stamp">
      <g filter="url(#ink)" fill="none" stroke="{RED}">
        <rect x="-128" y="-34" width="256" height="68" rx="6" stroke-width="4"/>
        <rect x="-119" y="-25" width="238" height="50" rx="3" stroke-width="1.5"/>
        <text x="0" y="10" font-size="29" font-weight="800" letter-spacing="5"
              fill="{RED}" stroke="none" text-anchor="middle"
              textLength="206" lengthAdjust="spacing">DECLASSIFIED</text>
      </g>
    </g>
  </g>

  <!-- typed dossier lines -->
  {tbody}

  <!-- bottom bar -->
  <path d="M0 {H - 50}H{W}" stroke="{LINE}"/>
  <text x="56" y="{H - 20}" font-size="13" letter-spacing="3" fill="{MUTED}" {tl(BOTTOM, 13, 3)}>CLEARANCE <tspan fill="{FG}">PUBLIC</tspan>  ·  STATUS <tspan fill="{AMBER}">ACTIVE</tspan>  ·  LOCATION</text>
  <rect x="{f(56 + BOTTOM_W + 8)}" y="{H - 34}" width="150" height="18" fill="url(#hatch)" stroke="{LINE}"/>
  <text x="{W - 56}" y="{H - 20}" font-size="13" letter-spacing="3" fill="{MUTED}" text-anchor="end" {tl("SCANNING ▮", 13, 3)}>SCANNING<tspan class="blink" fill="{AMBER}"> ▮</tspan></text>

  <!-- CRT overlays -->
  <rect class="band" width="{W}" height="120" fill="url(#band)"/>
  <rect width="{W}" height="{H}" fill="url(#scan)" pointer-events="none"/>
  {hud_corners(0, 62, W, H - 50, L=16, inset=12, op=".55")}
  </g>
  <rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="15.5" fill="none" stroke="{LINE}"/>
</svg>
"""


def footer():
    FH = 72
    css = COMMON_CSS + """
    @media (prefers-reduced-motion: reduce) { * { animation: none !important; } }"""
    bars = []
    # redaction strips either side of the label
    for x, w in ((56, 120), (186, 54), (250, 168)):
        bars.append(f'<rect x="{x}" y="28" width="{w}" height="16" fill="url(#hatch)" stroke="{LINE}"/>')
    for x, w in ((782, 168), (960, 54), (1024, 120)):
        bars.append(f'<rect x="{x}" y="28" width="{w}" height="16" fill="url(#hatch)" stroke="{LINE}"/>')
    return f"""<svg xmlns="http://www.w3.org/2000/svg" xml:space="preserve" viewBox="0 0 {W} {FH}" width="{W}" height="{FH}" role="img" aria-labelledby="t">
  <title id="t">End of file</title>
  <defs>{COMMON_DEFS}
    <clipPath id="panel"><rect width="{W}" height="{FH}" rx="12"/></clipPath>
  </defs>
  <style>{css}
  </style>
  <g clip-path="url(#panel)">
  <rect width="{W}" height="{FH}" fill="url(#bg)"/>
  <rect width="{W}" height="{FH}" fill="url(#grid)"/>
  {"".join(bars)}
  <text x="{W / 2}" y="41" font-size="14" letter-spacing="5" fill="{MUTED}" text-anchor="middle" {tl("END OF FILE  ▮", 14, 5)}>END OF FILE  <tspan fill="{AMBER}" class="blink">▮</tspan></text>
  <rect class="band" width="{W}" height="120" fill="url(#band)"/>
  <rect width="{W}" height="{FH}" fill="url(#scan)"/>
  </g>
  <rect x=".5" y=".5" width="{W - 1}" height="{FH - 1}" rx="11.5" fill="none" stroke="{LINE}"/>
</svg>
"""


(OUT / "header.svg").write_text(header())
(OUT / "footer.svg").write_text(footer())
print("wrote", OUT / "header.svg", OUT / "footer.svg")
