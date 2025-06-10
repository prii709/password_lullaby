import wave
import struct
import math

def synthesize_melody_to_audio(melody_sequence, output_filename="lullaby.wav"):
    print(f"Synthesizing real audio for melody: {melody_sequence}...")

    sample_rate = 44100
    amplitude = 16000  # For 16-bit PCM

    # Mapping note names to frequencies (you can expand this)
    note_freqs = {
        'C4': 261.63, 'D4': 293.66, 'E4': 329.63, 'F4': 349.23,
        'G4': 392.00, 'A4': 440.00, 'B4': 493.88,
        'C5': 523.25, 'D5': 587.33, 'E5': 659.26, 'G5': 783.99
    }

    audio_data = []

    for note, duration in melody_sequence:
        freq = note_freqs.get(note, 440.0)  # Default to A4 if unknown
        duration_samples = int(sample_rate * duration)
        for i in range(duration_samples):
            t = i / sample_rate
            sample = int(amplitude * math.sin(2 * math.pi * freq * t))
            audio_data.append(sample)

    try:
        with wave.open(output_filename, 'w') as wf:
            wf.setnchannels(1)           # Mono
            wf.setsampwidth(2)           # 16-bit
            wf.setframerate(sample_rate)
            for sample in audio_data:
                packed_sample = struct.pack('<h', sample)
                wf.writeframes(packed_sample)

        print(f"✅ Real audio synthesized and saved to: {output_filename}")
        return output_filename
    except Exception as e:
        print(f"❌ Error writing audio: {e}")
        return None
