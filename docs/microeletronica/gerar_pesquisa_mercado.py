"""
Gera fig_mercado.png: 3-panel market research figure for AquaMonitor report.
"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

# ── Paleta aqua/blue ───────────────────────────────────────────────────────────
AQUA   = '#007F8C'
BLUE1  = '#005F8C'
BLUE2  = '#3399CC'
BLUE3  = '#66B8D4'
BLUE4  = '#99D0E0'
GRAY   = '#B0C4C8'
PROJ   = '#FF6B35'   # destaque para a solução proposta

fig, axes = plt.subplots(1, 3, figsize=(12, 7))
fig.patch.set_facecolor('#F0F8FF')

# ══════════════════════════════════════════════════════════════════════════════
# PAINEL 1 — Mercado de Aquicultura Brasil (R$ bilhões)
# ══════════════════════════════════════════════════════════════════════════════
ax1 = axes[0]
anos   = [2020, 2021, 2022, 2023, 2024, 2025, 2026]
valores = [9.2, 10.1, 11.3, 12.0, 12.8, 13.7, 14.6]
cores_bar = [BLUE2]*6 + [PROJ]   # 2026 = projetado

bars = ax1.bar(anos, valores, color=cores_bar, edgecolor='white', linewidth=0.8, width=0.7)
ax1.set_title('Mercado de Aquicultura\nBrasil (R\$ bilhões)', fontsize=11,
              fontweight='bold', color=BLUE1, pad=10)
ax1.set_xlabel('Ano', fontsize=9, color='#333333')
ax1.set_ylabel('R\$ bilhões', fontsize=9, color='#333333')
ax1.set_ylim(0, 17)
ax1.set_xticks(anos)
ax1.set_xticklabels([str(a) for a in anos], fontsize=8, rotation=30)
ax1.tick_params(axis='y', labelsize=8)
ax1.set_facecolor('#F8FDFF')
ax1.spines['top'].set_visible(False)
ax1.spines['right'].set_visible(False)
ax1.spines['left'].set_color('#AAAAAA')
ax1.spines['bottom'].set_color('#AAAAAA')
ax1.yaxis.grid(True, linestyle='--', alpha=0.4, color='#AAAAAA')
ax1.set_axisbelow(True)

for bar, val in zip(bars, valores):
    ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.2,
             f'{val:.1f}', ha='center', va='bottom', fontsize=7.5,
             fontweight='bold', color=BLUE1)

# Anotação "projetado"
ax1.annotate('Projetado', xy=(2026, 14.6), xytext=(2024.8, 15.6),
             fontsize=7.5, color=PROJ, fontweight='bold',
             arrowprops=dict(arrowstyle='->', color=PROJ, lw=1.2))

# ══════════════════════════════════════════════════════════════════════════════
# PAINEL 2 — Soluções de Monitoramento de Qualidade da Água (pizza)
# ══════════════════════════════════════════════════════════════════════════════
ax2 = axes[1]
labels = [
    'Manual/\nLaboratorial',
    'Sistemas\nComerciais\n(>R\$8k)',
    'DIY/\nArduino',
    'CI Customizado\n(proposto)',
]
sizes  = [45, 30, 18, 7]
cores_pie = [BLUE2, BLUE3, GRAY, PROJ]
explode = (0, 0, 0, 0.12)

wedges, texts, autotexts = ax2.pie(
    sizes, labels=labels, colors=cores_pie, autopct='%1.0f%%',
    startangle=120, explode=explode,
    textprops={'fontsize': 8},
    wedgeprops={'edgecolor': 'white', 'linewidth': 1.5},
    pctdistance=0.75,
)
for at in autotexts:
    at.set_fontsize(8.5)
    at.set_fontweight('bold')
    at.set_color('white')
autotexts[-1].set_color('#333333')

ax2.set_title('Soluções de Monitoramento\nde Qualidade da Água', fontsize=11,
              fontweight='bold', color=BLUE1, pad=10)
ax2.set_facecolor('#F8FDFF')

# ══════════════════════════════════════════════════════════════════════════════
# PAINEL 3 — Custo por Unidade (barras horizontais)
# ══════════════════════════════════════════════════════════════════════════════
ax3 = axes[2]
items  = [
    'Módulo ADC\ncomercial',
    'ADC discreto\n+ opamp',
    'MCU c/ ADC\nintegrado',
    'CI customizado\n(escala)',
]
custos = [85, 28, 18, 4]
cores_h = [BLUE2, BLUE2, BLUE2, PROJ]

y_pos = np.arange(len(items))
hbars = ax3.barh(y_pos, custos, color=cores_h, edgecolor='white',
                 linewidth=0.8, height=0.6)

ax3.set_yticks(y_pos)
ax3.set_yticklabels(items, fontsize=8.5)
ax3.set_xlabel('Custo por unidade (R\$)', fontsize=9, color='#333333')
ax3.set_title('Custo por Unidade —\nSolução de ADC', fontsize=11,
              fontweight='bold', color=BLUE1, pad=10)
ax3.set_xlim(0, 100)
ax3.set_facecolor('#F8FDFF')
ax3.spines['top'].set_visible(False)
ax3.spines['right'].set_visible(False)
ax3.spines['left'].set_color('#AAAAAA')
ax3.spines['bottom'].set_color('#AAAAAA')
ax3.xaxis.grid(True, linestyle='--', alpha=0.4, color='#AAAAAA')
ax3.set_axisbelow(True)
ax3.tick_params(axis='x', labelsize=8)

for bar, val in zip(hbars, custos):
    ax3.text(bar.get_width() + 1.2, bar.get_y() + bar.get_height()/2,
             f'R\${val}', va='center', ha='left', fontsize=9,
             fontweight='bold', color=BLUE1 if val > 4 else PROJ)

# Legenda de destaque
proj_patch = mpatches.Patch(color=PROJ, label='Solução proposta (AquaMonitor)')
fig.legend(handles=[proj_patch], loc='lower center', fontsize=8.5,
           framealpha=0.9, edgecolor=GRAY, ncol=1, bbox_to_anchor=(0.5, 0.01))

fig.suptitle('Pesquisa de Mercado — Projeto AquaMonitor',
             fontsize=13, fontweight='bold', color=BLUE1, y=0.98)

plt.tight_layout(rect=[0, 0.06, 1, 0.96])
plt.savefig('fig_mercado.png', dpi=150, bbox_inches='tight',
            facecolor=fig.get_facecolor())
print('fig_mercado.png saved successfully.')
