# from pyparsing import parseString
import argparse
import nltk
import re

from preprocessing import uni2buck
from preprocessing.preprocessor import space_mixed_words, test_lang
from preprocessing.ar_ctype import normalize
from parsing.stemmer import stemmer
from parsing.goodness_of_fit import choose_best_parse


def preprocess(string):
#     norm_string = ''
#     for word in string.split(' '):
#         norm_string += "%s " % space_mixed_words(punct_spacer(normalize(word)))  # TODO: Replace this with own
#         norm_string = re.sub(' +', ' ', norm_string)
#     norm_string = norm_string.strip()
#     return norm_string
    pass


particles = ['باش', 'لو', 'فماش', 'فما', 'ثم', 'ثماش', 'غادي', 'بعد', 'لكن',
             'انشالله','بش', 'ياخي', 'زعمة']
pronouns = ['انت', 'انا', 'انتي', 'هو', 'هي', 'هم', 'هما', 'احنا']
neg_pron = ['ماكش', 'ماكمش', 'ماناش', 'مانيش', 'ماهاش', 'ماهمش', 'ماهواش', 'ماهوش', 'ماهياش', 'ماهيش']
emph_pron = ['راهو', 'راني', 'راهي', 'راك', 'رانا', 'راهم', 'راو', 'راه',
    'هاك', 'هاو', 'هاني', 'هانا', 'هاهم', 'هاهي', 'هاكم']
rel_pron = ['اللي', 'الي']
dem_pron = ['هذه', 'هاذي', 'هذايا']
interog = ['قداش', 'كيفاش', 'وقتاش', 'اشنو', 'علاه', 'علاش', 'اشني', 'اشنوه', 'اشنيه']
prep = ['الى', 'من', 'في', 'على', 'كي', 'كيفما', 'كيف', 'ع', 'م']
noun = ['الله']


def load_saved_parses():
    saved_parses = {}
    for part in particles:
        saved_parses[part] = (part, 'PART')
    for pro in pronouns:
        saved_parses[pro] = (pro, 'PRO')
    for np in neg_pron:
        saved_parses[np] = (np, 'NEG-COP')
    for ep in emph_pron:
        saved_parses[ep] = (ep, 'EMPH-PRO')
    for rp in rel_pron:
        saved_parses[rp] = (rp, 'REL-PRO')
    for dp in dem_pron:
        saved_parses[dp] = (dp, 'DEM-PRO')
    for intr in interog:
        saved_parses[intr] = (intr, 'INTEROG')
    for prepos in prep:
        saved_parses[prepos] = (prepos, 'P')
    for nn in noun:
        saved_parses[nn] = (nn, 'N')
    return saved_parses


def parse(string):
    """
    Morphologically segments, POS taggs, and lemmatizes string of Tunisian Arabic text.
    :param string: Tunisian Arabic text
    :return: list: parses in the format ('word', 'POS')
    """
    saved_parses = load_saved_parses()
    tokens = nltk.tokenize.wordpunct_tokenize(string)  # TODO: Need to add preprocessing
    parsed_list = []
    for word in tokens:
        if word in saved_parses.keys():
            parsed_list.append(saved_parses[word])
            continue
        if not word.isalpha():
            parsed_list.append((word, 'PUNCT'))
            continue
        if test_lang(word) != 'AR':
            parsed_list.append((word, 'FW'))
            continue
        if word in saved_parses:
            parsed_list.append(saved_parses[word])
            continue
        parse_dict = stemmer(word)
        parse, pos = choose_best_parse(parse_dict)
        pos_list = pos.split('_')
        mapped = list(zip(parse, pos_list))
        parsed_list.extend(mapped)
    return parsed_list


if __name__ == '__main__':
    argparser = argparse.ArgumentParser()
    argparser.add_argument("--string", type=str,
                           help="string to parse")
    args = argparser.parse_args()
    parse(args.string)
