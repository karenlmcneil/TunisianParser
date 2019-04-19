from unittest import TestCase

from _Final.parser.preprocessing import uni2buck
from _Final.parser.parsing.stemmer import stemmer, extract_stem, extract_suffix


class StemmerTest(TestCase):

    ar_string = 'عربي'
    test_words = [ ('كتبت', 2),
        ('نكتب', 2),
        ('ويكتبوا', 5),
        ('كتاب', 1),
        ('الكتاب', 2),
        ('كتابها', 2),
        ('وكتابو', 6),
        ('مانيش', 5),
        ('منحبش', 5)
        ]
    vbd = 'كتبت'

    def test_transliteration_to_buckwalter(self):
        bw = uni2buck.transString(self.ar_string, reverse=True)
        self.assertEqual(bw, 'Crby')

    def test_simple_stemmer(self):
        for w, num in self.test_words:
            parse_list = stemmer(w)
            #print(w, ' has ', len(parse_list), 'parse(s)')
            #for p in parse_list:
                #print(p, '\n')
            self.assertEqual(len(parse_list), num)

    def test_returns_dict_with_correct_key(self):
        parse_dict = stemmer(self.vbd)
        self.assertIsNotNone(parse_dict.get('VBD'))
        for k in parse_dict.keys():
            self.assertEqual(str(type(k)), "<class 'str'>")

    def test_verb_stem_defined(self):
        parse_dict = stemmer(self.vbd)
        parse = parse_dict.get('VBD')
        self.assertEqual(extract_stem(parse), 'كتب')

    def test_verb_suffix_defined(self):
        parse_dict = stemmer(self.vbd)
        parse = parse_dict.get('VBD')
        self.assertEqual(extract_suffix(parse), 'ت')
