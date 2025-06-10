# Tests for the character mapper
import unittest
from audio_utils.char_mapper import password_to_notes, SIMPLE_MAPPING

class TestCharMapper(unittest.TestCase):

    def test_password_to_notes_basic(self):
        self.assertEqual(password_to_notes("abc"), [SIMPLE_MAPPING['a'], SIMPLE_MAPPING['b'], SIMPLE_MAPPING['c']])

    def test_password_to_notes_empty(self):
        self.assertEqual(password_to_notes(""), [])

    def test_password_to_notes_unknown_chars(self):
        # Unknown characters should map to a default note (currently 'C4')
        self.assertEqual(password_to_notes("a_b"), [SIMPLE_MAPPING['a'], 'C4', SIMPLE_MAPPING['b']])

    def test_password_to_notes_case_insensitivity(self):
        self.assertEqual(password_to_notes("ABC"), [SIMPLE_MAPPING['a'], SIMPLE_MAPPING['b'], SIMPLE_MAPPING['c']])
        self.assertEqual(password_to_notes("AbC"), [SIMPLE_MAPPING['a'], SIMPLE_MAPPING['b'], SIMPLE_MAPPING['c']])

if __name__ == '__main__':
    unittest.main()
