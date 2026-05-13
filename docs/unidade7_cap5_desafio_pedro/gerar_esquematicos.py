#!/usr/bin/env python3
"""
gerar_esquematicos.py  --  Esquematicos para CRCChip v1.0
Unidade 7 | Capitulo 5 | PADIS
Autor: Pedro Victor dos Santos Oliveira  |  Prof.: Thiago Brito
"""
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, Arc, FancyArrowPatch
from matplotlib.path import Path
import os

os.chdir(os.path.dirname(os.path.abspath(__file__)))

# ─── Paleta ──────────────────────────────────────────────────────────────────
BLU  = '#1565C0'; GRN  = '#2E7D32'; ORG  = '#EF6C00'
RED  = '#C62828'; PUR  = '#6A1B9A'; GRY  = '#424242'
LGRY = '#ECEFF1'; WHT  = '#FFFFFF'; TEAL = '#00695C'
TBLU = '#1E88E5'

LW = 1.8  # espessura padrao das linhas

# ─── Primitivas de wire / dot / label ────────────────────────────────────────

def wire(ax, x0, y0, x1, y1, color=GRY, lw=LW):
    ax.plot([x0, x1], [y0, y1], color=color, lw=lw, solid_capstyle='round')

def wire_h(ax, x0, x1, y, **kw):
    wire(ax, x0, y, x1, y, **kw)

def wire_v(ax, x, y0, y1, **kw):
    wire(ax, x, y0, x, y1, **kw)

def dot(ax, x, y, color=GRY, r=0.04):
    ax.add_patch(plt.Circle((x, y), r, color=color, zorder=5))

def lbl(ax, x, y, txt, ha='center', va='center', color=GRY, size=9, bold=False):
    ax.text(x, y, txt, ha=ha, va=va, color=color,
            fontsize=size, fontweight='bold' if bold else 'normal',
            fontfamily='monospace')

def bubble(ax, x, y, r=0.1, color=GRY):
    ax.add_patch(plt.Circle((x, y), r, ec=color, fc=WHT, lw=LW, zorder=4))

# ─── Simbolos de portas logicas (IEEE 91/ANSI) ───────────────────────────────

def gate_and(ax, cx, cy, w=0.8, h=0.6, color=BLU, lbl_txt='&'):
    ax.plot([cx - w/2, cx, cx],
            [cy - h/2, cy - h/2, cy + h/2],
            color=color, lw=LW, solid_capstyle='round')
    ax.plot([cx - w/2, cx - w/2], [cy - h/2, cy + h/2], color=color, lw=LW)
    ax.plot([cx - w/2, cx], [cy + h/2, cy + h/2], color=color, lw=LW)
    theta = np.linspace(-np.pi/2, np.pi/2, 60)
    ax.plot(cx + h/2 * np.sin(theta), cy + h/2 * np.cos(theta),
            color=color, lw=LW)
    ax.text(cx - 0.05, cy, lbl_txt, ha='center', va='center',
            fontsize=8, color=color, fontweight='bold')
    return cx + h/2, cy

def gate_or(ax, cx, cy, w=0.8, h=0.6, color=GRN, lbl_txt='≥1'):
    t = np.linspace(-np.pi/2, np.pi/2, 60)
    back_r = 0.25
    ax.plot(cx - w/2 + back_r * (1 - np.cos(t)), cy + (h/2) * np.sin(t),
            color=color, lw=LW)
    ts = np.linspace(0, np.pi/2, 40)
    ax.plot(cx - w/2 + (w + h/2) * np.sin(ts)**1.4,
            cy + h/2 * np.cos(ts)**0.5, color=color, lw=LW)
    ax.plot(cx - w/2 + (w + h/2) * np.sin(ts)**1.4,
            cy - h/2 * np.cos(ts)**0.5, color=color, lw=LW)
    ax.text(cx, cy, lbl_txt, ha='center', va='center',
            fontsize=8, color=color, fontweight='bold')
    return cx + w * 0.85 + h/2 * 0.15, cy

def gate_xor(ax, cx, cy, w=0.8, h=0.6, color=ORG, lbl_txt='=1'):
    x_out, y_out = gate_or(ax, cx, cy, w, h, color=color, lbl=lbl_txt)
    t = np.linspace(-np.pi/2, np.pi/2, 60)
    back_r = 0.25
    off = -0.18
    ax.plot(cx - w/2 + off + back_r * (1 - np.cos(t)),
            cy + (h/2) * np.sin(t), color=color, lw=LW)
    return x_out, y_out

# patch: gate_or lbl kwarg issue
def gate_or(ax, cx, cy, w=0.8, h=0.6, color=GRN, lbl=None):
    lbl_txt = lbl if lbl is not None else '≥1'
    t = np.linspace(-np.pi/2, np.pi/2, 60)
    back_r = 0.25
    ax.plot(cx - w/2 + back_r * (1 - np.cos(t)), cy + (h/2) * np.sin(t),
            color=color, lw=LW)
    ts = np.linspace(0, np.pi/2, 40)
    ax.plot(cx - w/2 + (w + h/2) * np.sin(ts)**1.4,
            cy + h/2 * np.cos(ts)**0.5, color=color, lw=LW)
    ax.plot(cx - w/2 + (w + h/2) * np.sin(ts)**1.4,
            cy - h/2 * np.cos(ts)**0.5, color=color, lw=LW)
    ax.text(cx, cy, lbl_txt, ha='center', va='center',
            fontsize=8, color=color, fontweight='bold')
    return cx + w * 0.85 + h/2 * 0.15, cy

def gate_xor(ax, cx, cy, w=0.8, h=0.6, color=ORG, lbl_txt='=1'):
    x_out, y_out = gate_or(ax, cx, cy, w, h, color=color, lbl=lbl_txt)
    t = np.linspace(-np.pi/2, np.pi/2, 60)
    back_r = 0.25
    off = -0.18
    ax.plot(cx - w/2 + off + back_r * (1 - np.cos(t)),
            cy + (h/2) * np.sin(t), color=color, lw=LW)
    return x_out, y_out

def gate_not(ax, cx, cy, w=0.5, h=0.45, color=RED, lbl_txt='1'):
    ax.plot([cx - w/2, cx - w/2, cx + w/2 - h/4],
            [cy - h/2, cy + h/2, cy],
            color=color, lw=LW, solid_capstyle='round')
    ax.plot([cx - w/2, cx + w/2 - h/4],
            [cy - h/2, cy],
            color=color, lw=LW, solid_capstyle='round')
    ax.text(cx - 0.05, cy, lbl_txt, ha='center', va='center',
            fontsize=8, color=color, fontweight='bold')
    bubble(ax, cx + w/2 - h/4 + 0.1, cy, r=0.09, color=color)
    return cx + w/2 + 0.1, cy


# =============================================================================
# fig_schem_stage.png -- Estagio unico CRC-8
# =============================================================================
def fig_schem_stage():
    fig, ax = plt.subplots(figsize=(13, 8))
    ax.set_xlim(-0.5, 13); ax.set_ylim(-0.5, 8)
    ax.axis('off'); fig.patch.set_facecolor('#F5F8FC')

    # ── prev[7:0] bus input ──
    ax.add_patch(FancyBboxPatch((0.2, 3.0), 1.6, 2.0,
                                 boxstyle='round,pad=0.1',
                                 fc='#E3F2FD', ec=BLU, lw=1.8))
    ax.text(1.0, 4.0, 'prev[7:0]', ha='center', va='center',
            fontsize=9, fontweight='bold', color=BLU, fontfamily='monospace')
    # Bus wire from prev to XOR
    wire_h(ax, 1.8, 3.5, 4.0, color=BLU, lw=1.4)

    # prev[7] extracted (MSB)
    wire_h(ax, 1.8, 3.0, 5.2, color=BLU, lw=1.2)
    wire_v(ax, 3.0, 5.2, 6.5, color=BLU, lw=1.2)
    lbl(ax, 2.4, 5.4, 'prev[7]', color=BLU, size=8)
    wire_h(ax, 3.0, 3.8, 6.5, color=BLU, lw=1.2)
    dot(ax, 3.0, 5.2, color=BLU)

    # data_bit input
    ax.annotate('', xy=(3.8, 6.0), xytext=(3.8, 7.5),
                arrowprops=dict(arrowstyle='->', color=GRN, lw=1.8))
    lbl(ax, 3.8, 7.7, 'data_bit\n(data_in[7-i])', color=GRN, size=9)
    wire_h(ax, 3.8, 3.8, 6.0, color=GRN, lw=1.2)

    # XOR gate: topbit = prev[7] XOR data_bit
    gate_xor(ax, 4.5, 6.3, w=0.8, h=0.6, color=ORG)
    wire_h(ax, 3.0 + 0.8, 3.8, 6.5, color=BLU, lw=1.2)  # prev[7] -> XOR
    wire_h(ax, 3.8, 4.1, 6.0, color=GRN, lw=1.2)         # data_bit -> XOR
    lbl(ax, 4.5, 7.15, 'XOR₁: topbit = prev[7] ⊕ data_bit',
        color=ORG, size=8)
    # XOR output
    xor1_out_x = 4.5 + 0.73
    wire_h(ax, xor1_out_x, 6.2, 6.3, color=ORG)
    dot(ax, 6.0, 6.3, color=ORG)
    lbl(ax, 6.5, 6.55, 'topbit', color=ORG, size=8, bold=True)

    # Shift: {prev[6:0], 0}
    ax.add_patch(FancyBboxPatch((3.5, 2.6), 2.0, 1.0,
                                 boxstyle='round,pad=0.1',
                                 fc='#E8F5E9', ec=GRN, lw=1.5))
    ax.text(4.5, 3.1, 'SHIFT LEFT\n{prev[6:0], 0}',
            ha='center', va='center', fontsize=8, color=GRN, fontweight='bold')
    wire_h(ax, 1.8, 3.5, 3.1, color=BLU, lw=1.4)
    # Shift output
    wire_h(ax, 5.5, 6.3, 3.1, color=GRN, lw=1.4)
    dot(ax, 6.3, 3.1, color=GRN)

    # Conditional XOR with 0x07
    # Mux: if topbit -> XOR with 0x07 else XOR with 0x00
    ax.add_patch(FancyBboxPatch((7.0, 2.4), 2.0, 1.4,
                                 boxstyle='round,pad=0.1',
                                 fc='#FFF3E0', ec=ORG, lw=1.8))
    ax.text(8.0, 3.1, 'XOR₂\n(cond.)', ha='center', va='center',
            fontsize=9, fontweight='bold', color=ORG)
    ax.text(8.0, 2.65, 'if topbit: ⊕ 0x07', ha='center', va='center',
            fontsize=7.5, color=GRY, fontfamily='monospace')

    # Connections to conditional XOR
    wire_h(ax, 6.3, 7.0, 3.1, color=GRN, lw=1.4)   # shift -> XOR2
    wire_v(ax, 6.0, 6.3, 3.45, color=ORG, lw=1.4)   # topbit -> XOR2
    wire_h(ax, 6.0, 7.0, 3.45, color=ORG, lw=1.4)
    dot(ax, 6.3, 3.1, color=GRN)

    # Polynomial input
    lbl(ax, 8.0, 1.8, '0x07 = 0000 0111  (poly mask)',
        color=BLU, size=8, ha='center')
    ax.annotate('', xy=(7.5, 2.4), xytext=(7.5, 2.0),
                arrowprops=dict(arrowstyle='->', color=BLU, lw=1.4))

    # next[7:0] output
    ax.add_patch(FancyBboxPatch((10.0, 2.6), 1.6, 1.0,
                                 boxstyle='round,pad=0.1',
                                 fc='#F3E5F5', ec=PUR, lw=1.8))
    ax.text(10.8, 3.1, 'next[7:0]', ha='center', va='center',
            fontsize=9, fontweight='bold', color=PUR, fontfamily='monospace')
    wire_h(ax, 9.0, 10.0, 3.1, color=PUR, lw=1.8)
    ax.annotate('', xy=(12.2, 3.1), xytext=(11.6, 3.1),
                arrowprops=dict(arrowstyle='->', color=PUR, lw=1.8))
    lbl(ax, 12.4, 3.1, '→ s_{i+1}', color=PUR, size=9, bold=True)

    # Legend
    ax.text(0.5, 0.3,
            'Equação: s_{i+1} = {s_i[6:0], 0} ⊕ (topbit ? 0x07 : 0x00)',
            fontsize=9.5, color=GRY, style='italic',
            bbox=dict(fc='#ECEFF1', ec=GRY, alpha=0.8,
                      boxstyle='round,pad=0.3'))

    ax.set_title('Esquemático: Estágio CRC-8 (1 de 8 estágios desdobrados)\n'
                 'CRCChip v1.0 | topbit = prev[7] ⊕ data_bit → XOR condicional 0x07',
                 fontsize=11, fontweight='bold', color=BLU)
    plt.savefig('fig_schem_stage.png', dpi=150,
                bbox_inches='tight', facecolor='#F5F8FC')
    plt.close()
    print('Salvo: fig_schem_stage.png')


# =============================================================================
# fig_schem_crc8_pipeline.png -- 8 estagios em cascata
# =============================================================================
def fig_schem_crc8_pipeline():
    fig, ax = plt.subplots(figsize=(16, 8))
    ax.set_xlim(-0.5, 16); ax.set_ylim(-0.5, 8)
    ax.axis('off'); fig.patch.set_facecolor('#F5F8FC')

    stage_colors = [BLU, TBLU, TEAL, GRN, GRN, ORG, PUR, RED]
    stage_fcs    = ['#E3F2FD', '#E3F2FD', '#E0F2F1', '#E8F5E9',
                    '#E8F5E9', '#FFF3E0', '#F3E5F5', '#FFEBEE']

    spacing = 1.72
    bw, bh = 1.45, 3.0
    by = 2.2

    for i in range(8):
        bx = 0.3 + i * spacing
        # Stage box
        ax.add_patch(FancyBboxPatch((bx, by), bw, bh,
                                    boxstyle='round,pad=0.1',
                                    fc=stage_fcs[i], ec=stage_colors[i], lw=2.0))
        ax.text(bx + bw/2, by + bh/2 + 0.4, f's{i}',
                ha='center', va='center', fontsize=11, fontweight='bold',
                color=stage_colors[i])
        ax.text(bx + bw/2, by + bh/2,
                'XOR\ntopbit\n+\nSHIFT\n⊕0x07',
                ha='center', va='center', fontsize=7,
                color=GRY, linespacing=1.4)

        # data_in bit label above
        bit_idx = 7 - i
        ax.annotate('', xy=(bx + bw/2, by + bh), xytext=(bx + bw/2, by + bh + 1.0),
                    arrowprops=dict(arrowstyle='->', color=GRN, lw=1.4))
        ax.text(bx + bw/2, by + bh + 1.15, f'd[{bit_idx}]',
                ha='center', fontsize=8, color=GRN, fontweight='bold',
                fontfamily='monospace')

        # Inter-stage connection
        if i < 7:
            ax.annotate('', xy=(bx + bw + 0.27, by + bh/2),
                        xytext=(bx + bw, by + bh/2),
                        arrowprops=dict(arrowstyle='->', color=stage_colors[i],
                                        lw=1.6))
            ax.text(bx + bw + 0.135, by + bh/2 + 0.15,
                    f'→', ha='center', fontsize=9, color=stage_colors[i])

    # crc_in input (enters s0)
    ax.annotate('', xy=(0.3, by + bh/2), xytext=(-0.3, by + bh/2),
                arrowprops=dict(arrowstyle='->', color=ORG, lw=2.0))
    ax.text(-0.4, by + bh/2, 'crc_in\n[7:0]', ha='right', va='center',
            fontsize=9, color=ORG, fontweight='bold', fontfamily='monospace')

    # crc_out exits s7
    last_x = 0.3 + 7 * spacing + bw
    ax.annotate('', xy=(last_x + 0.9, by + bh/2), xytext=(last_x, by + bh/2),
                arrowprops=dict(arrowstyle='->', color=BLU, lw=2.0))
    ax.text(last_x + 1.0, by + bh/2, 'crc_out\n[7:0]', ha='left', va='center',
            fontsize=9, color=BLU, fontweight='bold', fontfamily='monospace')

    # data_in bus label (top)
    data_mid = 0.3 + 3.5 * spacing + bw/2
    ax.add_patch(FancyBboxPatch((0.2, 6.8), 13.8, 0.55,
                                 boxstyle='round,pad=0.1',
                                 fc='#E8F5E9', ec=GRN, lw=1.5, alpha=0.7))
    ax.text(7.1, 7.08, 'data_in[7:0]  →  d[7]→d[6]→...→d[0]  (bit por estágio)',
            ha='center', fontsize=9, fontweight='bold', color=GRN)

    # Stage labels underneath
    for i in range(8):
        bx = 0.3 + i * spacing
        ax.text(bx + bw/2, by - 0.3, f'Stage {i}',
                ha='center', fontsize=7.5, color=GRY, fontfamily='monospace')

    ax.set_title('Esquemático: CRC-8 Pipeline — 8 Estágios em Cascata\n'
                 'CRCChip v1.0 | crc_in → s0 → s1 → ... → s7 → crc_out | Puramente Combinacional',
                 fontsize=11, fontweight='bold', color=BLU)
    plt.savefig('fig_schem_crc8_pipeline.png', dpi=150,
                bbox_inches='tight', facecolor='#F5F8FC')
    plt.close()
    print('Salvo: fig_schem_crc8_pipeline.png')


# =============================================================================
# fig_schem_xor_network.png -- Rede XOR combinacional (fan-in tree)
# =============================================================================
def fig_schem_xor_network():
    """Show combinational XOR contribution for each output bit of crc_out."""
    # Compute which input bits contribute to each crc_out bit
    # by propagating unit vectors through the CRC-8/SMBUS algorithm
    def crc8_matrix():
        """Returns an 8x16 GF(2) matrix: crc_out = M * [data_in | crc_in]"""
        # column j: pass only bit j, rest 0
        cols = []
        # first 8: data_in bits d7..d0
        for bi in range(8):
            data = 1 << (7 - bi)
            crc  = 0
            s = crc
            for step in range(8):
                bit = (data >> (7 - step)) & 1
                topbit = ((s >> 7) ^ bit) & 1
                s = ((s << 1) & 0xFF) ^ (0x07 if topbit else 0x00)
            cols.append(s)
        # next 8: crc_in bits
        for bi in range(8):
            data = 0
            crc  = 1 << (7 - bi)
            s = crc
            for step in range(8):
                bit = (data >> (7 - step)) & 1
                topbit = ((s >> 7) ^ bit) & 1
                s = ((s << 1) & 0xFF) ^ (0x07 if topbit else 0x00)
            cols.append(s)
        return cols

    cols = crc8_matrix()
    # For each output bit (row 0=MSB..7=LSB), find contributing inputs
    contributors = []
    for out_bit in range(8):
        mask = 1 << (7 - out_bit)
        contrib = []
        for in_bit in range(16):
            if cols[in_bit] & mask:
                if in_bit < 8:
                    contrib.append(f'd[{7-in_bit}]')
                else:
                    contrib.append(f'c[{7-(in_bit-8)}]')
        contributors.append(contrib)

    fig, axes = plt.subplots(2, 4, figsize=(14, 10))
    fig.patch.set_facecolor('#F5F8FC')
    fig.suptitle('CRCChip v1.0 — Rede XOR Combinacional\n'
                 'Contribuições de data_in e crc_in para cada bit de crc_out',
                 fontsize=12, fontweight='bold', color=BLU)

    colors_in = {
        'd': BLU,   # data_in bits
        'c': ORG,   # crc_in bits
    }

    for out_i, (ax, contrib) in enumerate(zip(axes.flat, contributors)):
        ax.set_xlim(0, 6); ax.set_ylim(-0.5, len(contrib) + 1)
        ax.axis('off')
        ax.set_facecolor('#FAFAFA')

        out_lbl = f'crc_out[{7-out_i}]'
        ax.text(3.0, len(contrib) + 0.6, out_lbl,
                ha='center', fontsize=10, fontweight='bold', color=RED,
                bbox=dict(fc='#FFEBEE', ec=RED, alpha=0.85,
                          boxstyle='round,pad=0.3'))

        if not contrib:
            ax.text(3.0, len(contrib)/2, '= 0 (constante)',
                    ha='center', fontsize=9, color=GRY)
        else:
            # XOR fan-in tree visual
            n = len(contrib)
            for ci, src in enumerate(contrib):
                y_src = ci
                col = colors_in.get(src[0], GRY)
                ax.text(0.5, y_src + 0.35, src, ha='left', va='center',
                        fontsize=8.5, color=col, fontweight='bold',
                        fontfamily='monospace',
                        bbox=dict(fc=WHT, ec=col, alpha=0.7,
                                  boxstyle='round,pad=0.15', lw=0.8))
                ax.plot([1.55, 2.3], [y_src + 0.35, n/2], color=col,
                        lw=0.9, alpha=0.7)

            # XOR symbol at merge
            xor_cx, xor_cy = 2.8, n/2
            gate_xor(ax, xor_cx, xor_cy, w=0.7, h=0.55, color=ORG)
            ax.plot([xor_cx + 0.62, 5.0], [xor_cy, xor_cy],
                    color=RED, lw=1.8)
            ax.text(5.1, xor_cy, out_lbl, ha='left', va='center',
                    fontsize=8, color=RED, fontweight='bold',
                    fontfamily='monospace')

            ax.text(3.0, -0.35,
                    f'{n} entradas XOR',
                    ha='center', fontsize=8, color=GRY, style='italic')

        ax.set_title(f'crc_out[{7-out_i}]', fontsize=9,
                     fontweight='bold', color=RED, pad=3)

    plt.tight_layout()
    plt.savefig('fig_schem_xor_network.png', dpi=150,
                bbox_inches='tight', facecolor='#F5F8FC')
    plt.close()
    print('Salvo: fig_schem_xor_network.png')


# =============================================================================
# fig_schem_chip_full.png -- Visao completa do chip (blocos de pad)
# =============================================================================
def fig_schem_chip_full():
    fig, ax = plt.subplots(figsize=(16, 7))
    ax.set_xlim(-0.5, 16); ax.set_ylim(-0.5, 7)
    ax.axis('off'); fig.patch.set_facecolor('#F5F8FC')

    def pad_box(ax, x, y, w, h, label, color):
        ax.add_patch(FancyBboxPatch((x, y), w, h,
                                    boxstyle='round,pad=0.08',
                                    fc='#ECEFF1', ec=color, lw=1.8))
        ax.text(x + w/2, y + h/2, label, ha='center', va='center',
                fontsize=8.5, fontweight='bold', color=color,
                fontfamily='monospace')

    def arr_h(ax, x0, x1, y, label='', color=GRY, lw=2.0):
        ax.annotate('', xy=(x1, y), xytext=(x0, y),
                    arrowprops=dict(arrowstyle='->', color=color, lw=lw))
        if label:
            ax.text((x0 + x1)/2, y + 0.2, label, ha='center',
                    fontsize=8, color=color, fontfamily='monospace')

    # ── Core block ──
    core = FancyBboxPatch((5.5, 1.5), 5.0, 4.0, boxstyle='round,pad=0.15',
                           fc='#E3F2FD', ec=BLU, lw=2.5)
    ax.add_patch(core)
    ax.text(8.0, 3.8, 'CRC-8 CORE', ha='center', va='center',
            fontsize=13, fontweight='bold', color=BLU)
    ax.text(8.0, 3.2, '(8 Estágios)', ha='center', va='center',
            fontsize=10, color=TBLU)
    ax.text(8.0, 2.55,
            'G(x) = x⁸ + x² + x + 1\n0x07 | MSB-first',
            ha='center', va='center', fontsize=9, color=GRY,
            fontfamily='monospace',
            bbox=dict(fc='#DCEEFB', ec=BLU, alpha=0.7,
                      boxstyle='round,pad=0.2'))

    # Stage mini-boxes inside core
    for i in range(8):
        sx = 5.7 + i * 0.57
        ax.add_patch(FancyBboxPatch((sx, 4.55), 0.50, 0.55,
                                    boxstyle='round,pad=0.03',
                                    fc=WHT, ec=TBLU, lw=0.9))
        ax.text(sx + 0.25, 4.83, f's{i}', ha='center', va='center',
                fontsize=6, color=TBLU, fontweight='bold')

    # ── data_in pad (top) ──
    pad_box(ax, 6.5, 5.6, 3.0, 0.9, 'data_in[7:0]', GRN)
    ax.annotate('', xy=(8.0, 5.6), xytext=(8.0, 5.1),
                arrowprops=dict(arrowstyle='->', color=GRN, lw=1.8))
    ax.text(8.3, 5.38, '8 bits', fontsize=8, color=GRN, fontfamily='monospace')

    # ── crc_in pad (left) ──
    pad_box(ax, 1.0, 2.8, 2.0, 1.1, 'crc_in[7:0]\n(feedback)', ORG)
    arr_h(ax, 3.0, 5.5, 3.35, '8 bits', ORG)

    # ── crc_out pad (right) ──
    pad_box(ax, 13.0, 3.5, 2.0, 0.9, 'crc_out[7:0]', BLU)
    arr_h(ax, 10.5, 13.0, 3.95, '8 bits', BLU)

    # ── zero_flag pad (bottom right) ──
    pad_box(ax, 12.0, 1.5, 2.0, 0.8, 'zero_flag', RED)
    ax.annotate('', xy=(12.8, 1.5), xytext=(11.5, 1.8),
                arrowprops=dict(arrowstyle='->', color=RED, lw=1.5,
                                connectionstyle='arc3,rad=-0.2'))
    ax.text(11.8, 1.25, '1 bit', fontsize=8, color=RED, fontfamily='monospace')

    # ── Chip boundary ──
    ax.add_patch(FancyBboxPatch((0.2, 0.5), 15.3, 6.0,
                                 boxstyle='round,pad=0.1',
                                 fc='none', ec='#3949AB', lw=2.5, ls='--'))
    ax.text(8.0, 6.68, 'crc8_chip_top  —  CRCChip v1.0  |  CMOS 0,35µm  |  VDD=3,3V',
            ha='center', fontsize=10, color='#3949AB', fontweight='bold',
            style='italic')

    # ── Port labels ──
    ax.text(2.0, 4.3, 'Entrada:\ncrc_in[7:0]\n8 bits', ha='center', va='center',
            fontsize=8, color=ORG, fontfamily='monospace',
            bbox=dict(fc='#FFF3E0', ec=ORG, alpha=0.8,
                      boxstyle='round,pad=0.2'))
    ax.text(14.0, 2.2, 'Saída:\nzero_flag\n1 bit', ha='center', va='center',
            fontsize=8, color=RED, fontfamily='monospace',
            bbox=dict(fc='#FFEBEE', ec=RED, alpha=0.8,
                      boxstyle='round,pad=0.2'))

    ax.set_title('CRCChip v1.0 — Diagrama de Blocos Completo (Chip Top)\n'
                 'data_in + crc_in → CRC-8 CORE (8 estágios) → crc_out + zero_flag',
                 fontsize=11, fontweight='bold', color=BLU)
    plt.savefig('fig_schem_chip_full.png', dpi=150,
                bbox_inches='tight', facecolor='#F5F8FC')
    plt.close()
    print('Salvo: fig_schem_chip_full.png')


# ─── Main ─────────────────────────────────────────────────────────────────────
if __name__ == '__main__':
    fig_schem_stage()
    fig_schem_crc8_pipeline()
    fig_schem_xor_network()
    fig_schem_chip_full()
    print('\nTodos os 4 esquemáticos gerados.')
