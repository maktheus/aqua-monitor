"""
gerar_layout_soc.py
Simulated layout view for AquaMonitorSoC v1.0
800x600µm die, grayscale layers, 12x9
"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

fig, ax = plt.subplots(figsize=(12, 9))

DIE_W = 800
DIE_H = 600
PAD   = 40

ax.set_xlim(-10, DIE_W + 80)
ax.set_ylim(-30, DIE_H + 60)
ax.set_aspect('equal')
ax.axis('off')
ax.set_title('AquaMonitorSoC v1.0 — Simulated Layout View\n'
             '800×600 µm Die — CMOS TSMC 180nm — METAL1/METAL2 Routing',
             fontsize=11, fontweight='bold')

# ---- Layer colors (grayscale fills) ----
LAYERS = {
    'diff':   '#f0f0f0',  # very light gray — diffusion
    'poly':   '#d8d8d8',  # light gray — polysilicon
    'metal1': '#aaaaaa',  # medium gray — Metal1
    'metal2': '#666666',  # dark gray — Metal2
    'via':    '#333333',  # very dark — Vias
    'nwell':  '#eeeeee',  # very light — N-well
    'pad':    '#bbbbbb',  # pad metal
}

rng = np.random.default_rng(42)

def rect(ax, x, y, w, h, color, ec='none', lw=0.5, alpha=1.0, zorder=2):
    r = plt.Rectangle((x, y), w, h, facecolor=color, edgecolor=ec,
                       linewidth=lw, alpha=alpha, zorder=zorder)
    ax.add_patch(r)

# ---- Background / N-well regions ----
rect(ax, PAD, PAD, DIE_W - 2*PAD, DIE_H - 2*PAD, LAYERS['nwell'], zorder=1)

# ---- I/O ring ----
rect(ax, 0, 0, DIE_W, PAD, LAYERS['pad'], 'black', 0.8, zorder=3)
rect(ax, 0, DIE_H-PAD, DIE_W, PAD, LAYERS['pad'], 'black', 0.8, zorder=3)
rect(ax, 0, 0, PAD, DIE_H, LAYERS['pad'], 'black', 0.8, zorder=3)
rect(ax, DIE_W-PAD, 0, PAD, DIE_H, LAYERS['pad'], 'black', 0.8, zorder=3)

# ---- Pad cells (individual) ----
pad_w = 30
for i in range(10):
    px = 5 + i * (DIE_W - 10) / 10
    rect(ax, px, 5, pad_w, PAD - 10, LAYERS['metal2'], 'black', 0.5, zorder=4)
    rect(ax, px, DIE_H - PAD + 5, pad_w, PAD - 10, LAYERS['metal2'], 'black', 0.5, zorder=4)
for i in range(6):
    py = 5 + i * (DIE_H - 10) / 6
    rect(ax, 5, py, PAD - 10, 30, LAYERS['metal2'], 'black', 0.5, zorder=4)
    rect(ax, DIE_W - PAD + 5, py, PAD - 10, 30, LAYERS['metal2'], 'black', 0.5, zorder=4)

# ---- Analog blocks ----
AX = PAD + 15
split_x = PAD + int(0.40 * (DIE_W - 2*PAD))

def draw_block_layout(ax, x, y, w, h, name, diffusions=3):
    """Draw a block with diffusion/poly/metal layers."""
    # Block background
    rect(ax, x, y, w, h, LAYERS['diff'], 'black', 1.0, zorder=5)
    # Poly rows (gate fingers)
    poly_pitch = h / (diffusions + 1)
    for i in range(diffusions):
        py = y + (i + 0.7) * poly_pitch
        rect(ax, x + 3, py, w - 6, 3, LAYERS['poly'], 'none', 0, zorder=6)
    # Metal1 horizontal routes
    for i in range(2):
        my = y + h * (0.3 + i * 0.4)
        rect(ax, x, my, w, 2, LAYERS['metal1'], 'none', 0, zorder=7)
    # Metal2 vertical routes
    for i in range(3):
        mx = x + w * (0.25 + i * 0.25)
        rect(ax, mx, y, 2, h, LAYERS['metal2'], 'none', 0, zorder=7)
    # Label
    ax.text(x + w/2, y + h/2, name, ha='center', va='center',
            fontsize=7, fontweight='bold', zorder=9,
            bbox=dict(boxstyle='round,pad=0.2', fc='white', alpha=0.75, ec='none'))
    ax.text(x + w/2, y + 4, f'{w:.0f}×{h:.0f}µm', ha='center', va='bottom',
            fontsize=5.5, color='#444444', zorder=9)
    rect(ax, x, y, w, h, 'none', 'black', 1.2, zorder=8)

# Analog blocks
draw_block_layout(ax, AX,        PAD + 340, 80, 60, 'Comparator')
draw_block_layout(ax, AX + 100,  PAD + 340, 60, 60, 'Cap DAC')
draw_block_layout(ax, AX,        PAD + 250, 40, 60, '3:1 MUX')
draw_block_layout(ax, AX + 60,   PAD + 260, 50, 40, 'Bandgap')
draw_block_layout(ax, AX,        PAD + 170, 70, 50, 'S/H Cap')
draw_block_layout(ax, AX,        PAD + 50,  170, 80, 'Ana. Decap')

# Digital blocks
DX = split_x + 20
draw_block_layout(ax, DX,        PAD + 400, 120, 80, 'SAR FSM', 5)
draw_block_layout(ax, DX + 150,  PAD + 400, 100, 80, 'SPI Slave', 5)
draw_block_layout(ax, DX,        PAD + 330, 60,  40, 'Clk Div')
draw_block_layout(ax, DX + 80,   PAD + 330, 80,  40, 'Result Reg')
draw_block_layout(ax, DX + 180,  PAD + 330, 80,  40, 'Ch Seq')
draw_block_layout(ax, DX,        PAD + 270, 200, 40, 'Scan Chain')
draw_block_layout(ax, DX,        PAD + 50,  260, 200, 'Digital Decap', 2)

# ---- Routing channels ----
# Horizontal route: Comparator out to SAR FSM
y_route = PAD + 375
ax.plot([AX + 80, DX + 60], [y_route, y_route],
        color=LAYERS['metal2'], lw=2, zorder=10)
ax.text((AX + 80 + DX + 60)/2, y_route + 3, 'comp_out',
        ha='center', fontsize=5.5, color='#333333', zorder=11)

# DAC code route: SAR FSM to DAC
y_dac = PAD + 365
ax.plot([DX + 60, split_x + 5, AX + 130], [y_dac, y_dac, y_dac],
        color=LAYERS['metal1'], lw=1.5, zorder=10)
ax.text(split_x - 20, y_dac + 3, 'dac_code[3:0]',
        ha='center', fontsize=5.5, color='#333333', zorder=11)

# SPI routes
y_spi = PAD + 440
ax.plot([DX + 250, DIE_W - PAD], [y_spi, y_spi],
        color=LAYERS['metal2'], lw=2, zorder=10)
ax.text(DX + 290, y_spi + 3, 'SPI bus', ha='center',
        fontsize=5.5, color='#333333', zorder=11)

# Clock distribution
y_clk = DIE_H - PAD - 20
ax.plot([DX, DX + 260], [y_clk, y_clk],
        color=LAYERS['metal1'], lw=1.5, linestyle='--', zorder=10)
ax.text(DX + 130, y_clk + 3, 'clk_1mhz', ha='center',
        fontsize=5.5, color='#444444', zorder=11)

# ---- Analog/Digital split line ----
ax.plot([split_x, split_x], [PAD, DIE_H - PAD],
        'k--', lw=2.0, zorder=12)
ax.text(split_x + 2, DIE_H - PAD - 8,
        'Analog ↔ Digital\nboundary', ha='left', va='top',
        fontsize=6.5, color='black', zorder=13)

# ---- Domain labels ----
ax.text(AX + 90, DIE_H - PAD - 10,
        'ANALOG', ha='center', fontsize=9, fontweight='bold', color='#444444', zorder=13)
ax.text(DX + 150, DIE_H - PAD - 10,
        'DIGITAL', ha='center', fontsize=9, fontweight='bold', color='#111111', zorder=13)

# ---- Scale bar ----
sb_x = DIE_W - PAD - 120
sb_y = 8
ax.plot([sb_x, sb_x + 100], [sb_y, sb_y], 'k-', lw=2.5, zorder=15)
ax.plot([sb_x, sb_x], [sb_y - 4, sb_y + 4], 'k-', lw=2.5, zorder=15)
ax.plot([sb_x + 100, sb_x + 100], [sb_y - 4, sb_y + 4], 'k-', lw=2.5, zorder=15)
ax.text(sb_x + 50, sb_y - 8, '100 µm', ha='center', va='top', fontsize=8)

# ---- Legend ----
legend_patches = [
    mpatches.Patch(facecolor=LAYERS['nwell'],  edgecolor='black', label='Diffusion (N-well)'),
    mpatches.Patch(facecolor=LAYERS['poly'],   edgecolor='black', label='Poly (Gate)'),
    mpatches.Patch(facecolor=LAYERS['metal1'], edgecolor='black', label='Metal 1'),
    mpatches.Patch(facecolor=LAYERS['metal2'], edgecolor='black', label='Metal 2'),
    mpatches.Patch(facecolor=LAYERS['pad'],    edgecolor='black', label='Pad Metal (I/O Ring)'),
]
ax.legend(handles=legend_patches, loc='lower right',
          fontsize=7.5, framealpha=0.95)

ax.text(DIE_W/2, -25,
        'AquaMonitorSoC v1.0 — Simulated Layout — PADIS Unidade 7, Cap 5',
        ha='center', va='top', fontsize=7, color='gray', style='italic')

plt.tight_layout()
plt.savefig('fig_layout_soc.png', dpi=150, bbox_inches='tight', facecolor='white')
print("Saved: fig_layout_soc.png")
