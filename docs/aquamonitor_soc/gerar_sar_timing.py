"""
gerar_sar_timing.py
SAR ADC timing waveform — 2 complete conversions
pH=0110 (6), cond=1001 (9)
16x8 figure, black/white grid
"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

fig, axes = plt.subplots(8, 1, figsize=(16, 8), sharex=True)
fig.suptitle('SAR ADC Timing Diagram — AquaMonitorSoC v1.0\n'
             'Conversion 1: pH channel (code=0110)   Conversion 2: Cond channel (code=1001)',
             fontsize=11, fontweight='bold')

# Time axis: 20 clock cycles per conversion, 2 conversions = 40 cycles + gap
T = 40  # total time units

def draw_digital(ax, times, values, label, ylow=0, yhigh=1, color='black'):
    """Draw a digital waveform."""
    t_plot = [times[0]]
    v_plot = [values[0]]
    for i in range(1, len(times)):
        t_plot.append(times[i])
        t_plot.append(times[i])
        v_plot.append(v_plot[-1])
        v_plot.append(values[i])
    t_plot.append(T)
    v_plot.append(v_plot[-1])
    ax.step(t_plot, v_plot, where='post', color=color, lw=1.5)
    ax.fill_between(t_plot, ylow, v_plot, step='post', alpha=0.15, color=color)
    ax.set_ylabel(label, fontsize=8, rotation=0, ha='right', va='center', labelpad=60)
    ax.set_ylim(ylow - 0.2, yhigh + 0.4)
    ax.set_yticks([])
    ax.grid(axis='x', linestyle=':', color='gray', alpha=0.5)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

def draw_bus(ax, times, values, label, color='black'):
    """Draw a bus signal (multi-bit) as a band."""
    ax.set_ylabel(label, fontsize=8, rotation=0, ha='right', va='center', labelpad=60)
    ax.set_ylim(-0.1, 1.1)
    ax.set_yticks([])
    ax.grid(axis='x', linestyle=':', color='gray', alpha=0.5)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    # Draw as hatched rectangle segments
    for i in range(len(times) - 1):
        t0, t1 = times[i], times[i+1]
        val = values[i]
        ax.fill_between([t0, t1], 0.1, 0.9, color='lightgray', alpha=0.7)
        ax.plot([t0, t0], [0.1, 0.9], 'k-', lw=1.2)
        ax.plot([t1, t1], [0.1, 0.9], 'k-', lw=1.2)
        ax.plot([t0, t1], [0.1, 0.1], 'k-', lw=1.0)
        ax.plot([t0, t1], [0.9, 0.9], 'k-', lw=1.0)
        ax.text((t0 + t1)/2, 0.5, val, ha='center', va='center',
                fontsize=7, fontweight='bold')

# ---- CLK (0) ----
ax = axes[0]
clk_t = list(range(0, T+1))
clk_v = [(i % 2) for i in range(T+1)]
draw_digital(ax, clk_t, clk_v, 'CLK\n(1MHz)')
ax.axvline(x=20, color='gray', linestyle='--', lw=1, alpha=0.7)

# ---- START (1) ----
ax = axes[1]
start_t = [0, 1, 2, 21, 22]
start_v = [0, 1, 0,  1,  0]
draw_digital(ax, start_t, start_v, 'START')

# ---- CH_SEL[1:0] (2) ----
ax = axes[2]
ch_times = [0, 2,  22, 40]
ch_vals  = ['--', 'CH0\n(pH)', 'CH1\n(Cond)', '--']
draw_bus(ax, ch_times, ch_vals, 'CH_SEL\n[1:0]')

# ---- SAMPLE_EN (3) ----
ax = axes[3]
se_t = [0, 3, 4,  23, 24, 40]
se_v = [0, 1, 0,   1,  0,  0]
draw_digital(ax, se_t, se_v, 'SAMPLE\n_EN')

# ---- DAC_CODE[3:0] (4) — SAR approximation steps ----
ax = axes[4]
# Conversion 1: pH=0110 (6)  → trial: 8→4→6→6→6
dac_times = [0,  4,  5,   6,   7,   8,   9,
             20, 24, 25,  26,  27,  28,  29, 40]
dac_vals  = ['0000', '1000', '0100', '0110', '0110', '0110', '0110',
             '----',
             '1000', '1001', '1001', '1001', '1001', '1001', '1001']
draw_bus(ax, dac_times, dac_vals, 'DAC_CODE\n[3:0]')

# ---- COMP_OUT (5) ----
ax = axes[5]
# For pH=6 (6/16*1800=675mV): 8→0 (8>6 → no), 4→1 (4<6 → yes), 6→0 (6=6 → borderline)
co_t = [0, 4, 5,   6, 7,  8, 9,
        20, 24, 25, 26, 27, 28, 29, 40]
co_v = [0, 0, 1,   0, 0,  0, 0,
         0, 0, 1,  1,  1,  1,  1,  1]
draw_digital(ax, co_t, co_v, 'COMP\n_OUT')

# ---- EOC (6) ----
ax = axes[6]
eoc_t = [0, 8, 9,  28, 29, 40]
eoc_v = [0, 1, 0,   1,  0,  0]
draw_digital(ax, eoc_t, eoc_v, 'EOC')

# ---- RESULT[3:0] (7) ----
ax = axes[7]
res_times = [0, 9,       29,    40]
res_vals  = ['----', '0110\n(pH=6)', '1001\n(Cond=9)', '----']
draw_bus(ax, res_times, res_vals, 'RESULT\n[3:0]')

# ---- X-axis labels ----
axes[7].set_xlabel('ADC Clock Cycles (1 MHz → 1µs per cycle)', fontsize=9)
axes[7].set_xlim(0, T)
axes[7].set_xticks(range(0, T+1, 2))
axes[7].set_xticklabels([str(i) for i in range(0, T+1, 2)], fontsize=7)

# Conversion annotations
for ax in axes:
    ax.axvline(x=2, color='black', linestyle=':', lw=0.8, alpha=0.4)
    ax.axvline(x=8, color='black', linestyle=':', lw=0.8, alpha=0.4)
    ax.axvline(x=22, color='black', linestyle=':', lw=0.8, alpha=0.4)
    ax.axvline(x=28, color='black', linestyle=':', lw=0.8, alpha=0.4)

axes[0].text(5, 1.25, 'Conversion 1: pH channel', ha='center', fontsize=8,
             style='italic', color='#333333')
axes[0].text(25, 1.25, 'Conversion 2: Conductivity channel', ha='center',
             fontsize=8, style='italic', color='#333333')

# State annotations
state_labels = [
    (2, 'CH_SEL'), (3, 'SAMPLE'), (4, 'BIT3'), (5, 'BIT2'),
    (6, 'BIT1'), (7, 'BIT0'), (8, 'DONE')
]
for t, lbl in state_labels:
    axes[3].text(t + 0.5, 1.2, lbl, ha='center', fontsize=6, color='gray', rotation=45)

plt.tight_layout(rect=[0.08, 0, 1, 0.93])
plt.savefig('fig_sar_timing.png', dpi=150, bbox_inches='tight', facecolor='white')
print("Saved: fig_sar_timing.png")
