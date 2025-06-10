# audio_utils/generation.py

import numpy as np
import librosa # For more advanced audio manipulation if needed

# Assuming these might be useful for a lullaby context
DEFAULT_SAMPLE_RATE = 44100
DEFAULT_DURATION_PER_CHAR = 0.5  # seconds
DEFAULT_NOTE_FREQ = 440.0  # A4 note

def text_to_basic_sound(text, char_duration=DEFAULT_DURATION_PER_CHAR, sample_rate=DEFAULT_SAMPLE_RATE):
    """
    Generates a very basic sound representation of text.
    Each character becomes a short tone.
    This is a highly simplified placeholder.
    """
    total_duration = len(text) * char_duration
    t = np.linspace(0, total_duration, int(total_duration * sample_rate), endpoint=False)
    audio_signal = np.zeros_like(t)

    current_time = 0
    for char_code in [ord(c) for c in text]:
        # Map character code to a frequency (very basic mapping)
        # Ensure frequency is within a listenable range, e.g., 100Hz to 1000Hz
        freq = np.interp(char_code, [ord('a'), ord('z')], [200, 800]) # Example for lowercase letters
        freq = np.clip(freq, 100, 1000) # Clip to a reasonable range

        # Generate a sine wave for this character's duration
        char_t_end = current_time + char_duration
        char_t = np.linspace(current_time, char_t_end, int(char_duration * sample_rate), endpoint=False)

        # Ensure char_t is not empty
        if char_t.size > 0:
            # Apply a simple envelope to avoid clicks
            envelope = 0.5 * (1 - np.cos(2 * np.pi * np.arange(char_t.size) / char_t.size))

            # Find indices in the main timeline t that correspond to char_t
            start_idx = int(current_time * sample_rate)
            end_idx = int(char_t_end * sample_rate)

            if end_idx > start_idx and end_idx <= audio_signal.shape[0]: # Ensure indices are valid
                 audio_signal[start_idx:end_idx] += envelope * 0.5 * np.sin(2 * np.pi * freq * (char_t - current_time))

        current_time = char_t_end

    # Normalize
    if np.max(np.abs(audio_signal)) > 0:
        audio_signal /= np.max(np.abs(audio_signal))

    return audio_signal

def load_background_music(filepath):
    """
    Placeholder for loading background music.
    Uses librosa for actual loading.
    """
    try:
        data, sr = librosa.load(filepath, sr=DEFAULT_SAMPLE_RATE)
        return data
    except Exception as e:
        print(f"Error loading background music: {e}")
        return np.array([])

def mix_audio(main_audio, background_audio, background_level=0.3):
    """
    Mixes main audio with background audio.
    Ensures they are of the same length by padding or truncating the background.
    """
    len_main = len(main_audio)
    len_background = len(background_audio)

    if len_main == 0:
        return background_audio # Or handle as an error

    if len_background == 0:
        return main_audio

    # Adjust background audio length to match main audio
    if len_main > len_background:
        # Pad background audio
        padding = len_main - len_background
        background_audio = np.pad(background_audio, (0, padding), 'wrap') # 'wrap' or 'constant'
    else:
        # Truncate background audio
        background_audio = background_audio[:len_main]

    mixed_audio = main_audio + background_level * background_audio

    # Normalize to prevent clipping
    if np.max(np.abs(mixed_audio)) > 0:
        mixed_audio /= np.max(np.abs(mixed_audio))

    return mixed_audio

# This is the main function that would be called by app.py
def text_to_lullaby(password_text, model_output_placeholder, background_music_path=None):
    """
    Main function to convert password text to a lullaby.
    This will eventually use the ML model output.
    """
    print(f"Generating lullaby for: '{password_text}'")
    print(f"Model output (placeholder): {model_output_placeholder}")

    # 1. Generate basic sound from text (placeholder)
    generated_audio = text_to_basic_sound(password_text)

    # 2. TODO: Use the 'model_output_placeholder' to modify the audio
    #    This could involve changing pitch, rhythm, adding effects based on the model
    #    For now, we're not using the model_output_placeholder.

    # 3. Apply some effects (example)
    # from .effects import apply_reverb # Local import to avoid circular dependency issues at init
    # generated_audio = apply_reverb(generated_audio, reverb_level=0.3, decay_time=1.0)

    # 4. Load and mix background music if provided
    if background_music_path:
        background_audio = load_background_music(background_music_path)
        if background_audio.size > 0:
            generated_audio = mix_audio(generated_audio, background_audio, background_level=0.2)

    # 5. Save or return the audio
    # For now, returning the numpy array. App.py would handle saving to a file.
    return generated_audio


print("audio_utils.generation module loaded")
