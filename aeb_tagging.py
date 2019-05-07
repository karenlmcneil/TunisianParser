import argparse
from nltk.tag import DefaultTagger, UnigramTagger, BigramTagger, TrigramTagger, brill, brill_trainer
from preprocessing.preprocessor import test_lang
import random
import re


def tokenize_sents(text):
    """Use a regular expression tokenizer to split the corpus text into
    sentences.
    :param text: String of plain text.
    :return: List of sentences
    """
    sents = re.split(r'([.!؟])', text)  # capture group to maintain punct

    # join punctuation to previous sentence
    new_sents = []
    for i, s in enumerate(sents):
        if i == 0:
            continue
        new_sents.append(sents[i - 1] + s)
    return new_sents


# This function only used once, to make the main data set
def filter_and_shuffle_corpus(text):
    """
    Shuffles Tunisian Arabic corpus and removes French and MSA sents.
    :param text: String of plain text.
    :return: None. Saves a file with the new corpus.
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
    with open('data/corpus_sents.txt', 'w') as trainfile:
        for sent in sents:
            trainfile.write(sent + '\n')
    return


def make_sentence_list(filename):
    """
    Takes a tsv of 'word \t tag' lines and produces a list of sentences with (w, tag)
    tuples.
    :param filenname: tsv file of format: word \t POS \n
    :return: array of sentences, each sentence is an array of tuples
    """
    sents = []
    p = re.compile(r'([.!؟])')
    with open(filename, 'r') as infile:
        tup_list = []
        for l in infile:
            try:
                w, t = l.strip().split('\t')
                tup_list.append((w, t))
                if re.match(p, w):
                    sents.append(tup_list)
                    tup_list = []
            except ValueError:  # handle blank lines
                continue
        if tup_list:
            sents.append(tup_list)
    return sents


def backoff_tagger(train_sents, test_sents, tagger_classes, backoff=None):
    """
    Trains a succession of POS backoff taggers, with each tagger becoming
    the backoff for the next.
    :param train_sents: list of sentences, each sentence a list of (word, POS) tuples
    :param test_sents: list of sentences, each sentence a list of (word, POS) tuples
    :param tagger_classes: list of NLTK backoff tagger classes
    :param backoff: final backoff tagger (like DefaultTagger)
    :return: backoff: the class of the uppermost tagger
    :return: scores: list of scores for each of the tagger classes
    """
    scores = []
    for cls in tagger_classes:
        backoff = cls(train_sents, backoff=backoff)
        tagger_name = backoff.unicode_repr().split(':')[0][1:]
        scores.append(backoff.evaluate(test_sents))
    return backoff, scores


def evaluate_nltk_pos_taggers(gold_standard_filename, num_folds=10, loo=False):
    """
    Evaluates the NLTK backoff taggers on the corpus data. Uses cross-validation.
    :param gold_standard_filename: tsv file of format: word \t POS \n
    :param num_folds: int: number of folds for cross-validation
    :param loo: bool: whether to use Leave One Out cross-validation
    :return:
    """
    data_array = make_sentence_list(gold_standard_filename)
    if loo:  # Leave One Out cross-validation
        num_folds = len(data_array)-1
    backoff = DefaultTagger('N')
    tagger_classes = [UnigramTagger, BigramTagger, TrigramTagger]
    subset_size = int(len(data_array) / num_folds)
    scores = {
        'DefaultTagger': [],
        'UnigramTagger': [],
        'BigramTagger': [],
        'TrigramTagger': [],
    }

    # k-fold cross-validation
    for i in range(num_folds):

        # training and testing data for this round
        testing_this_round = data_array[i * subset_size:][:subset_size]
        training_this_round = data_array[:i * subset_size] + data_array[(i + 1) * subset_size:]

        # compute score for taggers
        default_score = backoff.evaluate(testing_this_round)
        trigram, tagger_scores = backoff_tagger(training_this_round, testing_this_round,
                                                tagger_classes, backoff=backoff)
        uni_score, bi_score, tri_score = tagger_scores

        # save scores
        scores['DefaultTagger'].append(default_score)
        scores['UnigramTagger'].append(uni_score)
        scores['BigramTagger'].append(bi_score)
        scores['TrigramTagger'].append(tri_score)

    for k, v in scores.items():  # average scores across folds
        if v:
            scores[k] = sum(v)/len(v)
    print(scores)
    return scores


if __name__ == '__main__':
    argparser = argparse.ArgumentParser()
    argparser.add_argument("--filename", type=str, default="data/gold_standard_403.tsv",
                           help="tsv file with gold standard POS tags")
    argparser.add_argument("--n_folds", type=int, default=10,
                           help="number of folds for cross-fold validation")
    argparser.add_argument("--loo", type=bool, default=False,
                           help="Leave One Out cross validation. If set to True, n_folds will be ignored")
    args = argparser.parse_args()
    evaluate_nltk_pos_taggers(args.filename, args.n_folds, args.loo)
