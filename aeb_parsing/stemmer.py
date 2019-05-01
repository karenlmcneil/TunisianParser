from pyparsing import ParseException, Literal

from aeb_parsing.pyparsing_grammar import word_types


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


def add_conj(word_type_list):
    new_list = []
    for type in word_type_list:
        new_list.append(type)
        new_type = Literal('و') + type
        new_type.setName('C_' + type.name)
        new_list.append(new_type)
    return(new_list)


def stemmer(arabic_word):
    parse_dict = {}
    all_word_types = add_conj(word_types)  # add conjunctions here, to avoid repetition in grammar
    for word_type in all_word_types:
        try:
            parse = word_type.parseString(arabic_word, parseAll=True)
            parse_dict[str(word_type)] = parse  # converting pyparsing object
            # 'word_type' to a string so it can be used for lookup
        except ParseException:
            pass
    return parse_dict
