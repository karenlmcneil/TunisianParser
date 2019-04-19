from django.test import TestCase

from aeb_parser.preprocessing.ar_ctype import normalize
from aeb_parser.preprocessing import preprocessor
from aeb_parser.parser import parser, preprocess
from aeb_parser.models import Parse



class PreprocessorTest(TestCase):

    maxDiff=None

    # Inserts space between words and punctuation
    def test_space_between_punctuation(self):
        string = "هذه كلمة، صاح؟ "
        output = preprocessor.punct_spacer(string)

        self.assertEqual(output, 'هذه كلمة ، صاح ؟')


    # Given a word, the parser determines if it is Arabic or Latin script based
    # on the first character
    def test_word_is_Arabic_or_foreign(self):
        ar_word = 'كتاب'
        fr_word = 'période'

        lang1 = preprocessor.test_lang(ar_word)
        lang2 = preprocessor.test_lang(fr_word)

        self.assertEqual(lang1, 'AR')
        self.assertEqual(lang2, 'FW')


    # If a word is a combination of Arabic and foreign, inserts a space in
    # between the characters
    def test_separate_mixed_words(self):
        string = "يكمل الdiscours متاعو"
        output = preprocessor.space_mixed_words(string)

        correct_string = "يكمل ال discours متاعو"
        self.assertEqual(output, correct_string)


    # If a word is Arabic, it strips the harakat and normalizes the spelling
    def test_normalize_spelling(self):
        vowelled_word = 'كِتَابَةٌ'
        normalized_word = normalize(vowelled_word)
        self.assertEqual(normalized_word, 'كتابة')

    # Everything works together
    def test_preprocessing(self):
        string = """        و  الdiscours متاعو خدملي فاها، يها بش تردوهالي تيخوانا؟ أنا"""
        p = preprocess(string)
        outstring = 'و discours ال متاعو خدملي ، فاها يها بش تردوهالي ؟ تيخوانا انا'
        self.assertEqual(len(p), len(outstring))

