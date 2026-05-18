"""
gerar_sensor_interface.py
Sensor conditioning circuits for pH, Conductivity, Temperature PTAT
3 sub-diagrams, black/white, 14x8
"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

fig, axes = plt.subplots(1, 3, figsize=(14, 8))
fig.suptitle('AquaMonitorSoC v1.0 — Sensor Conditioning Circuits\n'
             'Signal conditioning for pH, Conductivity and Temperature channels',
             fontsize=12, fontweight='bold')

def box_circ(ax, x, y, w, h, text, fc='white', ec='black', fs=8):
    r = plt.Rectangle((x - w/2, y - h/2), w, h,
                       facecolor=fc, edgecolor=ec, linewidth=1.5)
    ax.add_patch(r)
    ax.text(x, y, text, ha='center', va='center', fontsize=fs)

def circle_circ(ax, x, y, r, text, fc='white', ec='black', fs=7):
    c = plt.Circle((x, y), r, facecolor=fc, edgecolor=ec, linewidth=1.5)
    ax.add_patch(c)
    ax.text(x, y, text, ha='center', va='center', fontsize=fs)

def wire(ax, x1, y1, x2, y2):
    ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle='->', color='black', lw=1.2))

def line(ax, x1, y1, x2, y2, **kwargs):
    ax.plot([x1, x2], [y1, y2], 'k-', lw=1.2, **kwargs)

# ================================================================
# Panel 1: pH Sensor
# ================================================================
ax = axes[0]
ax.set_xlim(0, 10)
ax.set_ylim(0, 10)
ax.axis('off')
ax.set_title('pH Sensor\n(Potentiometric Glass Electrode)', fontsize=10, fontweight='bold')

# pH glass electrode
circle_circ(ax, 1.5, 7.5, 0.7, 'pH\nElect.', fc='#f0f0f0', fs=7)
ax.text(1.5, 8.5, 'Glass Electrode', ha='center', fontsize=7, style='italic')
ax.text(1.5, 6.5, 'Vin: 0–420mV', ha='center', fontsize=6.5, color='gray')

# TIA (Transimpedance Amplifier)
box_circ(ax, 4.0, 7.5, 1.8, 1.0, 'TIA\n(OA+Rfb=10GΩ)', fc='white', fs=7)
ax.text(4.0, 6.7, 'High-Z input\nRin > 10TΩ', ha='center', fontsize=6, color='gray')

# R divider
box_circ(ax, 6.5, 7.5, 1.4, 0.8, 'R Divider\nR1=R2=100kΩ', fc='white', fs=7)
ax.text(6.5, 6.8, '÷2 → 0–1.8V', ha='center', fontsize=6, color='gray')

# Buffer
box_circ(ax, 8.8, 7.5, 1.0, 0.7, 'Buffer\n(OA)', fc='white', fs=7)
ax.text(8.8, 6.9, 'VIN_pH', ha='center', fontsize=7, color='black', fontweight='bold')

# Wires
wire(ax, 2.2, 7.5, 3.1, 7.5)
wire(ax, 4.9, 7.5, 5.8, 7.5)
wire(ax, 7.2, 7.5, 8.3, 7.5)
ax.text(2.6, 7.7, 'Vpot', ha='center', fontsize=6.5, style='italic')
ax.text(5.4, 7.7, 'Vtia', ha='center', fontsize=6.5, style='italic')
ax.text(7.7, 7.7, 'Vdiv', ha='center', fontsize=6.5, style='italic')

# VDD/GND ref lines
line(ax, 4.0, 7.0, 4.0, 6.2)
ax.text(4.0, 6.0, 'GND', ha='center', fontsize=6.5)

# Calibration note
ax.text(5.0, 5.5,
        'pH Conditioning:\n'
        '• Nernst voltage: 59.16 mV/pH\n'
        '• Range: 0–14 pH = 0–840 mV\n'
        '• After ÷2: 0–420 mV\n'
        '• After buffer: 0–1.8V (×4.3)',
        ha='center', va='top', fontsize=7,
        bbox=dict(boxstyle='round', fc='#f8f8f8', ec='gray', lw=0.8))

ax.text(5.0, 2.8,
        'Rc: C_bypass=100nF\n(anti-aliasing @ fc=1kHz)',
        ha='center', va='top', fontsize=6.5, color='gray')

# ================================================================
# Panel 2: Conductivity Sensor
# ================================================================
ax = axes[1]
ax.set_xlim(0, 10)
ax.set_ylim(0, 10)
ax.axis('off')
ax.set_title('Conductivity Sensor\n(AC Excitation Method)', fontsize=10, fontweight='bold')

# AC excitation source
circle_circ(ax, 1.2, 7.5, 0.65, 'AC\n1kHz', fc='#f0f0f0', fs=7)
ax.text(1.2, 8.4, 'Excitation Osc.', ha='center', fontsize=7, style='italic')

# Conductivity cell
box_circ(ax, 3.2, 7.5, 1.4, 0.9, 'Cond Cell\nK=1.0 cm⁻¹', fc='#f0f0f0', fs=7)
ax.text(3.2, 6.8, 'Rcel: 500Ω–2MΩ', ha='center', fontsize=6, color='gray')

# Precision rectifier
box_circ(ax, 5.5, 7.5, 1.5, 0.85, 'Full-wave\nRectifier', fc='white', fs=7)
ax.text(5.5, 6.8, '4× OA circuit', ha='center', fontsize=6, color='gray')

# Low-pass filter
box_circ(ax, 7.7, 7.5, 1.4, 0.85, 'LPF\nR=1kΩ C=160nF', fc='white', fs=7)
ax.text(7.7, 6.8, 'fc=1kHz', ha='center', fontsize=6, color='gray')

# Output
ax.text(9.3, 7.5, 'VIN\nCond', ha='center', va='center',
        fontsize=7, fontweight='bold')

# Wires
wire(ax, 1.85, 7.5, 2.5, 7.5)
wire(ax, 3.9, 7.5, 4.75, 7.5)
wire(ax, 6.25, 7.5, 7.0, 7.5)
wire(ax, 8.4, 7.5, 9.0, 7.5)

ax.text(2.1, 7.7, 'Vexc', ha='center', fontsize=6.5, style='italic')
ax.text(4.3, 7.7, 'Vac', ha='center', fontsize=6.5, style='italic')
ax.text(6.6, 7.7, 'Vdc', ha='center', fontsize=6.5, style='italic')

# Conductivity calibration
ax.text(5.0, 5.8,
        'Conductivity Conditioning:\n'
        '• Range: 0–2000 µS/cm\n'
        '• AC excitation: VAC=1Vpeak, f=1kHz\n'
        '• Vout = VAC × Rref / Rcell\n'
        '• Rref = 4.7 kΩ\n'
        '• Full-scale: 0→1.8V',
        ha='center', va='top', fontsize=7,
        bbox=dict(boxstyle='round', fc='#f8f8f8', ec='gray', lw=0.8))

ax.text(5.0, 2.9,
        'C_bypass=100nF anti-aliasing\n'
        'Electrode: SS304 plates, d=1mm',
        ha='center', va='top', fontsize=6.5, color='gray')

# ================================================================
# Panel 3: Temperature PTAT
# ================================================================
ax = axes[2]
ax.set_xlim(0, 10)
ax.set_ylim(0, 10)
ax.axis('off')
ax.set_title('Temperature Sensor\n(PTAT — Proportional to Abs. Temp.)',
             fontsize=10, fontweight='bold')

# PTAT core (diode pair)
box_circ(ax, 1.5, 7.5, 1.4, 1.0, 'PTAT Cell\nQ1/Q2 ×8',
         fc='#f0f0f0', fs=7)
ax.text(1.5, 6.7, 'ΔVBE ≈ 1.6mV/°C', ha='center', fontsize=6, color='gray')

# Current mirror
box_circ(ax, 3.6, 7.5, 1.3, 0.85, 'Current\nMirror', fc='white', fs=7)
ax.text(3.6, 6.8, 'Iptat=10µA@27°C', ha='center', fontsize=6, color='gray')

# V/I converter
box_circ(ax, 5.7, 7.5, 1.4, 0.85, 'I→V Conv.\nR=10kΩ', fc='white', fs=7)
ax.text(5.7, 6.8, 'V=IR', ha='center', fontsize=6, color='gray')

# Output buffer + level shift
box_circ(ax, 8.0, 7.5, 1.5, 0.85, 'Buffer+\nLevel Shift', fc='white', fs=7)
ax.text(8.0, 6.8, '−40..125°C\n→0..1.8V', ha='center', fontsize=6, color='gray')

ax.text(9.5, 7.5, 'VIN\nTemp', ha='center', va='center',
        fontsize=7, fontweight='bold')

# Wires
wire(ax, 2.2, 7.5, 2.95, 7.5)
wire(ax, 4.25, 7.5, 5.0, 7.5)
wire(ax, 6.4, 7.5, 7.25, 7.5)
wire(ax, 8.75, 7.5, 9.2, 7.5)

ax.text(2.6, 7.7, 'IPTAT', ha='center', fontsize=6.5, style='italic')
ax.text(4.6, 7.7, 'Imirr', ha='center', fontsize=6.5, style='italic')
ax.text(6.8, 7.7, 'Vptat', ha='center', fontsize=6.5, style='italic')

# VDD connection to PTAT
line(ax, 1.5, 8.0, 1.5, 8.6)
ax.text(1.5, 8.75, 'AVDD\n1.8V', ha='center', fontsize=6.5, color='gray')

# PTAT calibration
ax.text(5.0, 5.9,
        'PTAT Temperature Conditioning:\n'
        '• BJT pair (HBT-like in CMOS 180nm)\n'
        '• Sensitivity: 1.6 mV/°C\n'
        '• Range: −40..125°C → 0..265mV\n'
        '• After ×6.8 gain + offset: 0..1.8V\n'
        '• Nonlinearity < 0.5°C (corrected)',
        ha='center', va='top', fontsize=7,
        bbox=dict(boxstyle='round', fc='#f8f8f8', ec='gray', lw=0.8))

ax.text(5.0, 3.0,
        'Bandgap reference: 1.2V ±0.1%\n'
        'Used as bias for all 3 channels',
        ha='center', va='top', fontsize=6.5, color='gray')

plt.tight_layout(rect=[0, 0, 1, 0.92])
plt.savefig('fig_sensor_interface.png', dpi=150, bbox_inches='tight', facecolor='white')
print("Saved: fig_sensor_interface.png")
