"""
Gera o esquematico transistor-level do comparador diferencial de 2 estagios
para o relatorio relatorio_comparador_v2.tex
Saida: fig_schem_comparator.png
"""

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyArrowPatch
import numpy as np

# ── Paleta de cores (igual ao relatorio) ───────────────────────────────────
AQUA      = "#008080"
CODEBLUE  = "#000099"
DARKGRAY  = "#333333"
LIGHTGRAY = "#F2F2F2"
GREEN     = "#007300"
RED       = "#990000"
ORANGE    = "#CC6600"

fig, ax = plt.subplots(figsize=(13, 10))
ax.set_aspect("equal")
ax.axis("off")
ax.set_xlim(-1, 14)
ax.set_ylim(-1, 12)

fig.patch.set_facecolor(LIGHTGRAY)
ax.set_facecolor(LIGHTGRAY)

# ── Helpers ─────────────────────────────────────────────────────────────────

def wire(ax, x1, y1, x2, y2, color=DARKGRAY, lw=1.6, zorder=2):
    ax.plot([x1, x2], [y1, y2], color=color, lw=lw, zorder=zorder,
            solid_capstyle="round")

def node_dot(ax, x, y, color=DARKGRAY, r=0.08):
    ax.add_patch(plt.Circle((x, y), r, color=color, zorder=5))

def label(ax, x, y, txt, ha="center", va="center", fs=9,
          color=DARKGRAY, bold=False, bg=None):
    kw = dict(fontsize=fs, ha=ha, va=va, color=color, zorder=8,
              fontweight="bold" if bold else "normal")
    if bg:
        kw["bbox"] = dict(boxstyle="round,pad=0.2", fc=bg, ec="none", alpha=0.85)
    ax.text(x, y, txt, **kw)

def draw_pmos(ax, cx, cy, flipped=False):
    """
    PMOS symbol: gate on left, source on top, drain on bottom.
    cx,cy = centre of channel bar.
    flipped: mirror horizontally (gate on right side).
    """
    W, H = 0.35, 0.70        # channel box half-width / half-height
    gl   = 0.45              # gate lead length
    arrow_r = 0.13           # bulk-arrow inset circle radius

    sign = -1 if flipped else 1

    # Channel box (body rectangle)
    rect = plt.Rectangle((cx - W, cy - H), 2*W, 2*H,
                          linewidth=1.5, edgecolor=AQUA, facecolor="white", zorder=3)
    ax.add_patch(rect)

    # Gate line (horizontal from left or right)
    gate_x = cx - sign * (W + gl)
    ax.plot([gate_x, cx - sign * W], [cy, cy],
            color=AQUA, lw=1.8, zorder=4)

    # Source (top)  Drain (bottom)
    ax.plot([cx, cx], [cy + H, cy + H + 0.5],
            color=AQUA, lw=1.8, zorder=4)
    ax.plot([cx, cx], [cy - H, cy - H - 0.5],
            color=AQUA, lw=1.8, zorder=4)

    # PMOS bubble on gate
    circle = plt.Circle((cx - sign * W - sign * 0.12, cy),
                         0.10, linewidth=1.2, edgecolor=AQUA,
                         facecolor="white", zorder=5)
    ax.add_patch(circle)

    # Arrow on source (pointing inward = PMOS)
    ax.annotate("",
        xy=(cx, cy + H - 0.01),
        xytext=(cx, cy + H + 0.35),
        arrowprops=dict(arrowstyle="->", color=AQUA, lw=1.5),
        zorder=6)

    return dict(gate=(gate_x, cy),
                source=(cx, cy + H + 0.5),
                drain=(cx, cy - H - 0.5))


def draw_nmos(ax, cx, cy, flipped=False):
    """
    NMOS symbol: gate on left, source on bottom, drain on top.
    flipped: gate on right.
    """
    W, H = 0.35, 0.70
    gl   = 0.45

    sign = -1 if flipped else 1

    rect = plt.Rectangle((cx - W, cy - H), 2*W, 2*H,
                          linewidth=1.5, edgecolor=CODEBLUE,
                          facecolor="white", zorder=3)
    ax.add_patch(rect)

    # Gate
    gate_x = cx - sign * (W + gl)
    ax.plot([gate_x, cx - sign * W], [cy, cy],
            color=CODEBLUE, lw=1.8, zorder=4)

    # Drain (top)  Source (bottom)
    ax.plot([cx, cx], [cy + H, cy + H + 0.5],
            color=CODEBLUE, lw=1.8, zorder=4)
    ax.plot([cx, cx], [cy - H, cy - H - 0.5],
            color=CODEBLUE, lw=1.8, zorder=4)

    # Arrow on drain (pointing inward = NMOS)
    ax.annotate("",
        xy=(cx, cy + H - 0.01),
        xytext=(cx, cy + H + 0.35),
        arrowprops=dict(arrowstyle="<-", color=CODEBLUE, lw=1.5),
        zorder=6)

    return dict(gate=(gate_x, cy),
                drain=(cx, cy + H + 0.5),
                source=(cx, cy - H - 0.5))


def draw_vdd_symbol(ax, x, y, lbl="VDD"):
    ax.plot([x, x], [y, y + 0.4], color=RED, lw=2, zorder=4)
    ax.plot([x - 0.35, x + 0.35], [y + 0.4, y + 0.4],
            color=RED, lw=2.5, zorder=4)
    label(ax, x, y + 0.72, lbl, fs=9, color=RED, bold=True)


def draw_gnd_symbol(ax, x, y):
    ax.plot([x, x], [y - 0.3, y], color=DARKGRAY, lw=2, zorder=4)
    for i, w in enumerate([0.35, 0.22, 0.10]):
        yy = y - 0.3 - i * 0.15
        ax.plot([x - w, x + w], [yy, yy], color=DARKGRAY, lw=2.0, zorder=4)


# ════════════════════════════════════════════════════════════════════════════
#  LAYOUT POSITIONS
#  M5  (tail PMOS)   — top centre
#  M1  (diff left)   — second row, left
#  M2  (diff right)  — second row, right
#  M3  (mirror diode)— third row, left
#  M4  (mirror copy) — third row, right
#  M6  (CS NMOS)     — bottom right
#  M7  (load PMOS)   — above M6
# ════════════════════════════════════════════════════════════════════════════

# --- M5  PMOS tail current source (cx=6.5, top) ---
M5_CX, M5_CY = 6.5, 9.2
m5 = draw_pmos(ax, M5_CX, M5_CY)

# VDD above M5
draw_vdd_symbol(ax, M5_CX, m5["source"][1])

# --- M1  PMOS diff left (INM) ---
M1_CX, M1_CY = 4.5, 6.6
m1 = draw_pmos(ax, M1_CX, M1_CY)

# --- M2  PMOS diff right (INP) ---
M2_CX, M2_CY = 8.5, 6.6
m2 = draw_pmos(ax, M2_CX, M2_CY, flipped=True)

# Vtail node  (connect drain of M5, sources of M1 & M2)
Vtail_Y = m5["drain"][1]                     # = M5_CY - H - 0.5
# Route: M5 drain down to Vtail_Y, then horizontal to M1 and M2 sources
wire(ax, M5_CX, Vtail_Y, M5_CX, M1_CY + 0.70 + 0.5)   # vertical stub down from M5

# Horizontal Vtail rail at Vtail_Y level connecting both differential sources
wire(ax, M1_CX, Vtail_Y, M2_CX, Vtail_Y)
# From diff pair sources up to Vtail rail
wire(ax, M1_CX, m1["source"][1], M1_CX, Vtail_Y)
wire(ax, M2_CX, m2["source"][1], M2_CX, Vtail_Y)
wire(ax, M5_CX, Vtail_Y, M5_CX, Vtail_Y)      # ensure dot
node_dot(ax, M1_CX, Vtail_Y)
node_dot(ax, M2_CX, Vtail_Y)
node_dot(ax, M5_CX, Vtail_Y)
label(ax, 5.6, Vtail_Y + 0.15, "Vtail", fs=8, color=GREEN, bold=True,
      bg="white")

# Vbias label for M5 gate
wire(ax, m5["gate"][0], m5["gate"][1], m5["gate"][0] - 0.5, m5["gate"][1])
label(ax, m5["gate"][0] - 0.9, m5["gate"][1],
      "Vbias", fs=8, color=ORANGE, bold=True)
node_dot(ax, m5["gate"][0], m5["gate"][1])

# --- M3  NMOS mirror diode (left, below M1) ---
M3_CX, M3_CY = 4.5, 3.8
m3 = draw_nmos(ax, M3_CX, M3_CY)

# --- M4  NMOS mirror copy (right, below M2) ---
M4_CX, M4_CY = 8.5, 3.8
m4 = draw_nmos(ax, M4_CX, M4_CY, flipped=True)

# Vd1 node: drain of M1, gate+drain of M3, gate of M4
Vd1_Y = m1["drain"][1]               # = M1_CY - H - 0.5
wire(ax, M1_CX, Vd1_Y, M3_CX, m3["drain"][1])   # M1 drain -> M3 drain (vertical)
# M3 gate shorting to its own drain (diode connection)
# Gate is at (m3["gate"][0], m3["gate"][1])
wire(ax, m3["gate"][0], m3["gate"][1], m3["gate"][0], Vd1_Y - 0.1)
node_dot(ax, m3["gate"][0], Vd1_Y - 0.1)
wire(ax, m3["gate"][0], Vd1_Y - 0.1, M3_CX, Vd1_Y - 0.1)
node_dot(ax, M3_CX, Vd1_Y - 0.1)
# Horizontal Vd1 bus from M3 gate to M4 gate (going left from M4)
# M4 gate is on the right side (flipped)
m4_gate_x = m4["gate"][0]   # right side
wire(ax, m3["gate"][0], m3["gate"][1],
     m3["gate"][0], 5.05)
wire(ax, m3["gate"][0], 5.05, m4_gate_x, 5.05)
wire(ax, m4_gate_x, 5.05, m4_gate_x, m4["gate"][1])
node_dot(ax, m3["gate"][0], m3["gate"][1])
node_dot(ax, m4_gate_x, m4["gate"][1])
label(ax, 6.5, 5.05 + 0.18, "Vd1", fs=8.5, color=AQUA, bold=True,
      bg="white")

# Vout1 node: drain of M2, drain of M4, gate of M6
Vout1_Y = m2["drain"][1]
wire(ax, M2_CX, Vout1_Y, M4_CX, m4["drain"][1])

# GND for M3 and M4 sources
draw_gnd_symbol(ax, M3_CX, m3["source"][1])
draw_gnd_symbol(ax, M4_CX, m4["source"][1])

# --- M6  NMOS common-source (output stage driver) ---
M6_CX, M6_CY = 11.0, 2.8
m6 = draw_nmos(ax, M6_CX, M6_CY)
draw_gnd_symbol(ax, M6_CX, m6["source"][1])

# --- M7  PMOS active load (above M6) ---
M7_CX, M7_CY = 11.0, 5.8
m7 = draw_pmos(ax, M7_CX, M7_CY, flipped=True)
draw_vdd_symbol(ax, M7_CX, m7["source"][1])

# Vout node: drain of M6 meets drain of M7
Vout_Y = (m6["drain"][1] + m7["drain"][1]) / 2
wire(ax, M6_CX, m6["drain"][1], M6_CX, Vout_Y)
wire(ax, M7_CX, m7["drain"][1], M7_CX, Vout_Y)
node_dot(ax, M6_CX, Vout_Y)
# Vout output lead
wire(ax, M6_CX, Vout_Y, M6_CX + 0.9, Vout_Y, color=RED)
label(ax, M6_CX + 1.35, Vout_Y, "Vout\n(comp_out)",
      fs=8.5, color=RED, bold=True, ha="left")
node_dot(ax, M6_CX + 0.9, Vout_Y, color=RED)

# Vbias2 for M7 gate
wire(ax, m7["gate"][0], m7["gate"][1], m7["gate"][0] + 0.4, m7["gate"][1])
label(ax, m7["gate"][0] + 0.85, m7["gate"][1],
      "Vbias2", fs=8, color=ORANGE, bold=True, ha="left")
node_dot(ax, m7["gate"][0], m7["gate"][1])

# Connect Vout1 -> M6 gate
# Vout1 is at (M4_CX, Vout1_Y); M6 gate is at m6["gate"]
# Route: Vout1 node right -> down -> M6 gate
Vout1_bus_x = M4_CX          # where Vout1 rail sits horizontally
wire(ax, Vout1_bus_x, Vout1_Y, Vout1_bus_x, Vout1_Y)   # dot
node_dot(ax, M2_CX, Vout1_Y)
node_dot(ax, M4_CX, m4["drain"][1])
# Vout1 horizontal stub to the right, then down to M6 gate
wire(ax, M4_CX, Vout1_Y, 10.0, Vout1_Y)
wire(ax, 10.0, Vout1_Y, 10.0, m6["gate"][1])
wire(ax, 10.0, m6["gate"][1], m6["gate"][0], m6["gate"][1])
node_dot(ax, 10.0, m6["gate"][1])
label(ax, 9.35, Vout1_Y + 0.18, "Vout1",
      fs=8.5, color=AQUA, bold=True, bg="white")

# INP label on M2 gate
wire(ax, m2["gate"][0], m2["gate"][1], m2["gate"][0] + 0.3, m2["gate"][1])
label(ax, m2["gate"][0] + 0.75, m2["gate"][1],
      "INP (+)", fs=9, color=GREEN, bold=True, ha="left")

# INM label on M1 gate
wire(ax, m1["gate"][0], m1["gate"][1], m1["gate"][0] - 0.3, m1["gate"][1])
label(ax, m1["gate"][0] - 0.75, m1["gate"][1],
      "INM (−)", fs=9, color=GREEN, bold=True, ha="right")

# ── Transistor labels ─────────────────────────────────────────────────────
label(ax, M5_CX + 0.55, M5_CY + 0.2, "M5\nPMOS\n10/2", fs=7.5,
      color=AQUA, ha="left")
label(ax, M1_CX - 0.55, M1_CY,       "M1\nPMOS\n20/1", fs=7.5,
      color=AQUA, ha="right")
label(ax, M2_CX + 0.55, M2_CY,       "M2\nPMOS\n20/1", fs=7.5,
      color=AQUA, ha="left")
label(ax, M3_CX - 0.55, M3_CY,       "M3\nNMOS\n10/1", fs=7.5,
      color=CODEBLUE, ha="right")
label(ax, M4_CX + 0.55, M4_CY,       "M4\nNMOS\n10/1", fs=7.5,
      color=CODEBLUE, ha="left")
label(ax, M6_CX + 0.55, M6_CY,       "M6\nNMOS\n10/0.5", fs=7.5,
      color=CODEBLUE, ha="left")
label(ax, M7_CX + 0.55, M7_CY,       "M7\nPMOS\n20/0.5", fs=7.5,
      color=AQUA, ha="left")

# ── Stage dividers (shaded backgrounds) ──────────────────────────────────
stage1 = mpatches.FancyBboxPatch(
    (2.8, 2.8), 7.6, 8.2,
    boxstyle="round,pad=0.15",
    linewidth=1.4, linestyle="--",
    edgecolor=AQUA, facecolor=AQUA, alpha=0.04, zorder=0)
ax.add_patch(stage1)
label(ax, 3.2, 10.7, "Estágio 1\n(Par Diferencial + Espelho)",
      fs=8, color=AQUA, bold=True, ha="left", bg="white")

stage2 = mpatches.FancyBboxPatch(
    (9.5, 1.2), 3.5, 6.8,
    boxstyle="round,pad=0.15",
    linewidth=1.4, linestyle="--",
    edgecolor=CODEBLUE, facecolor=CODEBLUE, alpha=0.04, zorder=0)
ax.add_patch(stage2)
label(ax, 11.25, 7.65, "Estágio 2\n(Amplificador CS)",
      fs=8, color=CODEBLUE, bold=True, ha="center", bg="white")

# ── Title ─────────────────────────────────────────────────────────────────
ax.text(6.5, 11.5,
        "Esquemático Transistor-Level — Comparador Diferencial CMOS 0.18 µm",
        ha="center", va="center", fontsize=11, fontweight="bold",
        color=DARKGRAY,
        bbox=dict(boxstyle="round,pad=0.4", fc="white",
                  ec=AQUA, lw=1.5))

# ── Legend ────────────────────────────────────────────────────────────────
leg_patches = [
    mpatches.Patch(facecolor=AQUA,      label="PMOS (M1, M2, M5, M7)"),
    mpatches.Patch(facecolor=CODEBLUE,  label="NMOS (M3, M4, M6)"),
    mpatches.Patch(facecolor=GREEN,     label="Entradas (INP, INM)"),
    mpatches.Patch(facecolor=RED,       label="Saída (Vout)"),
    mpatches.Patch(facecolor=ORANGE,    label="Polarização (Vbias)"),
]
ax.legend(handles=leg_patches, loc="lower left",
          fontsize=7.5, framealpha=0.9,
          facecolor="white", edgecolor=AQUA,
          bbox_to_anchor=(-0.02, -0.02))

plt.tight_layout(pad=0.5)
plt.savefig("fig_schem_comparator.png", dpi=150, bbox_inches="tight",
            facecolor=LIGHTGRAY)
plt.close()
print("fig_schem_comparator.png gerado com sucesso.")
