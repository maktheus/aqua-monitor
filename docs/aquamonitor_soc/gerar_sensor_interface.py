"""
gerar_sensor_interface.py — AquaMonitorSoC v1.0
3 sensor conditioning chain diagrams, no overlaps.
Each panel is a clean left-to-right signal chain with generous spacing.
"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

fig, axes = plt.subplots(3, 1, figsize=(14, 12))
fig.patch.set_facecolor('white')
fig.suptitle('AquaMonitorSoC v1.0 — Circuitos de Condicionamento de Sinal\n'
             'Canais: pH · Condutividade · Temperatura PTAT',
             fontsize=13, fontweight='bold', y=0.99)

# ─── helper: draw a block ────────────────────────────────────────────────────
def blk(ax, x, y, w, h, title, sub='', fc='white', fs=8):
    ax.add_patch(plt.Rectangle((x-w/2, y-h/2), w, h,
                                fc=fc, ec='black', lw=1.4, zorder=3))
    cy = y + h*0.15 if sub else y
    ax.text(x, cy, title, ha='center', va='center', fontsize=fs,
            fontweight='bold', zorder=4)
    if sub:
        ax.text(x, y-h*0.22, sub, ha='center', va='center',
                fontsize=fs-1.5, color='#555', zorder=4)

def circle(ax, x, y, r, title, sub='', fc='#f0f0f0', fs=8):
    ax.add_patch(plt.Circle((x, y), r, fc=fc, ec='black', lw=1.4, zorder=3))
    cy = y + r*0.2 if sub else y
    ax.text(x, cy, title, ha='center', va='center', fontsize=fs,
            fontweight='bold', zorder=4)
    if sub:
        ax.text(x, y-r*0.45, sub, ha='center', va='center',
                fontsize=fs-1.5, color='#555', zorder=4)

def wire(ax, x1, y, x2, lbl='', color='black'):
    ax.annotate('', xy=(x2, y), xytext=(x1, y),
                arrowprops=dict(arrowstyle='->', color=color, lw=1.2))
    if lbl:
        ax.text((x1+x2)/2, y+0.12, lbl, ha='center', va='bottom',
                fontsize=7, style='italic', color='#333')

# ═══════════════════════════════════════════════════════════════════
# Panel 0: pH Sensor
# ═══════════════════════════════════════════════════════════════════
ax = axes[0]
ax.set_xlim(0, 14)
ax.set_ylim(-1.0, 2.5)
ax.axis('off')
ax.set_title('Canal pH — Eletrodo de Vidro Potenciométrico',
             fontsize=10, fontweight='bold', pad=4)

# Signal chain: Electrode → TIA → Gain+Offset → Anti-alias LPF → VIN_pH
Y = 1.0
circle(ax, 1.2,  Y, 0.55, 'Eletrodo\npH', '0–420mV', fc='#f0f0f0', fs=7)
blk(ax,    3.5,  Y, 2.2, 0.80, 'Amp. Transimpedância', 'Rfb = 10 GΩ\nRin > 10 TΩ', fs=7)
blk(ax,    6.5,  Y, 2.0, 0.80, 'Ganho + Offset', '×4.3  +  Vref', fs=7)
blk(ax,    9.4,  Y, 1.8, 0.80, 'Filtro Anti-alias', 'LPF: R=160kΩ\nC=100nF, fc=10Hz', fs=7)
blk(ax,   12.2, Y, 1.2, 0.80, 'Buffer\n(OA)', 'VIN_pH\n0–1.8V', fc='#e8e8e8', fs=7)

wire(ax, 1.75, Y, 2.4,  'Vpot\n(0–420mV)')
wire(ax, 4.60, Y, 5.5,  'Vtia')
wire(ax, 7.50, Y, 8.5,  'Vgain')
wire(ax, 10.3, Y, 11.6, 'Vfilt')

# Note box
ax.text(7.0, -0.45,
        'Equação de Nernst: V = 0.0592 × (7 – pH) V  |  '
        'Sensibilidade: 59.2 mV/pH  |  Escala: 0–840 mV → 0–1.8V',
        ha='center', va='center', fontsize=7.5,
        bbox=dict(boxstyle='round,pad=0.3', fc='#f8f8f8', ec='#aaa', lw=0.8))

# ═══════════════════════════════════════════════════════════════════
# Panel 1: Conductivity Sensor
# ═══════════════════════════════════════════════════════════════════
ax = axes[1]
ax.set_xlim(0, 14)
ax.set_ylim(-1.0, 2.5)
ax.axis('off')
ax.set_title('Canal Condutividade — Excitação AC com Retificador de Precisão',
             fontsize=10, fontweight='bold', pad=4)

Y = 1.0
circle(ax, 1.2,  Y, 0.55, 'Osc.\n1kHz', 'Vexc=1V', fc='#f0f0f0', fs=7)
blk(ax,    3.4,  Y, 2.0, 0.80, 'Célula Cond.', 'K=1.0 cm⁻¹\nRcel: 500Ω–2MΩ', fs=7)
blk(ax,    6.3,  Y, 2.0, 0.80, 'Retificador\nPrecisão', 'Full-wave\n4× OA', fs=7)
blk(ax,    9.2,  Y, 1.8, 0.80, 'Filtro Passa-Baixa', 'R=4.7kΩ\nC=33nF, fc=1kHz', fs=7)
blk(ax,   12.0, Y, 1.6, 0.80, 'Buffer\n(OA)', 'VIN_Cond\n0–1.8V', fc='#e8e8e8', fs=7)

wire(ax, 1.75, Y, 2.4,  'Vexc')
wire(ax, 4.40, Y, 5.3,  'Vac_cell')
wire(ax, 7.30, Y, 8.3,  'Vdc_rect')
wire(ax, 10.1, Y, 11.2, 'Vdc_filt')

ax.text(7.0, -0.45,
        'Vout = Vexc × Rref / Rcell  |  Rref = 4.7 kΩ  |  '
        'Faixa: 0–2000 µS/cm → 0–1.8V  |  Eletrodo: aço inox SS316, d=2mm',
        ha='center', va='center', fontsize=7.5,
        bbox=dict(boxstyle='round,pad=0.3', fc='#f8f8f8', ec='#aaa', lw=0.8))

# ═══════════════════════════════════════════════════════════════════
# Panel 2: Temperature PTAT
# ═══════════════════════════════════════════════════════════════════
ax = axes[2]
ax.set_xlim(0, 14)
ax.set_ylim(-1.0, 2.5)
ax.axis('off')
ax.set_title('Canal Temperatura — Sensor PTAT (Proporcional à Temperatura Absoluta)',
             fontsize=10, fontweight='bold', pad=4)

Y = 1.0
blk(ax,    1.5,  Y, 2.0, 0.80, 'Célula PTAT', 'Q1/Q2 (N=8)\nΔVBE≈1.6mV/°C', fc='#f0f0f0', fs=7)
blk(ax,    4.3,  Y, 1.8, 0.80, 'Espelho\nCorrente', 'Iptat=10µA\n@ 27°C', fs=7)
blk(ax,    7.0,  Y, 1.8, 0.80, 'Conv. I→V', 'R=10kΩ\nVptat=I×R', fs=7)
blk(ax,    9.8,  Y, 2.0, 0.80, 'Ganho + Offset', '×6.8 + Vshift\n−40→125°C', fs=7)
blk(ax,   12.3, Y, 1.4, 0.80, 'Buffer\n(OA)', 'VIN_Temp\n0–1.8V', fc='#e8e8e8', fs=7)

wire(ax, 2.50, Y, 3.4,  'IPTAT')
wire(ax, 5.20, Y, 6.1,  'Imirror')
wire(ax, 7.90, Y, 8.8,  'Vptat')
wire(ax, 10.8, Y, 11.6, 'Vgain')

ax.text(7.0, -0.45,
        'Sensibilidade: 1.6 mV/°C  |  Faixa: −40..125°C → 0..265mV → (×6.8) → 0..1.8V  |  '
        'Não-linearidade < 0.5°C (corrigida por SW)',
        ha='center', va='center', fontsize=7.5,
        bbox=dict(boxstyle='round,pad=0.3', fc='#f8f8f8', ec='#aaa', lw=0.8))

plt.tight_layout(rect=[0, 0, 1, 0.97])
plt.savefig('fig_sensor_interface.png', dpi=150, bbox_inches='tight', facecolor='white')
print("Saved: fig_sensor_interface.png")
