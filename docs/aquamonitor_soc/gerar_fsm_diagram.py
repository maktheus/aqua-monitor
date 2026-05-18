"""
gerar_fsm_diagram.py
SAR Control FSM state diagram — 8 Moore states
Black/white matplotlib + patches, 12x10
"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

fig, ax = plt.subplots(figsize=(12, 10))
ax.set_xlim(-1, 13)
ax.set_ylim(-1, 11)
ax.axis('off')

ax.set_title('SAR ADC Control FSM — AquaMonitorSoC v1.0\n'
             'Moore Machine · 8 States · CMOS TSMC 180nm',
             fontsize=12, fontweight='bold', pad=10)

# ---- State positions (x, y) ----
states = {
    'IDLE':   (6.0, 9.0),
    'CH_SEL': (2.0, 7.0),
    'SAMPLE': (2.0, 5.0),
    'BIT3':   (2.0, 3.0),
    'BIT2':   (5.5, 3.0),
    'BIT1':   (9.0, 3.0),
    'BIT0':   (9.0, 6.0),
    'DONE':   (9.0, 9.0),
}

# Moore outputs per state
outputs = {
    'IDLE':   'sample_en=0\neoc=0',
    'CH_SEL': 'sample_en=0\neoc=0\ndac_code=0000',
    'SAMPLE': 'sample_en=1\ndac_code=1000',
    'BIT3':   'dac_code[3]=trial\ndac_code[2]=1',
    'BIT2':   'dac_code[2]=trial\ndac_code[1]=1',
    'BIT1':   'dac_code[1]=trial\ndac_code[0]=1',
    'BIT0':   'dac_code[0]=trial',
    'DONE':   'eoc=1\nresult=trial_reg',
}

R = 0.75  # circle radius

def draw_state(ax, name, x, y, is_initial=False, is_final=False):
    """Draw a state circle with label and outputs."""
    fc = '#f0f0f0' if name not in ('IDLE', 'DONE') else '#d8d8d8'
    circle = plt.Circle((x, y), R, color='black', fill=True,
                         facecolor=fc, linewidth=2, zorder=3)
    ax.add_patch(circle)
    if is_initial:
        circle2 = plt.Circle((x, y), R + 0.12, color='black', fill=False,
                              linewidth=1.5, zorder=2)
        ax.add_patch(circle2)
    # State name
    ax.text(x, y + 0.2, name, ha='center', va='center',
            fontsize=8, fontweight='bold', zorder=4)
    # Outputs (Moore)
    ax.text(x, y - 0.2, outputs[name], ha='center', va='top',
            fontsize=5.5, zorder=4, color='#333333',
            bbox=dict(boxstyle='round,pad=0.1', fc='white', alpha=0.7, ec='none'))

for name, (x, y) in states.items():
    draw_state(ax, name, x, y, is_initial=(name == 'IDLE'))

# ---- Arrow helper ----
def arrow_between(ax, s1, s2, label='', offset=(0, 0), labelpos=0.5, curve=0.0):
    x1, y1 = states[s1]
    x2, y2 = states[s2]
    dx, dy = x2 - x1, y2 - y1
    dist = np.sqrt(dx**2 + dy**2)
    # Start/end points on circle perimeter
    sx = x1 + dx/dist * R
    sy = y1 + dy/dist * R
    ex = x2 - dx/dist * R
    ey = y2 - dy/dist * R

    if curve == 0.0:
        ax.annotate('', xy=(ex, ey), xytext=(sx, sy),
                    arrowprops=dict(arrowstyle='->', color='black',
                                   lw=1.4, connectionstyle='arc3,rad=0'))
    else:
        ax.annotate('', xy=(ex, ey), xytext=(sx, sy),
                    arrowprops=dict(arrowstyle='->', color='black',
                                   lw=1.4,
                                   connectionstyle=f'arc3,rad={curve}'))
    # Label
    if label:
        mx = sx + (ex - sx) * labelpos + offset[0]
        my = sy + (ey - sy) * labelpos + offset[1]
        ax.text(mx, my, label, ha='center', va='center', fontsize=7,
                style='italic',
                bbox=dict(boxstyle='round,pad=0.15', fc='white', alpha=0.85, ec='none'))

# ---- Transitions ----
# IDLE → CH_SEL
arrow_between(ax, 'IDLE', 'CH_SEL', 'start=1', offset=(-0.3, 0.1), curve=0.15)
# IDLE self-loop (start=0)
cx, cy = states['IDLE']
loop = mpatches.Arc((cx + 0.5, cy + 0.9), 0.7, 0.55,
                    angle=0, theta1=20, theta2=340, color='black', lw=1.2)
ax.add_patch(loop)
ax.annotate('', xy=(cx + 0.18, cy + 0.72), xytext=(cx + 0.82, cy + 0.72),
            arrowprops=dict(arrowstyle='->', color='black', lw=1.2))
ax.text(cx + 0.5, cy + 1.55, 'start=0', ha='center', va='center',
        fontsize=7, style='italic')

# CH_SEL → SAMPLE
arrow_between(ax, 'CH_SEL', 'SAMPLE', '(unconditional)')
# SAMPLE → BIT3
arrow_between(ax, 'SAMPLE', 'BIT3', '(unconditional)')
# BIT3 → BIT2
arrow_between(ax, 'BIT3', 'BIT2', '(evaluate bit3)')
# BIT2 → BIT1
arrow_between(ax, 'BIT2', 'BIT1', '(evaluate bit2)')
# BIT1 → BIT0
arrow_between(ax, 'BIT1', 'BIT0', '(evaluate bit1)', curve=-0.2)
# BIT0 → DONE
arrow_between(ax, 'BIT0', 'DONE', '(evaluate bit0)')
# DONE → IDLE
arrow_between(ax, 'DONE', 'IDLE', '(unconditional)', curve=-0.15)

# Comparator note
ax.text(5.5, 0.3,
        'In BITn states: keep bit n if comp_out=1 (VIN > VDAC), clear if comp_out=0',
        ha='center', va='center', fontsize=8,
        bbox=dict(boxstyle='round,pad=0.3', fc='#f5f5f5', ec='black', lw=1))

# Comparator input annotation
for s in ['BIT3', 'BIT2', 'BIT1', 'BIT0']:
    x, y = states[s]
    ax.text(x - 1.2, y, 'comp_out', ha='center', va='center',
            fontsize=6, color='gray', style='italic')
    ax.annotate('', xy=(x - R, y),
                xytext=(x - 1.0, y),
                arrowprops=dict(arrowstyle='->', color='gray', lw=0.8))

# Legend
ax.text(-0.8, 10.5, 'Legend:', fontsize=8, fontweight='bold')
circle_l = plt.Circle((-0.5, 10.0), 0.25, color='black', fill=True,
                      facecolor='#f0f0f0', linewidth=1.5, zorder=3)
ax.add_patch(circle_l)
ax.text(-0.1, 10.0, '= State (Moore outputs inside)', fontsize=7, va='center')

circle_init = plt.Circle((3.5, 10.0), 0.25, color='black', fill=True,
                         facecolor='#d8d8d8', linewidth=1.5, zorder=3)
ax.add_patch(circle_init)
circle_init2 = plt.Circle((3.5, 10.0), 0.38, color='black', fill=False,
                           linewidth=1.2, zorder=2)
ax.add_patch(circle_init2)
ax.text(3.9, 10.0, '= Initial/Final State', fontsize=7, va='center')

plt.tight_layout()
plt.savefig('fig_fsm_states.png', dpi=150, bbox_inches='tight', facecolor='white')
print("Saved: fig_fsm_states.png")
