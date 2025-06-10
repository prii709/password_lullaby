# Password Lullaby Bot - Main Application
from audio_utils.char_mapper import password_to_notes
from model.singing_synthesis import load_diffsinger_model, generate_melody_from_notes
from audio_utils.synthesis import synthesize_melody_to_audio

def get_password_input():
    '''Prompts the user for a password and returns it.'''
    password = input("Enter your password: ")
    # PRIVACY NOTE: The password string obtained here is processed immediately
    # by char_mapper.password_to_notes and is not stored or logged.
    return password

def main():
    print("Welcome to the Password Lullaby Bot!")

    if not load_diffsinger_model():
        print("Failed to load the synthesis model. Exiting.")
        return

    password = get_password_input()
    notes = password_to_notes(password)

    if not notes:
        print("Could not map password to notes. Exiting.")
        return

    melody = generate_melody_from_notes(notes)

    if melody:
        print(f"Successfully generated melody (simulated): {melody}")
        audio_file = synthesize_melody_to_audio(melody)
        if audio_file:
            print(f"Lullaby audio (simulated) saved to: {audio_file}")
            print("You would normally play this file with an audio player.")
        else:
            print("Failed to synthesize audio.")
    else:
        print("Failed to generate melody.")

if __name__ == "__main__":
    main()
