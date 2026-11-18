from unittest import TestCase

from preprocessing.ar_ctype import normalize
from preprocessing import preprocessor
from preprocessing.preprocessor import tokenize_with_spans


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
        vowelled_word = 'إڤِتَابَةٌ'
        normalized_word = normalize(vowelled_word)
        self.assertEqual('اقتابة', normalized_word)

    def test_normalize_spelling1(self):
        w = 'إلّي'
        normalized_word = normalize(w)
        self.assertEqual('الي', normalized_word)



def test_repeated_words_have_distinct_offsets():
    text = "كتاب كتاب"

    assert tokenize_with_spans(text) == [
        {"surface": "كتاب", "start": 0, "end": 4},
        {"surface": "كتاب", "start": 5, "end": 9},
    ]


def test_diacritics_do_not_change_original_offsets():
    text = "إلّي مشيت"

    assert tokenize_with_spans(text) == [
        {"surface": "إلّي", "start": 0, "end": 4},
        {"surface": "مشيت", "start": 5, "end": 9},
    ]
    for token in tokenize_with_spans(text):
        assert text[token["start"]:token["end"]] == token["surface"]


def test_mixed_script_tokens():
    text = "الdiscours متاعو"

    assert tokenize_with_spans(text) == [
        {"surface": "ال", "start": 0, "end": 2},
        {"surface": "discours", "start": 2, "end": 10},
        {"surface": "متاعو", "start": 11, "end": 16},
    ]


def test_punctuation_and_newlines():
    text = "سلام!\nمشيت."

    assert tokenize_with_spans(text) == [
        {"surface": "سلام", "start": 0, "end": 4},
        {"surface": "!", "start": 4, "end": 5},
        {"surface": "مشيت", "start": 6, "end": 10},
        {"surface": ".", "start": 10, "end": 11},
    ]
