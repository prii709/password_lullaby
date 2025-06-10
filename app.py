# Password Lullaby Bot - Main Application
from getpass import getpass
from audio_utils.char_mapper import password_to_notes
from model.singing_synthesis import load_diffsinger_model, generate_melody_from_notes
from audio_utils.synthesis import synthesize_melody_to_audio

def get_password_input():
    '''Prompts the user for a password and returns it securely.'''
    password = getpass("Enter your password: ")
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
        audio_path = synthesize_melody_to_audio(melody, output_filename="lullaby.wav")
        print(f"Lullaby saved at: {audio_path}")
    else:
        print("Melody generation failed. Exiting.")

if __name__ == "__main__":
    main()
