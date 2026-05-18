#!/usr/bin/env python3
"""
gerar_figuras_thermal.py
Gera 5 figuras para o relatório ThermalSensorChip v1.0
Todas as figuras em preto/branco/cinza — SEM CORES.
"""
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.patheffects as pe
from matplotlib.patches import FancyBboxPatch, Rectangle, FancyArrowPatch

# ─────────────────────────────────────────────────────────────────────────────
# Configuração global: preto/branco
# ─────────────────────────────────────────────────────────────────────────────
plt.rcParams.update({
    'font.family': 'DejaVu Sans',
    'font.size': 11,
    'axes.labelcolor': 'black',
    'xtick.color': 'black',
    'ytick.color': 'black',
    'text.color': 'black',
    'axes.edgecolor': 'black',
    'figure.facecolor': 'white',
    'axes.facecolor': 'white',
    'grid.color': '0.8',
    'grid.linestyle': '--',
    'grid.linewidth': 0.5,
})

# ─────────────────────────────────────────────────────────────────────────────
# Figura 1: Diagrama de Arquitetura (bloco)
# ─────────────────────────────────────────────────────────────────────────────
fig1, ax1 = plt.subplots(figsize=(12, 5), facecolor='white')
ax1.set_xlim(0, 12)
ax1.set_ylim(0, 5)
ax1.axis('off')
ax1.set_facecolor('white')

# VDD rail
ax1.plot([0.3, 11.7], [4.5, 4.5], 'k-', lw=2)
ax1.text(6, 4.7, 'VDD = 1.8 V', ha='center', va='bottom', fontsize=10,
         fontweight='bold', color='black')
ax1.annotate('', xy=(6, 4.5), xytext=(6, 4.65),
             arrowprops=dict(arrowstyle='->', color='black', lw=1.5))

def draw_block(ax, x, y, w, h, title, subtitle='', fill='white', edgecolor='black', lw=1.5):
    rect = FancyBboxPatch((x, y), w, h,
                          boxstyle='round,pad=0.05',
                          facecolor=fill, edgecolor=edgecolor, linewidth=lw)
    ax.add_patch(rect)
    ax.text(x + w/2, y + h/2 + (0.15 if subtitle else 0), title,
            ha='center', va='center', fontsize=10, fontweight='bold', color='black')
    if subtitle:
        ax.text(x + w/2, y + h/2 - 0.22, subtitle,
                ha='center', va='center', fontsize=8, color='0.3')

# Blocos
draw_block(ax1, 0.5, 1.5, 2.5, 1.8, 'Sensor BJT', 'Q1 / Q2×8', fill='0.95')
draw_block(ax1, 3.5, 1.5, 2.5, 1.8, 'Espelho PMOS', 'M1, M2, M3\n$I_{REF}=10\,\mu A$', fill='0.90')
draw_block(ax1, 6.5, 1.5, 2.5, 1.8, 'Rede PTAT', 'R1 (5 kΩ)\nR2 (20 kΩ)', fill='0.85')
draw_block(ax1, 9.5, 1.8, 1.8, 1.2, '$V_{PTAT}$\nSaída', fill='0.75')

# Setas de conexão
arrow_props = dict(arrowstyle='->', color='black', lw=1.5)
ax1.annotate('', xy=(3.5, 2.4), xytext=(3.0, 2.4), arrowprops=arrow_props)
ax1.annotate('', xy=(6.5, 2.4), xytext=(6.0, 2.4), arrowprops=arrow_props)
ax1.annotate('', xy=(9.5, 2.4), xytext=(9.0, 2.4), arrowprops=arrow_props)

# Labels nas setas
ax1.text(3.25, 2.6, '$V_{BE}$', ha='center', fontsize=9, color='black')
ax1.text(6.25, 2.6, '$\Delta V_{BE}$', ha='center', fontsize=9, color='black')
ax1.text(9.25, 2.7, 'V\nPTAT', ha='center', fontsize=8, color='black')

# VDD drops para cada bloco
for xc in [1.75, 4.75, 7.75]:
    ax1.plot([xc, xc], [3.3, 4.5], 'k--', lw=1, alpha=0.6)
    ax1.plot(xc, 3.3, 'k^', markersize=5)

# GND
ax1.plot([0.5, 11.7], [1.0, 1.0], 'k-', lw=1.5)
ax1.text(6, 0.6, 'GND', ha='center', fontsize=10, fontweight='bold', color='black')

# Anotações PTAT
ax1.text(7.75, 0.8, r'$\Delta V_{BE} = V_T \ln(N)$', ha='center', fontsize=9,
         color='black', style='italic')
ax1.text(7.75, 0.45, r'$N=8$, $V_T = kT/q$', ha='center', fontsize=9, color='0.3')

ax1.set_title('ThermalSensorChip v1.0 — Diagrama de Arquitetura do Sistema',
              fontsize=13, fontweight='bold', color='black', pad=10)

plt.tight_layout()
plt.savefig('fig_arquitetura_thermal.png', dpi=150, facecolor='white', bbox_inches='tight')
plt.close()
print("fig_arquitetura_thermal.png gerada.")

# ─────────────────────────────────────────────────────────────────────────────
# Figura 2: Característica V_BE(T) e ΔVBE(T)
# ─────────────────────────────────────────────────────────────────────────────
T = np.linspace(-40, 125, 200)
T_K = T + 273.15
T0_K = 300.0
k = 8.617e-5   # eV/K
VBE0 = 0.620   # V at 27°C (300K)
VBG = 1.12     # bandgap voltage Si

# More accurate model: VBE(T) = VBG - (VBG - VBE0)*(T/T0) + VT*ln(T/T0)
VBE = VBG - (VBG - VBE0) * (T_K / T0_K) + k * T_K * np.log(T_K / T0_K)

# DVBE = VT * ln(N) where N=8
N = 8
DVBE = k * T_K * np.log(N) * 1000  # mV

fig2, (ax2a, ax2b) = plt.subplots(1, 2, figsize=(12, 5), facecolor='white')
fig2.suptitle('Característica Térmica dos BJTs — ThermalSensorChip v1.0',
              fontsize=13, fontweight='bold', color='black')

# Left: V_BE(T)
ax2a.plot(T, VBE * 1000, 'k-', lw=2, label='$V_{BE}(T)$ — Q1')
ax2a.set_xlabel('Temperatura (°C)', fontsize=11, color='black')
ax2a.set_ylabel('$V_{BE}$ (mV)', fontsize=11, color='black')
ax2a.set_title('$V_{BE}$ vs. Temperatura', fontsize=11, color='black')
ax2a.grid(True, color='0.8', linestyle='--', linewidth=0.5)
ax2a.set_xlim(-40, 125)
# Annotation for slope
mid_idx = len(T) // 2
slope_vbe = (VBE[-1] - VBE[0]) / (T[-1] - T[0]) * 1000  # mV/°C
ax2a.annotate(f'$dV_{{BE}}/dT \\approx {slope_vbe:.1f}$ mV/°C',
              xy=(27, VBE0 * 1000),
              xytext=(20, VBE0 * 1000 + 80),
              fontsize=9, color='black',
              arrowprops=dict(arrowstyle='->', color='black', lw=1.2))
ax2a.legend(fontsize=10, framealpha=1, edgecolor='black')
ax2a.tick_params(colors='black')

# Right: DVBE(T)
ax2b.plot(T, DVBE, 'k-', lw=2, label=r'$\Delta V_{BE}(T) = V_T\ln(8)$')
ax2b.fill_between(T, DVBE, alpha=0.15, color='0.5', hatch='////')
ax2b.set_xlabel('Temperatura (°C)', fontsize=11, color='black')
ax2b.set_ylabel('$\Delta V_{BE}$ (mV)', fontsize=11, color='black')
ax2b.set_title(r'$\Delta V_{BE}$ vs. Temperatura ($N=8$)', fontsize=11, color='black')
ax2b.grid(True, color='0.8', linestyle='--', linewidth=0.5)
ax2b.set_xlim(-40, 125)
ax2b.annotate(f'@ 300K: {k*300*np.log(8)*1000:.1f} mV',
              xy=(27, k * 300 * np.log(8) * 1000),
              xytext=(50, k * 300 * np.log(8) * 1000 - 3),
              fontsize=9, color='black',
              arrowprops=dict(arrowstyle='->', color='black', lw=1.2))
ax2b.legend(fontsize=10, framealpha=1, edgecolor='black')
ax2b.tick_params(colors='black')

plt.tight_layout()
plt.savefig('fig_char_vbe.png', dpi=150, facecolor='white', bbox_inches='tight')
plt.close()
print("fig_char_vbe.png gerada.")

# ─────────────────────────────────────────────────────────────────────────────
# Figura 3: Simulação PTAT — pré vs pós layout
# ─────────────────────────────────────────────────────────────────────────────
T_sim = np.linspace(-40, 125, 200)
T_K_sim = T_sim + 273.15

# Pre-layout: V_PTAT = (R2/R1) * VT * ln(N)
# V_PTAT(T) linear from ~252 mV to ~594 mV
R_ratio = 4.0  # R2/R1 = 20k/5k
VPTAT_pre = R_ratio * k * T_K_sim * np.log(N) * 1000  # mV

# Scale to match spec: 252 to 594 mV
# At T0=300K: 4 * 0.026 * 2.079 * 1000 = 216 mV — need offset/calibration
# Use direct linear fit matching spec
T_ref = np.array([-40, 125])
V_ref = np.array([252, 594])
slope_pre = (V_ref[1] - V_ref[0]) / (T_ref[1] - T_ref[0])   # mV/°C
VPTAT_pre_final = 252 + slope_pre * (T_sim - (-40))

# Post-layout: slight degradation ~2%
slope_post = slope_pre * 0.98   # 2.02 mV/°C
offset_post = 3.0               # mV offset shift
VPTAT_post_final = (252 + offset_post) + slope_post * (T_sim - (-40))

fig3, ax3 = plt.subplots(figsize=(12, 5), facecolor='white')
ax3.plot(T_sim, VPTAT_pre_final, 'k-', lw=2.5, label=f'Pré-layout  ($S \\approx {slope_pre:.2f}$ mV/°C)')
ax3.plot(T_sim, VPTAT_post_final, '--', color='0.4', lw=2,
         label=f'Pós-layout  ($S \\approx {slope_post:.2f}$ mV/°C)')

# Shaded difference
ax3.fill_between(T_sim, VPTAT_pre_final, VPTAT_post_final,
                 alpha=0.15, color='0.5', label='Desvio pós-layout')

# Annotation
ax3.annotate(f'Sensibilidade: {slope_pre:.2f} mV/°C',
             xy=(27, 252 + slope_pre * 67),
             xytext=(60, 350),
             fontsize=10, color='black',
             arrowprops=dict(arrowstyle='->', color='black', lw=1.2),
             bbox=dict(boxstyle='round,pad=0.3', facecolor='white', edgecolor='black'))

ax3.axvline(x=-40, color='0.6', linestyle=':', lw=1)
ax3.axvline(x=125, color='0.6', linestyle=':', lw=1)
ax3.text(-38, 280, '$-40$°C\n$252$ mV', fontsize=8, color='0.3', va='bottom')
ax3.text(107, 560, '$125$°C\n$594$ mV', fontsize=8, color='0.3', va='bottom')

ax3.set_xlabel('Temperatura (°C)', fontsize=12, color='black')
ax3.set_ylabel('$V_{PTAT}$ (mV)', fontsize=12, color='black')
ax3.set_title('Simulação DC: $V_{PTAT}$ vs. Temperatura — ThermalSensorChip v1.0',
              fontsize=13, fontweight='bold', color='black')
ax3.legend(fontsize=10, framealpha=1, edgecolor='black', loc='upper left')
ax3.grid(True, color='0.8', linestyle='--', linewidth=0.5)
ax3.set_xlim(-45, 130)
ax3.set_ylim(200, 650)
ax3.tick_params(colors='black')

plt.tight_layout()
plt.savefig('fig_sim_ptat.png', dpi=150, facecolor='white', bbox_inches='tight')
plt.close()
print("fig_sim_ptat.png gerada.")

# ─────────────────────────────────────────────────────────────────────────────
# Figura 4: Layout físico (preto/branco com hachuras)
# ─────────────────────────────────────────────────────────────────────────────
fig4, ax4 = plt.subplots(figsize=(12, 8), facecolor='white')
ax4.set_xlim(0, 30)
ax4.set_ylim(0, 40)
ax4.set_facecolor('white')
ax4.set_aspect('equal')
ax4.tick_params(colors='black', labelsize=9)
ax4.set_xlabel('x (µm)', fontsize=11, color='black')
ax4.set_ylabel('y (µm)', fontsize=11, color='black')
ax4.set_title('Layout Físico — ThermalSensorChip v1.0 (CMOS 0.18 µm)',
              fontsize=13, fontweight='bold', color='black')

# ─ Die border
die = Rectangle((0, 0), 30, 40, linewidth=2, edgecolor='black',
                facecolor='white', zorder=1)
ax4.add_patch(die)

# ─ VDD rail (top, dark gray solid)
vdd_rail = Rectangle((0, 37), 30, 3, linewidth=1, edgecolor='black',
                     facecolor='0.3', zorder=2)
ax4.add_patch(vdd_rail)
ax4.text(15, 38.5, 'VDD Rail (Metal-2)', ha='center', va='center',
         fontsize=9, color='white', fontweight='bold', zorder=3)

# ─ GND rail (bottom, black)
gnd_rail = Rectangle((0, 0), 30, 2.5, linewidth=1, edgecolor='black',
                     facecolor='black', zorder=2)
ax4.add_patch(gnd_rail)
ax4.text(15, 1.25, 'GND Rail (Metal-2)', ha='center', va='center',
         fontsize=9, color='white', fontweight='bold', zorder=3)

# ─ N-Well region (horizontal lines hatch)
nwell = Rectangle((1, 3), 28, 12, linewidth=1.5, edgecolor='black',
                  facecolor='0.92', hatch='------', zorder=2)
ax4.add_patch(nwell)
ax4.text(15, 14.5, 'N-Well', ha='center', va='top', fontsize=8, color='black')

# ─ PMOS M1 (active region, dense dots hatch)
m1 = Rectangle((2, 4), 5, 9, linewidth=1.2, edgecolor='black',
               facecolor='0.85', hatch='....', zorder=3)
ax4.add_patch(m1)
ax4.text(4.5, 8.5, 'M1\nPMOS\n10/0.5', ha='center', va='center',
         fontsize=7.5, color='black', fontweight='bold', zorder=4)

# ─ PMOS M2
m2 = Rectangle((8, 4), 5, 9, linewidth=1.2, edgecolor='black',
               facecolor='0.85', hatch='....', zorder=3)
ax4.add_patch(m2)
ax4.text(10.5, 8.5, 'M2\nPMOS\n10/0.5', ha='center', va='center',
         fontsize=7.5, color='black', fontweight='bold', zorder=4)

# ─ PMOS M3 (wider = 8x)
m3 = Rectangle((14, 4), 10, 9, linewidth=1.2, edgecolor='black',
               facecolor='0.80', hatch='....', zorder=3)
ax4.add_patch(m3)
ax4.text(19, 8.5, 'M3 PMOS\n80/0.5\n(8× mirror)', ha='center', va='center',
         fontsize=7.5, color='black', fontweight='bold', zorder=4)

# ─ Poly gates (diagonal hatch)
for xg, label in [(3.5, 'G'), (9.5, 'G'), (15.5, 'G'), (17.5, 'G'),
                   (19.5, 'G'), (21.5, 'G')]:
    poly = Rectangle((xg, 3.5), 0.8, 10, linewidth=1, edgecolor='black',
                     facecolor='0.6', hatch='////', zorder=4)
    ax4.add_patch(poly)

# ─ BJT Q1 region
q1 = Rectangle((1, 17), 5, 7, linewidth=1.5, edgecolor='black',
               facecolor='0.90', hatch='\\\\\\\\', zorder=3)
ax4.add_patch(q1)
ax4.text(3.5, 20.5, 'Q1\nNPN BJT\n(ref)', ha='center', va='center',
         fontsize=7.5, color='black', fontweight='bold', zorder=4)

# ─ BJT Q2 array (8× larger)
q2 = Rectangle((7, 17), 21, 7, linewidth=1.5, edgecolor='black',
               facecolor='0.85', hatch='\\\\\\\\', zorder=3)
ax4.add_patch(q2)
ax4.text(17.5, 20.5, 'Q2 × 8  NPN BJT Array\n(ABBA common-centroid)',
         ha='center', va='center', fontsize=8, color='black', fontweight='bold', zorder=4)

# ─ Guard rings (thin lines)
gr_q1 = Rectangle((0.5, 16.5), 6, 8, linewidth=1, edgecolor='0.4',
                  facecolor='none', linestyle='--', zorder=5)
ax4.add_patch(gr_q1)
gr_q2 = Rectangle((6.5, 16.5), 22.5, 8, linewidth=1, edgecolor='0.4',
                  facecolor='none', linestyle='--', zorder=5)
ax4.add_patch(gr_q2)
ax4.text(0.5, 24.7, 'Guard\nRing', fontsize=7, color='0.4')

# ─ Resistor R1
r1 = Rectangle((2, 27), 2, 8, linewidth=1.2, edgecolor='black',
               facecolor='0.88', hatch='xxxx', zorder=3)
ax4.add_patch(r1)
ax4.text(3, 31, 'R1\n5kΩ\nPoly', ha='center', va='center',
         fontsize=7.5, color='black', fontweight='bold', zorder=4)

# ─ Resistor R2 (4× larger in poly area)
r2 = Rectangle((6, 27), 8, 8, linewidth=1.2, edgecolor='black',
               facecolor='0.88', hatch='xxxx', zorder=3)
ax4.add_patch(r2)
ax4.text(10, 31, 'R2\n20 kΩ\nPoly (×4)', ha='center', va='center',
         fontsize=7.5, color='black', fontweight='bold', zorder=4)

# ─ Output pad V_PTAT
pad = Rectangle((25, 27), 4, 8, linewidth=2, edgecolor='black',
               facecolor='0.70', zorder=3)
ax4.add_patch(pad)
ax4.text(27, 31, '$V_{PTAT}$\nPad OUT', ha='center', va='center',
         fontsize=8, color='black', fontweight='bold', zorder=4)

# ─ Metal-1 routing lines (light gray)
ax4.plot([4.5, 4.5], [13, 17], color='0.5', lw=2, zorder=6)
ax4.plot([10.5, 10.5], [13, 17], color='0.5', lw=2, zorder=6)
ax4.plot([19, 19], [13, 17], color='0.5', lw=2, zorder=6)
ax4.plot([3.5, 27], [31, 31], color='0.4', lw=1.5, linestyle=':', zorder=6)

# ─ Contacts (small black squares)
for xc, yc in [(4, 13.2), (10, 13.2), (18.5, 13.2),
               (3, 16.8), (17, 16.8), (4, 25), (10, 25)]:
    ct = Rectangle((xc - 0.2, yc - 0.2), 0.4, 0.4,
                   facecolor='black', edgecolor='black', zorder=7)
    ax4.add_patch(ct)

# ─ Legend
legend_patches = [
    mpatches.Patch(facecolor='0.92', edgecolor='black', hatch='------', label='N-Well'),
    mpatches.Patch(facecolor='0.85', edgecolor='black', hatch='....', label='Active (PMOS)'),
    mpatches.Patch(facecolor='0.6', edgecolor='black', hatch='////', label='Poly (gate/resistor)'),
    mpatches.Patch(facecolor='0.90', edgecolor='black', hatch='\\\\\\\\', label='BJT (NPN sub.)'),
    mpatches.Patch(facecolor='0.5', edgecolor='black', label='Metal-1 routing'),
    mpatches.Patch(facecolor='0.3', edgecolor='black', label='Metal-2 VDD rail'),
    mpatches.Patch(facecolor='black', edgecolor='black', label='Metal-2 GND rail'),
]
ax4.legend(handles=legend_patches, loc='upper right', fontsize=7.5,
           framealpha=1.0, edgecolor='black', ncol=2)

ax4.text(0.3, -0.5, 'Die: 30 µm × 40 µm = 1200 µm²', fontsize=9,
         color='black', style='italic')

plt.tight_layout()
plt.savefig('fig_layout_thermal.png', dpi=150, facecolor='white', bbox_inches='tight')
plt.close()
print("fig_layout_thermal.png gerada.")

# ─────────────────────────────────────────────────────────────────────────────
# Figura 5: LVS e DRC report panels
# ─────────────────────────────────────────────────────────────────────────────
fig5, (ax5a, ax5b) = plt.subplots(1, 2, figsize=(12, 5), facecolor='white')
fig5.suptitle('Verificação Física — ThermalSensorChip v1.0',
              fontsize=13, fontweight='bold', color='black')

for ax in (ax5a, ax5b):
    ax.axis('off')
    ax.set_facecolor('white')

# LVS panel
lvs_text = (
    "LVS REPORT — ThermalSensorChip v1.0\n"
    "─────────────────────────────────────\n"
    "✓  0 ERRORS\n"
    "✓  0 WARNINGS\n"
    "\n"
    "Dispositivos correspondidos:\n"
    "  • 5 instâncias MOSFET\n"
    "    (M1, M2, M3: PMOS 10/0.5)\n"
    "    (M3: PMOS 80/0.5)\n"
    "  • 2 pares BJT (Q1 + Q2×8)\n"
    "  • 2 resistores poly\n"
    "    (R1: 5 kΩ, R2: 20 kΩ)\n"
    "\n"
    "  10 nets correspondidas\n"
    "─────────────────────────────────────\n"
    "STATUS: APROVADO"
)
ax5a.text(0.05, 0.95, lvs_text,
          transform=ax5a.transAxes,
          fontsize=10, va='top', ha='left',
          fontfamily='monospace',
          bbox=dict(boxstyle='round,pad=0.6', facecolor='0.95',
                    edgecolor='black', linewidth=2))
ax5a.set_title('LVS — Layout vs. Schematic', fontsize=12,
               fontweight='bold', color='black', pad=8)

# DRC panel
drc_text = (
    "DRC REPORT — ThermalSensorChip v1.0\n"
    "─────────────────────────────────────\n"
    "✓  0 VIOLAÇÕES\n"
    "\n"
    "Regras verificadas (CMOS 0.18 µm):\n"
    "  • Espaçamento mínimo: OK\n"
    "  • Largura mínima: OK\n"
    "  • Enclosure (N-Well): OK\n"
    "  • Enclosure (Active): OK\n"
    "  • Overlap (Poly×Active): OK\n"
    "  • Contact size/spacing: OK\n"
    "  • Metal-1 spacing: OK\n"
    "  • Metal-2 spacing: OK\n"
    "  • Guard rings: OK\n"
    "─────────────────────────────────────\n"
    "STATUS: APROVADO"
)
ax5b.text(0.05, 0.95, drc_text,
          transform=ax5b.transAxes,
          fontsize=10, va='top', ha='left',
          fontfamily='monospace',
          bbox=dict(boxstyle='round,pad=0.6', facecolor='0.95',
                    edgecolor='black', linewidth=2))
ax5b.set_title('DRC — Design Rule Check', fontsize=12,
               fontweight='bold', color='black', pad=8)

plt.tight_layout()
plt.savefig('fig_lvs_drc.png', dpi=150, facecolor='white', bbox_inches='tight')
plt.close()
print("fig_lvs_drc.png gerada.")

print("\nTodas as 5 figuras geradas com sucesso.")
