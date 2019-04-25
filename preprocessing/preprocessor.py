import re


def test_lang(string):
    """Takes a string and determines if it is written in Arabic characters
    or foreign, by testing whether the first character has a case attribute.
    This is intended for Arabic texts that may have English or French words
    added. If it encounters another case-less language (Chinese for instance),
    it will falsely identify it as Arabic."""

    p = re.compile('\W')
    a = string[0]
    if not string:
        return ''
    elif a.isalpha() and not (a.islower() or a.isupper()):
        lang = 'AR'
    elif p.match(a):
        lang = 'PT'
    else:
        lang = 'FW'
    return lang


def space_mixed_words(string):
    """Takes a string and inserts space between Arabic and foreign letters.
    Returns a string.
    string = 'الmixed'
    space_mixed_words(string)
    'ال mixed'
    """

    w = list(string)
    for l in w[1:]:
        if test_lang(l) != test_lang(w[w.index(l)-1]):
            w.insert(w.index(l), ' ')
    return re.sub(' +',' ',''.join(w))
