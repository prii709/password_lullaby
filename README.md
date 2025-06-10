# Password Lullaby Bot

Password Lullaby Bot is an AI-driven application designed to convert user passwords into personalized lullaby-style melodies. This project explores the intersection of creative AI, audio processing, and user interaction, with a strong emphasis on user privacy.

## Core Idea
The bot maps each password character (or its phonetic representation) to musical notes or syllables. These are then intended to be synthesized into a soothing audio output using a neural singing voice synthesis model like DiffSinger (currently simulated).

## Privacy
A fundamental design principle is **user privacy**. Passwords are processed in memory and are **not stored** at any point in the application.

## Current Status
This project is currently in a simulated phase:
- Password input is handled via a command-line interface.
- Passwords are mapped to musical notes based on a simple character mapping.
- Melody generation (DiffSinger integration) is simulated.
- Audio synthesis is simulated, producing a dummy WAV file.

## Project Structure
- `app.py`: Main application script (CLI).
- `audio_utils/`: Modules for audio processing.
  - `char_mapper.py`: Maps password characters to notes.
  - `synthesis.py`: (Simulated) audio synthesis.
- `model/`: Modules for the singing synthesis model.
  - `singing_synthesis.py`: (Simulated) DiffSinger integration.
- `tests/`: Unit tests.
  - `test_char_mapper.py`: Tests for the character mapping logic.
- `requirements.txt`: Project dependencies.
- `README.md`: This file.

## Setup and Running
1. **Clone the repository (if applicable).**
2. **Create a virtual environment (recommended):**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
   *Note: The current `requirements.txt` lists placeholders like `diffsinger`. You would need to install actual libraries for real model integration and audio work.*

4. **Run the application:**
   ```bash
   python app.py
   ```
   The application will prompt you to enter a password.

5. **Run tests:**
   ```bash
   python -m unittest discover tests
   ```

## Future Development
- Integrate a real DiffSinger (or similar) model.
- Implement actual audio synthesis from the model's output.
- Refine character-to-note/phoneme mapping for better musicality.
- Potentially develop a simple web interface (e.g., using Flask).
