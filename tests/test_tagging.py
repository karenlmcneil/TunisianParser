from os import path
import re
import shutil, tempfile
import unittest

from aeb_tagging import make_sentence_list


class DataPrepTest(unittest.TestCase):

    test_data = [
        [('word1', 'TAG1'), ('word2', 'TAG2'), ('word3', 'TAG3'), ('word4', 'TAG4'), ('.', 'PUNCT')],
        [('word1', 'TAG1'), ('word2', 'TAG2'), ('word3', 'TAG3'), ('word4', 'TAG4'), ('.', 'PUNCT')],
        [('word1', 'TAG1'), ('word2', 'TAG2'), ('word3', 'TAG3'), ('word4', 'TAG4'), ('.', 'PUNCT')],
        [('word1', 'TAG1'), ('word2', 'TAG2'), ('word3', 'TAG3'), ('word4', 'TAG4'), ('.', 'PUNCT')],
        [('word1', 'TAG1'), ('word2', 'TAG2'), ('word3', 'TAG3'), ('word4', 'TAG4'), ('.', 'PUNCT')],
        [('word1', 'TAG1'), ('word2', 'TAG2'), ('word3', 'TAG3'), ('word4', 'TAG4'), ('.', 'PUNCT')],
        [('word1', 'TAG1'), ('word2', 'TAG2'), ('word3', 'TAG3'), ('word4', 'TAG4'), ('.', 'PUNCT')],
        [('word1', 'TAG1'), ('word2', 'TAG2'), ('word3', 'TAG3'), ('word4', 'TAG4'), ('.', 'PUNCT')],
        [('word1', 'TAG1'), ('word2', 'TAG2'), ('word3', 'TAG3'), ('word4', 'TAG4'), ('.', 'PUNCT')],
        [('word1', 'TAG1'), ('word2', 'TAG2'), ('word3', 'TAG3'), ('word4', 'TAG4'), ('.', 'PUNCT')]
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
        self.assertEqual(10, len(test_list))

