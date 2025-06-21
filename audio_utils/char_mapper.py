# audio_utils/char_mapper.py

NOTE_MAP = {
    "C4": 60, "D4": 62, "E4": 64, "F4": 65, "G4": 67, "A4": 69, "B4": 71,
    "C5": 72, "D5": 74, "E5": 76
}

CHAR_TO_NOTE = {
    'a': 'C4', 'b': 'D4', 'c': 'E4', 'd': 'F4', 'e': 'G4', 'f': 'A4', 'g': 'B4',
    'h': 'C5', 'i': 'D5', 'j': 'E5', 'k': 'C4', 'l': 'D4', 'm': 'E4', 'n': 'F4',
    'o': 'G4', 'p': 'A4', 'q': 'B4', 'r': 'C5', 's': 'D5', 't': 'E5', 'u': 'C4',
    'v': 'D4', 'w': 'E4', 'x': 'F4', 'y': 'G4', 'z': 'A4',
    '0': 'B4', '1': 'C5', '2': 'D5', '3': 'E5', '4': 'C4',
    '5': 'D4', '6': 'E4', '7': 'F4', '8': 'G4', '9': 'A4',
    '@': 'B4', '#': 'C5', '$': 'D5', '!': 'E5'
}

def password_to_notes(password: str):
    notes = []
    for char in password.lower():
        note_name = CHAR_TO_NOTE.get(char, 'C4')  # Default to C4
        midi_note = NOTE_MAP.get(note_name, 60)   # Default MIDI for C4
        notes.append(midi_note)
    return notes
