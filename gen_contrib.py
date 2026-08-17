# -*- coding: utf-8 -*-
"""Generate self-hosted GitHub-style contribution-graph SVGs (teal themed)
that reproduce the @anusual multi-year story. Stylized, not exact daily data."""
import os, random

ROOT = os.path.dirname(os.path.abspath(__file__))
CELL, GAP = 11, 3
STEP = CELL + GAP
COLS, ROWS = 53, 7
ML, MT = 30, 20
PAL = ["#ebedf0", "#b9e7e1", "#6fccc1", "#2ba696", "#0d7d73"]  # teal scale
MONTHS_JAN = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
MONTHS_JUN = ["Jun","Jul","Aug","Sep","Oct","Nov","Dec","Jan","Feb","Mar","Apr","May","Jun"]

def render(levels, months):
    W = ML + COLS * STEP + 6
    H = MT + ROWS * STEP + 4
    p = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" '
         f'width="{W}" height="{H}" font-family="JetBrains Mono, ui-monospace, monospace">']
    n = len(months)
    for i, m in enumerate(months):
        x = ML + int(round(i * COLS / n)) * STEP
        p.append(f'<text x="{x}" y="12" font-size="10" fill="#97a0ab">{m}</text>')
    for r, lab in [(1, "Mon"), (3, "Wed"), (5, "Fri")]:
        y = MT + r * STEP + CELL - 1
        p.append(f'<text x="0" y="{y}" font-size="9" fill="#97a0ab">{lab}</text>')
    for c in range(COLS):
        for r in range(ROWS):
            x, y = ML + c * STEP, MT + r * STEP
            p.append(f'<rect x="{x}" y="{y}" width="{CELL}" height="{CELL}" rx="2" fill="{PAL[levels[c][r]]}"/>')
    p.append('</svg>')
    return "\n".join(p)

def blank():
    return [[0] * ROWS for _ in range(COLS)]

# ---- 2024: 50 contributions, only late Oct-Dec ----
random.seed(2024)
lv = blank()
for c in range(43, COLS):
    for r in range(ROWS):
        if random.random() < 0.42:
            lv[c][r] = random.choice([1, 1, 2, 2, 3, 4])
open(os.path.join(ROOT, "assets/gh-2024.svg"), "w").write(render(lv, MONTHS_JAN))

# ---- 2025: 1,266, ramping through the year ----
random.seed(2025)
lv = blank()
for c in range(COLS):
    ramp = 0.22 + 0.6 * (c / COLS)
    for r in range(ROWS):
        pr = ramp * (0.5 if r in (0, 6) else 1.0)
        if random.random() < pr:
            hi = 1 + int(random.random() * (1 + 3 * (c / COLS)))
            lv[c][r] = min(4, max(1, hi))
open(os.path.join(ROOT, "assets/gh-2025.svg"), "w").write(render(lv, MONTHS_JAN))

# ---- last year: 1,563, dense throughout, lighter at the recent edge ----
random.seed(2026)
lv = blank()
for c in range(COLS):
    base = 0.72 if c < COLS - 3 else 0.4
    for r in range(ROWS):
        pr = base * (0.55 if r in (0, 6) else 1.0)
        if random.random() < pr:
            lv[c][r] = random.choice([1, 2, 2, 3, 3, 4])
open(os.path.join(ROOT, "assets/gh-lastyear.svg"), "w").write(render(lv, MONTHS_JUN))

print("wrote assets/gh-2024.svg, gh-2025.svg, gh-lastyear.svg")
