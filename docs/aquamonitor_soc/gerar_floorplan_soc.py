"""
gerar_floorplan_soc.py
Chip floorplan for AquaMonitorSoC v1.0
Die: 800x600µm, analog/digital split
Black/white, 12x9
"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch

fig, ax = plt.subplots(figsize=(12, 9))

# Die dimensions (in µm, scaled to plot coords 1:1)
DIE_W = 800
DIE_H = 600

ax.set_xlim(-20, DIE_W + 20)
ax.set_ylim(-20, DIE_H + 50)
ax.set_aspect('equal')
ax.axis('off')

ax.set_title('AquaMonitorSoC v1.0 — Chip Floorplan\n'
             'Die Size: 800×600 µm — CMOS TSMC 180nm — VDD=1.8V',
             fontsize=12, fontweight='bold', pad=8)

# ---- Die outline ----
die = plt.Rectangle((0, 0), DIE_W, DIE_H,
                     fill=False, edgecolor='black', linewidth=3)
ax.add_patch(die)

# ---- I/O Ring (pad cells) ----
PAD = 40  # pad ring width in µm
io = plt.Rectangle((0, 0), DIE_W, DIE_H,
                   fill=True, facecolor='#cccccc', edgecolor='black', linewidth=2,
                   zorder=1)
ax.add_patch(io)
core = plt.Rectangle((PAD, PAD), DIE_W - 2*PAD, DIE_H - 2*PAD,
                      fill=True, facecolor='white', edgecolor='black',
                      linewidth=1.5, zorder=2)
ax.add_patch(core)

# ---- Analog/Digital split dashed line ----
split_x = PAD + 0.40 * (DIE_W - 2*PAD)  # 40% analog
ax.plot([split_x, split_x], [PAD, DIE_H - PAD],
        'k--', linewidth=2.0, zorder=5)

# ---- Domain labels ----
ax.text(PAD + 0.20*(DIE_W-2*PAD), DIE_H - PAD - 15,
        'ANALOG DOMAIN', ha='center', va='top',
        fontsize=10, fontweight='bold', color='#333333', zorder=6)
ax.text(split_x + 0.30*(DIE_W-2*PAD), DIE_H - PAD - 15,
        'DIGITAL DOMAIN', ha='center', va='top',
        fontsize=10, fontweight='bold', color='#111111', zorder=6)

# ---- Helper to draw a block ----
def block(ax, x, y, w, h, label, sublabel='', fc='#f0f0f0', ec='black',
          lw=1.5, fontsize=8, zorder=4):
    r = plt.Rectangle((x, y), w, h, facecolor=fc, edgecolor=ec,
                       linewidth=lw, zorder=zorder)
    ax.add_patch(r)
    if sublabel:
        ax.text(x + w/2, y + h*0.62, label, ha='center', va='center',
                fontsize=fontsize, fontweight='bold', zorder=zorder+1)
        ax.text(x + w/2, y + h*0.28, sublabel, ha='center', va='center',
                fontsize=6.5, color='#555555', zorder=zorder+1)
    else:
        ax.text(x + w/2, y + h/2, label, ha='center', va='center',
                fontsize=fontsize, fontweight='bold', zorder=zorder+1)
    # Area label
    area_str = f'{w:.0f}×{h:.0f}µm'
    ax.text(x + w/2, y + 4, area_str, ha='center', va='bottom',
            fontsize=5.5, color='gray', zorder=zorder+1)

# ---- ANALOG BLOCKS ----
AX = PAD + 10
AY_start = PAD + 20

# Comparator: 80×60µm
block(ax, AX,        AY_start + 300, 80, 60, 'Comparator', '80×60µm', fc='#e8e8e8')
# DAC: 60×60µm
block(ax, AX + 100,  AY_start + 300, 60, 60, 'Cap DAC\n4-bit', '60×60µm', fc='#e8e8e8')
# MUX: 40×60µm
block(ax, AX,        AY_start + 200, 40, 60, '3:1 MUX', '40×60µm', fc='#e8e8e8')
# Bandgap ref: 50×40µm
block(ax, AX + 60,   AY_start + 210, 50, 40, 'Bandgap\nRef', '50×40µm', fc='#d8d8d8')
# S/H cap: 70×50µm
block(ax, AX,        AY_start + 120, 70, 50, 'S/H Cap\nArray', '70×50µm', fc='#e8e8e8')
# Decap: full width
block(ax, AX,        AY_start,       170, 80, 'Analog Decap', '170×80µm',
      fc='#f5f5f5', fontsize=7)

# ---- DIGITAL BLOCKS ----
DX = split_x + 20
DY_start = PAD + 20

# SAR FSM: 120×80µm
block(ax, DX,        DY_start + 380, 120, 80, 'SAR FSM', '120×80µm', fc='#d0d0d0')
# SPI Slave: 100×80µm
block(ax, DX + 150,  DY_start + 380, 100, 80, 'SPI Slave', '100×80µm', fc='#d0d0d0')
# Clock Div: 60×40µm
block(ax, DX,        DY_start + 310, 60,  40, 'Clk Div\n/8', '60×40µm', fc='#e0e0e0')
# Result Reg: 80×40µm
block(ax, DX + 80,   DY_start + 310, 80,  40, 'Result Reg', '80×40µm', fc='#e0e0e0')
# Channel Seq: 80×40µm
block(ax, DX + 180,  DY_start + 310, 80,  40, 'Ch Seq', '80×40µm', fc='#e0e0e0')
# Scan chain: 200×40µm
block(ax, DX,        DY_start + 240, 200, 40, 'Scan Chain (DFT)', '200×40µm',
      fc='#f0f0f0', fontsize=7)
# Digital Decap
block(ax, DX,        DY_start,       260, 200, 'Digital Decap & Filler Cells',
      '260×200µm', fc='#f8f8f8', fontsize=7)

# ---- Routing channel annotation ----
ax.plot([split_x - 5, split_x - 5], [PAD + 50, DIE_H - PAD - 40],
        'k:', lw=0.8, zorder=3)

# ---- I/O pad labels (around perimeter) ----
pad_labels_bottom = ['GND', 'VDD', 'SPI_CS', 'SPI_MOSI', 'SPI_MISO',
                     'SPI_CLK', 'VPH', 'VCOND', 'VTEMP', 'RESET']
pad_labels_top = ['VDD', 'CLK_8M', 'DAC_SW0', 'DAC_SW1', 'DAC_SW2',
                  'DAC_SW3', 'MUX_S0', 'MUX_S1', 'COMP_IN', 'EOC']
pad_labels_left = ['AVDD', 'AGND', 'VREF', 'COMP_OUT']
pad_labels_right = ['DVDD', 'DGND', 'TEST', 'LED']

n = len(pad_labels_bottom)
for i, lbl in enumerate(pad_labels_bottom):
    px = (i + 0.5) * DIE_W / n
    ax.text(px, -12, lbl, ha='center', va='top', fontsize=5.5, rotation=45)
    ax.plot([px, px], [0, 15], 'k-', lw=0.8)

for i, lbl in enumerate(pad_labels_top):
    px = (i + 0.5) * DIE_W / n
    ax.text(px, DIE_H + 12, lbl, ha='center', va='bottom', fontsize=5.5, rotation=45)
    ax.plot([px, px], [DIE_H - 15, DIE_H], 'k-', lw=0.8)

for i, lbl in enumerate(pad_labels_left):
    py = (i + 0.5) * DIE_H / len(pad_labels_left)
    ax.text(-12, py, lbl, ha='right', va='center', fontsize=5.5)
    ax.plot([0, 15], [py, py], 'k-', lw=0.8)

for i, lbl in enumerate(pad_labels_right):
    py = (i + 0.5) * DIE_H / len(pad_labels_right)
    ax.text(DIE_W + 12, py, lbl, ha='left', va='center', fontsize=5.5)
    ax.plot([DIE_W - 15, DIE_W], [py, py], 'k-', lw=0.8)

# ---- Scale bar ----
sb_x, sb_y = 650, -15
ax.plot([sb_x, sb_x + 100], [sb_y, sb_y], 'k-', lw=2)
ax.plot([sb_x, sb_x], [sb_y - 4, sb_y + 4], 'k-', lw=2)
ax.plot([sb_x + 100, sb_x + 100], [sb_y - 4, sb_y + 4], 'k-', lw=2)
ax.text(sb_x + 50, sb_y - 8, '100 µm', ha='center', va='top', fontsize=7)

# ---- Legend ----
legend_patches = [
    mpatches.Patch(facecolor='#cccccc', edgecolor='black', label='I/O Ring (Pad Cells)'),
    mpatches.Patch(facecolor='#e8e8e8', edgecolor='black', label='Analog Blocks'),
    mpatches.Patch(facecolor='#d0d0d0', edgecolor='black', label='Digital Core Blocks'),
    mpatches.Patch(facecolor='#f8f8f8', edgecolor='black', label='Decap / Filler'),
]
ax.legend(handles=legend_patches, loc='lower right',
          fontsize=7, framealpha=0.9)

ax.text(400, -35,
        'AquaMonitorSoC v1.0 — PADIS Unidade 7, Cap 5 — CMOS TSMC 180nm',
        ha='center', va='top', fontsize=7, color='gray', style='italic')

plt.tight_layout()
plt.savefig('fig_floorplan_soc.png', dpi=150, bbox_inches='tight', facecolor='white')
print("Saved: fig_floorplan_soc.png")
