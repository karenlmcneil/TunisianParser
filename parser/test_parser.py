from unittest import TestCase
from .parser import Parser


class TestParser(TestCase):

    def test_existing_parse(self):
        string = 'باش'
        p = Parser(string)
        parse = p.parse()
        expected_output = [[('باش', 'PART')]]
        self.assertEqual(expected_output, parse)

    def test_single_word(self):
        string = 'الكتاب'
        p = Parser(string)
        parse = p.parse()
        expected_output = [[('ال', 'DT'), ('كتاب', 'NN')]]
        self.assertEqual(expected_output, parse)

    # def test_multiword_string(self):
    #     string = 'هذه العربية وهذه الmixed!'
    #     lemma_list = parser(string)
    #     self.assertEqual(lemma_list, ['هذه', 'عربي', 'هذه', 'mixed', '!'])
    #
    # def test_real_sentences(self):
    #     test_sent = 'ومن وقتاش رجعت تحكي معاه المدير؟'
    #     test_key = ['من', 'وقتاش', 'رجع', 'حكي', 'مع', 'مدير']
    #     lemma_list = parser(test_sent)
    #     self.assertEqual(lemma_list, test_key)