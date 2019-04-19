# from pyparsing import parseString
import re


from _Final.parser.preprocessing import uni2buck
from _Final.parser.preprocessing.preprocessor import space_mixed_words, \
    punct_spacer, test_lang
from _Final.parser.preprocessing.ar_ctype import normalize
from _Final.parser.parsing.stemmer import stemmer
from _Final.parser.parsing.goodness_of_fit import choose_best_parse


def preprocess(string):
    norm_string = ''
    for word in string.split(' '):
        norm_string += "%s " % space_mixed_words(punct_spacer(normalize(word)))  # TODO: Replace this with own
        norm_string = re.sub(' +', ' ', norm_string)
    norm_string = norm_string.strip()
    return norm_string


preloaded_words = ['باش', 'انت', 'اللي', 'التي', 'الذي', 'الذين', 'الي', 'الله',
        'لو', 'فماش', 'قداش', 'كيباش', 'وقتاش', 'علاه', 'اشنو', 'هذه', 'هاذي',
        'هذايا', 'غادي', 'بعد', 'لكن', 'انشالله', 'الى', 'من', 'في', 'على', 'بش',
        ]


def preload_common_words():
    for word in preloaded_words:
        p = Parse(raw=word)
        p.raw_bw  = uni2buck.transString(word, reverse=True)
        p.parse_string, p.pos = word, 'UNIN'
        p.stem = word
        p.save()
        part = p.raw
        pp = ParsePart(part=part, parse=p)
        pp.part_bw = p.raw_bw
        pp.save()


def parser(string):

    try:
        Parse.objects.get(raw=preloaded_words[0])
    except ObjectDoesNotExist:
        preload_common_words()

    parsed_list = []
    string = preprocess(string.strip())
    for word in string.split(' '):
        if word:
            try:
                p = Parse.objects.get(raw=word)
                parsed_list.append(p.stem)
            except ObjectDoesNotExist:
                p = Parse(raw=word)
                p.raw_bw = uni2buck.transString(word, reverse=True)
                if test_lang(word) == 'AR':
                    parse_dict = stemmer(word)
                    p.parse, p.pos = choose_best_parse(parse_dict)
                    try:
                        p.stem = p.parse.stem.asList()[0]
                    except:
                        p.stem = p.parse.stem
                    parsed_list.append(p.stem)
                    p.save()
                    for part in p.parse.asList():
                        pp = ParsePart(part=part, parse=p)
                        pp.part_bw = uni2buck.transString(part, reverse=True)
                        pp.save()
                else:
                    p.parse = word
                    p.pos = 'FW'
                    p.stem = word
                    parsed_list.append(p.stem)
                    p.save()
                    pp = ParsePart(part=word, parse=p)
                    pp.save()
    return parsed_list
