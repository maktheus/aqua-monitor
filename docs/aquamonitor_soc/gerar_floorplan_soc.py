"""
gerar_floorplan_soc.py — AquaMonitorSoC v1.0
Redesigned floorplan: all blocks computed with explicit spacing to avoid overlaps.
Die: 800x600µm, analog (left 40%) / digital (right 60%)
"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

fig, ax = plt.subplots(figsize=(13, 10))
DIE_W, DIE_H = 800, 600
PAD = 45   # I/O ring width

ax.set_xlim(-25, DIE_W + 90)
ax.set_ylim(-40, DIE_H + 60)
ax.set_aspect('equal')
ax.axis('off')
fig.patch.set_facecolor('white')

ax.set_title('AquaMonitorSoC v1.0 — Floorplan do Chip\n'
             'Die: 800×600 µm · CMOS TSMC 180nm · VDD = 1.8V',
             fontsize=12, fontweight='bold', pad=10)

# ─── Die outline ──────────────────────────────────────────────────────────────
ax.add_patch(plt.Rectangle((0, 0), DIE_W, DIE_H,
             fc='#cccccc', ec='black', lw=2.5, zorder=1))  # I/O ring fill
ax.add_patch(plt.Rectangle((PAD, PAD), DIE_W-2*PAD, DIE_H-2*PAD,
             fc='white', ec='black', lw=1.5, zorder=2))    # core area

# ─── Analog / Digital boundary ────────────────────────────────────────────────
SPLIT = PAD + int(0.40*(DIE_W - 2*PAD))   # x = 333
ax.plot([SPLIT, SPLIT], [PAD, DIE_H-PAD], 'k--', lw=2.0, zorder=5)

# ─── Domain labels ────────────────────────────────────────────────────────────
ax.text(PAD + (SPLIT-PAD)//2, DIE_H-PAD-12,
        'ANALÓGICO', ha='center', fontsize=11, fontweight='bold', color='#444', zorder=6)
ax.text(SPLIT + (DIE_W-PAD-SPLIT)//2, DIE_H-PAD-12,
        'DIGITAL', ha='center', fontsize=11, fontweight='bold', color='#111', zorder=6)

# ─── Block helper ─────────────────────────────────────────────────────────────
def blk(x, y, w, h, name, sub='', fc='#e8e8e8'):
    ax.add_patch(plt.Rectangle((x, y), w, h, fc=fc, ec='black', lw=1.4, zorder=4))
    cx, cy = x + w/2, y + h/2
    if sub:
        ax.text(cx, cy+h*0.18, name, ha='center', va='center',
                fontsize=7.5, fontweight='bold', zorder=5)
        ax.text(cx, cy-h*0.18, sub, ha='center', va='center',
                fontsize=6.0, color='#555', zorder=5)
    else:
        ax.text(cx, cy, name, ha='center', va='center',
                fontsize=7.5, fontweight='bold', zorder=5)
    # size annotation at top-left inside block
    ax.text(x+3, y+h-5, f'{w}×{h}µm', ha='left', va='top',
            fontsize=5.5, color='#777', zorder=5)

# ─── ANALOG blocks (x from PAD+15, stacked with 15µm gaps) ───────────────────
AX = PAD + 15
GAP = 15   # gap between blocks

# Stack from top:  Comparator · Cap DAC (same row) · MUX · Bandgap (same row) · S/H · Decap
#  Comparator 80×65 at (AX, 390)
#  Cap DAC    60×65 at (AX+100, 390)    → ends AX+160 < SPLIT-PAD ✓
#  MUX        55×55 at (AX, 310)
#  Bandgap    60×55 at (AX+75, 310)
#  S/H Cap    80×55 at (AX, 240)
#  Bias Gen   80×45 at (AX, 180)
#  Ana Decap  170×90 at (AX, 65)

blk(AX,       390, 80, 65, 'Comparador',  '80×65µm')
blk(AX+100,   390, 60, 65, 'Cap DAC\n4-bit', '60×65µm')
blk(AX,       310, 55, 55, '3:1 MUX',     '55×55µm')
blk(AX+75,    310, 60, 55, 'Bandgap\nRef', '60×55µm')
blk(AX,       235, 80, 55, 'S/H Cap\nArray', '80×55µm')
blk(AX,       175, 80, 45, 'Bias Gen',     '80×45µm', fc='#f0f0f0')
blk(AX,        65, 170, 90, 'Analog Decap (filler)', fc='#f8f8f8')

# ─── DIGITAL blocks (x from SPLIT+20, stacked with 20µm gaps) ────────────────
DX = SPLIT + 20
GAP_D = 18

# Heights chosen so stack fits in core height (DIE_H - 2*PAD = 510µm)
# Stack from top: SAR FSM 130×80 · SPI Slave 110×80 (same row)
#                 Clk Div 70×45 · Result Reg 90×45 · Ch Seq 90×45 (same row)
#                 Scan Chain 210×45
#                 Digital Decap 270×80
# Gaps: 20µm between rows

# Row 1 top: y=400  SAR FSM 80high → top=480; SPI 80high, same y
blk(DX,       400, 130, 80, 'SAR FSM',    '130×80µm', fc='#d0d0d0')
blk(DX+160,   400, 110, 80, 'SPI Slave',  '110×80µm', fc='#d0d0d0')

# Row 2: y=340  h=45 → top=385; gap from row2_top(385) to row1_bot(400)=15µm
blk(DX,       335, 70,  45, 'Clk Div /8', '70×45µm',  fc='#e0e0e0')
blk(DX+90,    335, 90,  45, 'Result Reg', '90×45µm',  fc='#e0e0e0')
blk(DX+200,   335, 80,  45, 'Ch Seq',     '80×45µm',  fc='#e0e0e0')

# Row 3: y=275  h=45 → top=320; gap=15
blk(DX,       270, 210, 45, 'Scan Chain (DFT)', fc='#eeeeee')

# Row 4: y=65  h=180 → top=245; gap=25
blk(DX,        65, 270, 180, 'Digital Decap & Filler', fc='#f8f8f8')

# ─── I/O pad labels ──────────────────────────────────────────────────────────
bot_pads = ['GND','VDD','RESET','SPI_CS','SPI_CLK','SPI_MOSI',
            'SPI_MISO','VPH','VCOND','VTEMP']
top_pads = ['VDD','CLK_8M','DAC_SW[3:0]','MUX_S[2:0]','COMP_OUT',
            'EOC','AVDD','AGND','VREF','TEST']

for i, lbl in enumerate(bot_pads):
    px = (i+0.5)*DIE_W/len(bot_pads)
    ax.text(px, -8, lbl, ha='center', va='top', fontsize=5.5, rotation=40)
    ax.plot([px, px], [0, 12], 'k-', lw=0.7)

for i, lbl in enumerate(top_pads):
    px = (i+0.5)*DIE_W/len(top_pads)
    ax.text(px, DIE_H+8, lbl, ha='center', va='bottom', fontsize=5.5, rotation=40)
    ax.plot([px, px], [DIE_H-12, DIE_H], 'k-', lw=0.7)

left_pads = ['AVDD','AGND','COMP_IN','VREF_EXT']
right_pads = ['DVDD','DGND','LED','IRQ']
for i, lbl in enumerate(left_pads):
    py = (i+0.5)*DIE_H/len(left_pads)
    ax.text(-8, py, lbl, ha='right', va='center', fontsize=5.5)
    ax.plot([0, 12], [py, py], 'k-', lw=0.7)
for i, lbl in enumerate(right_pads):
    py = (i+0.5)*DIE_H/len(right_pads)
    ax.text(DIE_W+8, py, lbl, ha='left', va='center', fontsize=5.5)
    ax.plot([DIE_W-12, DIE_W], [py, py], 'k-', lw=0.7)

# ─── Scale bar ───────────────────────────────────────────────────────────────
sb_x, sb_y = 620, -25
ax.plot([sb_x, sb_x+100], [sb_y, sb_y], 'k-', lw=2.2)
for ex in (sb_x, sb_x+100):
    ax.plot([ex, ex], [sb_y-4, sb_y+4], 'k-', lw=2.2)
ax.text(sb_x+50, sb_y-7, '100 µm', ha='center', va='top', fontsize=7.5)

# ─── Legend ──────────────────────────────────────────────────────────────────
patches = [
    mpatches.Patch(fc='#cccccc', ec='black', label='I/O Ring (Pad Cells)'),
    mpatches.Patch(fc='#e8e8e8', ec='black', label='Blocos Analógicos'),
    mpatches.Patch(fc='#d0d0d0', ec='black', label='Blocos Digitais Core'),
    mpatches.Patch(fc='#e0e0e0', ec='black', label='Blocos Digitais Aux'),
    mpatches.Patch(fc='#f8f8f8', ec='black', label='Decap / Filler'),
]
ax.legend(handles=patches, loc='lower right', fontsize=7.5, framealpha=0.95)

ax.text(DIE_W/2, -38,
        'AquaMonitorSoC v1.0 — PADIS Unidade 7, Cap 5 — CMOS TSMC 180nm',
        ha='center', va='top', fontsize=7, color='gray', style='italic')

plt.tight_layout()
plt.savefig('fig_floorplan_soc.png', dpi=150, bbox_inches='tight', facecolor='white')
print("Saved: fig_floorplan_soc.png")
