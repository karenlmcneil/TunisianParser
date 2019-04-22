# from pyparsing import parseString
import argparse
import nltk
import re

from .preprocessing import uni2buck
from .preprocessing.preprocessor import space_mixed_words, test_lang
from .preprocessing.ar_ctype import normalize
from .parsing.stemmer import stemmer
from .parsing.goodness_of_fit import choose_best_parse


# def preprocess(string):
#     norm_string = ''
#     for word in string.split(' '):
#         norm_string += "%s " % space_mixed_words(punct_spacer(normalize(word)))  # TODO: Replace this with own
#         norm_string = re.sub(' +', ' ', norm_string)
#     norm_string = norm_string.strip()
#     return norm_string


particles = ['باش', 'انت', 'اللي', 'التي', 'الذي', 'الذين', 'الي', 'الله',
             'لو', 'فماش', 'قداش', 'كيباش', 'وقتاش', 'علاه', 'اشنو', 'هذه', 'هاذي',
             'هذايا', 'غادي', 'بعد', 'لكن', 'انشالله', 'الى', 'من', 'في', 'على', 'بش',
             ]


saved_parses = {}  # TODO: Save to file

for part in particles:
    saved_parses[part] = (part, 'PART')


class Parser:
    """Object for parsing Tunisian Arabic strings"""

    def __init__(self, string):
        self.string = string
        self.parsed_list = []

    def parse(self):

        if self.string in saved_parses.values():
            return saved_parses[self.string]

        tokens = nltk.tokenize.wordpunct_tokenize(self.string)  # TODO: Need to add preprocessing

        for word in tokens:
            if not word.isalpha():
                self.parsed_list.append((word, 'PUNCT'))
                continue
            if test_lang(word) != 'AR':
                self.parsed_list.append((word, 'FW'))
                continue
            if word in saved_parses:
                self.parsed_list.append(saved_parses[word])
                continue
            parse_dict = stemmer(word)
            print(parse_dict)
            parse, pos = choose_best_parse(parse_dict)
            print(parse)
            pos_list = pos.split('_')
            # try:
            #     stem = parse.stem.asList()[0]  # because stem is sometimes a list
            # except:
            #     stem = parse.stem
            mapped = list(zip(parse, pos_list))
            self.parsed_list.extend(mapped)
                    # for part in parse.asList():
                    #     pp = ParsePart(part=part, parse=p)
                    #     pp.part_bw = uni2buck.transString(part, reverse=True)
                    #     pp.save()
        #             else:
        #                 p.parse = word
        #                 p.pos = 'FW'
        #                 p.stem = word
        #                 parsed_list.append(p.stem)
        #                 p.save()
        #                 pp = ParsePart(part=word, parse=p)
        #                 pp.save()
        return self.parsed_list


if __name__ == '__main__':
    argparser = argparse.ArgumentParser()
    argparser.add_argument("--string", type=str, default="../sts_strings/stsbenchmark/sts-dev.csv",
                           help="string to parse")
    args = argparser.parse_args()
    Parser(args.string)
