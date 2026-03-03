# Reworked version of the Lab 4.ipnyb file by the Colorado School of Mines Physics Department
# Optimized for use in Microsoft Visual Studio Code


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# ============================================================
# SECTION 3 — SINGLE WAVEFORM (TEK0000.CSV type file)
# ============================================================

print("\n========== SECTION 3 ==========\n")

filename = 'TEK0000.CSV'   # Change name/directory if needed. Ideally keep the data files in the same folder as the code

# Detect oscilloscope format
with open(filename, 'r') as file:
    first_line = file.readline()

if first_line == "Model,TBS1052C\n":
    waveform = pd.read_csv(
        filename,
        header=14,
        index_col=0,
        names=['Time(s)', 'V']
    )
else:
    waveform = pd.read_csv(
        filename,
        header=None,
        usecols=[3, 4],
        index_col=0,
        names=['Time(s)', 'V']
    )

# Plot waveform
plt.figure()
plt.plot(waveform.index, waveform['V'])
plt.title("Captured Waveform")
plt.xlabel("Time (s)")
plt.ylabel("Voltage (V)")
plt.grid(True)
plt.show()

# Peak-to-Peak
PP = waveform['V'].max() - waveform['V'].min()

# Frequency Calculation
crossings = np.where(np.diff(np.signbit(waveform['V']).astype(int)) < 0)[0]
period = np.mean(np.diff(crossings)) * np.mean(np.diff(waveform.index))
frequency = 1 / period

print("Peak-to-Peak Voltage: {:.4f} V".format(PP))
print("Period: {:.6f} s".format(period))
print("Frequency: {:.4f} Hz".format(frequency))


# ============================================================
# SECTION 4 — TWO WAVEFORMS (F0000CH1.CSV & F0000CH2.CSV)
# ============================================================

print("\n========== SECTION 4 ==========\n")

file_ch1 = 'F0000CH1.CSV' # Change file names and directories as needed
file_ch2 = 'F0000CH2.CSV'

ch1 = pd.read_csv(
    file_ch1,
    header=None,
    usecols=[3, 4],
    index_col=0,
    names=['Time (s)', 'V_CH1']
)

ch2 = pd.read_csv(
    file_ch2,
    header=None,
    usecols=[3, 4],
    index_col=0,
    names=['Time (s)', 'V_CH2']
)

waveforms = ch1.join(ch2)

# Plot both waveforms together
plt.figure()
plt.plot(waveforms.index, waveforms['V_CH1'])
plt.plot(waveforms.index, waveforms['V_CH2'])
plt.title("CH1 and CH2")
plt.xlabel("Time (s)")
plt.ylabel("Voltage (V)")
plt.legend(["CH1", "CH2"])
plt.grid(True)
plt.show()

# Peak-to-Peak for both
PP = {}
for column in waveforms.columns:
    PP[column] = waveforms[column].max() - waveforms[column].min()

# Phase Shift Calculation
crossings = {}
w = np.hanning(10)

for column in waveforms.columns:
    smoothed = np.convolve(w / w.sum(), waveforms[column], mode='valid')
    crossings[column] = np.where(np.diff(np.signbit(smoothed).astype(int)) < 0)[0]

l = min(len(crossings['V_CH1']), len(crossings['V_CH2']))

samples_shift = np.mean(
    crossings['V_CH1'][:l] - crossings['V_CH2'][:l]
)

period_samples = np.mean(np.diff(crossings['V_CH1']))

phase_shift = -360 * samples_shift / period_samples

# Print results
print("Peak-to-Peak Voltages:")
for k, v in PP.items():
    print(f"{k}: {v:.4f} V")

print("\nPhase Shift: {:.4f} degrees".format(phase_shift))