
import pyaudio

# Initialize PyAudio
audio = pyaudio.PyAudio()

# Audio configuration
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 1024

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
        data = stream.read(CHUNK)
        print("Audio captured:", len(data), "bytes")

except KeyboardInterrupt:
    print("\nStopping microphone...")

finally:
    stream.stop_stream()
    stream.close()
    audio.terminate()
