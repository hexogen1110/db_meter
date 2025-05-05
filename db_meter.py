import sounddevice as sd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from collections import deque

# Configuration
SAMPLE_RATE = 44100  # Hz
DURATION = 0.1       # seconds
WINDOW_SIZE = 100    # Number of points to keep in plot

# Data buffer
db_history = deque([0]*WINDOW_SIZE, maxlen=WINDOW_SIZE)

# Calculate dB from audio samples
def calculate_db_level(indata):
    rms = np.sqrt(np.mean(indata**2))
    return 20 * np.log10(rms) if rms > 0 else -np.inf

# Audio callback function
def audio_callback(indata, frames, time, status):
    db = calculate_db_level(indata)
    db_history.append(db)

# Animation update
def update_plot(frame):
    ydata = list(db_history)
    line.set_ydata(ydata)

    # Calculate stats
    max_db = max(ydata)
    avg_db = np.mean(ydata)

    # Update max line
    max_line.set_ydata([max_db] * len(x))
    max_text.set_text(f"Max: {max_db:.1f} dB")
    max_text.set_position((x[0], max_db + 1))

    # Update avg line
    avg_line.set_ydata([avg_db] * len(x))
    avg_text.set_text(f"Avg: {avg_db:.1f} dB")
    avg_text.set_position((x[0], avg_db + 1))

    return line, max_line, avg_line, max_text, avg_text

# Set up plot
fig, ax = plt.subplots()
x = np.linspace(-WINDOW_SIZE * DURATION, 0, WINDOW_SIZE)

# Main line
line, = ax.plot(x, list(db_history), label='dB Level')

# Max and Avg lines
max_line, = ax.plot(x, [0]*WINDOW_SIZE, 'r-', label='Max dB')
avg_line, = ax.plot(x, [0]*WINDOW_SIZE, 'b--', label='Avg dB')

# Text labels
max_text = ax.text(x[0], 0, '', color='red', fontsize=10)
avg_text = ax.text(x[0], 0, '', color='blue', fontsize=10)

# Axis setup
ax.set_ylim(-100, 0)
ax.set_xlim(x[0], x[-1])
ax.set_xlabel('Time (s)')
ax.set_ylabel('dB Level')
ax.set_title('Live Microphone dB Level')
ax.legend(loc='lower right')

# Start audio stream and plot
def main():
    with sd.InputStream(callback=audio_callback, channels=1, samplerate=SAMPLE_RATE,
                        blocksize=int(SAMPLE_RATE * DURATION)):
        ani = animation.FuncAnimation(fig, update_plot, interval=DURATION*1000, blit=True)
        plt.show()

if __name__ == "__main__":
    main()
