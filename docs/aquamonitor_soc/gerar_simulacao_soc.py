"""
gerar_simulacao_soc.py
Post-simulation results for AquaMonitorSoC v1.0
4 subplots: input ramp, DAC tracking, digital code, EOC pulses
14x10, black/white
"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

fig, axes = plt.subplots(4, 1, figsize=(14, 10), sharex=True)
fig.suptitle('AquaMonitorSoC v1.0 — Simulation Results\n'
             '3-Channel SAR ADC · 4-bit · 1MHz ADC Clock · VDD=1.8V',
             fontsize=12, fontweight='bold')

# ---- Time axis ----
# 3 channels × 10 conversions per channel = 30 conversion windows
# Each conversion: ~10 cycles @ 1MHz = 10µs
# Total: 300µs (we'll model as 3 blocks of 100µs each)
t_end = 300  # µs
N_CH  = 3
t     = np.linspace(0, t_end, 3000)

# ---- Input voltages (ramp 0→1.8V per channel) ----
# Each channel is active for 1/3 of the time
# Channel 0 (pH): 0→1.8V
# Channel 1 (cond): 0→1.8V
# Channel 2 (temp): 0→1.8V
vin_ph   = np.linspace(0.0, 1.8, len(t))  # continuous for illustration
vin_cond = np.linspace(0.0, 1.4, len(t))
vin_temp = np.linspace(0.2, 1.6, len(t))

# ================================================================
# Subplot 1: Input voltage ramp
# ================================================================
ax1 = axes[0]
ax1.plot(t, vin_ph,   '-',  color='black',   lw=1.5, label='pH channel')
ax1.plot(t, vin_cond, '--', color='#555555', lw=1.5, label='Conductivity')
ax1.plot(t, vin_temp, ':',  color='#888888', lw=1.5, label='Temperature')
ax1.set_ylabel('VIN (V)', fontsize=10)
ax1.set_ylim(-0.1, 2.1)
ax1.axhline(1.8, color='gray', linestyle=':', lw=1, alpha=0.5, label='VDD=1.8V')
ax1.legend(loc='upper left', fontsize=8, ncol=4)
ax1.grid(True, linestyle=':', alpha=0.5)
ax1.set_title('Input Voltage Ramp — 3 Sensor Channels', fontsize=10, pad=4)
ax1.spines['top'].set_visible(False)
ax1.spines['right'].set_visible(False)

# ================================================================
# Subplot 2: DAC output tracking (staircase)
# ================================================================
ax2 = axes[1]
LSB = 1.8 / 16  # 112.5 mV

def make_stairstep(vin_array, t_array, conv_period=10.0):
    """Generate DAC staircase that tracks the input with SAR quantization."""
    t_out  = []
    v_out  = []
    t_cur  = t_array[0]
    while t_cur < t_array[-1]:
        # Find closest vin sample
        idx  = np.searchsorted(t_array, t_cur)
        if idx >= len(vin_array): break
        vin  = vin_array[idx]
        code = min(int(vin / LSB), 15)
        vq   = code * LSB
        t_out.extend([t_cur, t_cur + conv_period])
        v_out.extend([vq, vq])
        t_cur += conv_period
    return np.array(t_out), np.array(v_out)

t_dac_ph,   v_dac_ph   = make_stairstep(vin_ph,   t, 10.0)
t_dac_cond, v_dac_cond = make_stairstep(vin_cond, t, 10.0)
t_dac_temp, v_dac_temp = make_stairstep(vin_temp, t, 10.0)

ax2.plot(t_dac_ph,   v_dac_ph,   '-',  color='black',   lw=1.2, label='pH DAC out')
ax2.plot(t_dac_cond, v_dac_cond, '--', color='#555555', lw=1.2, label='Cond DAC out')
ax2.plot(t_dac_temp, v_dac_temp, ':',  color='#888888', lw=1.2, label='Temp DAC out')
ax2.plot(t, vin_ph,   '-',  color='black',   lw=0.6, alpha=0.3)
ax2.plot(t, vin_cond, '--', color='#555555', lw=0.6, alpha=0.3)
ax2.plot(t, vin_temp, ':',  color='#888888', lw=0.6, alpha=0.3)
ax2.set_ylabel('VDAC (V)', fontsize=10)
ax2.set_ylim(-0.1, 2.1)
ax2.legend(loc='upper left', fontsize=8, ncol=3)
ax2.grid(True, linestyle=':', alpha=0.5)
ax2.set_title('DAC Output Tracking Input (Staircase Quantization)',
              fontsize=10, pad=4)
ax2.spines['top'].set_visible(False)
ax2.spines['right'].set_visible(False)

# ================================================================
# Subplot 3: Digital code output over time
# ================================================================
ax3 = axes[2]

def make_code_steps(vin_array, t_array, conv_period=10.0):
    """Generate quantized digital code steps."""
    t_out = []
    c_out = []
    t_cur = t_array[0]
    while t_cur < t_array[-1]:
        idx  = np.searchsorted(t_array, t_cur)
        if idx >= len(vin_array): break
        vin  = vin_array[idx]
        code = min(int(vin / LSB), 15)
        t_out.extend([t_cur, t_cur + conv_period])
        c_out.extend([code, code])
        t_cur += conv_period
    return np.array(t_out), np.array(c_out)

t_c_ph,   c_ph   = make_code_steps(vin_ph,   t, 10.0)
t_c_cond, c_cond = make_code_steps(vin_cond, t, 10.0)
t_c_temp, c_temp = make_code_steps(vin_temp, t, 10.0)

ax3.step(t_c_ph,   c_ph,   '-',  where='post', color='black',   lw=1.5, label='pH code')
ax3.step(t_c_cond, c_cond, '--', where='post', color='#555555', lw=1.5, label='Cond code')
ax3.step(t_c_temp, c_temp, ':',  where='post', color='#888888', lw=1.5, label='Temp code')
ax3.set_ylabel('Digital Code\n(0–15)', fontsize=10)
ax3.set_ylim(-1, 17)
ax3.set_yticks([0, 4, 8, 12, 15])
ax3.legend(loc='upper left', fontsize=8, ncol=3)
ax3.grid(True, linestyle=':', alpha=0.5)
ax3.set_title('ADC Output Code — 3 Channels Sequential Conversion',
              fontsize=10, pad=4)
ax3.spines['top'].set_visible(False)
ax3.spines['right'].set_visible(False)

# ================================================================
# Subplot 4: EOC pulses
# ================================================================
ax4 = axes[3]
# EOC fires every 10µs (once per channel conversion)
eoc_times = np.arange(9, t_end, 10)
eoc_signal = np.zeros_like(t)
for et in eoc_times:
    idx = np.searchsorted(t, et)
    if idx < len(eoc_signal):
        eoc_signal[idx] = 1.0
        if idx + 1 < len(eoc_signal):
            eoc_signal[idx + 1] = 1.0

# Plot as vertical lines
for et in eoc_times:
    ax4.plot([et, et], [0, 1], 'k-', lw=1.2)
ax4.set_ylabel('EOC\n(pulse)', fontsize=10)
ax4.set_ylim(-0.1, 1.5)
ax4.set_xlabel('Time (µs)', fontsize=11)

# Annotate which channel each EOC corresponds to
for i, et in enumerate(eoc_times[:15]):
    ch_name = ['pH', 'Cond', 'Temp'][i % 3]
    ax4.text(et, 1.1, ch_name, ha='center', va='bottom',
             fontsize=5.5, rotation=90, color='#444444')

ax4.set_title('EOC Pulses — End-of-Conversion (10µs interval)',
              fontsize=10, pad=4)
ax4.grid(True, axis='x', linestyle=':', alpha=0.5)
ax4.spines['top'].set_visible(False)
ax4.spines['right'].set_visible(False)

# ---- Shared x-axis ----
axes[3].set_xlim(0, t_end)
for ax in axes:
    ax.axvline(100, color='gray', linestyle='--', lw=0.8, alpha=0.4)
    ax.axvline(200, color='gray', linestyle='--', lw=0.8, alpha=0.4)

axes[0].text(50,  1.95, 'Cycle 1→100µs', ha='center', fontsize=7, color='gray')
axes[0].text(150, 1.95, 'Cycle 101→200µs', ha='center', fontsize=7, color='gray')
axes[0].text(250, 1.95, 'Cycle 201→300µs', ha='center', fontsize=7, color='gray')

plt.tight_layout(rect=[0, 0, 1, 0.95])
plt.savefig('fig_sim_soc.png', dpi=150, bbox_inches='tight', facecolor='white')
print("Saved: fig_sim_soc.png")
