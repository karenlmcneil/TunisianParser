import nltk
import re

# POS tagging: https://www.nltk.org/book/ch06.html
# Brill tagger: https://www.nltk.org/book/ch05.html

# def_art = ["al"]
# def_art_short = ["l"]
# poss_suffixes = ["y", "ya", "na", "k", "km", "w", "h", "ha", "hm"]
noun_suffixes = ["ي", "يا", "نا", "ك", "كم", "و", "ه", "ها", "هم"]

filename = 'asraar.txt'
p = re.compile('[ًٌٍَُِّْ]')

tokens = []

with open(filename) as inf:
    for l in inf:
        l = re.sub(p, '', l)
        tokens.append(nltk.tokenize.wordpunct_tokenize(l))


def pos_features(word):
    features = {}
    for suffix in noun_suffixes:
        features['endswith({})'.format(suffix)] = word.endswith(suffix)
    return features