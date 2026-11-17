
import pyaudio
import numpy as np
import pyautogui

# Initialize PyAudio
audio = pyaudio.PyAudio()

# Audio configuration
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 4096

# Voice detection configuration
VOLUME_THRESHOLD = 1500

# Humming frequency configuration (Hz)
HUMMING_MIN_FREQ = 80
HUMMING_MAX_FREQ = 220

# Detection states
is_loud = False
is_humming = False

# Open microphone stream
stream = audio.open(
    format=FORMAT,
    channels=CHANNELS,
    rate=RATE, 
    input=True,
    frames_per_buffer=CHUNK
)

print("Listening... Press CTRL+C to stop.")
print("Speak loudly to jump and hum to duck!")

try:
    while True:
        # Capture audio
        data = stream.read(CHUNK, exception_on_overflow=False)

        # Convert audio bytes into numerical samples
        samples = np.frombuffer(data, dtype=np.int16).astype(np.float32)

        # Calculate RMS volume
        rms = np.sqrt(np.mean(samples ** 2))

        # Calculate FFT
        fft_values = np.fft.rfft(samples)
        magnitudes = np.abs(fft_values)

        # Get corresponding frequencies
        frequencies = np.fft.rfftfreq(len(samples), 1 / RATE)

        # Ignore DC component
        magnitudes[0] = 0

        # Find dominant frequency
        dominant_index = np.argmax(magnitudes)
        dominant_frequency = frequencies[dominant_index]

        # Detect humming
        humming_detected = (
            HUMMING_MIN_FREQ <= dominant_frequency <= HUMMING_MAX_FREQ
            and rms > 300
        )

        # Detect loud voice for jumping
        if rms > VOLUME_THRESHOLD and not is_loud:
            print("JUMP!")
            pyautogui.press("space")
            is_loud = True

        elif rms <= VOLUME_THRESHOLD:
            is_loud = False

        # Detect humming for ducking
        if humming_detected and not is_humming:
            print("DUCK!")
            pyautogui.keyDown("down")
            is_humming = True

        elif not humming_detected and is_humming:
            print("STOP DUCKING!")
            pyautogui.keyUp("down")
            is_humming = False

        print(
            f"Volume: {rms:.0f} | "
            f"Frequency: {dominant_frequency:.1f} Hz"
        )

except KeyboardInterrupt:
    print("\nStopping microphone...")

finally:
    # Release keys in case they are still held
    pyautogui.keyUp("down")

    stream.stop_stream()
    stream.close()
    audio.terminate()
