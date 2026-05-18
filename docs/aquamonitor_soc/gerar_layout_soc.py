"""
gerar_layout_soc.py — AquaMonitorSoC v1.0
Simulated layout view. Block positions match floorplan exactly.
All labels inside block centres only, no overflow.
"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

fig, ax = plt.subplots(figsize=(13, 10))
DIE_W, DIE_H = 800, 600
PAD = 45
rng = np.random.default_rng(42)

ax.set_xlim(-10, DIE_W + 100)
ax.set_ylim(-35, DIE_H + 65)
ax.set_aspect('equal')
ax.axis('off')
fig.patch.set_facecolor('white')
ax.set_title('AquaMonitorSoC v1.0 — Vista de Layout Simulado\n'
             'Die 800×600 µm · CMOS TSMC 180nm · Metal 1 & Metal 2',
             fontsize=11, fontweight='bold', pad=8)

# ─── Layer palette (grayscale) ────────────────────────────────────────────────
L = {'nwell': '#efefef', 'diff': '#e0e0e0', 'poly': '#c8c8c8',
     'metal1': '#a0a0a0', 'metal2': '#606060', 'pad': '#b0b0b0'}

def r(ax, x, y, w, h, fc, ec='none', lw=0.5, z=2):
    ax.add_patch(plt.Rectangle((x,y), w, h, fc=fc, ec=ec, lw=lw, zorder=z))

# ─── I/O ring ─────────────────────────────────────────────────────────────────
r(ax, 0, 0, DIE_W, DIE_H, L['pad'], 'black', 2.5, 1)
r(ax, PAD, PAD, DIE_W-2*PAD, DIE_H-2*PAD, L['nwell'], 'black', 1.2, 2)

# Pad cells
for i in range(10):
    px = 5 + i*(DIE_W-10)/10
    r(ax, px, 3,         26, PAD-8, L['metal2'], 'black', 0.5, 3)
    r(ax, px, DIE_H-PAD+5, 26, PAD-8, L['metal2'], 'black', 0.5, 3)
for i in range(5):
    py = 5 + i*(DIE_H-10)/5
    r(ax, 3,          py, PAD-8, 26, L['metal2'], 'black', 0.5, 3)
    r(ax, DIE_W-PAD+5, py, PAD-8, 26, L['metal2'], 'black', 0.5, 3)

SPLIT = PAD + int(0.40*(DIE_W-2*PAD))  # 333

# ─── Block drawing (diff + poly rows + metal1/2 routing stubs) ───────────────
def draw_blk(x, y, w, h, name, n_poly=3, z=5):
    r(ax, x, y, w, h, L['diff'], 'black', 1.2, z)
    # poly "gate fingers"
    if h > 20:
        pitch = h/(n_poly+1)
        for i in range(n_poly):
            r(ax, x+4, y+(i+0.6)*pitch, w-8, 3, L['poly'], z=z+1)
    # metal1 horizontals
    for frac in (0.30, 0.70):
        r(ax, x, y+h*frac, w, 2, L['metal1'], z=z+2)
    # metal2 verticals
    for frac in (0.25, 0.50, 0.75):
        r(ax, x+w*frac, y, 2, h, L['metal2'], z=z+2)
    # label centred, white background
    ax.text(x+w/2, y+h/2, name, ha='center', va='center',
            fontsize=7, fontweight='bold', zorder=z+3,
            bbox=dict(boxstyle='round,pad=0.2', fc='white', alpha=0.80, ec='none'))
    ax.add_patch(plt.Rectangle((x, y), w, h, fc='none', ec='black', lw=1.2, zorder=z+3))

AX  = PAD + 15
DX  = SPLIT + 20

# ── analog ────────────────────────────────────────────────────────────────────
draw_blk(AX,      390, 80, 65, 'Comparador')
draw_blk(AX+100,  390, 60, 65, 'Cap DAC')
draw_blk(AX,      310, 55, 55, '3:1 MUX')
draw_blk(AX+75,   310, 60, 55, 'Bandgap')
draw_blk(AX,      235, 80, 55, 'S/H Cap')
draw_blk(AX,      175, 80, 45, 'Bias Gen')
draw_blk(AX,       65,170, 90, 'Ana. Decap', n_poly=2)

# ── digital ───────────────────────────────────────────────────────────────────
draw_blk(DX,      400,130, 80, 'SAR FSM',   n_poly=5)
draw_blk(DX+160,  400,110, 80, 'SPI Slave', n_poly=5)
draw_blk(DX,      335, 70, 45, 'Clk Div')
draw_blk(DX+90,   335, 90, 45, 'Result Reg')
draw_blk(DX+200,  335, 80, 45, 'Ch Seq')
draw_blk(DX,      270,210, 45, 'Scan Chain', n_poly=2)
draw_blk(DX,       65,270,180, 'Dig. Decap', n_poly=2)

# ─── Routing traces ──────────────────────────────────────────────────────────
# comp_out: Comparator right edge → SAR FSM left edge (horizontal)
y_co = PAD + 422
ax.plot([AX+80, DX], [y_co, y_co], color=L['metal2'], lw=2, zorder=8)
ax.text((AX+80+DX)//2, y_co+4, 'comp_out', ha='center',
        fontsize=5.5, color='#222', zorder=9)

# dac_code: SAR FSM bottom → Cap DAC (vertical + horizontal)
x_dac = DX + 65
ax.plot([x_dac, x_dac], [PAD+400, PAD+395], color=L['metal1'], lw=1.5, zorder=8)
ax.plot([x_dac, AX+130], [PAD+395, PAD+395], color=L['metal1'], lw=1.5, zorder=8)
ax.text((x_dac+AX+130)//2, PAD+399, 'dac_code[3:0]', ha='center',
        fontsize=5.5, color='#222', zorder=9)

# SPI bus to right edge
y_spi = PAD+440
ax.plot([DX+270, DIE_W-PAD], [y_spi, y_spi], color=L['metal2'], lw=2, zorder=8)
ax.text(DX+310, y_spi+4, 'SPI bus', ha='center',
        fontsize=5.5, color='#222', zorder=9)

# Clock distribution (dashed metal1)
y_clk = DIE_H-PAD-20
ax.plot([DX, DX+280], [y_clk, y_clk], color=L['metal1'], lw=1.5,
        ls='--', zorder=8)
ax.text(DX+140, y_clk+4, 'clk_1mhz (distribuição H-tree)', ha='center',
        fontsize=5.5, color='#444', zorder=9)

# ─── Boundary & labels ───────────────────────────────────────────────────────
ax.plot([SPLIT, SPLIT], [PAD, DIE_H-PAD], 'k--', lw=2.0, zorder=10)
ax.text(SPLIT+4, DIE_H-PAD-8, 'Analógico ↔ Digital',
        ha='left', va='top', fontsize=6.5, color='#111', zorder=11)

ax.text(AX+90, DIE_H-PAD-10, 'ANALÓGICO',
        ha='center', fontsize=9, fontweight='bold', color='#555', zorder=11)
ax.text(DX+155, DIE_H-PAD-10, 'DIGITAL',
        ha='center', fontsize=9, fontweight='bold', color='#111', zorder=11)

# ─── Scale bar ───────────────────────────────────────────────────────────────
sb_x = DIE_W - 130
ax.plot([sb_x, sb_x+100], [-20, -20], 'k-', lw=2.5)
for ex in (sb_x, sb_x+100):
    ax.plot([ex, ex], [-24, -16], 'k-', lw=2.5)
ax.text(sb_x+50, -27, '100 µm', ha='center', va='top', fontsize=8)

# ─── Legend ──────────────────────────────────────────────────────────────────
patches = [
    mpatches.Patch(fc=L['nwell'],  ec='black', label='N-Well / Difusão'),
    mpatches.Patch(fc=L['poly'],   ec='black', label='Polisilício (Gate)'),
    mpatches.Patch(fc=L['metal1'], ec='black', label='Metal 1'),
    mpatches.Patch(fc=L['metal2'], ec='black', label='Metal 2'),
    mpatches.Patch(fc=L['pad'],    ec='black', label='Pad Metal (I/O Ring)'),
]
ax.legend(handles=patches, loc='lower right', fontsize=7.5, framealpha=0.95)

ax.text(DIE_W/2, -33,
        'AquaMonitorSoC v1.0 — Layout Simulado — PADIS Unidade 7, Cap 5',
        ha='center', va='top', fontsize=7, color='gray', style='italic')

plt.tight_layout()
plt.savefig('fig_layout_soc.png', dpi=150, bbox_inches='tight', facecolor='white')
print("Saved: fig_layout_soc.png")
