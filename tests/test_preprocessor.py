from unittest import TestCase

from preprocessing.ar_ctype import normalize
from preprocessing import preprocessor


class TestPreprocessor(TestCase):

    def test_word_is_Arabic_or_foreign(self):
        # Given a word, the parser determines if it is Arabic or Latin script based
        # on the first character
        ar_word = 'كتاب'
        fr_word = 'période'

        lang1 = preprocessor.test_lang(ar_word)
        lang2 = preprocessor.test_lang(fr_word)

        self.assertEqual('AR', lang1)
        self.assertEqual('FW', lang2)

    def test_separate_mixed_words(self):
        # If a word is a combination of Arabic and foreign, inserts a space in
        # between the characters
        string = "يكمل الdiscours متاعو"
        output = preprocessor.space_mixed_words(string)

        correct_string = "يكمل ال discours متاعو"
        self.assertEqual(correct_string, output)

    def test_normalize_spelling(self):
        # If a word is Arabic, it strips the harakat and normalizes the spelling
        vowelled_word = 'ڤِتَابَةٌ'
        normalized_word = normalize(vowelled_word)
        self.assertEqual('قتابة', normalized_word)

