from numpy import array
from preprocessing.preprocessor import test_lang
import random
import re
from sklearn.model_selection import KFold


# sentence tokenization: https://nlpforhackers.io/splitting-text-into-sentences/
# POS tagging: https://www.nltk.org/book/ch06.html
#               https://nlpforhackers.io/training-pos-tagger/
# Brill tagger: https://www.nltk.org/book/ch05.html

# def_art = ["al"]
# def_art_short = ["l"]
# poss_suffixes = ["y", "ya", "na", "k", "km", "w", "h", "ha", "hm"]


def tokenize_sents(text):
    """Use a regular expression tokenizer to split the corpus text into
    sentences."""
    sents = re.split(r'([.!؟])', text)  # capture group to maintain punct
    # join punctuation to previous sentence
    new_sents = []
    for i, s in enumerate(sents):
        if i == 0:
            continue
        new_sents.append(sents[i - 1] + s)
    return new_sents

# This function only used once, to make the main data set
def make_training_and_test_data(text, corpus_size=1000, hold_out_percent=0.9):
    """
    Take a larger corpus, shuffles it, and makes a training and test
    data set out of a subset of the corpus.
    :param text: String of plain text.
    :param corpus_size: Desired size of subcorpus for annotation. Default size
    is 1,000 sentences.
    :param hold_out_percent: Desired portion of the subcorpus to hold out for
    training. Default is 90%.
    :return: None. Saves a file with the training corpus and one of testing
    corpus.
    """

    # Split corpus into sentences
    sents = tokenize_sents(text)
    print("Length of corpus is ", len(sents), "sentences.")

    # remove sentences that start with English or French, or contain MSA
    msa_features = ['ليس', 'لست', 'ليست', 'ليسوا', 'الذي', 'الذين', 'التي', 'ماذا', 'عن']
    p = re.compile('|'.join(msa_features))
    sents = [sent for sent in sents
             if test_lang(sent[0]) == 'AR' and not re.search(p, sent)]
    print("After removal of foreign and MSA, length of corpus is ", len(sents), "sentences.")

    # make training and testing corpus
    random.shuffle(sents)
    subcorpus = sents[:corpus_size]
    rest_of_corpus = sents[corpus_size:]
    split = int(len(subcorpus) * hold_out_percent)
    subcorpus_train = subcorpus[:split]
    subcorpus_test = subcorpus[split:]
    with open('data/corpus_train.txt', 'w') as trainfile, open('data/corpus_test.txt', 'w') as testfile:
        for trn_sent in subcorpus_train:
            trainfile.write(trn_sent + '\n')
        for test_sent in subcorpus_test:
            testfile.write(test_sent + '\n')
    with open('data/corpus_rest.txt', 'w') as restfile:
        restfile.write('\n'.join(rest_of_corpus))
    return

def make_sentence_list(filename):
    """
    Takes a tsv of word \t\ tag pairs and produces a list of sentences with (w, tag)
    tuples.
    :param filenname: tsv file of format: word \t POS
    :return: list of sentences, each sentence is a list of tuples
    """
    tup_list = []
    p = re.compile(r'([.!؟])')
    with open(filename, 'r') as infile:
        sent = []
        for l in infile:
            w, t = l.strip().split('\t')
            sent.append((w, t))
            if re.match(p, w):
                tup_list.append(sent)
                sent = []
        if sent:
            tup_list.append(sent)
    return tup_list

def evaluate_nltk_pos_taggers(gold_standard_filename):
    pass

# >>> from nltk.tag import DefaultTagger
# >>> tagger = DefaultTagger('NN')
# >>> tagger.tag(['Hello', 'World'])
# [('Hello', 'NN'), ('World', 'NN')]
# >>> from nltk.corpus import treebank
# >>> test_sents = treebank.tagged_sents()[3000:]
# >>> tagger.evaluate(test_sents)
# 0.14331966328512843

# >>> from nltk.tag import untag
# >>> untag([('Hello', 'NN'), ('World', 'NN')])
# ['Hello', 'World']

# >>> tagger1 = DefaultTagger('NN')
# >>> tagger2 = UnigramTagger(train_sents, backoff=tagger1)
# >>> tagger2.evaluate(test_sents)
# 0.8758471832505935

# >>> import pickle
# >>> f = open('tagger.pickle', 'wb')
# >>> pickle.dump(tagger, f)
# >>> f.close()
# >>> f = open('tagger.pickle', 'rb')
# >>> tagger = pickle.load(f)

# def backoff_tagger(train_sents, tagger_classes, backoff=None):
#     """
#     from tag_util import backoff_tagger
#     backoff = DefaultTagger('NN')
#     tagger = backoff_tagger(train_sents, [UnigramTagger, BigramTagger, TrigramTagger], backoff=backoff)
#     > tagger.evaluate(test_sents)
#     0.8806820634578028
#     :param train_sents:
#     :param tagger_classes:
#     :param backoff:
#     :return:
#     """
#     for cls in tagger_classes:
#         backoff = cls(train_sents, backoff=backoff)
#
#     return backoff

# >>> from nltk.tag.sequential import ClassifierBasedPOSTagger
# >>> tagger = ClassifierBasedPOSTagger(train=train_sents)
# >>> tagger.evaluate(test_sents)
# 0.9309734513274336
# >>> default = DefaultTagger('NN')
# >>> tagger = ClassifierBasedPOSTagger(train=train_sents, backoff=default, cutoff_prob=0.3)
# >>> tagger.evaluate(test_sents)
# 0.9311029570472696

# def pos_features(word):
#     noun_suffixes = ["ي", "يا", "نا", "ك", "كم", "و", "ه", "ها", "هم"]
#     features = {}
#     for suffix in noun_suffixes:
#         features['endswith({})'.format(suffix)] = word.endswith(suffix)
#     return features
