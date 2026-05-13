#!/usr/bin/env python3
"""
gerar_layout_fisico.py  --  Layout fisico CMOS para CRCChip v1.0
Unidade 7 | Capitulo 5 | PADIS
Autor: Pedro Victor dos Santos Oliveira  |  Prof.: Thiago Brito
Estilo Cadence Virtuoso: N-Well/Active/P+N+/Poly/Contact/Metal1/Metal2
"""
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, Rectangle
import os

os.chdir(os.path.dirname(os.path.abspath(__file__)))

# ─── Camadas CMOS (cores Cadence Virtuoso / Magic) ───────────────────────────
LAYERS = {
    'nwell':    {'fc': '#FFD0D0', 'ec': '#CC8888', 'lw': 1.0, 'alpha': 0.55, 'label': 'N-Well'},
    'active':   {'fc': '#C8F0C8', 'ec': '#448844', 'lw': 0.8, 'alpha': 0.75, 'label': 'Active'},
    'pplus':    {'fc': '#FF88AA', 'ec': '#CC2266', 'lw': 0.6, 'alpha': 0.70, 'label': 'P+ diffusion'},
    'nplus':    {'fc': '#FFBB66', 'ec': '#CC6600', 'lw': 0.6, 'alpha': 0.70, 'label': 'N+ diffusion'},
    'poly':     {'fc': '#EE44CC', 'ec': '#991188', 'lw': 0.8, 'alpha': 0.85, 'label': 'Poly (Gate)'},
    'contact':  {'fc': '#555555', 'ec': '#222222', 'lw': 0.5, 'alpha': 0.90, 'label': 'Contact'},
    'metal1':   {'fc': '#4477EE', 'ec': '#1144BB', 'lw': 0.7, 'alpha': 0.80, 'label': 'Metal1'},
    'metal2':   {'fc': '#EE9922', 'ec': '#AA5500', 'lw': 0.7, 'alpha': 0.75, 'label': 'Metal2'},
    'metal2_h': {'fc': '#EE9922', 'ec': '#AA5500', 'lw': 0.7, 'alpha': 0.60, 'label': 'Metal2'},
}

def lay(ax, layer, x, y, w, h, zorder=None):
    s = LAYERS[layer]
    z = zorder if zorder else {'nwell': 1, 'active': 2, 'pplus': 3, 'nplus': 3,
                               'poly': 4, 'contact': 5, 'metal1': 6,
                               'metal2': 7, 'metal2_h': 7}.get(layer, 4)
    r = Rectangle((x, y), w, h,
                  fc=s['fc'], ec=s['ec'], lw=s['lw'],
                  alpha=s['alpha'], zorder=z)
    ax.add_patch(r)

def contacts(ax, x0, y0, cols, rows, pitch=0.9, size=0.5):
    for r in range(rows):
        for c in range(cols):
            lay(ax, 'contact',
                x0 + c * pitch, y0 + r * pitch, size, size, zorder=5)

def legend_patches():
    return [mpatches.Patch(fc=v['fc'], ec=v['ec'], lw=1.0,
                           label=v['label'], alpha=0.85)
            for k, v in LAYERS.items() if k != 'metal2_h']


# =============================================================================
# FIGURA 1 — Layout celula XOR2 CMOS (adapted for CRC: A=prev_bit, B=data_bit)
# =============================================================================
def fig_layout_xor2_crc():
    fig, ax = plt.subplots(figsize=(11, 8))
    ax.set_xlim(-1, 14); ax.set_ylim(-1, 11)
    ax.set_facecolor('#F0F0F0')
    fig.patch.set_facecolor('#F5F8FC')
    ax.set_aspect('equal')
    ax.grid(True, color='#CCCCCC', lw=0.3, zorder=0)
    ax.set_xlabel('X (µm)', fontsize=10)
    ax.set_ylabel('Y (µm)', fontsize=10)

    # ── Cell boundary ──
    ax.add_patch(Rectangle((-0.5, -0.5), 13.5, 10.5,
                            fc='none', ec='#3949AB', lw=2.0, ls='--', zorder=9))

    # ── PMOS pair: Common-Centroid ABBA (N-Well) ──
    # M1(A) | M2(B) | M3(B) | M4(A) — 4 columns, ABBA arrangement
    lay(ax, 'nwell', 0.5, 4.5, 12.0, 5.0)

    labels_abba = ['M1(A)', 'M2(B)', 'M3(B)', 'M4(A)']
    pmos_colors = ['#CC2266', '#990055', '#990055', '#CC2266']
    for i, lbl_t in enumerate(labels_abba):
        bx = 0.8 + i * 2.8
        lay(ax, 'active', bx, 5.5, 2.2, 3.0)
        lay(ax, 'pplus',  bx, 5.5, 2.2, 3.0)
        for f in range(3):
            contacts(ax, bx + f * 0.7 + 0.1, 5.7, 1, 3, pitch=0.85, size=0.45)
        # poly gates (2 per transistor)
        lay(ax, 'poly', bx + 0.72, 5.0, 0.35, 4.0)
        lay(ax, 'poly', bx + 1.55, 5.0, 0.35, 4.0)
        ax.text(bx + 1.1, 9.3, lbl_t, ha='center', fontsize=7,
                color=pmos_colors[i], fontweight='bold',
                bbox=dict(fc='white', ec=pmos_colors[i], alpha=0.75, pad=1.5))

    ax.text(6.3, 4.7, 'PMOS  W=3µm  (ABBA Common-Centroid)',
            ha='center', fontsize=7.5, color='#CC2266',
            bbox=dict(fc='white', ec='#CC2266', alpha=0.8, pad=2))

    # ── NMOS pair (below) ──
    # M5(A) | M6(B) — 2 transistors (series for XOR pull-down)
    for i, (lbl_n, bx_n) in enumerate([('M5(A)\nW=1.5µm', 1.2),
                                        ('M6(B)\nW=1.5µm', 7.0)]):
        lay(ax, 'active', bx_n, 0.8, 4.0, 2.5)
        lay(ax, 'nplus',  bx_n, 0.8, 4.0, 2.5)
        for f in range(4):
            contacts(ax, bx_n + f * 0.9 + 0.1, 1.0, 1, 2, pitch=0.9, size=0.48)
        lay(ax, 'poly', bx_n + 1.5, 0.3, 0.35, 3.5)
        lay(ax, 'poly', bx_n + 2.5, 0.3, 0.35, 3.5)
        ax.text(bx_n + 2.0, -0.65, lbl_n, ha='center', fontsize=7,
                color='#CC6600', fontweight='bold',
                bbox=dict(fc='white', ec='#CC6600', alpha=0.75, pad=1.5))

    # ── P+ Guard ring (left) ──
    lay(ax, 'pplus', -0.8, -0.3, 0.5, 10.0)
    contacts(ax, -0.75, 0.2, 1, 9, pitch=1.0, size=0.40)
    ax.text(-1.1, 5.0, 'P+\nGuard', ha='center', fontsize=6.5,
            color='#CC2266', rotation=90)

    # ── N+ Guard ring (right) ──
    lay(ax, 'nplus', 12.5, -0.3, 0.5, 10.0)
    contacts(ax, 12.55, 0.2, 1, 9, pitch=1.0, size=0.40)
    ax.text(13.3, 5.0, 'N+\nGuard', ha='center', fontsize=6.5,
            color='#CC6600', rotation=90)

    # ── VDD Metal2 rail (top) ──
    lay(ax, 'metal2', -0.5, 9.0, 13.0, 0.75)
    ax.text(12.2, 9.35, 'VDD', fontsize=9, color='#AA5500', fontweight='bold')

    # ── GND Metal2 rail (bottom) ──
    lay(ax, 'metal2', -0.5, -0.45, 13.0, 0.50)
    ax.text(12.2, -0.22, 'GND', fontsize=9, color='#AA5500', fontweight='bold')

    # ── Output Metal1 (Z = topbit) ──
    lay(ax, 'metal1', 5.8, 2.5, 0.6, 6.0)
    ax.text(7.0, 5.5, 'Z = topbit\n(A⊕B)', fontsize=8, color='#1144BB',
            fontweight='bold', rotation=90, va='center')

    # ── Input Metal1 pads ──
    lay(ax, 'metal1', -0.5, 6.5, 1.6, 0.55)
    lay(ax, 'metal1', -0.5, 4.0, 1.6, 0.55)
    ax.text(-0.8, 6.78, 'A\n(prev_bit)', ha='right', fontsize=8,
            color='#1144BB', fontweight='bold', va='center')
    ax.text(-0.8, 4.28, 'B\n(data_bit)', ha='right', fontsize=8,
            color='#1144BB', fontweight='bold', va='center')

    # Legend
    ax.legend(handles=legend_patches(), loc='upper right',
              fontsize=7, framealpha=0.9, ncol=2)

    ax.set_title('Layout Físico — Célula XOR2 CMOS (CRCChip v1.0)\n'
                 'A=prev_bit, B=data_bit → Z=topbit | W_P=3µm W_N=1.5µm | ABBA Common-Centroid | Guard Rings P+/N+',
                 fontsize=11, fontweight='bold', color='#1565C0')
    plt.tight_layout()
    plt.savefig('fig_layout_xor2_crc.png', dpi=150,
                bbox_inches='tight', facecolor='#F5F8FC')
    plt.close()
    print('Salvo: fig_layout_xor2_crc.png')


# =============================================================================
# FIGURA 2 — Layout do Die completo CRCChip (48µm x 32µm)
# =============================================================================
def fig_layout_crc_die():
    W, H = 48.0, 32.0
    fig, ax = plt.subplots(figsize=(12, 8))
    ax.set_xlim(-2, W + 4); ax.set_ylim(-5, H + 3)
    ax.set_facecolor('#E8E8E8')
    fig.patch.set_facecolor('#F5F8FC')
    ax.set_aspect('equal')
    ax.grid(True, color='#BBBBBB', lw=0.3, zorder=0)
    ax.set_xlabel('X (µm)', fontsize=10)
    ax.set_ylabel('Y (µm)', fontsize=10)

    # ── Die boundary ──
    ax.add_patch(Rectangle((0, 0), W, H,
                            fc='#FAFAFA', ec='#333333', lw=2.5, zorder=1))

    # ════ TOP BAND: 8 XOR stage cells (N-Well region) ════
    lay(ax, 'nwell', 1.5, 18.0, 45.0, 10.0)

    stage_labels = [f's{i}' for i in range(8)]
    for i, slbl in enumerate(stage_labels):
        bx = 2.0 + i * 5.4

        # PMOS section (XOR pair per stage: 2 PMOS)
        for f in range(3):
            lay(ax, 'active', bx + f * 1.5, 22.5, 1.1, 4.0)
            lay(ax, 'pplus',  bx + f * 1.5, 22.5, 0.7, 4.0)
            contacts(ax, bx + f * 1.5 + 0.1, 22.7, 1, 3, pitch=1.0, size=0.50)
        for f in range(2):
            lay(ax, 'poly', bx + f * 1.5 + 0.75, 22.0, 0.35, 5.0)

        # NMOS section
        for f in range(3):
            lay(ax, 'active', bx + f * 1.5, 18.5, 1.1, 3.0)
            lay(ax, 'nplus',  bx + f * 1.5, 18.5, 0.7, 3.0)
            contacts(ax, bx + f * 1.5 + 0.1, 18.7, 1, 2, pitch=1.0, size=0.50)
        for f in range(2):
            lay(ax, 'poly', bx + f * 1.5 + 0.75, 18.0, 0.35, 4.0)

        # Metal1 inter-stage interconnect
        lay(ax, 'metal1', bx + 0.2, 21.0, 3.8, 0.45)

        ax.text(bx + 2.2, 28.8, slbl, ha='center', fontsize=7.5,
                color='#1144BB', fontweight='bold',
                bbox=dict(fc='#E3F2FD', ec='#1565C0', alpha=0.85, pad=1.5))

    ax.text(24.5, 29.7, '8 Estágios XOR (s0 … s7)  —  Banda Superior',
            ha='center', fontsize=8.5, fontweight='bold', color='#1565C0',
            bbox=dict(fc='#E3F2FD', ec='#1565C0', alpha=0.8, pad=3))

    # ════ MIDDLE BAND: Metal1 routing / interconnect ════
    lay(ax, 'metal1', 0.5, 13.5, W - 1.0, 3.5)
    ax.text(W/2, 15.25, 'Metal1 Interconnect — Roteamento de Barramentos [7:0]',
            ha='center', fontsize=7.5, fontweight='bold', color='#1144BB',
            bbox=dict(fc='#E8EAF6', ec='#1144BB', alpha=0.8, pad=2))

    # 8-bit bus lines
    for bit in range(8):
        y_wire = 13.8 + bit * 0.36
        ax.plot([0.5, W - 0.5], [y_wire, y_wire],
                color='#4477EE', lw=0.6, alpha=0.6, zorder=6)

    # ════ BOTTOM BAND: zero_flag logic (NOR tree) + I/O pads ════
    lay(ax, 'nwell', 1.5, 3.0, 45.0, 9.0)

    # NOR-8 tree (zero_flag): 8 cells
    for i in range(8):
        bx = 2.0 + i * 5.2
        lay(ax, 'active', bx, 5.0, 3.8, 4.5)
        lay(ax, 'pplus',  bx, 6.5, 3.8, 2.0)
        lay(ax, 'nplus',  bx, 5.0, 3.8, 1.5)
        lay(ax, 'poly',   bx + 1.3, 4.5, 0.35, 5.5)
        lay(ax, 'poly',   bx + 2.3, 4.5, 0.35, 5.5)
        contacts(ax, bx + 0.2, 5.2, 1, 3, pitch=1.0, size=0.50)
        contacts(ax, bx + 1.5, 5.2, 1, 3, pitch=1.0, size=0.50)

    ax.text(24.5, 3.2, 'NOR-8 Tree (zero_flag logic)  —  Banda Inferior',
            ha='center', fontsize=8, fontweight='bold', color='#C62828',
            bbox=dict(fc='#FFEBEE', ec='#C62828', alpha=0.8, pad=3))

    # I/O Pads (top edge, metal2)
    pad_in = ['d[7]', 'd[6]', 'd[5]', 'd[4]', 'd[3]', 'd[2]', 'd[1]', 'd[0]']
    for i, pn in enumerate(pad_in):
        px = 1.5 + i * 5.4
        lay(ax, 'metal2', px, -4.2, 4.5, 2.5)
        ax.text(px + 2.25, -4.8, pn, ha='center', fontsize=6.5,
                color='#AA5500', fontweight='bold')

    # Right side pads: crc_in / crc_out / zero_flag
    right_pads = [
        ('crc_in[7:0]', H - 5.0),
        ('crc_out[7:0]', H - 12.0),
        ('zero_flag', H - 19.0),
    ]
    for pn, py in right_pads:
        lay(ax, 'metal2', W + 0.5, py - 1.2, 3.5, 2.4)
        ax.text(W + 2.25, py, pn, ha='center', va='center', fontsize=6,
                color='#AA5500', fontweight='bold')

    # ════ VDD Metal2 top rail ════
    lay(ax, 'metal2',  0.0, H - 1.5, W, 1.2)
    ax.text(W + 0.3, H - 1.0, 'VDD', fontsize=8, color='#AA5500', fontweight='bold')

    # ════ GND Metal2 bottom rail ════
    lay(ax, 'metal2',  0.0, 0.0, W, 1.0)
    ax.text(W + 0.3, 0.3, 'GND', fontsize=8, color='#AA5500', fontweight='bold')

    # Annotation
    ax.text(W/2, -2.5,
            f'CRCChip v1.0  |  {W:.0f} µm × {H:.0f} µm = {W*H:.0f} µm²  |  CMOS 0,35µm',
            ha='center', fontsize=9, color='#333333', fontweight='bold')

    ax.legend(handles=legend_patches(), loc='lower right',
              fontsize=7, framealpha=0.95, ncol=2,
              bbox_to_anchor=(1.0, 0.0))

    ax.set_title('Layout Físico — CRCChip v1.0 (Die Completo)\n'
                 '8 Estágios XOR | Metal1 Routing | NOR-8 Flag | CMOS 0,35µm',
                 fontsize=12, fontweight='bold', color='#1565C0')
    plt.tight_layout()
    plt.savefig('fig_layout_crc_die.png', dpi=150,
                bbox_inches='tight', facecolor='#F5F8FC')
    plt.close()
    print('Salvo: fig_layout_crc_die.png')


# =============================================================================
# FIGURA 3 — Zoom: Stage 0 (XOR2 + shift bit cell + cond XOR transistors)
# =============================================================================
def fig_layout_stage_zoom():
    fig, ax = plt.subplots(figsize=(13, 9))
    ax.set_xlim(-1, 20); ax.set_ylim(-1, 14)
    ax.set_facecolor('#E8E8E8')
    fig.patch.set_facecolor('#F5F8FC')
    ax.set_aspect('equal')
    ax.grid(True, color='#CCCCCC', lw=0.3, zorder=0)
    ax.set_xlabel('X (µm)', fontsize=10)
    ax.set_ylabel('Y (µm)', fontsize=10)

    ax.add_patch(Rectangle((-0.3, -0.3), 19.6, 13.6,
                            fc='none', ec='#3949AB', lw=2.5, ls='--', zorder=9))

    # ── XOR2 transistors for topbit computation ──
    # Common-Centroid ABBA: M1a | M2a | M2b | M1b (PMOS, N-Well)
    lay(ax, 'nwell', 0.0, 6.5, 13.5, 7.0)

    trios = [('M1a', 0.4), ('M2a', 3.5), ('M2b', 6.6), ('M1b', 9.7)]
    top_colors = ['#CC2266', '#990055', '#990055', '#CC2266']
    for (lbl_m, bx), tc in zip(trios, top_colors):
        lay(ax, 'active', bx,       8.0, 2.5, 4.2)
        lay(ax, 'pplus',  bx,       8.0, 2.5, 4.2)
        for f in range(3):
            contacts(ax, bx + f * 0.75 + 0.1, 8.2, 1, 3, pitch=0.85, size=0.45)
        lay(ax, 'poly', bx + 0.78, 7.5, 0.35, 5.0)
        lay(ax, 'poly', bx + 1.72, 7.5, 0.35, 5.0)
        ax.text(bx + 1.25, 13.1, lbl_m, ha='center', fontsize=7.5,
                fontweight='bold', color=tc,
                bbox=dict(fc='white', ec=tc, alpha=0.75, pad=1.5))

    ax.text(6.7, 7.0, 'XOR2 PMOS (Common-Centroid ABBA)\nM1a|M2a|M2b|M1b  W=3µm L=0.35µm',
            ha='center', fontsize=7.5, color='#1144BB',
            bbox=dict(fc='white', ec='#1144BB', alpha=0.8, pad=2))

    # ── Shift-register bit cell (Metal1 feedback wire) ──
    lay(ax, 'nwell', 13.5, 6.5, 5.5, 7.0)
    # 2 PMOS for shift cell
    for j, (lbl_s, bx_s) in enumerate([('M5\n(SH-P)', 14.0), ('M6\n(SH-P)', 16.5)]):
        lay(ax, 'active', bx_s, 8.2, 1.8, 3.5)
        lay(ax, 'pplus',  bx_s, 8.2, 1.8, 3.5)
        contacts(ax, bx_s + 0.1, 8.4, 1, 3, pitch=0.9, size=0.45)
        lay(ax, 'poly', bx_s + 0.75, 7.7, 0.35, 4.5)
        ax.text(bx_s + 0.9, 13.1, lbl_s, ha='center', fontsize=7.5,
                fontweight='bold', color='#CC2266',
                bbox=dict(fc='white', ec='#CC2266', alpha=0.75, pad=1.5))
    # Metal1 feedback wire
    lay(ax, 'metal1', 14.0, 11.8, 4.0, 0.55)
    ax.annotate('', xy=(18.2, 12.05), xytext=(14.0, 12.05),
                arrowprops=dict(arrowstyle='->', color='#4477EE', lw=1.5))
    ax.text(16.1, 12.55, 'Metal1 feedback\n(shift out → next stage)',
            ha='center', fontsize=6.5, color='#1144BB',
            bbox=dict(fc='white', ec='#1144BB', alpha=0.8, pad=1.5))

    # ── Conditional XOR gate transistors (NMOS below) ──
    # M3, M4 (conditional XOR NMOS), M7 (shift NMOS)
    nmos_cells = [('M3\n(XOR-N)', 0.0), ('M4\n(XOR-N)', 4.5),
                  ('M7\n(SH-N)', 13.5)]
    for (lbl_n, bx_n) in nmos_cells:
        lay(ax, 'active', bx_n, 1.0, 3.8, 4.2)
        lay(ax, 'nplus',  bx_n, 1.0, 3.8, 4.2)
        for f in range(4):
            contacts(ax, bx_n + f * 0.85 + 0.1, 1.3, 1, 3, pitch=0.9, size=0.45)
        lay(ax, 'poly', bx_n + 1.4, 0.5, 0.35, 5.2)
        lay(ax, 'poly', bx_n + 2.4, 0.5, 0.35, 5.2)
        ax.text(bx_n + 2.0, -0.6, lbl_n, ha='center', fontsize=7.5,
                fontweight='bold', color='#CC6600',
                bbox=dict(fc='white', ec='#CC6600', alpha=0.75, pad=1.5))

    ax.text(4.0, 0.1, 'XOR2 NMOS  (W=1.5µm)', ha='center', fontsize=7,
            color='#CC6600',
            bbox=dict(fc='white', ec='#CC6600', alpha=0.8, pad=1.5))

    # ── VDD / GND rails ──
    lay(ax, 'metal2', -0.2, 12.5, 19.4, 0.8)
    lay(ax, 'metal2', -0.2, -0.2, 19.4, 0.6)
    ax.text(19.2, 12.8, 'VDD', fontsize=8, color='#AA5500', fontweight='bold')
    ax.text(19.2, -0.05, 'GND', fontsize=8, color='#AA5500', fontweight='bold')

    # ── Input/Output Metal1 ──
    lay(ax, 'metal1', -0.8, 9.5, 1.0, 0.5)   # A (prev_bit)
    lay(ax, 'metal1', -0.8, 3.5, 1.0, 0.5)   # B (data_bit[7])
    lay(ax, 'metal1', 5.6, 5.5, 0.6, 7.5)    # topbit output
    ax.text(-0.9, 9.75, 'A\n(prev)', ha='right', fontsize=7.5,
            color='#1144BB', fontweight='bold')
    ax.text(-0.9, 3.75, 'B\n(d[7])', ha='right', fontsize=7.5,
            color='#1144BB', fontweight='bold')
    ax.text(7.2, 9.0, 'topbit\n→ cond. XOR', fontsize=7.5,
            color='#1144BB', fontweight='bold',
            bbox=dict(fc='white', ec='#1144BB', alpha=0.8, pad=1.5))

    # Legend
    ax.legend(handles=legend_patches(), loc='upper right',
              fontsize=7, framealpha=0.95, ncol=2)

    ax.set_title('Layout Físico — Stage 0 (Zoom)  |  CRCChip v1.0\n'
                 'XOR2 topbit (M1-M4) + Shift cell (M5-M6) + Cond. XOR (M7) | Guard Rings | CMOS 0,35µm',
                 fontsize=11, fontweight='bold', color='#1565C0')
    plt.tight_layout()
    plt.savefig('fig_layout_stage_zoom.png', dpi=150,
                bbox_inches='tight', facecolor='#F5F8FC')
    plt.close()
    print('Salvo: fig_layout_stage_zoom.png')


# ─── Main ─────────────────────────────────────────────────────────────────────
if __name__ == '__main__':
    fig_layout_xor2_crc()
    fig_layout_crc_die()
    fig_layout_stage_zoom()
    print('\nTodos os 3 layouts físicos gerados.')
