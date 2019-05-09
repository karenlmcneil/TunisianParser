import argparse
import csv
import re

from preprocessing.preprocessor import test_lang, preprocess
from aeb_parsing.stemmer import stemmer
from aeb_parsing.goodness_of_fit import choose_best_parse


particles = ['باش', 'لو', 'بعد', 'اي', 'يا', 'انشالله','بش', 'ياخي', 'زعمة']
adverbs = ['غادي', 'هنا', 'هناك', 'برشه', 'برشا', 'برشة', 'شوية',
           'شويه', 'شويا', 'هكا', 'هكة', 'هكاكة', 'هكاكا']
existential = ['فماش', 'فما', 'ثم', 'ثماش', 'ثمه', 'فمه']
pronouns = ['انت', 'انا', 'انتي', 'هو', 'هي', 'هم', 'هما', 'احنا']
neg_pron = ['ماكش', 'ماكمش', 'ماناش', 'مانيش', 'ماهاش', 'ماهمش',
            'ماهواش', 'ماهوش', 'ماهياش', 'ماهيش']
emph_pron = ['راهو', 'راني', 'راهي', 'راك', 'رانا', 'راهم', 'راو', 'راه',
    'هاك', 'هاو', 'هاني', 'هانا', 'هاهم', 'هاهي', 'هاكم']
rel_pron = ['اللي', 'الي']
dem_pron = ['هذه', 'هاذي', 'هذايا', 'هاي', 'هاذية']
interog = ['قداش', 'كيفاش', 'وقتاش', 'اشنو', 'علاه', 'علاش', 'اشني',
           'اشنوه', 'اشنيه', 'اشبي', 'اش']
prep = ['الى', 'من', 'في', 'على', 'كي', 'كيفما', 'كيف', 'ع', 'م', 'نحو']
noun = ['الله', 'ماتش']
conj = ['و', 'لكن', 'ولكن', 'الا', 'والا']
neg = ['موش' , 'مش']


def load_saved_parses():
    saved_parses = {}
    for part in particles:
        saved_parses[part] = (part, 'PART')
    for adv in adverbs:
        saved_parses[adv] = (adv, 'ADV')
    for ext in existential:
        saved_parses[ext] = (ext, 'EXT')
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
        saved_parses[prepos] = (prepos, 'PREP')
    for nn in noun:
        saved_parses[nn] = (nn, 'N')
    for c in conj:
        saved_parses[c] = (c, 'C')
    for n in neg:
        saved_parses[n] = (n, 'NEG')
    return saved_parses


def parse_string(string):
    """
    Morphologically segments and POS tags string of Tunisian Arabic text.
    :param string: Tunisian Arabic text
    :return: list of parse tuples in the format ('word', 'POS')
    """
    # print("string")
    saved_parses = load_saved_parses()
    tokens = preprocess(string)
    # print("after preprocessing: ", tokens)
    parsed_list = []
    for word in tokens:
        if word in saved_parses.keys():
            # print(word, "in saved keys")
            parsed_list.append(saved_parses[word])
            continue
        if not word.isalpha():
            # print(word, "is not alpha")
            parsed_list.append((word, 'PUNCT'))
            continue
        if test_lang(word) != 'AR':
            # print(word, "is not arabic")
            parsed_list.append((word, 'FW'))
            continue
        # print("none of three conditions is true")
        # print("word is still ", word)
        parse_dict = stemmer(word)
        # print(parse_dict)
        parse, pos = choose_best_parse(parse_dict, debug=False)
        pos = re.sub('UNINVBD', 'VBD', pos)
        pos = re.sub('UNIN', 'N', pos)  # default to noun for uninflected unknown words
        pos_list = pos.split('_')
        mapped = list(zip(parse, pos_list))
        parsed_list.extend(mapped)
    return parsed_list


def parse_file(filename):
    name, ext = filename.split('.')
    new_filename = name + '_parsed' + '.tsv'
    with open(filename, 'r') as infile, open(new_filename, 'w') as tsvfile:
        writer = csv.writer(tsvfile, delimiter='\t', lineterminator='\n')
        for line in infile:
            for w, pos in parse_string(line):
                writer.writerow([w, pos])
    return


if __name__ == '__main__':
    argparser = argparse.ArgumentParser()
    argparser.add_argument("--string", type=str, default="ماكلمتهاش",
                           help="string to parse")
    args = argparser.parse_args()
    parse_list = parse_string(args.string)
    print(parse_list)