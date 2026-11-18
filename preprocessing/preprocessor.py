import html
import re
import nltk
from preprocessing.ar_ctype import normalize


def test_lang(char):
    """Takes a string and determines if it is written in Arabic characters
    or foreign, by testing whether the first character has a case attribute.
    This is intended for Arabic texts that may have English or French words
    added. If it encounters another case-less language (Chinese for instance),
    it will falsely identify it as Arabic."""
    if not char or not char.isalpha():
        return None
    char = char[0]
    if char.isalpha() and not (char.islower() or char.isupper()):
        lang = 'AR'
    else:
        lang = 'FW'
    return lang

def space_mixed_words(string):
    """Takes a string and inserts space between Arabic and foreign letters.
    Returns a string.
    Example:  'الmixed' -->  'ال mixed'
    """
    w = list(string)
    for l in w[1:]:
        if test_lang(l) != test_lang(w[w.index(l) - 1]):
            w.insert(w.index(l), ' ')
    return re.sub(' +', ' ', ''.join(w))

def preprocess(string):
    """
    Takes raw Arabic text and prepares it for parsing.
    :param string: Tunisian Arabic text
    :return: list of sentences, each of which is a list of normalized tokens
    """
    string = string.strip()
    string = html.escape(string)
    string = normalize(string)
    string = space_mixed_words(string)
    tokens = nltk.tokenize.wordpunct_tokenize(string)
    return tokens

def tokenize_with_spans(text):
    """
    Tokenize original text while preserving character offsets.

    Separates Arabic and Latin-script sequences, punctuation,
    and numbers without modifying the original characters.
    """
    pattern = re.compile(
        r"[^\W\d_]+(?:[\u064B-\u065F\u0670]+[^\W\d_]*)*|\d+|[^\w\s]",
        re.UNICODE,
    )

    results = []

    for match in pattern.finditer(text):
        surface = match.group()

        # Separate adjacent Arabic and Latin text.
        boundaries = [0]

        for index in range(1, len(surface)):
            previous = test_lang(surface[index - 1])
            current = test_lang(surface[index])

            if previous and current and previous != current:
                boundaries.append(index)

        boundaries.append(len(surface))

        for start_index, end_index in zip(boundaries, boundaries[1:]):
            results.append({
                "surface": surface[start_index:end_index],
                "start": match.start() + start_index,
                "end": match.start() + end_index,
            })

    return results
