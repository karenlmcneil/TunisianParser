from unittest import TestCase
from .parser import Parser


class TestParser(TestCase):

    def test_existing_parse(self):
        string = 'باش'
        p = Parser(string)
        parse = p.parse()
        expected_output = [('باش', 'PART')]
        self.assertEqual(expected_output, parse)

    def test_single_word(self):
        string = 'الكتاب'
        p = Parser(string)
        parse = p.parse()
        expected_output = [('ال', 'DET'), ('كتاب', 'N')]
        self.assertEqual(expected_output, parse)

    def test_multiword_string(self):
        string = 'هذه العربية وهذه الmixed!'
        p = Parser(string)
        parse = p.parse()
        expected_output = [('هذه', 'PART'), ('ال', 'DET'), ('عربية', 'N'), ('و', 'C'),
            ('هذه', 'UNIN'), ('ال', 'DET'), ('mixed', 'N'), ('!', 'PUNCT')]
        self.assertEqual(expected_output, parse)

    def test_multiple_prefix(self):
        string = 'والكتاب'
        p = Parser(string)
        parse = p.parse()
        print("parse is ", parse)
        expected_output = [('و', 'C'), ('ال', 'DET'), ('كتاب', 'N')]
        self.assertEqual(expected_output, parse)

    # def test_real_sentences(self):
    #     test_sent = 'ومن وقتاش رجعت تحكي معاه المدير؟'
    #     test_key = ['من', 'وقتاش', 'رجع', 'حكي', 'مع', 'مدير']
    #     lemma_list = parser(test_sent)
    #     self.assertEqual(lemma_list, test_key)