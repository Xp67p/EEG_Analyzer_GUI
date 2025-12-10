import pandas as pd
import matplotlib.pyplot as plt
from scipy.signal import butter,filtfilt
import numpy as np


FS = 160                                #samplingrate/how fast data was sampled


def load_eeg(file_path, channel='O1..'):                #Load EEG function
    df = pd.read_csv(file_path)
    return df[channel].values

def bandpass(data, lowcut, highcut, fs=FS, order=4):    #Bandpass filter
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = butter(order, [low, high], btype='band')
    return filtfilt(b, a, data)   # Apply zero-phase filtering (no time shift)

def compute_power(signal):     #Compute band power
    return np.mean(signal ** 2)


# Load one open and closed file
closed_signal = load_eeg(r"C:\Users\Xp677\Desktop\University\Signals & Systems\EEG_dataset\closed\S001.csv")
open_signal   = load_eeg(r"C:\Users\Xp677\Desktop\University\Signals & Systems\EEG_dataset\open\S001.csv")

# Extract alpha band (8-13 Hz)
closed_alpha = bandpass(closed_signal, 8, 13)
open_alpha   = bandpass(open_signal, 8, 13)

# Compute alpha power
closed_power = compute_power(closed_alpha)
open_power   = compute_power(open_alpha)

print("Closed Eyes Alpha Power:", closed_power)
print("Open Eyes Alpha Power:", open_power)

# Simple bar comparison
plt.bar(["Closed", "Open"], [closed_power, open_power], color=["blue","orange"])
plt.title("Alpha Power Comparison")
plt.ylabel("Power (Mean squared amplitude)")
plt.show()
