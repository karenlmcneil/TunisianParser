import os

from django.test import TestCase
from unittest import skip


from aeb_parser.parsing.parse_eval import evaluate_parser, evaluate_parser_stem, make_binary


class ParserEvalTest(TestCase):

    def test_gold_standard_exists(self):
        self.assertTrue(os.path.exists('data/arabic_testing.txt'))

    @skip  #this takes a long time to run
    def test_evaluate_parser(self):
        accuracy, precision, recall = evaluate_parser(data_length=2000)
        print('Accuracy: ', accuracy*100, '%, Precision: ', precision*100, \
            '%, Recall: ', recall*100, "%")
        self.assertGreater(accuracy, 0)
        self.assertGreater(precision, 0)
        self.assertGreater(recall, 0)

    def test_make_binary(self):
        word = 'و+ال+بيت'
        self.assertEqual(make_binary(word), '10100')


class ParserStemEvalTest(TestCase):

    def test_stem_gold_standard_exists(self):
        self.assertTrue(os.path.exists('data/arabic_stem_testing.txt'))
        self.assertTrue(os.path.exists('data/arabic_test_string.txt'))

    #@skip  #this takes a long time to run
    def test_evaluate_parser_stem(self):
        accuracy = evaluate_parser_stem(data_length=2000)
        print('Accuracy: ', accuracy*100)
        self.assertGreater(accuracy, 0)


