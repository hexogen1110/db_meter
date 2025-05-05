# 🎤 Real-Time Audio Meter Tools

This project contains two simple real-time audio monitoring tools built with Python:

1. **`db_meter.py`** – A live microphone dB level plotter.
2. **`db_meter_fft.py`** – A real-time spectrogram visualizer with adjustable dB threshold.

## 🛠️ Requirements

Make sure to install the following Python packages:

```bash
pip install sounddevice numpy matplotlib
```

## 📈 Tool Descriptions

### 1. `db_meter.py` – dB Meter

- Continuously measures microphone input volume and displays it in decibels (dB).
- Shows a live plot with:
  - Current dB level
  - Max and average values
- Uses Matplotlib animation to update in real-time.

#### Run:

```bash
python db_meter.py
```

---

### 2. `db_meter_fft.py` – Live Spectrogram

- Displays a real-time frequency spectrogram up to 15,000 Hz.
- Computes FFT from microphone input every 0.1 seconds.
- Converts magnitudes to dB scale.
- Includes a slider to adjust the dB threshold shown in the spectrogram.

#### Run:

```bash
python db_meter_fft.py
```

## 🎧 Notes

- Requires a working microphone.
- Ensure your operating system allows microphone access for Python.
- On some systems (e.g., macOS), you may need to grant additional permissions.

## 📄 License

This project is provided for educational and research purposes. You are free to use and modify it.
