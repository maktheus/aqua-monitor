"""
gerar_arquitetura_soc.py — AquaMonitorSoC v1.0
Block diagram redesigned to avoid overlaps: clean grid layout.
"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch
import matplotlib.patheffects as pe

fig, ax = plt.subplots(figsize=(16, 11))
ax.set_xlim(0, 16)
ax.set_ylim(0, 11)
ax.axis('off')
fig.patch.set_facecolor('white')

# ─── helpers ───────────────────────────────────────────────────────────────────
def box(ax, x, y, w, h, title, sub='', fc='white', ec='black', lw=1.5, ts=9, ss=7):
    r = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.07",
                       fc=fc, ec=ec, lw=lw, zorder=3)
    ax.add_patch(r)
    cx, cy = x + w/2, y + h/2
    if sub:
        ax.text(cx, cy + h*0.18, title, ha='center', va='center',
                fontsize=ts, fontweight='bold', zorder=4)
        ax.text(cx, cy - h*0.20, sub, ha='center', va='center',
                fontsize=ss, color='#444', zorder=4)
    else:
        ax.text(cx, cy, title, ha='center', va='center',
                fontsize=ts, fontweight='bold', zorder=4)

def arr(ax, x1, y1, x2, y2, lbl='', lpos=0.45, loffx=0, loffy=0.13, lw=1.3):
    ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle='->', color='black', lw=lw,
                                connectionstyle='arc3,rad=0.0'))
    if lbl:
        mx = x1 + (x2-x1)*lpos + loffx
        my = y1 + (y2-y1)*lpos + loffy
        ax.text(mx, my, lbl, ha='center', va='bottom', fontsize=7,
                style='italic', color='#222',
                bbox=dict(boxstyle='round,pad=0.1', fc='white', alpha=0.9, ec='none'),
                zorder=5)

def domain(ax, x, y, w, h, lbl, ls='--', lw=1.2, fc='none', ec='#888'):
    r = plt.Rectangle((x, y), w, h, fill=(fc != 'none'),
                       fc=fc, ec=ec, lw=lw, ls=ls, zorder=1)
    ax.add_patch(r)
    ax.text(x + w/2, y + h + 0.15, lbl, ha='center', va='bottom',
            fontsize=8, fontweight='bold', color='#555', zorder=5)

# ─── title ─────────────────────────────────────────────────────────────────────
ax.text(8, 10.65, 'AquaMonitorSoC v1.0 — Arquitetura do Sistema',
        ha='center', fontsize=14, fontweight='bold')
ax.text(8, 10.30, 'SAR ADC 4-bit Time-Multiplexed · 3 Canais Sensoriais · CMOS TSMC 180nm · VDD = 1.8V',
        ha='center', fontsize=9, color='#333')

# ─── COLUMN 1: sensors (x 0.3 – 2.5) ─────────────────────────────────────────
domain(ax, 0.2, 1.9, 2.4, 5.8, 'DOMÍNIO SENSOR')
box(ax, 0.4, 6.8, 1.9, 0.75, 'Sensor pH',      '0–14 pH | 0–1.8V', fc='#f5f5f5', ts=8, ss=7)
box(ax, 0.4, 5.6, 1.9, 0.75, 'Condutividade',  '0–2000µS/cm | 0–1.8V', fc='#f5f5f5', ts=8, ss=7)
box(ax, 0.4, 4.4, 1.9, 0.75, 'Temp. PTAT',    '−40..125°C | 0–1.8V', fc='#f5f5f5', ts=8, ss=7)
box(ax, 0.4, 2.2, 1.9, 0.75, 'Cond. Front-End','TIA / AC+Rect / Buffer', fc='#f5f5f5', ts=8, ss=7)

# ─── COLUMN 2: analog domain (x 2.9 – 5.5) ────────────────────────────────────
domain(ax, 2.8, 1.9, 2.8, 5.8, 'DOMÍNIO ANALÓGICO', ec='#333', lw=1.5)
box(ax, 3.0, 6.8, 2.3, 0.75, '3:1 MUX Analógico',  'sel[2:0] controle digital', fc='white', ts=8, ss=7)
box(ax, 3.0, 5.6, 2.3, 0.75, 'Comparador Dinâmico', '2-estágio, offset < 2mV', fc='white', ts=8, ss=7)
box(ax, 3.0, 4.4, 2.3, 0.75, 'DAC Capacitivo 4-bit', 'C_unit=20fF, R-2R ladder', fc='white', ts=8, ss=7)
box(ax, 3.0, 2.2, 2.3, 0.75, 'Ref. Bandgap',         '1.2V ±0.1%, PTAT curr.', fc='#eee', ts=8, ss=7)

# ─── COLUMN 3: digital domain (x 5.9 – 10.5) ─────────────────────────────────
domain(ax, 5.8, 1.9, 4.8, 5.8, 'DOMÍNIO DIGITAL', ec='#111', lw=1.8)
box(ax, 6.0, 6.8, 2.4, 0.75, 'SAR FSM',       'Moore, 8 estados', fc='#e0e0e0', ts=9, ss=7)
box(ax, 6.0, 5.6, 2.4, 0.75, 'Reg. Resultado', 'result[3:0], status[7:0]', fc='white', ts=8, ss=7)
box(ax, 6.0, 4.4, 2.4, 0.75, 'Sequenciador',   'ch_sel[1:0], round-robin', fc='white', ts=8, ss=7)
box(ax, 6.0, 3.2, 2.4, 0.75, 'Divisor Clock',  '8MHz → 1MHz (/8)', fc='#e0e0e0', ts=8, ss=7)
box(ax, 6.0, 2.2, 2.4, 0.75, 'SPI Slave',      '16-bit: CH|RESULT|STATUS', fc='#e0e0e0', ts=8, ss=7)

# ─── COLUMN 4: SPI interface (x 11.0 – 13.5) ──────────────────────────────────
domain(ax, 10.9, 3.0, 2.8, 5.0, 'INTERFACE SPI', ls='--', ec='#888')
box(ax, 11.1, 6.8, 2.4, 0.75, 'MCU / Host',  'SPI Master externo', fc='#f5f5f5', ts=8, ss=7)
box(ax, 11.1, 5.2, 2.4, 0.75, 'SPI Bus',     'SCLK / MOSI / MISO / CS_n', fc='white', ts=8, ss=7)
box(ax, 11.1, 3.2, 2.4, 0.75, 'LED / Status','led_ready, eoc pulse', fc='white', ts=8, ss=7)

# ─── external clock ───────────────────────────────────────────────────────────
box(ax, 5.9, 9.3, 2.4, 0.55, 'Divisor Clock  8MHz→1MHz', fc='#eee', ts=8, lw=1.2)
ax.annotate('', xy=(5.9, 9.57), xytext=(4.8, 9.57),
            arrowprops=dict(arrowstyle='->', color='black', lw=1.1))
ax.text(4.7, 9.57, 'clk_8mhz', ha='right', va='center', fontsize=7)
ax.annotate('', xy=(7.3, 9.3), xytext=(7.3, 8.2),
            arrowprops=dict(arrowstyle='->', color='black', lw=1.1))
ax.text(7.5, 8.75, 'clk_1mhz', ha='left', va='center', fontsize=7)

# ─── sensor → conditioning ───────────────────────────────────────────────────
arr(ax, 1.35, 6.8,  1.35, 2.95,  '', lw=1.0)   # pH down to front-end
arr(ax, 1.7,  5.6,  1.7,  2.95,  '', lw=1.0)   # cond
arr(ax, 2.1,  4.4,  2.1,  2.95,  '', lw=1.0)   # temp

# ─── conditioning → MUX ───────────────────────────────────────────────────────
arr(ax, 2.30, 2.57, 3.0, 2.57, 'Vcond\nVpH\nVtemp', lpos=0.5, loffy=0.05, lw=1.2)

# ─── MUX output → comparator ─────────────────────────────────────────────────
arr(ax, 4.15, 6.80, 4.15, 6.35, 'VIN', loffx=0.25)

# ─── DAC → comparator ────────────────────────────────────────────────────────
arr(ax, 4.15, 4.40, 4.15, 4.95, 'VDAC', loffx=0.28)

# ─── comparator → FSM ────────────────────────────────────────────────────────
arr(ax, 5.30, 5.97, 6.00, 7.17, 'comp_out', lpos=0.5, loffx=0.15, loffy=0.10)

# ─── FSM → DAC code ──────────────────────────────────────────────────────────
ax.annotate('', xy=(5.30, 4.75), xytext=(6.00, 7.05),
            arrowprops=dict(arrowstyle='->', color='black', lw=1.2,
                            connectionstyle='arc3,rad=0.3'))
ax.text(5.05, 5.9, 'dac_code\n[3:0]', ha='right', va='center', fontsize=7,
        style='italic', color='#222',
        bbox=dict(boxstyle='round,pad=0.1', fc='white', alpha=0.9, ec='none'), zorder=5)

# ─── FSM → sample_en ─────────────────────────────────────────────────────────
ax.annotate('', xy=(5.30, 5.62), xytext=(6.00, 6.85),
            arrowprops=dict(arrowstyle='->', color='black', lw=1.0,
                            connectionstyle='arc3,rad=0.25'))
ax.text(5.2, 6.25, 'sample\n_en', ha='right', va='center', fontsize=7,
        style='italic', color='#222',
        bbox=dict(boxstyle='round,pad=0.1', fc='white', alpha=0.9, ec='none'), zorder=5)

# ─── FSM → mux sel ───────────────────────────────────────────────────────────
ax.annotate('', xy=(3.00, 7.17), xytext=(6.00, 7.17),
            arrowprops=dict(arrowstyle='->', color='black', lw=1.1,
                            connectionstyle='arc3,rad=0.0'))
ax.text(4.50, 7.35, 'mux_sel[2:0]', ha='center', va='bottom', fontsize=7,
        style='italic', color='#222',
        bbox=dict(boxstyle='round,pad=0.1', fc='white', alpha=0.9, ec='none'), zorder=5)

# ─── sequencer → FSM start ────────────────────────────────────────────────────
arr(ax, 8.40, 7.17, 8.40, 7.17, '')
arr(ax, 8.40, 4.77, 8.40, 6.80, 'start\nch_sel', lpos=0.5, loffx=0.35)

# ─── FSM → result reg ────────────────────────────────────────────────────────
arr(ax, 7.20, 6.80, 7.20, 6.35, 'result[3:0]', loffx=0.55)

# ─── result reg → SPI slave ───────────────────────────────────────────────────
arr(ax, 7.20, 5.60, 7.20, 2.95, 'data_in\n[15:0]', lpos=0.5, loffx=0.55)

# ─── SPI slave → SPI bus ─────────────────────────────────────────────────────
arr(ax, 8.40, 2.57, 11.10, 5.57, 'SPI 16-bit', lpos=0.5, loffx=0.20, loffy=0.15)

# ─── SPI bus ↔ MCU ───────────────────────────────────────────────────────────
ax.annotate('', xy=(12.30, 5.95), xytext=(12.30, 6.80),
            arrowprops=dict(arrowstyle='<->', color='black', lw=1.3))

# ─── EOC ─────────────────────────────────────────────────────────────────────
arr(ax, 8.40, 6.80, 11.10, 3.57, 'eoc', lpos=0.5, loffx=0.20, loffy=0.10)

# ─── power labels ────────────────────────────────────────────────────────────
for xp, lbl in [(0.25, 'VDD=1.8V'), (2.85, 'AVDD=1.8V'), (5.85, 'DVDD=1.8V')]:
    ax.text(xp, 1.70, lbl, fontsize=7, color='#888', ha='left')

# ─── legend ──────────────────────────────────────────────────────────────────
patches = [
    mpatches.Patch(fc='#f5f5f5', ec='black', label='Sensor / Front-End'),
    mpatches.Patch(fc='white',   ec='black', label='Blocos Analógicos'),
    mpatches.Patch(fc='#e0e0e0', ec='black', label='Blocos Digitais'),
    mpatches.Patch(fc='#eee',    ec='black', label='Referência / Relógio'),
]
ax.legend(handles=patches, loc='lower right', fontsize=7.5, framealpha=0.95)

ax.text(8, 0.15, 'AquaMonitorSoC v1.0 — PADIS Unidade 7, Capítulo 5 — CMOS TSMC 180nm',
        ha='center', fontsize=7.5, color='gray', style='italic')

plt.tight_layout()
plt.savefig('fig_arquitetura_soc.png', dpi=150, bbox_inches='tight', facecolor='white')
print("Saved: fig_arquitetura_soc.png")
