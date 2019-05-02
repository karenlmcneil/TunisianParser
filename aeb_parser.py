import argparse
import nltk
import re

from preprocessing.preprocessor import space_mixed_words, test_lang, preprocess
from aeb_parsing.stemmer import stemmer
from aeb_parsing.goodness_of_fit import choose_best_parse


particles = ['باش', 'لو', 'فماش', 'فما', 'ثم', 'ثماش', 'غادي', 'بعد', 'لكن',
             'انشالله','بش', 'ياخي', 'زعمة']
pronouns = ['انت', 'انا', 'انتي', 'هو', 'هي', 'هم', 'هما', 'احنا']
neg_pron = ['ماكش', 'ماكمش', 'ماناش', 'مانيش', 'ماهاش', 'ماهمش', 'ماهواش', 'ماهوش', 'ماهياش', 'ماهيش']
emph_pron = ['راهو', 'راني', 'راهي', 'راك', 'رانا', 'راهم', 'راو', 'راه',
    'هاك', 'هاو', 'هاني', 'هانا', 'هاهم', 'هاهي', 'هاكم']
rel_pron = ['اللي', 'الي']
dem_pron = ['هذه', 'هاذي', 'هذايا']
interog = ['قداش', 'كيفاش', 'وقتاش', 'اشنو', 'علاه', 'علاش', 'اشني', 'اشنوه', 'اشنيه']
prep = ['الى', 'من', 'في', 'على', 'كي', 'كيفما', 'كيف', 'ع', 'م', 'نحو']
noun = ['الله']
conj = ['و']
neg = ['موش' , 'مش']


def load_saved_parses():
    saved_parses = {}
    for part in particles:
        saved_parses[part] = (part, 'PART')
    for pro in pronouns:
        saved_parses[pro] = (pro, 'PRO')
    for np in neg_pron:
        saved_parses[np] = (np, 'NEGCOP')
    for ep in emph_pron:
        saved_parses[ep] = (ep, 'EMPH')
    for rp in rel_pron:
        saved_parses[rp] = (rp, 'REL')
    for dp in dem_pron:
        saved_parses[dp] = (dp, 'DEM')
    for intr in interog:
        saved_parses[intr] = (intr, 'INTEROG')
    for prepos in prep:
        saved_parses[prepos] = (prepos, 'P')
    for nn in noun:
        saved_parses[nn] = (nn, 'N')
    for c in conj:
        saved_parses[c] = (c, 'C')
    for n in neg:
        saved_parses[n] = (n, 'NEG')
    return saved_parses


def parse(string):
    """
    Morphologically segments and POS tags string of Tunisian Arabic text.
    :param string: Tunisian Arabic text
    :return: list: parses in the format ('word', 'POS')
    """
    saved_parses = load_saved_parses()
    tokens = preprocess(string)
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
        parse_dict = stemmer(word)
        parse, pos = choose_best_parse(parse_dict, debug=False)
        pos = re.sub('UNINVBD', 'VBD', pos)
        pos = re.sub('UNIN', 'N', pos)  # default to noun for uninflected unknown words
        pos_list = pos.split('_')
        mapped = list(zip(parse, pos_list))
        parsed_list.extend(mapped)
    return parsed_list


if __name__ == '__main__':
    argparser = argparse.ArgumentParser()
    argparser.add_argument("--string", type=str, default="ماكلمتهاش",
                           help="string to parse")
    args = argparser.parse_args()
    parse_list = parse(args.string)
    print(parse_list)