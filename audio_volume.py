
import pyaudio
import numpy as np

# Initialize PyAudio
audio = pyaudio.PyAudio()

# Audio configuration
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 1024

# Voice detection configuration
THRESHOLD = 2000
is_loud = False

# Open microphone stream
stream = audio.open(
    format=FORMAT,
    channels=CHANNELS,
    rate=RATE,
    input=True,
    frames_per_buffer=CHUNK
)

print("Listening... Press CTRL+C to stop.")

try:
    while True:
        data = stream.read(CHUNK, exception_on_overflow=False)

        samples = np.frombuffer(data, dtype=np.int16)

        rms = np.sqrt(np.mean(samples.astype(np.float32) ** 2))

        if rms > THRESHOLD and not is_loud:
            print("VOICE DETECTED!")
            is_loud = True

        elif rms <= THRESHOLD:
            is_loud = False

        print(f"Volume: {rms:.2f}")

except KeyboardInterrupt:
    print("\nStopping microphone...")

finally:
    stream.stop_stream()
    stream.close()
    audio.terminate()
