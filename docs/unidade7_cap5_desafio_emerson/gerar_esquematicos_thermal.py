#!/usr/bin/env python3
"""
gerar_esquematicos_thermal.py
Gera 3 esquemáticos para o relatório ThermalSensorChip v1.0
Todos em preto/branco — SEM CORES.
"""
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, Circle, Arc, FancyArrowPatch
import matplotlib.patheffects as pe

plt.rcParams.update({
    'font.family': 'DejaVu Sans',
    'font.size': 10,
    'axes.labelcolor': 'black',
    'text.color': 'black',
    'figure.facecolor': 'white',
    'axes.facecolor': 'white',
})

# ─────────────────────────────────────────────────────────────────────────────
# Helpers para desenho de componentes
# ─────────────────────────────────────────────────────────────────────────────
def draw_pmos(ax, cx, cy, scale=1.0, label=''):
    """Draw PMOS symbol: source at top, drain at bottom, gate on left."""
    s = scale
    # Body lines
    ax.plot([cx, cx], [cy + 0.5*s, cy + 0.9*s], 'k-', lw=1.5)  # source
    ax.plot([cx, cx], [cy - 0.9*s, cy - 0.5*s], 'k-', lw=1.5)  # drain
    ax.plot([cx - 0.5*s, cx - 0.5*s], [cy - 0.5*s, cy + 0.5*s], 'k-', lw=1.5)  # channel
    ax.plot([cx - 0.5*s, cx], [cy + 0.5*s, cy + 0.5*s], 'k-', lw=1.5)  # source connect
    ax.plot([cx - 0.5*s, cx], [cy - 0.5*s, cy - 0.5*s], 'k-', lw=1.5)  # drain connect
    # Gate line
    ax.plot([cx - 0.8*s, cx - 0.65*s], [cy, cy], 'k-', lw=1.5)  # gate wire
    ax.plot([cx - 0.65*s, cx - 0.65*s], [cy - 0.5*s, cy + 0.5*s], 'k-', lw=3.5)  # gate electrode
    # PMOS bubble on gate
    circ = Circle((cx - 0.73*s, cy), 0.08*s, facecolor='white', edgecolor='black', lw=1.5, zorder=5)
    ax.add_patch(circ)
    # Arrow indicating PMOS direction (pointing up = source to drain)
    ax.annotate('', xy=(cx, cy + 0.1*s), xytext=(cx, cy - 0.1*s),
                arrowprops=dict(arrowstyle='->', color='black', lw=1.2))
    if label:
        ax.text(cx + 0.25*s, cy, label, ha='left', va='center', fontsize=8, color='black')

def draw_npn(ax, cx, cy, scale=1.0, label=''):
    """Draw NPN BJT symbol."""
    s = scale
    # Base vertical line
    ax.plot([cx - 0.5*s, cx - 0.5*s], [cy - 0.5*s, cy + 0.5*s], 'k-', lw=2)
    # Collector line (top right)
    ax.plot([cx - 0.5*s, cx + 0.5*s], [cy + 0.3*s, cy + 0.7*s], 'k-', lw=1.5)
    # Emitter line (bottom right) with arrow
    ax.annotate('', xy=(cx + 0.5*s, cy - 0.7*s), xytext=(cx - 0.5*s, cy - 0.3*s),
                arrowprops=dict(arrowstyle='->', color='black', lw=1.5))
    ax.plot([cx - 0.5*s, cx + 0.5*s], [cy - 0.3*s, cy - 0.7*s], 'k-', lw=1.5)
    # Base connection
    ax.plot([cx - 0.9*s, cx - 0.5*s], [cy, cy], 'k-', lw=1.5)
    # Circle
    circ = Circle((cx, cy), 0.65*s, facecolor='white', edgecolor='black', lw=1.5, zorder=4)
    ax.add_patch(circ)
    if label:
        ax.text(cx + 0.8*s, cy, label, ha='left', va='center', fontsize=8, color='black')

def draw_resistor(ax, x1, y1, x2, y2, label='', n_zigzag=5):
    """Draw a resistor between two points (vertical or horizontal)."""
    if abs(x2 - x1) < 0.01:  # vertical
        y_mid = (y1 + y2) / 2
        h = abs(y2 - y1) * 0.5
        x = x1
        ax.plot([x, x], [y1, y_mid - h/2], 'k-', lw=1.5)
        ax.plot([x, x], [y_mid + h/2, y2], 'k-', lw=1.5)
        # Zigzag
        ys = np.linspace(y_mid - h/2, y_mid + h/2, 2*n_zigzag + 1)
        xs = [x + (0.15 if i % 2 == 1 else -0.15 if i % 2 == 0 else 0)
              for i in range(len(ys))]
        xs[0] = x; xs[-1] = x
        ax.plot(xs, ys, 'k-', lw=1.5)
        if label:
            ax.text(x + 0.4, (y1 + y2)/2, label, ha='left', va='center',
                    fontsize=8, color='black')
    else:  # horizontal
        x_mid = (x1 + x2) / 2
        w = abs(x2 - x1) * 0.5
        y = y1
        ax.plot([x1, x_mid - w/2], [y, y], 'k-', lw=1.5)
        ax.plot([x_mid + w/2, x2], [y, y], 'k-', lw=1.5)
        xs2 = np.linspace(x_mid - w/2, x_mid + w/2, 2*n_zigzag + 1)
        ys2 = [y + (0.15 if i % 2 == 1 else -0.15 if i % 2 == 0 else 0)
               for i in range(len(xs2))]
        ys2[0] = y; ys2[-1] = y
        ax.plot(xs2, ys2, 'k-', lw=1.5)
        if label:
            ax.text((x1+x2)/2, y + 0.3, label, ha='center', va='bottom',
                    fontsize=8, color='black')

def draw_gnd(ax, x, y, scale=0.5):
    """Draw GND symbol."""
    ax.plot([x, x], [y, y - 0.15*scale/0.5], 'k-', lw=1.5)
    for i, (w, shift) in enumerate([(0.4, 0), (0.25, -0.12), (0.12, -0.24)]):
        yy = y - (0.15 + shift) * scale/0.5
        ax.plot([x - w*scale/0.5/2, x + w*scale/0.5/2], [yy, yy], 'k-', lw=1.5)

def draw_vdd(ax, x, y, label='VDD', scale=1.0):
    """Draw VDD power supply symbol."""
    ax.plot([x, x], [y, y + 0.3*scale], 'k-', lw=1.5)
    ax.plot([x - 0.25*scale, x + 0.25*scale], [y + 0.3*scale, y + 0.3*scale], 'k-', lw=2)
    ax.text(x, y + 0.5*scale, label, ha='center', va='bottom', fontsize=9,
            fontweight='bold', color='black')

# ─────────────────────────────────────────────────────────────────────────────
# Figura 1: Célula PTAT completa
# ─────────────────────────────────────────────────────────────────────────────
fig1, ax1 = plt.subplots(figsize=(13, 9), facecolor='white')
ax1.set_xlim(-1, 14)
ax1.set_ylim(-2, 10)
ax1.axis('off')
ax1.set_facecolor('white')
ax1.set_title('Esquemático da Célula PTAT — ThermalSensorChip v1.0',
              fontsize=13, fontweight='bold', color='black', pad=10)

# VDD rail
ax1.plot([-0.5, 13.5], [9.0, 9.0], 'k-', lw=2)
ax1.text(6.5, 9.3, 'VDD = 1.8 V', ha='center', fontweight='bold', fontsize=11)

# ── M1 (diode-connected) at x=2
m1x, m1y = 2, 6.5
ax1.plot([m1x, m1x], [9.0, m1y + 0.9], 'k-', lw=1.5)  # source to VDD
draw_pmos(ax1, m1x, m1y, scale=0.9, label='M1\nPMOS\n10/0.5')
ax1.plot([m1x, m1x], [m1y - 0.9, m1y - 1.5], 'k-', lw=1.5)  # drain down
# Diode connect (gate to drain)
ax1.plot([m1x - 0.8*0.9, m1x - 0.8*0.9], [m1y, m1y - 1.5], 'k-', lw=1.2)
ax1.plot([m1x - 0.8*0.9, m1x], [m1y - 1.5, m1y - 1.5], 'k-', lw=1.2)
# vbias label
ax1.text(m1x - 1.1, m1y - 1.5, 'vbias', ha='right', fontsize=8.5, color='black',
         style='italic')

# ── M2 at x=6
m2x, m2y = 6, 6.5
ax1.plot([m2x, m2x], [9.0, m2y + 0.9], 'k-', lw=1.5)
draw_pmos(ax1, m2x, m2y, scale=0.9, label='M2\nPMOS\n10/0.5')
ax1.plot([m2x, m2x], [m2y - 0.9, m2y - 1.5], 'k-', lw=1.5)
# Gate connects to vbias
ax1.plot([m2x - 0.8*0.9, m1x - 0.8*0.9], [m2y, m2y], 'k-', lw=1.2)
ax1.text(m2x + 0.3, m2y - 1.3, 'n1', fontsize=8.5, color='black', style='italic')

# ── M3 at x=10 (8x wider)
m3x, m3y = 10, 6.5
ax1.plot([m3x, m3x], [9.0, m3y + 0.9], 'k-', lw=1.5)
draw_pmos(ax1, m3x, m3y, scale=0.9, label='M3\nPMOS\n80/0.5\n(8×)')
ax1.plot([m3x, m3x], [m3y - 0.9, m3y - 1.5], 'k-', lw=1.5)
ax1.plot([m3x - 0.8*0.9, m1x - 0.8*0.9], [m3y, m2y], 'k--', lw=1.0)
ax1.text(m3x + 0.3, m3y - 1.3, 'n2', fontsize=8.5, color='black', style='italic')

# ── Q1 NPN at x=6, y=2
q1x, q1y = 6, 2.5
ax1.plot([m2x, q1x], [m2y - 1.5, q1y + 0.7], 'k-', lw=1.5)  # collector from M2
draw_npn(ax1, q1x, q1y, scale=0.7, label='Q1')
# Base to collector (diode connect)
ax1.plot([q1x - 0.9*0.7, q1x + 0.5*0.7], [q1y, q1y + 0.7*0.7], 'k-', lw=1.2)
# Emitter to GND
ax1.plot([q1x + 0.5*0.7, q1x + 0.5*0.7], [q1y - 0.7*0.7, q1y - 1.5], 'k-', lw=1.5)
draw_gnd(ax1, q1x + 0.5*0.7, q1y - 1.5)

# ── Q2 NPN at x=10, y=2
q2x, q2y = 10, 2.5
ax1.plot([m3x, q2x], [m3y - 1.5, q2y + 0.7], 'k-', lw=1.5)  # collector from M3
draw_npn(ax1, q2x, q2y, scale=0.7, label='Q2×8')
# Base to collector
ax1.plot([q2x - 0.9*0.7, q2x + 0.5*0.7], [q2y, q2y + 0.7*0.7], 'k-', lw=1.2)
# Emitter to GND
ax1.plot([q2x + 0.5*0.7, q2x + 0.5*0.7], [q2y - 0.7*0.7, q2y - 1.5], 'k-', lw=1.5)
draw_gnd(ax1, q2x + 0.5*0.7, q2y - 1.5)

# ── R1 (from n1=node between M2 and Q1, down to delta)
r1x = 2
ax1.plot([q1x, r1x + 0.5], [q1y + 0.7, q1y + 0.7], 'k-', lw=1.2)
ax1.plot([r1x + 0.5, r1x + 0.5], [q1y + 0.7, 1.0], 'k-', lw=1.2)
draw_resistor(ax1, r1x + 0.5, 1.0, r1x + 0.5, -0.5, label='R1 = 5 kΩ')
ax1.text(r1x + 0.5, 0.25, 'delta', ha='center', fontsize=8, color='black',
         style='italic', bbox=dict(facecolor='white', edgecolor='none'))

# ── R2 (from delta to GND)
draw_resistor(ax1, r1x + 0.5, -0.5, r1x + 0.5, -1.5, label='R2 = 20 kΩ')
draw_gnd(ax1, r1x + 0.5, -1.5)

# Output node label
ax1.annotate('$V_{PTAT}$ output',
             xy=(r1x + 0.5, 0.0),
             xytext=(r1x - 0.8, -0.5),
             fontsize=9, color='black',
             arrowprops=dict(arrowstyle='->', color='black', lw=1.2),
             bbox=dict(boxstyle='round,pad=0.3', facecolor='0.95', edgecolor='black'))

# Equation box
eq_box = dict(boxstyle='round,pad=0.4', facecolor='0.95', edgecolor='black', lw=1)
ax1.text(12.5, 4.0,
         r'$\Delta V_{BE} = V_T\ln(N)$' + '\n' + r'$V_{PTAT} = \frac{R_2}{R_1}\Delta V_{BE}$' + '\n' + r'$\approx 2.06\,\mathrm{mV/°C}$',
         ha='center', va='center', fontsize=9, color='black',
         bbox=eq_box, transform=ax1.transData)

plt.tight_layout()
plt.savefig('fig_schem_ptat_cell.png', dpi=150, facecolor='white', bbox_inches='tight')
plt.close()
print("fig_schem_ptat_cell.png gerada.")

# ─────────────────────────────────────────────────────────────────────────────
# Figura 2: Princípio do sensor BJT
# ─────────────────────────────────────────────────────────────────────────────
fig2, ax2 = plt.subplots(figsize=(10, 8), facecolor='white')
ax2.set_xlim(0, 10)
ax2.set_ylim(-1, 9)
ax2.axis('off')
ax2.set_facecolor('white')
ax2.set_title('Princípio do Sensor Térmico BJT — ThermalSensorChip v1.0',
              fontsize=12, fontweight='bold', color='black', pad=10)

# ── BJT symbol (large) centered
bx, by = 3.5, 5.0
draw_npn(ax2, bx, by, scale=1.0, label='NPN\n(substrate)')

# Annotations B/C/E
ax2.text(bx - 1.6, by, 'B', fontsize=11, fontweight='bold', color='black')
ax2.text(bx + 0.8, by + 1.0, 'C', fontsize=11, fontweight='bold', color='black')
ax2.text(bx + 0.8, by - 1.0, 'E', fontsize=11, fontweight='bold', color='black')

# Temperature arrow
ax2.annotate('', xy=(bx, by + 1.8), xytext=(bx, by + 0.9),
             arrowprops=dict(arrowstyle='->', color='black', lw=2,
                             connectionstyle='arc3,rad=0'))
ax2.text(bx + 0.2, by + 1.35, 'T ↑', fontsize=10, color='black', fontweight='bold')

# Equation boxes on right
eq_style = dict(boxstyle='round,pad=0.4', facecolor='0.95', edgecolor='black', lw=1)
ax2.text(7.0, 7.5,
         r'$V_{BE}(T) = V_{BG} - (V_{BG}-V_{BE0})\frac{T}{T_0}$' + '\n' + r'$+ V_T\ln\!\left(\frac{T}{T_0}\right)$',
         ha='center', va='center', fontsize=9.5, color='black', bbox=eq_style)
ax2.text(7.0, 5.5,
         r'$V_T = \frac{kT}{q} \approx 26\,\mathrm{mV}$ @ 300K',
         ha='center', va='center', fontsize=9.5, color='black', bbox=eq_style)
ax2.text(7.0, 3.8,
         r'$\frac{dV_{BE}}{dT} \approx -1.2\,\mathrm{mV/°C}$',
         ha='center', va='center', fontsize=10, color='black',
         fontweight='bold', bbox=eq_style)

# Table V_BE vs T
ax2.text(1.5, 2.5, 'Tabela: $V_{BE}$ vs. Temperatura (modelo)',
         fontsize=10, fontweight='bold', color='black')
col_headers = ['T (°C)', '$V_{BE}$ (mV)']
rows = [('-40', '742'), ('27', '620'), ('85', '523'), ('125', '452')]
table_x = [1.5, 4.5]
row_h = 0.45
ax2.plot([1.3, 6.0], [2.2, 2.2], 'k-', lw=1.2)
ax2.plot([1.3, 6.0], [1.75, 1.75], 'k-', lw=0.8)
for i, h in enumerate(col_headers):
    ax2.text(table_x[i], 2.0, h, ha='center', va='center', fontsize=9,
             fontweight='bold', color='black')
for j, (t_val, v_val) in enumerate(rows):
    yy = 1.75 - (j + 0.5) * row_h
    facecolor = '0.92' if j % 2 == 0 else 'white'
    ax2.add_patch(FancyBboxPatch((1.3, yy - row_h/2), 4.7, row_h,
                                  boxstyle='square,pad=0', facecolor=facecolor,
                                  edgecolor='0.7', linewidth=0.5))
    ax2.text(table_x[0], yy, t_val, ha='center', va='center', fontsize=9, color='black')
    ax2.text(table_x[1], yy, v_val, ha='center', va='center', fontsize=9, color='black')

ax2.plot([1.3, 1.3], [-0.05, 2.2], 'k-', lw=0.8)
ax2.plot([6.0, 6.0], [-0.05, 2.2], 'k-', lw=0.8)
ax2.plot([3.5, 3.5], [-0.05, 2.2], 'k-', lw=0.5)

# I_C formula
ax2.text(7.0, 1.8,
         r'$I_C = I_S \exp\!\left(\frac{V_{BE}}{V_T}\right)$',
         ha='center', va='center', fontsize=10, color='black', bbox=eq_style)
ax2.text(7.0, 0.5,
         r'$I_S \propto T^3 \exp\!\left(-\frac{V_{BG}}{V_T}\right)$',
         ha='center', va='center', fontsize=9.5, color='black', bbox=eq_style)

plt.tight_layout()
plt.savefig('fig_schem_bjt_sensor.png', dpi=150, facecolor='white', bbox_inches='tight')
plt.close()
print("fig_schem_bjt_sensor.png gerada.")

# ─────────────────────────────────────────────────────────────────────────────
# Figura 3: Visão completa do chip
# ─────────────────────────────────────────────────────────────────────────────
fig3, ax3 = plt.subplots(figsize=(14, 7), facecolor='white')
ax3.set_xlim(-1, 15)
ax3.set_ylim(-1, 8)
ax3.axis('off')
ax3.set_facecolor('white')
ax3.set_title('ThermalSensorChip v1.0 — Visão Completa (I/O + Núcleo)',
              fontsize=13, fontweight='bold', color='black', pad=10)

def chip_block(ax, x, y, w, h, title, details='', fill='0.93'):
    rect = FancyBboxPatch((x, y), w, h,
                          boxstyle='round,pad=0.1',
                          facecolor=fill, edgecolor='black', linewidth=1.5)
    ax.add_patch(rect)
    ax.text(x + w/2, y + h/2 + (0.2 if details else 0), title,
            ha='center', va='center', fontsize=9.5, fontweight='bold', color='black')
    if details:
        ax.text(x + w/2, y + h/2 - 0.3, details,
                ha='center', va='center', fontsize=8, color='0.3')

def pad_block(ax, x, y, w, h, label, arrow_dir='left'):
    rect = FancyBboxPatch((x, y), w, h,
                          boxstyle='round,pad=0.1',
                          facecolor='0.80', edgecolor='black', linewidth=2)
    ax.add_patch(rect)
    ax.text(x + w/2, y + h/2, label, ha='center', va='center',
            fontsize=8.5, fontweight='bold', color='black')

# ── Chip core border
core = FancyBboxPatch((3, 0.5), 9, 6.5,
                       boxstyle='round,pad=0.2',
                       facecolor='white', edgecolor='black', linewidth=2.5)
ax3.add_patch(core)
ax3.text(7.5, 6.7, 'CORE: ThermalSensorChip v1.0',
         ha='center', va='bottom', fontsize=11, fontweight='bold', color='black')
ax3.text(7.5, 6.3, '30 µm × 40 µm — CMOS 0.18 µm',
         ha='center', va='bottom', fontsize=9, color='0.3', style='italic')

# ── Internal blocks
chip_block(ax3, 3.5, 4.0, 2.8, 2.5, 'PMOS Mirror', 'M1, M2, M3\n(10/0.5, 80/0.5)')
chip_block(ax3, 3.5, 1.0, 2.8, 2.5, 'BJT Q1', 'NPN ref.\ndiode-conn.')
chip_block(ax3, 7.0, 1.0, 2.5, 5.5, 'BJT Q2×8\nArray', 'Common-\ncentroid\nABBA')
chip_block(ax3, 10.0, 1.0, 1.8, 2.5, 'R1\n5 kΩ', 'Poly\n2×50 µm')
chip_block(ax3, 10.0, 3.5, 1.8, 2.5, 'R2\n20 kΩ', 'Poly\n2×200 µm')

# ── Internal wires
ax3.plot([4.9, 4.9], [4.0, 3.5], 'k-', lw=1.5)
ax3.plot([4.9, 7.0], [3.5, 3.5], 'k-', lw=1.5)
ax3.plot([4.9, 4.9], [3.5, 3.5], 'k-', lw=1.5)
ax3.annotate('', xy=(7.0, 2.3), xytext=(6.3, 2.3),
             arrowprops=dict(arrowstyle='->', color='black', lw=1.2))
ax3.plot([9.5, 10.0], [2.3, 2.3], 'k-', lw=1.2)
ax3.plot([10.9, 10.9], [3.5, 3.5], 'k-', lw=1.2)
ax3.plot([10.9, 11.8], [3.5, 3.5], 'k-', lw=1.2)

# ── VDD pad (top)
pad_block(ax3, 5.5, 7.2, 1.8, 0.6, 'VDD PAD')
ax3.annotate('', xy=(6.4, 7.0), xytext=(6.4, 7.2),
             arrowprops=dict(arrowstyle='->', color='black', lw=1.5))

# ── GND pad (bottom)
pad_block(ax3, 5.5, -0.8, 1.8, 0.6, 'GND PAD')
ax3.annotate('', xy=(6.4, -0.2), xytext=(6.4, -0.4),
             arrowprops=dict(arrowstyle='->', color='black', lw=1.5))

# ── V_PTAT output pad (right)
pad_block(ax3, 12.2, 2.8, 2.5, 1.0, '$V_{PTAT}$\nOUT PAD')
ax3.annotate('', xy=(12.2, 3.3), xytext=(11.8, 3.3),
             arrowprops=dict(arrowstyle='->', color='black', lw=1.5))

# ── Annotations
ax3.text(5.5, 5.6, 'vbias', fontsize=8, color='0.3', style='italic')
ax3.text(8.3, 3.7, 'n1', fontsize=8, color='0.3', style='italic')
ax3.text(9.5, 2.1, 'n2', fontsize=8, color='0.3', style='italic')
ax3.text(11.5, 2.5, 'delta\n($V_{PTAT}$)', fontsize=8, color='black', style='italic',
         bbox=dict(facecolor='0.95', edgecolor='black', boxstyle='round,pad=0.2'))

# Spec box
spec_text = (
    "Especificações:\n"
    "  Process: CMOS 0.18 µm\n"
    "  VDD = 1.8 V\n"
    "  Range: -40 to 125°C\n"
    "  Sensitivity: ~2.06 mV/°C\n"
    "  I_DD: ~30 µA\n"
    "  Die: 30×40 µm²"
)
ax3.text(-0.8, 4.0, spec_text, fontsize=8.5, color='black', va='center',
         bbox=dict(boxstyle='round,pad=0.4', facecolor='0.95', edgecolor='black', lw=1))

plt.tight_layout()
plt.savefig('fig_schem_chip_full.png', dpi=150, facecolor='white', bbox_inches='tight')
plt.close()
print("fig_schem_chip_full.png gerada.")

print("\nTodos os 3 esquemáticos gerados com sucesso.")
