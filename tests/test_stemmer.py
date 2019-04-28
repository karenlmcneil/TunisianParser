from unittest import TestCase

from preprocessing import uni2buck
from parsing.stemmer import stemmer, extract_stem, extract_suffix


class StemmerTest(TestCase):

    ar_string = 'عربي'
    test_words = [ ('كتبت', 2),
        ('نكتب', 2),
        ('ويكتبوا', 5),
        ('كتاب', 1),
        ('الكتاب', 2),
        ('كتابها', 4),
        ('وكتابو', 10),
        ('مانيش', 6),
        ('منحبش', 5)
        ]
    vbd = 'كتبت'

    def test_transliteration_to_buckwalter(self):
        bw = uni2buck.transString(self.ar_string, reverse=True)
        self.assertEqual(bw, 'Crby')

    def test_simple_stemmer(self):
        for w, num in self.test_words:
            parse_list = stemmer(w)
            self.assertEqual(num, len(parse_list))

    def test_returns_dict_with_correct_key(self):
        parse_dict = stemmer(self.vbd)
        self.assertIsNotNone(parse_dict.get('VBD'))
        for k in parse_dict.keys():
            self.assertIsInstance(k, str)

    def test_verb_stem_defined(self):
        parse_dict = stemmer(self.vbd)
        parse = parse_dict.get('VBD')
        self.assertEqual('كتب', extract_stem(parse))

    def test_verb_suffix_defined(self):
        parse_dict = stemmer(self.vbd)
        parse = parse_dict.get('VBD')
        self.assertEqual('ت', extract_suffix(parse))
