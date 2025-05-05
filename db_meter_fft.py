import sounddevice as sd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.widgets import Slider

# Config
SAMPLE_RATE = 44100
DURATION = 0.1
FFT_SIZE = int(SAMPLE_RATE * DURATION)
HISTORY_LENGTH = 100  # Number of time steps in spectrogram
LOW_FREQ = 100
HIGH_FREQ = 15000

# Data buffers
audio_buffer = np.zeros(FFT_SIZE)
fft_history = []

# Threshold (can be changed with slider)
threshold_db = -80

# Callback for audio input
def audio_callback(indata, frames, time, status):
    global audio_buffer
    if status:
        print(status)
    audio_buffer = indata[:, 0]

# Compute FFT and convert to dB
def compute_fft(audio_data):
    windowed = audio_data * np.hanning(len(audio_data))
    fft = np.fft.rfft(windowed)
    magnitude_db = 20 * np.log10(np.abs(fft) + 1e-6)
    return magnitude_db

# Update plot
def update_plot(frame):
    global fft_history, threshold_db

    fft_slice = compute_fft(audio_buffer)
    #fft_slice = np.clip(fft_slice, threshold_db, 0)  # clip to hide low-magnitude
    # Filter by frequency
    freq_mask = (freqs >= LOW_FREQ) & (freqs <= HIGH_FREQ)
    fft_slice = fft_slice[freq_mask]
    filtered_freqs = freqs[freq_mask]
    
    if len(fft_history) >= HISTORY_LENGTH:
        fft_history.pop(0)
    fft_history.append(fft_slice)

    # Update spectrogram
    img.set_data(np.rot90(fft_history))
    img.set_clim(vmin=threshold_db, vmax=0)
    return [img]

# Handle slider change
def update_threshold(val):
    global threshold_db
    threshold_db = slider.val

# Prepare figure
fig, ax = plt.subplots()
plt.subplots_adjust(bottom=0.2)

# Prepare frequency & time axes
freqs = np.fft.rfftfreq(FFT_SIZE, 1/SAMPLE_RATE)
time_extent = HISTORY_LENGTH * DURATION

# Spectrogram image init
img = ax.imshow(np.zeros((len(freqs), HISTORY_LENGTH)), 
                aspect='auto', origin='lower',
                extent=[-time_extent, 0, freqs[0], freqs[-1]],
                cmap='inferno', vmin=threshold_db, vmax=0)

ax.set_xlabel("Time (s ago)")
ax.set_ylabel("Frequency (Hz)")
ax.set_title("Live Spectrogram (0–15000 Hz)")

# Add slider for dB threshold
ax_slider = plt.axes([0.25, 0.05, 0.5, 0.03])
slider = Slider(ax_slider, 'dB Threshold', -100, -20, valinit=threshold_db)
slider.on_changed(update_threshold)

# Start stream and animation
def main():
    with sd.InputStream(callback=audio_callback, channels=1,
                        samplerate=SAMPLE_RATE, blocksize=FFT_SIZE):
        ani = FuncAnimation(fig, update_plot, interval=DURATION*1000, blit=True)
        plt.show()

if __name__ == "__main__":
    main()
