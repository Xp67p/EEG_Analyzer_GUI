import pandas as pd
import matplotlib.pyplot as plt
from scipy.signal import butter, filtfilt
import numpy as np
import os

FS = 160  # sampling rate


def load_eeg(file_path, channel='O1..'):  # Load EEG function
    df = pd.read_csv(file_path)
    return df[channel].values


def bandpass(data, lowcut, highcut, fs=FS, order=4):  # Bandpass filter
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = butter(order, [low, high], btype='band')
    return filtfilt(b, a, data)  # zero-phase filtering


def compute_power(signal):  # Compute band power
    return np.mean(signal ** 2)


# folders
closed_folder = r"C:\Users\Xp677\Desktop\EEG_Analyzer_GUI\data\closed"
open_folder   = r"C:\Users\Xp677\Desktop\EEG_Analyzer_GUI\data\open"

# preload signals (fast version)
closed_signals = []
open_signals = []

for filename in os.listdir(closed_folder):
    if filename.endswith(".csv"):
        closed_signals.append(load_eeg(os.path.join(closed_folder, filename)))

for filename in os.listdir(open_folder):
    if filename.endswith(".csv"):
        open_signals.append(load_eeg(os.path.join(open_folder, filename)))


# band dictionary
bands = {
    "Delta": (0.5, 4),
    "Theta": (4, 8),
    "Alpha": (8, 13),
    "Beta": (13, 30),
    "Gamma": (30, 45)
}

# global dict so GUI can import them
closed_avg_band = {}
open_avg_band = {}

# compute mean power for each band
for name, (low, high) in bands.items():
    closed_vals = []
    open_vals = []

    for sig in closed_signals:
        filtered = bandpass(sig, low, high)
        closed_vals.append(compute_power(filtered))

    for sig in open_signals:
        filtered = bandpass(sig, low, high)
        open_vals.append(compute_power(filtered))

    closed_avg_band[name] = np.mean(closed_vals)
    open_avg_band[name]   = np.mean(open_vals)


# ============================================================
# Everything BELOW runs ONLY when running this file directly
# ============================================================
if __name__ == "__main__":

    # Load one example pair
    closed_signal = load_eeg(r"C:\Users\Xp677\Desktop\EEG_Analyzer_GUI\data\closed\S001.csv")
    open_signal   = load_eeg(r"C:\Users\Xp677\Desktop\EEG_Analyzer_GUI\data\open\S001.csv")

    # Extract alpha band
    closed_alpha = bandpass(closed_signal, 8, 13)
    open_alpha   = bandpass(open_signal, 8, 13)

    closed_power = compute_power(closed_alpha)
    open_power   = compute_power(open_alpha)

    print("Closed Eyes Alpha Power:", closed_power)
    print("Open Eyes Alpha Power:", open_power)

    plt.bar(["Closed", "Open"], [closed_power, open_power])
    plt.title("Alpha Power Comparison (Single Subject)")
    plt.ylabel("Mean squared amplitude")
    plt.show()

    # Multi-subject alpha averages
    closed_powers = []
    open_powers   = []

    for sig in closed_signals:
        closed_powers.append(compute_power(bandpass(sig, 8, 13)))

    for sig in open_signals:
        open_powers.append(compute_power(bandpass(sig, 8, 13)))

    closed_avg = np.mean(closed_powers)
    open_avg   = np.mean(open_powers)

    print("Average Closed Alpha:", closed_avg)
    print("Average Open Alpha:", open_avg)

    plt.bar(["Closed Avg", "Open Avg"], [closed_avg, open_avg])
    plt.title("Average Alpha Power Across All Subjects")
    plt.ylabel("Mean squared amplitude")
    plt.show()

    # Band-wise visualization
    bands_list = list(bands.keys())
    closed_vals_plot = [closed_avg_band[b] for b in bands_list]
    open_vals_plot   = [open_avg_band[b] for b in bands_list]

    x = np.arange(len(bands_list))
    width = 0.35

    plt.figure(figsize=(8, 5))
    plt.bar(x - width/2, closed_vals_plot, width, label="Closed")
    plt.bar(x + width/2, open_vals_plot,   width, label="Open")

    plt.xticks(x, bands_list)
    plt.ylabel("Mean power")
    plt.title("Band-wise Power Comparison")
    plt.legend()
    plt.grid(axis="y", alpha=0.3)
    plt.show()
