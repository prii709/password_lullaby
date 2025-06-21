# Password Lullaby Bot - Main Application
from getpass import getpass
from audio_utils.char_mapper import password_to_notes
from model.singing_synthesis import load_diffsinger_model, generate_singing_audio

def get_password_input():
    '''Prompts the user for a password and returns it securely.'''
    password = getpass("Enter your password: ")
    return password

import string

def char_to_phoneme(ch):
    if ch.lower() in string.ascii_lowercase:
        return ch.lower()
    elif ch.isdigit():
        return f"num_{ch}"
    else:
        return "sym"

def prepare_diffsinger_input(notes, password):
    if not notes or len(notes) == 0:
        raise ValueError("Note sequence is empty. Cannot synthesize audio.")

    ph_seq = [char_to_phoneme(ch) for ch in password]
    frame_shift = 0.0125  # Adjust if your model uses a different value
    frames_per_phoneme = int(0.3 / frame_shift)  # 0.3 seconds per phoneme
    ph_dur = [frames_per_phoneme] * len(ph_seq)
    note_seq = notes
    note_dur = [frames_per_phoneme] * len(note_seq)

    print(f"🗣️ Phoneme Sequence: {ph_seq}")
    return {
        "ph_seq": ph_seq,
        "ph_dur": ph_dur,
        "note_seq": note_seq,
        "note_dur": note_dur
    }



def main():
    print("🎵 Welcome to the Password Lullaby Bot 🎵")

    if not load_diffsinger_model():
        print("❌ Failed to load DiffSinger and vocoder. Exiting.")
        return

    password = get_password_input()
    notes = password_to_notes(password)
    print(f"🧠 Notes mapped from password: {notes}")

    if not notes:
        print("❌ Could not map password to notes. Exiting.")
        return

    diffsinger_input = prepare_diffsinger_input(notes, password)

    try:
        audio_path = generate_singing_audio(diffsinger_input, output_path="lullaby.wav")
        print(f"✅ Lullaby saved at: {audio_path}")
    except Exception as e:
        print(f"❌ Singing generation failed: {e}")

if __name__ == "__main__":
    main()
