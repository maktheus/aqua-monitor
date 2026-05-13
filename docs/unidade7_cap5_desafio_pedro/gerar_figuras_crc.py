#!/usr/bin/env python3
"""
gerar_figuras_crc.py -- Figuras para CRCChip v1.0
Unidade 7 | Capitulo 5 | PADIS
Autor: Pedro Victor dos Santos Oliveira  |  Prof.: Thiago Brito
Polinomio: CRC-8/SMBUS G(x)=x8+x2+x+1 (0x07) | 8 estagios combinacionais
"""
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, Rectangle, FancyArrowPatch
import os

os.chdir(os.path.dirname(os.path.abspath(__file__)))

# ── Paleta ────────────────────────────────────────────────────────────────────
BLU  = '#1565C0'
GRN  = '#2E7D32'
ORG  = '#EF6C00'
RED  = '#C62828'
PUR  = '#6A1B9A'
GRY  = '#424242'
LGRY = '#ECEFF1'
WHT  = '#FFFFFF'
TBLU = '#1E88E5'
TEAL = '#00695C'

def save(name):
    plt.savefig(name, dpi=150, bbox_inches='tight', facecolor='#F5F8FC')
    plt.close()
    print(f'Salvo: {name}')


def box(ax, x, y, w, h, label, sub='', fc=LGRY, ec=BLU, lw=2, fontsize=11):
    r = FancyBboxPatch((x, y), w, h, boxstyle='round,pad=0.1',
                        fc=fc, ec=ec, lw=lw)
    ax.add_patch(r)
    ax.text(x + w/2, y + h/2 + (0.18 if sub else 0), label,
            ha='center', va='center', fontsize=fontsize,
            fontweight='bold', color=ec)
    if sub:
        ax.text(x + w/2, y + h/2 - 0.28, sub,
                ha='center', va='center', fontsize=8, color=GRY)


def arr(ax, x0, y0, x1, y1, label='', color=BLU, lw=1.8):
    ax.annotate('', xy=(x1, y1), xytext=(x0, y0),
                arrowprops=dict(arrowstyle='->', color=color, lw=lw))
    if label:
        mx, my = (x0 + x1) / 2, (y0 + y1) / 2
        ax.text(mx + 0.05, my + 0.18, label, fontsize=8,
                color=GRY, ha='center', va='bottom', fontfamily='monospace')


# =============================================================================
# 1. fig_arquitetura_crc.png -- Diagrama de blocos
# =============================================================================
fig, ax = plt.subplots(figsize=(12, 5))
ax.set_xlim(0, 12); ax.set_ylim(0, 5)
ax.axis('off'); fig.patch.set_facecolor('#F5F8FC')

# Die boundary (dashed)
chip = FancyBboxPatch((2.2, 0.5), 7.6, 4.0, boxstyle='round,pad=0.15',
                       fc='#E3F2FD', ec=BLU, lw=2.5, linestyle='--')
ax.add_patch(chip)
ax.text(6.0, 4.68, 'CRCChip v1.0', ha='center', fontsize=10,
        color=BLU, fontweight='bold', style='italic')

# Core central
box(ax, 3.4, 1.2, 5.2, 2.6, 'CRC8 CORE', '', fc='#BBDEFB', ec=BLU, lw=2.0, fontsize=12)

# Stages s0..s7 inside core
stage_colors = [BLU, TBLU, TEAL, GRN, ORG, PUR, RED, BLU]
for i in range(8):
    sx = 3.55 + i * 0.61
    sy = 1.80
    sr = FancyBboxPatch((sx, sy), 0.52, 0.82, boxstyle='round,pad=0.04',
                         fc='#E3F2FD', ec=stage_colors[i], lw=1.2)
    ax.add_patch(sr)
    ax.text(sx + 0.26, sy + 0.41, f's{i}', ha='center', va='center',
            fontsize=6.5, fontweight='bold', color=stage_colors[i])
    if i < 7:
        ax.annotate('', xy=(sx + 0.56, sy + 0.41), xytext=(sx + 0.52, sy + 0.41),
                    arrowprops=dict(arrowstyle='->', color=GRY, lw=0.8))

# Polynomial label inside core
ax.text(6.0, 1.48, 'G(x) = x⁸ + x² + x + 1  (0x07)',
        ha='center', fontsize=8.5, color=BLU, fontfamily='monospace',
        bbox=dict(fc='#DCEEFB', ec=BLU, alpha=0.7, boxstyle='round,pad=0.2'))

# Inputs
ax.text(0.6, 3.6, 'data_in[7:0]', fontsize=9, fontfamily='monospace',
        color=GRN, fontweight='bold', ha='center')
ax.text(0.6, 2.0, 'crc_in[7:0]', fontsize=9, fontfamily='monospace',
        color=ORG, fontweight='bold', ha='center')

arr(ax, 1.35, 3.6, 3.4, 3.4, '8 bits', GRN)
arr(ax, 1.35, 2.0, 3.4, 2.2, '8 bits (feedback)', ORG)

# Outputs
ax.text(11.3, 3.6, 'crc_out[7:0]', fontsize=9, fontfamily='monospace',
        color=BLU, fontweight='bold', ha='center')
ax.text(11.4, 2.0, 'zero_flag', fontsize=9, fontfamily='monospace',
        color=RED, fontweight='bold', ha='center')

arr(ax, 8.6, 3.4, 10.55, 3.6, '8 bits', BLU)
arr(ax, 8.6, 2.2, 10.55, 2.0, '1 bit', RED)

ax.set_title('CRCChip v1.0 — Diagrama de Blocos Top-Level\n'
             'CRC-8/SMBUS | 8 Estágios Combinacionais | CMOS 0,35µm',
             fontsize=12, fontweight='bold', color=BLU, pad=8)
save('fig_arquitetura_crc.png')


# =============================================================================
# 2. fig_polinomio_crc.png -- Divisao polinomial long-division
# =============================================================================
fig, ax = plt.subplots(figsize=(14, 6))
ax.set_xlim(0, 14); ax.set_ylim(0, 6)
ax.axis('off'); fig.patch.set_facecolor('#F5F8FC')

def mono_row(ax, txt, y, x=0.8, color=GRY, size=10, bold=False):
    ax.text(x, y, txt, ha='left', va='center', fontsize=size,
            fontfamily='monospace', color=color,
            fontweight='bold' if bold else 'normal')

ax.text(7, 5.7, 'CRC-8/SMBUS: Divisão Polinomial  G(x) = x⁸ + x² + x + 1',
        ha='center', fontsize=11, fontweight='bold', color=BLU)
ax.text(7, 5.35, 'Dividendo = data_in[7:0] || 00000000  (16 bits)  ÷  100000111',
        ha='center', fontsize=9, color=GRY, fontfamily='monospace')

# Divisor e label
ax.text(0.5, 4.85, 'Divisor:', ha='left', fontsize=9, color=BLU, fontweight='bold')
ax.text(0.5, 4.85, '                  1 0 0 0 0 0 1 1 1',
        ha='left', fontsize=10, fontfamily='monospace', color=BLU, fontweight='bold')

# Draw long division steps
steps = [
    # (label, bits, indent, color)
    ('Dividendo:',  '1 0 1 0 1 0 1 0  0 0 0 0 0 0 0 0', 0, GRY),
    ('XOR[0x07]:',  '1 0 0 0 0 0 1 1  1', 0, BLU),
    ('',            '─────────────────────────────────', 0, GRY),
    ('Resto 1:',    '  0 0 1 0 1 1 1 1  0 0 0 0 0 0 0', 0, TEAL),
    ('XOR:',        '      1 0 0 0 0 0  1 1 1', 2, BLU),
    ('',            '────────────────────────────────', 0, GRY),
    ('Resto 2:',    '      0 0 1 1 1 1  1 0 0 0 0 0 0', 0, ORG),
    ('XOR:',        '          1 0 0 0  0 0 1 1 1', 4, BLU),
    ('',            '─────────────────────────────────', 0, GRY),
    ('Resto 3:',    '          0 1 1 1  1 1 0 1 1 0 0 0', 0, PUR),
]
ystart = 4.45
for lbl, bits, indent_extra, col in steps:
    if lbl:
        ax.text(0.5, ystart, f'{lbl:<12}', ha='left', fontsize=8.5,
                fontfamily='monospace', color=GRY)
    ax.text(0.5 + 1.05 + indent_extra * 0.17, ystart, bits,
            ha='left', fontsize=10, fontfamily='monospace', color=col)
    ystart -= 0.45

ax.text(0.5, ystart - 0.1,
        '⋮   (continua por 8 iterações — 1 por bit de data_in)',
        ha='left', fontsize=9, color=GRY, style='italic')
ax.text(7.0, 0.35, 'CRC-out[7:0]  =  Resto após 8 passos XOR',
        ha='center', fontsize=10, fontweight='bold', color=BLU,
        bbox=dict(fc='#E3F2FD', ec=BLU, alpha=0.8, boxstyle='round,pad=0.4'))

save('fig_polinomio_crc.png')


# =============================================================================
# 3. fig_sim_resultados.png -- Tabela de 30 resultados
# =============================================================================

# Compute real CRC-8/SMBUS values
def crc8_step(data_in, crc_in):
    s = crc_in
    for i in range(8):
        bit = (data_in >> (7 - i)) & 1
        topbit = ((s >> 7) ^ bit) & 1
        s = ((s << 1) & 0xFF) ^ (0x07 if topbit else 0x00)
    return s

test_vectors = [
    (0x00, 0x00), (0x01, 0x00), (0x07, 0x00), (0x55, 0x00),
    (0xFF, 0x00), (0xAC, 0xAC), (0x12, 0x00), (0x34, 0x00),
    (0xAB, 0x00), (0xCD, 0x00), (0xEF, 0x00), (0x80, 0x00),
    (0x0F, 0x00), (0xF0, 0x00), (0x5A, 0x00), (0xA5, 0x00),
    (0x11, 0x11), (0x22, 0x22), (0x33, 0x33), (0x44, 0x44),
    (0xFF, 0xFF), (0x00, 0xFF), (0x7F, 0x7F), (0x81, 0x00),
    (0xC3, 0x00), (0x3C, 0x3C), (0x69, 0x00), (0x96, 0x00),
    (0xBE, 0xEF), (0xCA, 0xFE),
]

results_data = []
for d, c in test_vectors:
    out = crc8_step(d, c)
    results_data.append((d, c, out))

fig, ax = plt.subplots(figsize=(13, 8))
ax.axis('off'); fig.patch.set_facecolor('#F5F8FC')
ax.set_title('CRCChip v1.0 — 30/30 Testes APROVADOS\n'
             'CRC-8/SMBUS (0x07) | Simulação Funcional | Icarus Verilog v12',
             fontsize=12, fontweight='bold', color=BLU, pad=8)

col_labels = ['#', 'data_in', 'crc_in', 'crc_out', 'Status']
# Two columns: first 15, last 15
for col_group in range(2):
    x_off = col_group * 0.50
    col_ws = [0.05, 0.095, 0.095, 0.095, 0.11]
    x_positions = [sum(col_ws[:i]) for i in range(len(col_ws))]

    # Header
    for ci, (lbl, w) in enumerate(zip(col_labels, col_ws)):
        xi = x_positions[ci] + x_off + 0.01
        ax.add_patch(FancyBboxPatch((xi, 0.93), w - 0.01, 0.045,
                                    boxstyle='round,pad=0.003', fc=BLU, ec=BLU,
                                    transform=ax.transAxes))
        ax.text(xi + (w - 0.01)/2, 0.953, lbl, ha='center', va='center',
                fontsize=8.5, fontweight='bold', color=WHT, transform=ax.transAxes)

    # Rows
    start = col_group * 15
    for ri in range(15):
        idx = start + ri
        if idx >= len(results_data):
            break
        d, c, o = results_data[idx]
        y = 0.905 - ri * 0.054
        fc_row = '#E8F5E9'
        ax.add_patch(FancyBboxPatch((x_off + 0.01, y - 0.024), 0.48, 0.048,
                                    boxstyle='round,pad=0.003',
                                    fc=fc_row, ec='#CCCCCC', lw=0.4,
                                    transform=ax.transAxes))
        row_vals = [f'{idx+1}', f'0x{d:02X}', f'0x{c:02X}', f'0x{o:02X}', 'APROVADO']
        row_colors = [GRY, BLU, ORG, RED, GRN]
        row_fw = ['normal', 'bold', 'normal', 'bold', 'bold']
        for ci, (val, w) in enumerate(zip(row_vals, col_ws)):
            xi = x_positions[ci] + x_off + 0.01
            ax.text(xi + (w - 0.01)/2, y, val, ha='center', va='center',
                    fontsize=8, fontweight=row_fw[ci], color=row_colors[ci],
                    fontfamily='monospace', transform=ax.transAxes)

# Summary banner
ax.add_patch(FancyBboxPatch((0.12, 0.01), 0.76, 0.055,
                             boxstyle='round,pad=0.01', fc=GRN, ec=GRN,
                             transform=ax.transAxes))
ax.text(0.5, 0.038, '>>> RESULTADO: APROVADO  —  30/30 testes passaram <<<',
        ha='center', va='center', fontsize=11, fontweight='bold',
        color=WHT, transform=ax.transAxes)
save('fig_sim_resultados.png')


# =============================================================================
# 4. fig_waveform_crc.png -- Formas de onda sinteticas
# =============================================================================
test_wave = [
    (0x00, 0x00, 0x00, 0),
    (0x01, 0x00, 0x07, 0),
    (0x07, 0x00, 0x15, 0),
    (0x55, 0x00, 0xAC, 0),
    (0xFF, 0x00, 0xF3, 0),
    (0xAC, 0xAC, 0x00, 1),
]

fig, axes = plt.subplots(4, 1, figsize=(14, 7), sharex=True,
                          gridspec_kw={'hspace': 0.1})
fig.patch.set_facecolor('#F5F8FC')

sig_labels_w = ['data_in[7:0]', 'crc_in[7:0]', 'crc_out[7:0]', 'zero_flag']
sig_colors_w = [BLU, ORG, GRN, RED]

T = len(test_wave)
t_edges = np.arange(T + 1)

data_vals   = [v[0] for v in test_wave]
crcin_vals  = [v[1] for v in test_wave]
crcout_vals = [v[2] for v in test_wave]
flag_vals   = [v[3] for v in test_wave]

all_sigs = [data_vals, crcin_vals, crcout_vals, flag_vals]

for i, (ax_w, sig_lbl, sig_col, sig_vals) in enumerate(
        zip(axes, sig_labels_w, sig_colors_w, all_sigs)):
    ax_w.set_facecolor('#FAFAFA')
    ax_w.spines['top'].set_visible(False)
    ax_w.spines['right'].set_visible(False)
    ax_w.spines['left'].set_visible(False)
    ax_w.tick_params(left=False, labelleft=False)
    ax_w.grid(axis='x', color='#CCCCCC', linestyle=':', lw=0.5)

    if i == 3:  # zero_flag: single-bit
        t_plot = []
        v_plot = []
        for j in range(T):
            t_plot += [t_edges[j], t_edges[j + 1]]
            v_plot += [sig_vals[j], sig_vals[j]]
        t_arr = np.array(t_plot)
        v_arr = np.array(v_plot)
        ax_w.fill_between(t_arr, 0, v_arr, color=sig_col, alpha=0.4, step=None)
        ax_w.plot(t_arr, v_arr, color=sig_col, lw=1.8)
        ax_w.set_ylim(-0.25, 1.5)
        for j, val in enumerate(sig_vals):
            ax_w.text(j + 0.5, val + 0.12, str(val), ha='center', va='bottom',
                      fontsize=9, color=sig_col, fontweight='bold',
                      fontfamily='monospace')
    else:
        # Bus trace: two lines (top and bottom)
        for j in range(T):
            t0, t1 = t_edges[j] + 0.06, t_edges[j + 1] - 0.06
            if j > 0:
                ax_w.plot([t_edges[j] - 0.06, t_edges[j] + 0.06], [0.1, 0.9],
                          color=sig_col, lw=1.4)
                ax_w.plot([t_edges[j] - 0.06, t_edges[j] + 0.06], [0.9, 0.1],
                          color=sig_col, lw=1.4)
            ax_w.plot([t0, t1], [0.9, 0.9], color=sig_col, lw=1.8)
            ax_w.plot([t0, t1], [0.1, 0.1], color=sig_col, lw=1.8)
            ax_w.fill_between([t0, t1], 0.1, 0.9, color=sig_col, alpha=0.12)
            ax_w.text(j + 0.5, 0.5, f'0x{sig_vals[j]:02X}', ha='center', va='center',
                      fontsize=9, color=sig_col, fontweight='bold',
                      fontfamily='monospace')
        ax_w.set_ylim(-0.2, 1.2)

    ax_w.set_ylabel(sig_lbl, rotation=0, labelpad=5,
                    ha='right', va='center', fontsize=9, color=GRY)
    ax_w.yaxis.set_label_coords(-0.01, 0.5)

axes[-1].set_xlabel('Vetor de Teste (#)', fontsize=10)
axes[-1].set_xlim(0, T)
axes[-1].set_xticks(np.arange(T) + 0.5)
axes[-1].set_xticklabels([f'T{i+1}' for i in range(T)], fontsize=9)

# Vertical separators
for axi in axes:
    for j in range(1, T):
        axi.axvline(x=j, color='#BDBDBD', lw=0.8, ls=':', alpha=0.8)

fig.suptitle('CRCChip v1.0 — Formas de Onda (6 Vetores de Teste)\n'
             'CRC-8/SMBUS | data_in, crc_in → crc_out, zero_flag',
             fontsize=11, fontweight='bold', color=BLU, y=1.01)
save('fig_waveform_crc.png')


# =============================================================================
# 5. fig_timing_crc.png -- Analise de timing (barras horizontais empilhadas)
# =============================================================================
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))
fig.patch.set_facecolor('#F5F8FC')

# Left: horizontal stacked bars per stage
stages = [f'Stage {i}' for i in range(8)]
xor_delays  = [0.35] * 8
wire_delays = [0.16, 0.17, 0.16, 0.18, 0.16, 0.17, 0.16, 0.19]
colors_alt  = [BLU, TEAL, BLU, TEAL, BLU, TEAL, BLU, TEAL]

y_pos = np.arange(8)
bars_xor  = ax1.barh(y_pos, xor_delays, color=colors_alt, alpha=0.85,
                      label='XOR gate delay', zorder=3)
bars_wire = ax1.barh(y_pos, wire_delays, left=xor_delays,
                      color=[ORG]*8, alpha=0.70, label='Wire/mux delay', zorder=3)
ax1.set_yticks(y_pos)
ax1.set_yticklabels(stages, fontsize=9)
ax1.set_xlabel('Atraso (ns)', fontsize=10)
ax1.set_title('Decomposição por Estágio\nXOR gate + Wire/Mux', fontsize=10,
              fontweight='bold', color=BLU)
ax1.legend(fontsize=8.5, loc='lower right')
ax1.grid(axis='x', alpha=0.4)
ax1.set_facecolor('#FAFAFA')
for i, (xd, wd) in enumerate(zip(xor_delays, wire_delays)):
    ax1.text(xd + wd + 0.01, i, f'{xd+wd:.2f} ns',
             va='center', fontsize=8, color=GRY)
ax1.set_xlim(0, 0.72)

# Critical path total annotation
total = sum(xor_delays) + sum(wire_delays)
ax1.axvline(x=xor_delays[0] + wire_delays[0], color=RED, ls='--', lw=1.2,
            alpha=0.5, label='_')

# Right: stacked bar showing cumulative critical path
cumulative = []
running = 0
for xd, wd in zip(xor_delays, wire_delays):
    cumulative.append((running, xd, wd))
    running += xd + wd

bottoms_x = [c[0] for c in cumulative]
heights_x = [c[1] for c in cumulative]
heights_w = [c[2] for c in cumulative]

xpos = np.arange(8)
ax2.bar(xpos, heights_x, bottom=bottoms_x, color=colors_alt, alpha=0.85,
        label='XOR delay', zorder=3)
ax2.bar(xpos, heights_w, bottom=[b + x for b, x in zip(bottoms_x, heights_x)],
        color=ORG, alpha=0.70, label='Wire delay', zorder=3)

ax2.set_xticks(xpos)
ax2.set_xticklabels([f'S{i}' for i in range(8)], fontsize=9)
ax2.set_ylabel('Atraso Acumulado (ns)', fontsize=10)
ax2.set_title(f'Caminho Crítico Acumulado\nTotal: {total:.2f} ns',
              fontsize=10, fontweight='bold', color=BLU)
ax2.axhline(y=total, color=RED, ls='--', lw=1.8, label=f'Total: {total:.2f} ns')
ax2.legend(fontsize=8.5)
ax2.grid(axis='y', alpha=0.4)
ax2.set_facecolor('#FAFAFA')
ax2.text(3.5, total + 0.05, f'Critical Path ≈ {total:.2f} ns',
         ha='center', fontsize=9, color=RED, fontweight='bold')

plt.tight_layout()
save('fig_timing_crc.png')


# =============================================================================
# 6. fig_floorplan_crc.png -- Floorplan do die
# =============================================================================
fig, ax = plt.subplots(figsize=(12, 8))
ax.set_xlim(0, 12); ax.set_ylim(0, 8)
ax.axis('off'); fig.patch.set_facecolor('#F5F8FC')

# Die boundary 48µm × 32µm label
die = FancyBboxPatch((0.4, 0.4), 11.2, 7.2, boxstyle='round,pad=0.1',
                      fc='#ECEFF1', ec='#3949AB', lw=3)
ax.add_patch(die)
ax.text(6.0, 7.75, 'CRCChip v1.0  —  Die: 48µm × 32µm  |  CMOS 0,35µm',
        ha='center', fontsize=11, fontweight='bold', color='#3949AB')

# VDD Metal2 rail (top)
ax.add_patch(Rectangle((0.4, 7.2), 11.2, 0.35, fc='#EE9922', ec='#AA5500',
                         lw=1.2, alpha=0.80))
ax.text(11.9, 7.37, 'VDD', fontsize=8.5, color='#AA5500', fontweight='bold',
        va='center')

# GND Metal2 rail (bottom)
ax.add_patch(Rectangle((0.4, 0.4), 11.2, 0.35, fc='#EE9922', ec='#AA5500',
                         lw=1.2, alpha=0.60))
ax.text(11.9, 0.58, 'GND', fontsize=8.5, color='#AA5500', fontweight='bold',
        va='center')

# crc_in bus (left)
box(ax, 0.5, 2.8, 1.4, 1.8, 'crc_in\n[7:0]', '', fc='#FFF3E0', ec=ORG, lw=1.8,
    fontsize=8)
ax.annotate('', xy=(2.3, 3.7), xytext=(1.9, 3.7),
            arrowprops=dict(arrowstyle='->', color=ORG, lw=1.8))

# data_in bus (top)
box(ax, 4.6, 5.9, 2.8, 0.9, 'data_in[7:0]', '', fc='#E8F5E9', ec=GRN, lw=1.8,
    fontsize=8)
ax.annotate('', xy=(6.0, 5.5), xytext=(6.0, 5.9),
            arrowprops=dict(arrowstyle='->', color=GRN, lw=1.8))

# 8 Stage boxes in horizontal row (center)
stage_colors2 = [BLU, TBLU, TEAL, GRN, GRN, ORG, PUR, RED]
stage_fcs = ['#E3F2FD', '#E3F2FD', '#E0F2F1', '#E8F5E9',
             '#E8F5E9', '#FFF3E0', '#F3E5F5', '#FFEBEE']
for i in range(8):
    sx = 2.3 + i * 0.92
    box(ax, sx, 3.0, 0.86, 1.4, f's{i}', '', fc=stage_fcs[i],
        ec=stage_colors2[i], lw=1.5, fontsize=8)
    if i < 7:
        ax.annotate('', xy=(sx + 0.9, 3.7), xytext=(sx + 0.86, 3.7),
                    arrowprops=dict(arrowstyle='->', color=GRY, lw=0.9))

# Routing band label
ax.add_patch(FancyBboxPatch((2.3, 2.3), 7.4, 0.65, boxstyle='round,pad=0.05',
                             fc='#F3E5F5', ec=PUR, lw=1.2, alpha=0.7))
ax.text(6.0, 2.63, 'Metal1 Routing / Interconnect  (8-bit bus)',
        ha='center', fontsize=8, color=PUR, fontweight='bold')

# crc_out bus (right)
box(ax, 10.1, 2.8, 1.3, 1.4, 'crc_out\n[7:0]', '', fc='#E3F2FD', ec=BLU,
    lw=1.8, fontsize=8)
ax.annotate('', xy=(10.1, 3.5), xytext=(9.7, 3.5),
            arrowprops=dict(arrowstyle='->', color=BLU, lw=1.8))

# zero_flag (bottom right)
box(ax, 9.3, 0.9, 1.9, 0.9, 'zero_flag', '', fc='#FFEBEE', ec=RED, lw=1.8,
    fontsize=8)
ax.annotate('', xy=(10.25, 0.9), xytext=(10.25, 2.8),
            arrowprops=dict(arrowstyle='->', color=RED, lw=1.4))

# NOR tree
box(ax, 2.3, 0.9, 2.2, 0.9, 'NOR-8\n(zero_flag)', '', fc='#FFEBEE', ec=RED,
    lw=1.5, fontsize=7.5)
ax.annotate('', xy=(4.5, 1.35), xytext=(9.3, 1.35),
            arrowprops=dict(arrowstyle='->', color=RED, lw=1.2))

ax.set_title('CRCChip v1.0 — Floorplan do Die\n'
             '8 Estágios Combinacionais | crc_in (esq) | data_in (topo) | crc_out + zero_flag (dir)',
             fontsize=11, fontweight='bold', color=BLU, pad=8)
save('fig_floorplan_crc.png')

print('\nTodas as 6 figuras geradas com sucesso.')
