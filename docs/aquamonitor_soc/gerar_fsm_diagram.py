"""
gerar_fsm_diagram.py — SAR Control FSM — AquaMonitorSoC v1.0
Redesigned: outputs outside circles, generous spacing, no overlap.
"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

fig, ax = plt.subplots(figsize=(14, 12))
ax.set_xlim(-0.5, 14.5)
ax.set_ylim(-1.5, 12.5)
ax.axis('off')
fig.patch.set_facecolor('white')

ax.set_title('SAR ADC Control FSM — AquaMonitorSoC v1.0\n'
             'Máquina de Moore · 8 Estados · Processo CMOS TSMC 180nm',
             fontsize=13, fontweight='bold', pad=12)

# ─── State layout: two rows ───────────────────────────────────────────────────
#  Row 1 (top):  IDLE  CH_SEL  SAMPLE  BIT3
#  Row 2 (mid):  DONE  BIT0    BIT1    BIT2
R = 0.65

states = {
    'IDLE':   (1.8,  9.5),
    'CH_SEL': (5.0,  9.5),
    'SAMPLE': (8.2,  9.5),
    'BIT3':   (11.4, 9.5),
    'BIT2':   (11.4, 5.5),
    'BIT1':   (8.2,  5.5),
    'BIT0':   (5.0,  5.5),
    'DONE':   (1.8,  5.5),
}

moore_outputs = {
    'IDLE':   ['sample_en=0', 'eoc=0', 'dac_code=0000'],
    'CH_SEL': ['mux_sel=ch_sel', 'dac_code=0000', 'sample_en=0'],
    'SAMPLE': ['sample_en=1', 'dac_code=1000', 'eoc=0'],
    'BIT3':   ['trial[3]=1', 'dac_code[3]=eval', 'sample_en=0'],
    'BIT2':   ['trial[2]=1', 'dac_code[2]=eval', 'sample_en=0'],
    'BIT1':   ['trial[1]=1', 'dac_code[1]=eval', 'sample_en=0'],
    'BIT0':   ['trial[0]=1', 'dac_code[0]=eval', 'sample_en=0'],
    'DONE':   ['eoc=1', 'result=trial_reg', 'sample_en=0'],
}

# ─── draw states ─────────────────────────────────────────────────────────────
def draw_state(name, x, y):
    is_init = (name == 'IDLE')
    is_done = (name == 'DONE')
    fc = '#d8d8d8' if (is_init or is_done) else '#f0f0f0'
    c = plt.Circle((x, y), R, color='black', fill=True, fc=fc, lw=2, zorder=4)
    ax.add_patch(c)
    if is_init:  # double circle for initial state
        c2 = plt.Circle((x, y), R + 0.12, fc='none', ec='black', lw=1.2, zorder=3)
        ax.add_patch(c2)
    ax.text(x, y, name, ha='center', va='center', fontsize=9,
            fontweight='bold', zorder=5)

for name, (x, y) in states.items():
    draw_state(name, x, y)

# ─── Moore outputs (placed BELOW state in row1, ABOVE in row2) ───────────────
for name, (x, y) in states.items():
    lines = moore_outputs[name]
    is_top_row = (y > 7.0)
    if is_top_row:
        oy = y - R - 0.22
        va = 'top'
    else:
        oy = y + R + 0.22
        va = 'bottom'
    txt = '\n'.join(lines)
    ax.text(x, oy, txt, ha='center', va=va, fontsize=6.5,
            color='#333',
            bbox=dict(boxstyle='round,pad=0.25', fc='#fafafa', ec='#aaa', lw=0.8),
            zorder=5)

# ─── transitions ─────────────────────────────────────────────────────────────
def edge(s1, s2, lbl='', rad=0.0, lpos=0.45, loffx=0.0, loffy=0.14):
    x1, y1 = states[s1]
    x2, y2 = states[s2]
    dx, dy = x2-x1, y2-y1
    dist = np.hypot(dx, dy)
    sx, sy = x1 + dx/dist*R, y1 + dy/dist*R
    ex, ey = x2 - dx/dist*R, y2 - dy/dist*R
    ax.annotate('', xy=(ex, ey), xytext=(sx, sy),
                arrowprops=dict(arrowstyle='->', color='black', lw=1.4,
                                connectionstyle=f'arc3,rad={rad}'))
    if lbl:
        mx = sx + (ex-sx)*lpos + loffx
        my = sy + (ey-sy)*lpos + loffy
        ax.text(mx, my, lbl, ha='center', va='bottom', fontsize=7.5,
                style='italic',
                bbox=dict(boxstyle='round,pad=0.15', fc='white', alpha=0.9, ec='none'),
                zorder=6)

# Sequential flow (top row left→right)
edge('IDLE',   'CH_SEL', 'start=1')
edge('CH_SEL', 'SAMPLE', 'unconditional')
edge('SAMPLE', 'BIT3',   'unconditional')

# Right-side vertical drop BIT3→BIT2
edge('BIT3', 'BIT2', 'eval bit3\ncomp_out', rad=0.05, loffx=0.8, loffy=0.0)

# Bottom row right→left
edge('BIT2', 'BIT1', 'eval bit2')
edge('BIT1', 'BIT0', 'eval bit1')
edge('BIT0', 'DONE', 'eval bit0')

# Left-side vertical DONE→IDLE (feedback arc)
ax.annotate('', xy=(1.8, 9.5-R), xytext=(1.8, 5.5+R),
            arrowprops=dict(arrowstyle='->', color='black', lw=1.4,
                            connectionstyle='arc3,rad=-0.5'))
ax.text(0.55, 7.5, 'unconditional\n(new cycle)', ha='center', va='center',
        fontsize=7, style='italic',
        bbox=dict(boxstyle='round,pad=0.15', fc='white', alpha=0.9, ec='none'), zorder=6)

# Self-loop on IDLE (start=0)
cx, cy = states['IDLE']
loop = mpatches.Arc((cx-0.5, cy+0.7), 0.8, 0.6, angle=0, theta1=10, theta2=350,
                    color='black', lw=1.2)
ax.add_patch(loop)
ax.annotate('', xy=(cx-0.12, cy+0.63), xytext=(cx-0.88, cy+0.63),
            arrowprops=dict(arrowstyle='->', color='black', lw=1.1))
ax.text(cx-0.5, cy+1.35, 'start=0', ha='center', fontsize=7.5, style='italic',
        bbox=dict(boxstyle='round,pad=0.15', fc='white', alpha=0.9, ec='none'), zorder=6)

# ─── comp_out input annotations for BIT states ───────────────────────────────
for name in ['BIT3', 'BIT2', 'BIT1', 'BIT0']:
    x, y = states[name]
    # Arrow comes from above or below based on row
    if y > 7:  # top row (BIT3)
        ax.annotate('', xy=(x+R, y), xytext=(x+R+1.1, y),
                    arrowprops=dict(arrowstyle='->', color='#666', lw=0.9))
        ax.text(x+R+1.2, y, 'comp_out', ha='left', va='center',
                fontsize=6.5, color='#555', style='italic')
    else:  # bottom row (BIT2, BIT1, BIT0)
        ax.annotate('', xy=(x, y+R), xytext=(x, y+R+0.8),
                    arrowprops=dict(arrowstyle='->', color='#666', lw=0.9))
        ax.text(x, y+R+0.9, 'comp_out', ha='center', va='bottom',
                fontsize=6.5, color='#555', style='italic')

# ─── info box ────────────────────────────────────────────────────────────────
ax.text(7.0, 0.8,
        'Em cada estado BITn: bit mantido se comp_out=1 (VIN > VDAC), '
        'descartado se comp_out=0\n'
        'Saída dac_code[n] é testada por 1 ciclo de clock (1 µs @ 1 MHz)',
        ha='center', va='center', fontsize=8.5,
        bbox=dict(boxstyle='round,pad=0.4', fc='#f5f5f5', ec='black', lw=1.2),
        zorder=5)

# ─── legend ──────────────────────────────────────────────────────────────────
c_norm = plt.Circle((0.6, 11.8), 0.25, fc='#f0f0f0', ec='black', lw=1.5)
c_init = plt.Circle((3.2, 11.8), 0.25, fc='#d8d8d8', ec='black', lw=1.5)
c_ini2 = plt.Circle((3.2, 11.8), 0.38, fc='none',    ec='black', lw=1.0)
for p in (c_norm, c_init, c_ini2):
    ax.add_patch(p)
ax.text(1.05, 11.8, 'Estado normal (saídas Moore abaixo/acima)',
        va='center', fontsize=8)
ax.text(3.65, 11.8, 'Estado inicial/final (IDLE / DONE)',
        va='center', fontsize=8)

plt.tight_layout()
plt.savefig('fig_fsm_states.png', dpi=150, bbox_inches='tight', facecolor='white')
print("Saved: fig_fsm_states.png")
