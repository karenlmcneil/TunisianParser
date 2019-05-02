import html
import random
from preprocessing.preprocessor import test_lang
import re


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


# def pos_features(word):
#     noun_suffixes = ["ي", "يا", "نا", "ك", "كم", "و", "ه", "ها", "هم"]
#     features = {}
#     for suffix in noun_suffixes:
#         features['endswith({})'.format(suffix)] = word.endswith(suffix)
#     return features
