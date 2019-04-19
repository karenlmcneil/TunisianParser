from unittest import TestCase, skip

from _Final.parser import parser

@skip
class ParseTest(TestCase):

    def test_multiword_string(self):
        string = 'هذه العربية وهذه الmixed!'
        lemma_list = parser(string)
        self.assertEqual(lemma_list, ['هذه', 'عربي', 'هذه', 'mixed', '!'])

    def test_real_sentences(self):
        test_sent = 'ومن وقتاش رجعت تحكي معاه المدير؟'
        test_key = ['من', 'وقتاش', 'رجع', 'حكي', 'مع', 'مدير']
        lemma_list = parser(test_sent)
        self.assertEqual(lemma_list, test_key)
