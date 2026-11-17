
import soundcard as sc
import numpy as np

# Audio configuration
SAMPLE_RATE = 44100
CHUNK_SIZE = 4096

# Get the default speaker (playback device)
speaker = sc.default_speaker()

# Get the loopback microphone associated with that speaker
loopback = sc.get_microphone(
    id=str(speaker.name),
    include_loopback=True
)

print(f"Capturing system audio from: {speaker.name}")
print("Play a YouTube video to test audio capture.")
print("Press CTRL+C to stop.")

try:
    with loopback.recorder(
        samplerate=SAMPLE_RATE,
        channels=2
    ) as recorder:

        while True:
            # Capture system audio
            data = recorder.record(numframes=CHUNK_SIZE)

            # Convert to mono
            samples = np.mean(data, axis=1)

            # Calculate RMS volume
            rms = np.sqrt(np.mean(samples ** 2))

            # Calculate FFT
            fft_values = np.fft.rfft(samples)
            magnitudes = np.abs(fft_values)

            # Corresponding frequencies
            frequencies = np.fft.rfftfreq(
                len(samples),
                1 / SAMPLE_RATE
            )

            # Ignore DC component
            magnitudes[0] = 0

            # Find dominant frequency
            dominant_index = np.argmax(magnitudes)
            dominant_frequency = frequencies[dominant_index]

            print(
                f"Volume: {rms:.5f} | "
                f"Frequency: {dominant_frequency:.1f} Hz"
            )

except KeyboardInterrupt:
    print("\nStopping system audio capture...")
