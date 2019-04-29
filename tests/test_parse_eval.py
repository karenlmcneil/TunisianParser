import shutil, tempfile
from os import path, getcwd
from unittest import TestCase

from parse_eval import evaluate_parser_segmentation, evaluate_parser_stem, make_binary, evaluate_pos_tagging


class ParserEvalTest(TestCase):

    def test_gold_standard_exists(self):
        self.assertTrue(path.exists('data/segmentation_gold.txt'))

    # @skip  #this takes a long time to run
    def test_evaluate_parser(self):
        accuracy, precision, recall = evaluate_parser_segmentation(data_length=2000)
        print('Accuracy: ', accuracy*100, '%, Precision: ', precision*100,
            '%, Recall: ', recall*100, "%")
        self.assertGreater(accuracy, 0)

    def test_make_binary(self):
        word = 'و+ال+بيت'
        self.assertEqual(make_binary(word), '10100')


class PartOfSpeechTaggingEvalTest(TestCase):

    test_parse = [('من', 'P'), ('وقتاش', 'INTEROG'), ('رجعت', 'VBD'), ('تحكي', 'VBZ'),
                   ('معا', 'N'), ('ه', 'PRO'), ('ال', 'DET'), ('مدير', 'N'), ('؟', 'PUNCT'),
                   ('هو', 'PRO'), ('مجنون', 'UNIN'), ('.', 'PUNCT')]
    gold_parse = [('من', 'P'), ('وقتاش', 'INTEROG'), ('رجعت', 'VBD'), ('تحكي', 'VBZ'),
                  ('معا', 'P'), ('ه', 'PRO'), ('ال', 'DET'), ('مدير', 'N'), ('؟', 'PUNCT'),
                  ('هو', 'PRO'), ('مجنون', 'ADJ'), ('.', 'PUNCT')]


    def setUp(self):
        # Create a temporary directory and testing files
        self.test_dir = tempfile.mkdtemp()
        with open(path.join(self.test_dir, 'gold.txt'), 'w') as goldfile:
            for w, t in self.gold_parse:
                goldfile.write(w + "\t" + t)

    def test_pos_tagging(self):
        accuracy = evaluate_pos_tagging(path.join(self.test_dir,'gold.txt'))
        self.assertNotEqual(0, accuracy)

    def tearDown(self):
        # Remove the directory after the test
        shutil.rmtree(self.test_dir)


class ParserStemEvalTest(TestCase):

    def test_stem_gold_standard_exists(self):
        self.assertTrue(path.exists('data/arabic_stem_testing.txt'))
        self.assertTrue(path.exists('data/arabic_test_string.txt'))

    def test_evaluate_parser_stem(self):
        accuracy = evaluate_parser_stem(data_length=2000)
        print('Accuracy: ', accuracy*100)
        self.assertGreater(accuracy, 0)


