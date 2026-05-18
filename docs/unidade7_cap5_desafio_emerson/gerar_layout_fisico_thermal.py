#!/usr/bin/env python3
"""
gerar_layout_fisico_thermal.py
Gera 2 figuras de layout físico para o ThermalSensorChip v1.0
Preto/branco com hachuras — SEM CORES.
"""
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import Rectangle, FancyBboxPatch

plt.rcParams.update({
    'font.family': 'DejaVu Sans',
    'font.size': 10,
    'axes.labelcolor': 'black',
    'text.color': 'black',
    'figure.facecolor': 'white',
    'axes.facecolor': 'white',
    'axes.edgecolor': 'black',
})

# ─────────────────────────────────────────────────────────────────────────────
# Figura 1: Zoom célula BJT Q1 vs Q2
# ─────────────────────────────────────────────────────────────────────────────
fig1, ax1 = plt.subplots(figsize=(10, 8), facecolor='white')
ax1.set_xlim(-1, 11)
ax1.set_ylim(-1, 9)
ax1.set_facecolor('white')
ax1.set_aspect('equal')
ax1.set_xlabel('x (µm)', fontsize=11, color='black')
ax1.set_ylabel('y (µm)', fontsize=11, color='black')
ax1.set_title('Layout Zoom — Célula BJT: Q1 (referência) vs. Q2×8 (array)\nThermalSensorChip v1.0',
              fontsize=12, fontweight='bold', color='black')
ax1.tick_params(colors='black')

# ── Q1 cell (left) ──────────────────────────────────────────────────────────
# N-Well (horizontal lines)
nw1 = Rectangle((0, 0), 3.5, 8, facecolor='0.93', edgecolor='black',
                 hatch='------', lw=1.5, zorder=2)
ax1.add_patch(nw1)
ax1.text(1.75, 8.2, 'N-Well Q1', ha='center', fontsize=9, color='black')

# P-base (light gray, no hatch)
pb1 = Rectangle((0.4, 0.8), 2.7, 6.4, facecolor='0.88', edgecolor='black',
                 lw=1.2, zorder=3)
ax1.add_patch(pb1)
ax1.text(1.75, 7.0, 'P-Base', ha='center', fontsize=8, color='black',
         style='italic')

# P+ emitter (dense dots)
em1 = Rectangle((0.9, 2.5), 1.7, 3.0, facecolor='0.75', edgecolor='black',
                 hatch='...', lw=1.2, zorder=4)
ax1.add_patch(em1)
ax1.text(1.75, 4.0, 'P+\nEmitter', ha='center', va='center', fontsize=7.5,
         color='black', fontweight='bold', zorder=5)

# N+ collector ring (diagonal)
# Top strip
nc1_t = Rectangle((0.4, 6.0), 2.7, 0.8, facecolor='0.65', edgecolor='black',
                   hatch='////', lw=1.2, zorder=4)
ax1.add_patch(nc1_t)
# Bottom strip
nc1_b = Rectangle((0.4, 1.0), 2.7, 0.8, facecolor='0.65', edgecolor='black',
                   hatch='////', lw=1.2, zorder=4)
ax1.add_patch(nc1_b)
# Left strip
nc1_l = Rectangle((0.4, 1.0), 0.5, 5.8, facecolor='0.65', edgecolor='black',
                   hatch='////', lw=1.2, zorder=4)
ax1.add_patch(nc1_l)
# Right strip
nc1_r = Rectangle((2.6, 1.0), 0.5, 5.8, facecolor='0.65', edgecolor='black',
                   hatch='////', lw=1.2, zorder=4)
ax1.add_patch(nc1_r)
ax1.text(1.75, 0.4, 'N+ Collector', ha='center', fontsize=7.5, color='black')

# Poly base contact (solid line on top of emitter)
ax1.plot([0.9, 2.6], [5.5, 5.5], 'k-', lw=3, zorder=6)
ax1.text(1.75, 5.7, 'Poly Base\nContact', ha='center', fontsize=7, color='black')

# Contacts
for xc, yc in [(1.2, 3.2), (1.75, 3.2), (2.3, 3.2),
               (1.2, 4.5), (1.75, 4.5), (2.3, 4.5)]:
    ct = Rectangle((xc - 0.12, yc - 0.12), 0.24, 0.24,
                   facecolor='black', edgecolor='black', zorder=7)
    ax1.add_patch(ct)

# Guard ring P+
ax1.add_patch(Rectangle((-0.3, -0.3), 4.1, 8.6,
                         facecolor='none', edgecolor='0.4', lw=1.5,
                         linestyle='--', zorder=1))
ax1.text(-0.4, -0.6, 'Guard Ring P+', fontsize=7.5, color='0.4')

ax1.text(1.75, -0.7, 'Q1 — BJT Referência\n(1× unidade)', ha='center',
         fontsize=9, fontweight='bold', color='black')

# ── Q2 array (right — 8× area) ──────────────────────────────────────────────
# N-Well Q2 (wider)
nw2 = Rectangle((4.5, 0), 6.0, 8, facecolor='0.93', edgecolor='black',
                 hatch='------', lw=1.5, zorder=2)
ax1.add_patch(nw2)
ax1.text(7.5, 8.2, 'N-Well Q2×8 (ABBA layout)', ha='center',
         fontsize=9, color='black')

# 8 emitter cells arranged ABBA (2 columns × 4 rows)
for row in range(4):
    for col in range(2):
        xe = 5.0 + col * 2.5
        ye = 0.5 + row * 1.8
        # P-base
        pb = Rectangle((xe, ye), 2.0, 1.5, facecolor='0.88', edgecolor='black',
                        lw=0.8, zorder=3)
        ax1.add_patch(pb)
        # P+ emitter
        em = Rectangle((xe + 0.3, ye + 0.2), 1.4, 1.1, facecolor='0.75',
                        edgecolor='black', hatch='...', lw=0.8, zorder=4)
        ax1.add_patch(em)
        # Label ABBA pattern
        abba_label = ['A', 'B', 'B', 'A'][row]
        ax1.text(xe + 1.0, ye + 0.75, abba_label, ha='center', va='center',
                 fontsize=9, fontweight='bold', color='black', zorder=5)
        # Contact
        ct = Rectangle((xe + 0.85, ye + 0.55), 0.3, 0.3,
                        facecolor='black', edgecolor='black', zorder=6)
        ax1.add_patch(ct)

# N+ collector frame for Q2
nc2 = Rectangle((4.7, 0.2), 5.6, 7.6, facecolor='none', edgecolor='black',
                 hatch='////', lw=1.5, zorder=4)
ax1.add_patch(nc2)

# Guard ring P+ for Q2
ax1.add_patch(Rectangle((4.3, -0.3), 6.3, 8.6,
                          facecolor='none', edgecolor='0.4', lw=1.5,
                          linestyle='--', zorder=1))

ax1.text(7.5, -0.7, 'Q2×8 — Array ABBA\n(8× área de Q1)', ha='center',
         fontsize=9, fontweight='bold', color='black')

# Size annotation
ax1.annotate('', xy=(4.5, 8.7), xytext=(0, 8.7),
             arrowprops=dict(arrowstyle='<->', color='black', lw=1.5))
ax1.text(2.25, 8.9, '~4 µm', ha='center', fontsize=8, color='black')

ax1.annotate('', xy=(10.5, 8.7), xytext=(4.5, 8.7),
             arrowprops=dict(arrowstyle='<->', color='black', lw=1.5))
ax1.text(7.5, 8.9, '~6 µm (8×)', ha='center', fontsize=8, color='black')

# Legend
legend_handles = [
    mpatches.Patch(facecolor='0.93', edgecolor='black', hatch='------',
                   label='N-Well'),
    mpatches.Patch(facecolor='0.75', edgecolor='black', hatch='...',
                   label='P+ Emitter'),
    mpatches.Patch(facecolor='0.65', edgecolor='black', hatch='////',
                   label='N+ Collector'),
    mpatches.Patch(facecolor='0.88', edgecolor='black',
                   label='P-Base'),
    mpatches.Patch(facecolor='black', edgecolor='black',
                   label='Contact / Metal'),
    mpatches.Patch(facecolor='none', edgecolor='0.4', linestyle='--',
                   label='Guard Ring P+'),
]
ax1.legend(handles=legend_handles, loc='lower right', fontsize=8,
           framealpha=1.0, edgecolor='black')

plt.tight_layout()
plt.savefig('fig_layout_bjt_cell.png', dpi=150, facecolor='white', bbox_inches='tight')
plt.close()
print("fig_layout_bjt_cell.png gerada.")

# ─────────────────────────────────────────────────────────────────────────────
# Figura 2: Die completo
# ─────────────────────────────────────────────────────────────────────────────
fig2, ax2 = plt.subplots(figsize=(12, 8), facecolor='white')
ax2.set_xlim(-2, 34)
ax2.set_ylim(-3, 45)
ax2.set_facecolor('white')
ax2.set_aspect('equal')
ax2.set_xlabel('x (µm)', fontsize=11, color='black')
ax2.set_ylabel('y (µm)', fontsize=11, color='black')
ax2.set_title('Layout Físico Completo — Die ThermalSensorChip v1.0\n(30 µm × 40 µm, CMOS 0.18 µm)',
              fontsize=12, fontweight='bold', color='black')
ax2.tick_params(colors='black')

# ── Die border
die = Rectangle((0, 0), 30, 40, linewidth=2.5, edgecolor='black',
                 facecolor='white', zorder=1)
ax2.add_patch(die)

# ── VDD rail (top)
vdd = Rectangle((0, 37), 30, 3, linewidth=1, edgecolor='black',
                 facecolor='0.25', zorder=2)
ax2.add_patch(vdd)
ax2.text(15, 38.5, 'VDD Rail — Metal-2', ha='center', va='center',
         fontsize=9, color='white', fontweight='bold', zorder=3)

# ── GND rail (bottom)
gnd = Rectangle((0, 0), 30, 2.5, linewidth=1, edgecolor='black',
                 facecolor='black', zorder=2)
ax2.add_patch(gnd)
ax2.text(15, 1.25, 'GND Rail — Metal-2', ha='center', va='center',
         fontsize=9, color='white', fontweight='bold', zorder=3)

# ── PMOS Mirror block (top area)
pmos = Rectangle((1, 27), 20, 9, linewidth=1.5, edgecolor='black',
                  facecolor='0.88', hatch='....', zorder=2)
ax2.add_patch(pmos)
ax2.text(11, 31.5, 'PMOS Mirror (M1 – M3)', ha='center', va='center',
         fontsize=10, fontweight='bold', color='black', zorder=3)
ax2.text(11, 30.5, 'W/L: 10/0.5 µm (M1,M2)  |  80/0.5 µm (M3)', ha='center',
         fontsize=8, color='0.3', zorder=3)

# Poly gates inside PMOS
for xg in [3, 6, 9, 12, 15, 18]:
    pg = Rectangle((xg, 27.5), 0.7, 8, facecolor='0.55', edgecolor='black',
                   hatch='////', lw=0.8, zorder=4)
    ax2.add_patch(pg)

# ── Q1 BJT ref
q1b = Rectangle((1, 15), 6, 11, linewidth=1.5, edgecolor='black',
                  facecolor='0.90', hatch='\\\\\\\\', zorder=2)
ax2.add_patch(q1b)
ax2.text(4, 20.5, 'Q1 BJT\nReferência', ha='center', va='center',
         fontsize=9, fontweight='bold', color='black', zorder=3)

# ── Q2×8 BJT array
q2b = Rectangle((8, 15), 14, 11, linewidth=1.5, edgecolor='black',
                  facecolor='0.85', hatch='\\\\\\\\', zorder=2)
ax2.add_patch(q2b)
ax2.text(15, 20.5, 'Q2×8 BJT Array\n(ABBA Common-Centroid)', ha='center', va='center',
         fontsize=9.5, fontweight='bold', color='black', zorder=3)

# Guard rings
ax2.add_patch(Rectangle((0.5, 14.5), 7, 12, facecolor='none', edgecolor='0.4',
                          lw=1, linestyle='--', zorder=5))
ax2.add_patch(Rectangle((7.5, 14.5), 15, 12, facecolor='none', edgecolor='0.4',
                          lw=1, linestyle='--', zorder=5))
ax2.text(0.2, 26.7, 'GR', fontsize=7, color='0.4')
ax2.text(7.6, 26.7, 'GR', fontsize=7, color='0.4')

# ── R1 resistor
r1b = Rectangle((1, 5), 4, 9, linewidth=1.5, edgecolor='black',
                  facecolor='0.88', hatch='xxxx', zorder=2)
ax2.add_patch(r1b)
ax2.text(3, 9.5, 'R1\n5 kΩ\n(Poly)\n2×50 µm', ha='center', va='center',
         fontsize=8.5, fontweight='bold', color='black', zorder=3)

# ── R2 resistor
r2b = Rectangle((6, 5), 16, 9, linewidth=1.5, edgecolor='black',
                  facecolor='0.88', hatch='xxxx', zorder=2)
ax2.add_patch(r2b)
ax2.text(14, 9.5, 'R2  —  20 kΩ  (Poly)\n2 µm × 200 µm (folded)', ha='center',
         va='center', fontsize=9, fontweight='bold', color='black', zorder=3)

# ── V_PTAT Output pad
out_pad = Rectangle((23, 5), 6, 9, linewidth=2, edgecolor='black',
                      facecolor='0.65', zorder=2)
ax2.add_patch(out_pad)
ax2.text(26, 9.5, '$V_{PTAT}$\nOUT\nPad', ha='center', va='center',
         fontsize=9.5, fontweight='bold', color='black', zorder=3)

# ── Metal-1 routing (light gray lines)
# PMOS to BJT
ax2.plot([11, 11], [27, 26], color='0.5', lw=2.5, zorder=6)
ax2.plot([4, 15, 15], [26, 26, 26], color='0.5', lw=2, zorder=6, linestyle='-')
ax2.plot([4, 4], [26, 26], color='0.5', lw=2, zorder=6)

# BJT to resistors
ax2.plot([4, 4], [15, 14], color='0.5', lw=2, zorder=6)
ax2.plot([15, 15], [15, 14], color='0.5', lw=2, zorder=6)
ax2.plot([4, 15], [14, 14], color='0.5', lw=2, zorder=6)

# Resistor chain
ax2.plot([5, 6], [9.5, 9.5], color='0.4', lw=2, zorder=6)

# R2 to output pad
ax2.plot([22, 23], [9.5, 9.5], color='0.4', lw=2, zorder=6)

# ── Dimension annotations
ax2.annotate('', xy=(30, -1.5), xytext=(0, -1.5),
             arrowprops=dict(arrowstyle='<->', color='black', lw=1.5))
ax2.text(15, -2.0, '30 µm', ha='center', fontsize=10, color='black')

ax2.annotate('', xy=(32, 40), xytext=(32, 0),
             arrowprops=dict(arrowstyle='<->', color='black', lw=1.5))
ax2.text(33, 20, '40 µm', va='center', fontsize=10, color='black', rotation=90)

# ── Area label
ax2.text(15, -3.5, 'Área total: 30 µm × 40 µm = 1200 µm²  |  CMOS 0.18 µm  |  VDD = 1.8 V',
         ha='center', fontsize=9, color='black', style='italic')

# Legend
legend_handles = [
    mpatches.Patch(facecolor='0.88', edgecolor='black', hatch='....',
                   label='PMOS Active'),
    mpatches.Patch(facecolor='0.55', edgecolor='black', hatch='////',
                   label='Poly (gates)'),
    mpatches.Patch(facecolor='0.90', edgecolor='black', hatch='\\\\\\\\',
                   label='BJT (NPN sub.)'),
    mpatches.Patch(facecolor='0.88', edgecolor='black', hatch='xxxx',
                   label='Poly Resistors'),
    mpatches.Patch(facecolor='0.5', edgecolor='black',
                   label='Metal-1 routing'),
    mpatches.Patch(facecolor='0.25', edgecolor='black',
                   label='Metal-2 VDD'),
    mpatches.Patch(facecolor='black', edgecolor='black',
                   label='Metal-2 GND'),
    mpatches.Patch(facecolor='0.65', edgecolor='black',
                   label='Output Pad'),
]
ax2.legend(handles=legend_handles, loc='upper right', fontsize=8,
           framealpha=1.0, edgecolor='black', ncol=2)

plt.tight_layout()
plt.savefig('fig_layout_die_full.png', dpi=150, facecolor='white', bbox_inches='tight')
plt.close()
print("fig_layout_die_full.png gerada.")

print("\nAmbas as figuras de layout geradas com sucesso.")
