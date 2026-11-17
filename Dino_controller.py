
import soundcard as sc
import numpy as np
import pyautogui

# ==========================
# AUDIO CONFIGURATION
# ==========================

SAMPLE_RATE = 44100
CHUNK_SIZE = 4096

# ==========================
# DETECTION CONFIGURATION
# ==========================

# System audio RMS is normalized between 0 and 1
VOLUME_THRESHOLD = 0.04

# Frequency range used for ducking
HUMMING_MIN_FREQ = 80
HUMMING_MAX_FREQ = 250

# Minimum audio level required for frequency detection
MIN_HUMMING_VOLUME = 0.015

# ==========================
# DETECTION STATES
# ==========================

is_loud = False
is_humming = False

# ==========================
# AUDIO DEVICE SETUP
# ==========================

speaker = sc.default_speaker()

loopback = sc.get_microphone(
    id=str(speaker.name),
    include_loopback=True
)

print(f"Capturing audio from: {speaker.name}")
print("Speak loudly in the video to jump.")
print("Play low-pitched humming to duck.")
print("Press CTRL+C to stop.")

# ==========================
# AUDIO PROCESSING
# ==========================

try:
    with loopback.recorder(
        samplerate=SAMPLE_RATE,
        channels=2
    ) as recorder:

        while True:

            # Capture system audio
            data = recorder.record(numframes=CHUNK_SIZE)

            # Convert stereo audio to mono
            samples = np.mean(data, axis=1)

            # Calculate RMS volume
            rms = np.sqrt(np.mean(samples ** 2))

            # Calculate FFT
            fft_values = np.fft.rfft(samples)
            magnitudes = np.abs(fft_values)

            # Calculate corresponding frequencies
            frequencies = np.fft.rfftfreq(
                len(samples),
                1 / SAMPLE_RATE
            )

            # Ignore DC component
            magnitudes[0] = 0

            # Find dominant frequency
            dominant_index = np.argmax(magnitudes)
            dominant_frequency = frequencies[dominant_index]

            # ==========================
            # JUMP DETECTION
            # ==========================

            if rms > VOLUME_THRESHOLD and not is_loud:

                print("JUMP!")

                pyautogui.press("space")

                is_loud = True

            elif rms <= VOLUME_THRESHOLD:

                is_loud = False

            # ==========================
            # DUCK DETECTION   

            humming_detected = (
                HUMMING_MIN_FREQ <= dominant_frequency <= HUMMING_MAX_FREQ
                and rms > MIN_HUMMING_VOLUME
            )

            if humming_detected and not is_humming:

                print("DUCK!")

                pyautogui.keyDown("down")

                is_humming = True

            elif not humming_detected and is_humming:

                print("STOP DUCKING!")

                pyautogui.keyUp("down")

                is_humming = False

            # ==========================
            # DEBUG INFORMATION
            # ==========================

            print(
                f"Volume: {rms:.4f} | "
                f"Frequency: {dominant_frequency:.1f} Hz"
            )

except KeyboardInterrupt:

    print("\nStopping Dino controller...")

finally:

    # Release keys if they are still held
    pyautogui.keyUp("down")
    pyautogui.keyUp("space")

    print("Controller stopped.")
