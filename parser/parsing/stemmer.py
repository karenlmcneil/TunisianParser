from pyparsing import ParseException

from parser.parsing.pyparsing_grammar import word_types


def extract_stem(pyparsing_object):
    try:
        stem = pyparsing_object.stem.asList()[0]
    except:
        stem = pyparsing_object.stem
    return stem


def extract_suffix(pyparsing_object):
    try:
        suffix = pyparsing_object.suffix.asList()[0]
    except:
        suffix = pyparsing_object.suffix
    return suffix


def extract_prefix(pyparsing_object):
    try:
        prefix = pyparsing_object.prefix.asList()[-1]
    except:
        prefix = pyparsing_object.prefix
    return prefix


def stemmer(arabic_word):
    parse_dict = {}
    for word_type in word_types:
        try:
            parse = word_type.parseString(arabic_word)
            parse_dict[str(word_type)] = parse #converting pyparsing object
            # 'word_type' to a string so it can be used for lookup
        except ParseException:
            pass
    return parse_dict
