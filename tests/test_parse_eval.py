import shutil, tempfile
from os import path, getcwd
from unittest import TestCase, skip

from parse_eval import evaluate_parser_segmentation, evaluate_parser_stem, make_binary, evaluate_pos_tagging


class SegmenterEvalTest(TestCase):

    test_data = "من وقتاش رجعت تحكي معا+ه ال+مدير+؟"

    def setUp(self):
        # Create a temporary directory and testing files
        self.test_dir = tempfile.mkdtemp()
        with open(path.join(self.test_dir, 'test.tsv'), 'w') as test_file:
            test_file.write(self.test_data)

    def test_gold_standard_exists(self):
        """Test that default file for segmentation eval exists"""
        self.assertTrue(path.exists('data/segmentation_gold.txt'))

    def test_evaluate_parser(self):
        accuracy, precision, recall = evaluate_parser_segmentation(path.join(self.test_dir, 'test.tsv'))
        print("\nTest Data Segmentation Accuracy: {:2.2%}, "
              "Precision: {:2.2%}, Recall: {:2.2%}".format(accuracy, precision, recall))
        self.assertGreater(accuracy, 0)

    def test_make_binary(self):
        word = 'و+ال+بيت'
        self.assertEqual(make_binary(word), '10100')


class PartOfSpeechTaggingEvalTest(TestCase):

    test_parse = [('من', 'P'), ('وقتاش', 'INTEROG'), ('رجعت', 'VBD'), ('تحكي', 'VBZ'),
                   ('معا', 'N'), ('ه', 'PRO'), ('ال', 'DET'), ('مدير', 'N'), ('؟', 'PUNCT'),
                   ('هو', 'PRO'), ('مجنون', 'N'), ('.', 'PUNCT')]
    gold_parse = [('من', 'P'), ('وقتاش', 'INTEROG'), ('رجعت', 'VBD'), ('تحكي', 'VBZ'),
                  ('معا', 'P'), ('ه', 'PRO'), ('ال', 'DET'), ('مدير', 'N'), ('؟', 'PUNCT'),
                  ('هو', 'PRO'), ('مجنون', 'ADJ'), ('.', 'PUNCT')]


    def setUp(self):
        # Create a temporary directory and testing files
        self.test_dir = tempfile.mkdtemp()
        with open(path.join(self.test_dir, 'gold.tsv'), 'w') as gold_file:
            for w, t in self.gold_parse:
                gold_file.write(w + "\t" + t + "\n")
        with open(path.join(self.test_dir, 'test.tsv'), 'w') as test_file:
            for w, t in self.test_parse:
                test_file.write(w + "\t" + t + "\n")

    def test_pos_tagging(self):
        accuracy = evaluate_pos_tagging(path.join(self.test_dir,'gold.tsv'),
                                        path.join(self.test_dir,'test.tsv'))
        print("Test data accuracy is ", accuracy)
        self.assertAlmostEqual(.8333333, accuracy)

    def tearDown(self):
        # Remove the directory after the test
        shutil.rmtree(self.test_dir)

@skip
class ParserStemEvalTest(TestCase):

    def test_stem_gold_standard_exists(self):
        self.assertTrue(path.exists('data/arabic_stem_testing.txt'))
        self.assertTrue(path.exists('data/arabic_test_string.txt'))

    def test_evaluate_parser_stem(self):
        accuracy = evaluate_parser_stem(data_length=2000)
        print('Accuracy: ', accuracy*100)
        self.assertGreater(accuracy, 0)


