from unittest import TestCase
from parser.parser import Parser


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
        expected_output = [('و', 'C'), ('ال', 'DET'), ('كتاب', 'N')]
        self.assertEqual(expected_output, parse)

    def test_past_verb(self):
        string = 'كتبت'
        p = Parser(string)
        parse = p.parse()
        expected_output = [('كتبت', 'VBD')]
        self.assertEqual(expected_output, parse)

    def test_past_verb_defective(self):
        string = 'مشيت'
        p = Parser(string)
        parse = p.parse()
        expected_output = [('مشيت', 'VBD')]
        self.assertEqual(expected_output, parse)

    def test_conj_past_verb(self):
        string = 'وكتبت'
        p = Parser(string)
        parse = p.parse()
        expected_output = [('و', 'C'), ('كتبت', 'VBD')]
        self.assertEqual(expected_output, parse)

    def test_present_verb(self):
        string = 'نمشيو'
        p = Parser(string)
        parse = p.parse()
        expected_output = [('نمشيو', 'VBZ')]
        self.assertEqual(expected_output, parse)

    def test_conj_present_verb(self):
        string = 'ونمشيو'
        p = Parser(string)
        parse = p.parse()
        expected_output = [('و', 'C'), ('نمشيو', 'VBZ')]
        self.assertEqual(expected_output, parse)

    def test_fail(self):
        # مشينا، عطيهولي، ما عطيهوليش
        self.fail('Write tests for other verb types')

    # def test_real_sentences(self):
    #     string = 'ومن وقتاش رجعت تحكي معاه المدير؟'
    #     p = Parser(string)
    #     parse = p.parse()
    #     print("parse is ", parse)
    #     expected_output = [('و', 'C'), ('من', 'P'), ('وقتاش', 'PART'), ('رجعت', 'VBD'),
    #                        ('تحكي', 'VBZ'), ('معا', 'PART'), ('ه', 'PRO'), ('ال', 'DET'),
    #                        ('مدير', 'N'), ('؟', 'PUNCT')]
    #     self.assertEqual(expected_output, parse)