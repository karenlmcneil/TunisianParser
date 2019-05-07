from unittest import TestCase
from aeb_parser import parse_string


class TestParser(TestCase):

    def test_existing_parse(self):
        string = 'باش'
        p = parse_string(string)
        expected_output = [('باش', 'PART')]
        self.assertEqual(expected_output, p)

    def test_single_word(self):
        string = 'الكتاب'
        p = parse_string(string)
        expected_output = [('ال', 'DET'), ('كتاب', 'N')]
        self.assertEqual(expected_output, p)

    def test_multiword_string(self):
        string = 'هذه العربية و هذه الmixed!'
        p = parse_string(string)
        expected_output = [('هذه', 'DEM'), ('ال', 'DET'), ('عربية', 'N'), ('و', 'C'),
            ('هذه', 'DEM'), ('ال', 'N'), ('mixed', 'FW'), ('!', 'PUNCT')]
        # 'N' instead of 'DET' for second 'ال' is an expected failure, since an
        # isolated determiner is not an expected word type
        self.assertEqual(expected_output, p)

    def test_particle_with_shadda(self):
        string = 'الّي'
        p = parse_string(string)
        expected_output = [('الي', 'REL')]
        self.assertEqual(expected_output, p)

    def test_verb_with_shadda(self):
        string = 'يرفّع'
        p = parse_string(string)
        expected_output = [('يرفع', 'VBZ')]
        self.assertEqual(expected_output, p)

    def test_multiple_prefix(self):
        string = 'والكتاب'
        p = parse_string(string)
        expected_output = [('و', 'C'), ('ال', 'DET'), ('كتاب', 'N')]
        self.assertEqual(expected_output, p)

    def test_past_verb(self):
        string = 'كتبت'
        p = parse_string(string)
        expected_output = [('كتبت', 'VBD')]
        self.assertEqual(expected_output, p)

    def test_past_verb_defective(self):
        string = 'مشيت'
        p = parse_string(string)
        expected_output = [('مشيت', 'VBD')]
        self.assertEqual(expected_output, p)

    def test_conj_past_verb(self):
        string = 'وكتبت'
        p = parse_string(string)
        expected_output = [('و', 'C'), ('كتبت', 'VBD')]
        self.assertEqual(expected_output, p)

    def test_present_verb(self):
        string = 'نمشيو'
        p = parse_string(string)
        expected_output = [('نمشيو', 'VBZ')]
        self.assertEqual(expected_output, p)

    def test_conj_present_verb(self):
        string = 'ونمشيو'
        p = parse_string(string)
        expected_output = [('و', 'C'), ('نمشيو', 'VBZ')]
        self.assertEqual(expected_output, p)

    def test_real_sentences(self):
        string = 'ومن وقتاش رجعت تحكي معاه المدير؟'
        p = parse_string(string)
        expected_output = [('و', 'C'), ('من', 'N'), ('وقتاش', 'INTEROG'), ('رجعت', 'VBD'),
                           ('تحكي', 'VBZ'), ('معا', 'N'), ('ه', 'PRO'), ('ال', 'DET'),
                           ('مدير', 'N'), ('؟', 'PUNCT')]
        self.assertEqual(expected_output, p)
