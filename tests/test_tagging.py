from os import path
import re
import shutil, tempfile
import unittest

from sklearn.model_selection import KFold

from nltk.tag import DefaultTagger, untag

from aeb_tagging import make_sentence_list, evaluate_nltk_pos_taggers


class DataPrepTest(unittest.TestCase):

    test_data = [
        [('word1', 'TAG1'), ('word2', 'TAG2'), ('word3', 'TAG3'), ('word4', 'TAG4'), ('.', 'PUNCT')],
        [('word2', 'TAG1'), ('word2', 'TAG2'), ('word3', 'TAG3'), ('word4', 'TAG4'), ('.', 'PUNCT')],
        [('word3', 'TAG1'), ('word2', 'TAG2'), ('word3', 'TAG3'), ('word4', 'TAG4'), ('.', 'PUNCT')],
        [('word4', 'TAG1'), ('word2', 'TAG2'), ('word3', 'TAG3'), ('word4', 'TAG4'), ('.', 'PUNCT')],
        [('word5', 'TAG1'), ('word2', 'TAG2'), ('word3', 'TAG3'), ('word4', 'TAG4'), ('.', 'PUNCT')],
        [('word6', 'TAG1'), ('word2', 'TAG2'), ('word3', 'TAG3'), ('word4', 'TAG4'), ('.', 'PUNCT')],
        [('word7', 'TAG1'), ('word2', 'TAG2'), ('word3', 'TAG3'), ('word4', 'TAG4'), ('.', 'PUNCT')],
        [('word8', 'TAG1'), ('word2', 'TAG2'), ('word3', 'TAG3'), ('word4', 'TAG4'), ('.', 'PUNCT')],
        [('word9', 'TAG1'), ('word2', 'TAG2'), ('word3', 'TAG3'), ('word4', 'TAG4'), ('.', 'PUNCT')],
        [('word10', 'TAG1'), ('word2', 'TAG2'), ('word3', 'TAG3'), ('word4', 'TAG4'), ('.', 'PUNCT')]
    ]

    def setUp(self):
        # Create a temporary directory and testing files
        self.test_dir = tempfile.mkdtemp()
        with open(path.join(self.test_dir, 'test.tsv'), 'w') as test_file:
            for sent in self.test_data:
                for w, t in sent:
                    test_file.write(w + '\t' + t + '\n')
        p = re.compile(r'([.!؟])')

    def test_make_sentence_list(self):
        test_list = make_sentence_list(path.join(self.test_dir, 'test.tsv'))
        self.assertEqual(self.test_data, test_list)

    def test_default_tagger(self):
        test_list = make_sentence_list(path.join(self.test_dir, 'test.tsv'))
        tagger = DefaultTagger('N')
        split = int(len(test_list) * .90)
        train_data = test_list[:split]
        test_data = test_list[split:]
        print(tagger.evaluate(train_data))
        print(tagger.evaluate(test_data))

    def test_backoff_tagger(self):
        tag_dict = evaluate_nltk_pos_taggers(path.join(self.test_dir, 'test.tsv'))
        self.assertIsInstance(tag_dict, dict)


