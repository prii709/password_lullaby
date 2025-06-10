# Character to Phoneme/Note Mapper
SIMPLE_MAPPING = {
    'a': 'C4', 'b': 'D4', 'c': 'E4', 'd': 'F4', 'e': 'G4', 'f': 'A4', 'g': 'B4', 'h': 'C5',
    'i': 'D5', 'j': 'E5', 'k': 'F5', 'l': 'G5', 'm': 'A5', 'n': 'B5', 'o': 'C4', 'p': 'D4',
    'q': 'E4', 'r': 'F4', 's': 'G4', 't': 'A4', 'u': 'B4', 'v': 'C5', 'w': 'D5', 'x': 'E5',
    'y': 'F5', 'z': 'G5',
    '0': 'C3', '1': 'D3', '2': 'E3', '3': 'F3', '4': 'G3', '5': 'A3', '6': 'B3', '7': 'C2', '8': 'D2', '9': 'E2',
    '!': 'F2', '@': 'G2', '#': 'A2', '$': 'B2', '%': 'C3', '^': 'D3', '&': 'E3', '*': 'F3', '(': 'G3', ')': 'A3',
    # Add more mappings as needed, consider uppercase, other symbols etc.
}

def password_to_notes(password):
    # PRIVACY NOTE: This function receives the password string for immediate
    # conversion to notes. The original password is not stored by this function.
    notes = []
    for char in password.lower(): # Convert to lowercase to simplify mapping
        notes.append(SIMPLE_MAPPING.get(char, 'C4')) # Default to C4 if char not in mapping
    return notes
