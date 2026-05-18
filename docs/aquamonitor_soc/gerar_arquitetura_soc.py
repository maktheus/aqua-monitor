"""
gerar_arquitetura_soc.py
Full SoC block diagram for AquaMonitorSoC v1.0
Black/white matplotlib, 14x10 figure
"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch

fig, ax = plt.subplots(figsize=(14, 10))
ax.set_xlim(0, 14)
ax.set_ylim(0, 10)
ax.axis('off')

# ---- Helper functions ----
def box(ax, x, y, w, h, label, sublabel='', fc='white', ec='black', lw=1.5, fontsize=9):
    rect = FancyBboxPatch((x, y), w, h,
                          boxstyle="round,pad=0.05",
                          facecolor=fc, edgecolor=ec, linewidth=lw)
    ax.add_patch(rect)
    if sublabel:
        ax.text(x + w/2, y + h*0.65, label, ha='center', va='center',
                fontsize=fontsize, fontweight='bold')
        ax.text(x + w/2, y + h*0.30, sublabel, ha='center', va='center',
                fontsize=7, color='#444444')
    else:
        ax.text(x + w/2, y + h/2, label, ha='center', va='center',
                fontsize=fontsize, fontweight='bold')

def arrow(ax, x1, y1, x2, y2, label='', lw=1.2):
    ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle='->', color='black', lw=lw))
    if label:
        mx, my = (x1+x2)/2, (y1+y2)/2
        ax.text(mx, my + 0.12, label, ha='center', va='bottom', fontsize=7,
                style='italic', color='#222222')

# ===== TITLE =====
ax.text(7, 9.6, 'AquaMonitorSoC v1.0 — Mixed-Signal SoC Architecture',
        ha='center', va='center', fontsize=13, fontweight='bold')
ax.text(7, 9.25, 'SAR ADC 4-bit · 3 Canais · CMOS TSMC 180nm · VDD=1.8V',
        ha='center', va='center', fontsize=9, color='#333333')

# ===== CLOCK DIVIDER (top center) =====
box(ax, 5.5, 8.2, 3.0, 0.75, 'Clock Divider  /8',
    '8 MHz → 1 MHz ADC Clock', fc='#f5f5f5', fontsize=8)
arrow(ax, 5.5, 8.57, 4.2, 8.57, '8MHz', lw=1)
ax.text(4.0, 8.57, '8MHz\nclk_8mhz', ha='right', va='center', fontsize=7)
arrow(ax, 8.5, 8.57, 9.2, 8.57, '1MHz', lw=1)
ax.text(9.3, 8.57, 'clk_1mhz', ha='left', va='center', fontsize=7)

# ===== SENSOR DOMAIN (left) =====
ax.text(1.0, 7.9, 'SENSOR DOMAIN', ha='center', va='center',
        fontsize=8, fontweight='bold', color='#555555')
# Dashed boundary for sensor domain
rect_sens = plt.Rectangle((0.1, 4.3), 2.5, 3.5,
                           fill=False, linestyle='--', edgecolor='gray', lw=1.2)
ax.add_patch(rect_sens)

box(ax, 0.25, 6.8, 1.7, 0.7, 'pH Sensor', '0–14 pH / 0–1.8V', fc='#f0f0f0', fontsize=7)
box(ax, 0.25, 5.85, 1.7, 0.7, 'Conductivity', '0–2000µS/cm / 0–1.8V', fc='#f0f0f0', fontsize=7)
box(ax, 0.25, 4.90, 1.7, 0.7, 'Temp PTAT', '−40..125°C / 0–1.8V', fc='#f0f0f0', fontsize=7)

# Sensor arrows to MUX
arrow(ax, 1.95, 7.15, 3.0, 6.85, 'VpH')
arrow(ax, 1.95, 6.20, 3.0, 6.45, 'Vcond')
arrow(ax, 1.95, 5.25, 3.0, 6.10, 'Vtemp')

# ===== ANALOG DOMAIN (center-left) =====
ax.text(4.5, 7.9, 'ANALOG DOMAIN', ha='center', va='center',
        fontsize=8, fontweight='bold', color='#555555')
rect_ana = plt.Rectangle((2.8, 4.3), 3.5, 3.5,
                          fill=False, linestyle='--', edgecolor='#333333', lw=1.5)
ax.add_patch(rect_ana)

# MUX
box(ax, 3.0, 6.3, 1.4, 0.9, '3:1 Analog\nMUX', fc='white', fontsize=8)
# Comparator
box(ax, 3.0, 5.05, 1.4, 0.9, 'Dynamic\nComparator', fc='white', fontsize=8)
# DAC
box(ax, 3.0, 4.35, 1.4, 0.55, '4-bit Cap DAC', fc='white', fontsize=8)

# MUX → Comparator
arrow(ax, 3.7, 6.3, 3.7, 5.95, 'VIN')
# Comparator → FSM
arrow(ax, 4.4, 5.5, 5.4, 5.5, 'comp_out')
# DAC → Comparator
arrow(ax, 3.7, 4.9, 3.7, 5.05, 'VDAC')
# MUX ctrl
arrow(ax, 5.55, 6.0, 4.4, 6.65, 'mux_sel[2:0]')

# ===== DIGITAL DOMAIN (center-right) =====
ax.text(7.6, 7.9, 'DIGITAL DOMAIN', ha='center', va='center',
        fontsize=8, fontweight='bold', color='#555555')
rect_dig = plt.Rectangle((5.3, 4.3), 4.5, 3.5,
                          fill=False, linestyle='-', edgecolor='#111111', lw=1.5)
ax.add_patch(rect_dig)

# SAR FSM
box(ax, 5.5, 6.1, 2.0, 1.4, 'SAR Control\nFSM',
    'Moore, 8 States', fc='#e8e8e8', fontsize=9)
# Result Register
box(ax, 5.5, 4.95, 2.0, 0.85, 'Result\nRegister', fc='white', fontsize=8)
# SPI Slave
box(ax, 7.7, 5.6, 1.9, 1.3, 'SPI Slave\n16-bit frame', fc='#e8e8e8', fontsize=8)
# Channel Sequencer
box(ax, 7.7, 4.5, 1.9, 0.85, 'Channel\nSequencer', fc='white', fontsize=8)

# FSM → DAC code
arrow(ax, 5.5, 6.45, 4.4, 4.62, 'dac_code[3:0]')
# FSM → sample_en
arrow(ax, 5.5, 7.1, 4.4, 5.5, 'sample_en', lw=1)
# FSM → Result Reg
arrow(ax, 6.5, 6.1, 6.5, 5.8, 'result[3:0]')
# Result Reg → SPI
arrow(ax, 7.5, 5.37, 7.7, 5.9, 'data_in[15:0]')
# Sequencer → FSM (start)
arrow(ax, 8.65, 5.35, 7.5, 6.45, 'start/ch_sel')
# ch_sel → MUX
arrow(ax, 7.7, 4.92, 4.4, 6.65, '')

# EOC
arrow(ax, 7.5, 6.8, 7.7, 6.6, 'eoc')
ax.annotate('', xy=(6.5, 6.95), xytext=(7.5, 6.95),
            arrowprops=dict(arrowstyle='->', color='black', lw=1.0))

# ===== SPI INTERFACE (right) =====
ax.text(11.5, 7.9, 'SPI INTERFACE', ha='center', va='center',
        fontsize=8, fontweight='bold', color='#555555')
rect_spi = plt.Rectangle((10.0, 5.2), 2.8, 2.6,
                          fill=False, linestyle='--', edgecolor='gray', lw=1.2)
ax.add_patch(rect_spi)

box(ax, 10.1, 6.8, 2.5, 0.7, 'MCU / Host', 'SPI Master', fc='#f0f0f0', fontsize=8)
box(ax, 10.1, 5.4, 2.5, 1.1, 'SPI Bus\nSCLK/MOSI\nMISO/CS_n', fc='white', fontsize=7)

arrow(ax, 9.6, 6.2, 10.1, 6.2, '')
arrow(ax, 10.1, 7.15, 9.6, 7.15, '')
ax.annotate('', xy=(9.6, 6.2), xytext=(9.6, 7.15),
            arrowprops=dict(arrowstyle='<->', color='black', lw=1.2))

# ===== STATUS / LED =====
box(ax, 5.5, 4.35, 1.0, 0.45, 'LED', fc='white', fontsize=7)
box(ax, 6.7, 4.35, 1.0, 0.45, 'Status', fc='white', fontsize=7)

# ===== POWER DOMAIN LABELS =====
ax.text(0.15, 4.0, 'VDD=1.8V', ha='left', va='center', fontsize=7, color='gray')
ax.text(2.85, 4.0, 'AVDD=1.8V', ha='left', va='center', fontsize=7, color='gray')
ax.text(5.35, 4.0, 'DVDD=1.8V', ha='left', va='center', fontsize=7, color='gray')

# ===== LEGEND =====
legend_patches = [
    mpatches.Patch(facecolor='#f0f0f0', edgecolor='black', label='Sensor/IO Blocks'),
    mpatches.Patch(facecolor='white', edgecolor='black', label='Analog Blocks'),
    mpatches.Patch(facecolor='#e8e8e8', edgecolor='black', label='Digital Blocks'),
]
ax.legend(handles=legend_patches, loc='lower right', fontsize=7, framealpha=0.9)

# ===== BOTTOM NOTE =====
ax.text(7, 0.15, 'AquaMonitorSoC v1.0 — PADIS Unidade 7, Cap 5 — CMOS TSMC 180nm',
        ha='center', va='center', fontsize=7, color='gray', style='italic')

plt.tight_layout()
plt.savefig('fig_arquitetura_soc.png', dpi=150, bbox_inches='tight',
            facecolor='white')
print("Saved: fig_arquitetura_soc.png")
