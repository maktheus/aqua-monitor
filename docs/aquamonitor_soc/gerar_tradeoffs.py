"""
gerar_tradeoffs.py
3-panel tradeoff figure for AquaMonitorSoC v1.0
16x6 figure, black/white
"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

fig, axes = plt.subplots(1, 3, figsize=(16, 6))
fig.suptitle('AquaMonitorSoC v1.0 — Architecture Tradeoff Analysis',
             fontsize=13, fontweight='bold')

GRAY_SHADES = ['#cccccc', '#888888', '#444444']

# ================================================================
# Panel 1: Resolução vs Área de Die
# ================================================================
ax1 = axes[0]
bits  = ['4-bit\nSAR', '8-bit\nSAR', '12-bit\nSAR']
areas = [800, 2400, 8000]   # µm²
colors1 = GRAY_SHADES

bars1 = ax1.bar(bits, areas, color=colors1, edgecolor='black',
                linewidth=1.2, width=0.55)

# Value labels
for bar, val in zip(bars1, areas):
    ax1.text(bar.get_x() + bar.get_width()/2,
             bar.get_height() + 80,
             f'{val} µm²',
             ha='center', va='bottom', fontsize=9, fontweight='bold')

ax1.set_title('Resolução vs Área de Die', fontsize=11, fontweight='bold', pad=8)
ax1.set_ylabel('Área de Die (µm²)', fontsize=10)
ax1.set_xlabel('Arquitetura SAR ADC', fontsize=10)
ax1.set_ylim(0, 9500)
ax1.grid(axis='y', linestyle='--', alpha=0.5)
ax1.spines['top'].set_visible(False)
ax1.spines['right'].set_visible(False)

# Annotation: chosen design
ax1.annotate('Design atual\n(escolhido)',
             xy=(0, 800), xytext=(0.8, 3500),
             fontsize=8, style='italic', color='#333333',
             arrowprops=dict(arrowstyle='->', color='#333333', lw=1.2))

# ================================================================
# Panel 2: Número de Sensores vs Latência
# ================================================================
ax2 = axes[1]
sensors  = ['1 sensor', '3 sensores\n(este projeto)', '6 sensores']
latencia = [4, 12, 24]   # µs
colors2  = GRAY_SHADES

bars2 = ax2.bar(sensors, latencia, color=colors2, edgecolor='black',
                linewidth=1.2, width=0.55)

for bar, val in zip(bars2, latencia):
    ax2.text(bar.get_x() + bar.get_width()/2,
             bar.get_height() + 0.3,
             f'{val} µs',
             ha='center', va='bottom', fontsize=9, fontweight='bold')

ax2.set_title('Nº de Sensores vs Latência\nde Conversão (Time-Mux)',
              fontsize=11, fontweight='bold', pad=8)
ax2.set_ylabel('Latência total de conversão (µs)', fontsize=10)
ax2.set_xlabel('Número de canais sensoriais', fontsize=10)
ax2.set_ylim(0, 28)
ax2.grid(axis='y', linestyle='--', alpha=0.5)
ax2.spines['top'].set_visible(False)
ax2.spines['right'].set_visible(False)

# Formula annotation
ax2.text(0.5, 22, 'Latência = N × (8+2) ciclos @ 1MHz',
         ha='center', va='center', fontsize=8,
         style='italic', color='#444444',
         bbox=dict(boxstyle='round', fc='#f5f5f5', ec='gray', lw=0.8))

# ================================================================
# Panel 3: Radar chart — Comparação de Arquiteturas
# ================================================================
ax3 = axes[2]
ax3.set_aspect('equal')

categories = ['Área', 'Potência', 'Latência\n(menor=melhor)',
              'Flexib.', 'Custo\n(menor=melhor)']
N = len(categories)
angles = [n / float(N) * 2 * np.pi for n in range(N)]
angles += angles[:1]  # close polygon

# Scores (0–10, 10=best): Area, Power, Latency, Flexibility, Cost
# Higher = better for all axes (latency/cost are inverted: lower phys = higher score)
archs = {
    'FSM Dedicada\n(este projeto)': [9, 9, 7, 5, 9],  # small, low power, good latency
    'RISC-V Softcore':              [5, 6, 8, 9, 7],  # medium, flexible
    'ESP32 (SoC ext.)':             [2, 3, 5, 10, 4], # large power, max flex
}
line_styles = ['-', '--', ':']
markers     = ['o', 's', '^']

# Draw gridlines
for level in [2, 4, 6, 8, 10]:
    circle_vals = [level] * N + [level]
    ax3.plot(angles, circle_vals, 'k-', lw=0.4, alpha=0.3)
    ax3.text(0, level, str(level), ha='center', va='center',
             fontsize=6, color='gray')

# Draw axis lines
for i, angle in enumerate(angles[:-1]):
    ax3.plot([0, angle * 10], [0, 10], 'k-', lw=0.4, alpha=0.3,
             transform=ax3.transData)

# Actually use polar-like manual plotting
ax3_real = ax3
ax3_real.set_xlim(-12, 12)
ax3_real.set_ylim(-12, 12)
ax3_real.axis('off')
ax3_real.set_title('Comparação de Arquiteturas\n(Spider/Radar Chart)',
                   fontsize=11, fontweight='bold', pad=8)

# Manual radar chart
center = (0, 0)
R_max = 10

for level in [2, 4, 6, 8, 10]:
    pts = []
    for i in range(N):
        ang = angles[i]
        pts.append((level * np.cos(ang), level * np.sin(ang)))
    pts.append(pts[0])
    xs = [p[0] for p in pts]
    ys = [p[1] for p in pts]
    ax3_real.plot(xs, ys, 'k-', lw=0.5, alpha=0.25)

# Axis lines and labels
for i in range(N):
    ang = angles[i]
    ax3_real.plot([0, R_max * np.cos(ang)], [0, R_max * np.sin(ang)],
                  'k-', lw=0.6, alpha=0.4)
    lx = (R_max + 1.5) * np.cos(ang)
    ly = (R_max + 1.5) * np.sin(ang)
    ax3_real.text(lx, ly, categories[i], ha='center', va='center',
                  fontsize=8, fontweight='bold')

# Plot architectures
for idx, (name, scores) in enumerate(archs.items()):
    pts = []
    for i in range(N):
        ang = angles[i]
        r = scores[i]
        pts.append((r * np.cos(ang), r * np.sin(ang)))
    pts.append(pts[0])
    xs = [p[0] for p in pts]
    ys = [p[1] for p in pts]
    ax3_real.plot(xs, ys, line_styles[idx], lw=1.8,
                  label=name, color=['black', '#555555', '#999999'][idx],
                  marker=markers[idx], markersize=5)
    ax3_real.fill(xs, ys, alpha=0.07,
                  color=['black', '#555555', '#999999'][idx])

ax3_real.legend(loc='lower center', fontsize=7,
                bbox_to_anchor=(0.5, -0.18), ncol=1,
                framealpha=0.9)

# Scale note
ax3_real.text(0, -12.5, 'Escala: 0=pior → 10=melhor\n(Área/Potência/Custo: menor valor físico = maior pontuação)',
              ha='center', va='top', fontsize=6.5, color='gray', style='italic')

plt.tight_layout(rect=[0, 0, 1, 0.94])
plt.savefig('fig_tradeoffs.png', dpi=150, bbox_inches='tight', facecolor='white')
print("Saved: fig_tradeoffs.png")
