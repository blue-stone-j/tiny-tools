'''
key points of this snippet
1. read data from csv file, the first row is header, use comma as seperator.
2. skip specific column
3. display the frequency spectra in one figure but on separate subplots

example data is large, you can download it here: https://drive.google.com/file/d/1i0SWkAqjVtyhPyeIDyAsQVO6KHhGkOtY/view?usp=drive_link
'''
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Read the CSV file
file_path = "../data/1d_fast_fourier_transform.csv"  # Replace with your file path
data = pd.read_csv(file_path)

# Display headers to verify columns
print("Headers:", data.columns)

# Skip specific columns if needed (optional)
columns_to_skip = ['SkipColumn1', 'SkipColumn2']  # Replace with actual names
columns_to_process = [col for col in data.columns if col not in columns_to_skip]

# Set parameters for FFT
sampling_rate = 1000  # Adjust this based on your data's sampling rate

# Set up grid dimensions
num_columns = min(len(columns_to_process), 6)  # No more than 6 subplots
rows = 2
cols = 3

# Create the figure and axes
fig, axs = plt.subplots(rows, cols, figsize=(15, 10))  # Adjust figure size as needed
axs = axs.flatten()  # Flatten the 2D array of axes for easy iteration

# Process each column
for idx, column in enumerate(columns_to_process):
    if idx >= len(axs):  # Skip additional columns if subplots are full
        print(f"Skipping column '{column}' because there are more than 6 columns.")
        break
    
    print(f"Processing column: {column}")
    
    # Convert the column to numeric, coercing errors to NaN
    series = pd.to_numeric(data[column], errors='coerce')
    
    # Drop NaN values to ensure valid numeric input
    series = series.dropna().to_numpy()
    
    if len(series) == 0:
        print(f"Skipping column '{column}' because it has no valid numeric data.")
        continue

    # FFT computation
    fft_result = np.fft.fft(series)
    frequencies = np.fft.fftfreq(len(series), d=1/sampling_rate)
    magnitude = np.abs(fft_result)
    
    # Keep only the positive frequencies
    positive_freqs = frequencies[:len(frequencies)//2]
    positive_magnitude = magnitude[:len(magnitude)//2]
    
    # Plot the frequency spectrum in the corresponding subplot
    axs[idx].plot(positive_freqs, positive_magnitude)
    axs[idx].set_title(f"Frequency Spectrum of {column}")
    axs[idx].set_xlabel("Frequency (Hz)")
    axs[idx].set_ylabel("Amplitude")
    axs[idx].grid()

# Hide unused subplots
for ax in axs[len(columns_to_process):]:
    ax.set_visible(False)

# Adjust layout to prevent overlap
plt.tight_layout()
plt.show()

