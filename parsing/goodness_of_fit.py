import nltk
import os

from parsing.pyparsing_grammar import vbz_suff_inflec, \
        poss_suffixes, def_art, def_art_short
from parsing.pyparsing_grammar import key_vbz_prefixes as vbz_prefixes, \
    key_vbd_suffixes as vbd_suffixes, dir_obj_suffixes, pronouns

from parsing.stemmer import extract_stem, extract_suffix, extract_prefix

corpus_text_location = 'data/corpus_clean.txt'
print("current directory is ", os.getcwd())
corpus_text = open(corpus_text_location, 'r').read()
fd = nltk.FreqDist(corpus_text.split())


def compute_ave_freq(word_forms):
    # word_forms is a list of morphological variations of a word, such as
    # ['كتبوا', 'كتبو', 'كتبنا', 'كتبت']

    try:
        return sum([fd.freq(form) for form in word_forms]) / len(word_forms)
    except ZeroDivisionError:
        return 0


def make_alt_noun_forms(parse):
    word_forms = []
    fem = False
    nisba = False
    stem = extract_stem(parse)
    if stem and stem[-1] == 'ة':
        fem = True
        fem_stem = stem[:-1] + 'ت'
    if stem and stem[-1] == 'ي':
        nisba = True
        word_forms.append(stem + 'ة')
    if len(stem)<2:
        pass
    else:
        suffix = extract_suffix(parse)
        prefix = extract_prefix(parse)
        # change taa marbuta to taa before adding suffixes
        for suf in poss_suffixes:
            if fem:
                word_forms.append(fem_stem + suf)
            else:
                word_forms.append(stem + suf)
        for pre in def_art + def_art_short:
            word_forms.append(pre + stem)
            if nisba: word_forms.append(pre + stem + 'ة')
        if prefix:
            try:
                word_forms.remove(prefix + stem)
            except ValueError:
                pass
            word_forms.append(stem)
        if suffix:
            try:
                word_forms.remove(stem + suffix)
            except ValueError:
                pass
            word_forms.append(stem)
    return stem, set(word_forms)


def make_alt_affixed_pron_forms(parse):
    word_forms = []
    stem = extract_stem(parse)
    prefix = extract_prefix(parse)
    suffix = extract_suffix(parse)
    if stem:
        for do in [o for o in dir_obj_suffixes if o != stem]:
            if prefix and suffix:
                word_forms.append(prefix + do + suffix)
            if prefix and not suffix:
                word_forms.append(prefix + do)
    return stem, set(word_forms)


def make_alt_ind_pron_forms(parse):
    word_forms = []
    stem = extract_stem(parse)
    prefix = extract_prefix(parse)
    suffix = extract_suffix(parse)
    if stem:
        for pronoun in [p for p in pronouns if p != stem and p[0] != 'ا']:
            if prefix and suffix:
                word_forms.append(prefix + pronoun + suffix)
            if prefix and not suffix:
                word_forms.append(prefix + pronoun)
    return stem, set(word_forms)


def make_alt_verb_forms(parse):
    word_forms = []
    stem = extract_stem(parse)
    if len(stem)<2:
        pass
    else:
        suffix = extract_suffix(parse)
        prefix = extract_prefix(parse)
        if suffix:
            word_forms.append(prefix + stem)
        if prefix:
            for suf in vbd_suffixes:
                word_forms.append(stem + suf)
            for pre in [p for p in vbz_prefixes if p != prefix]:
                word_forms.append(pre + stem)
                if suffix:
                    for suf in [s for s in vbz_suff_inflec if s != suffix]:
                        word_forms.append(pre + stem + suf)
                else:
                    for suf in vbz_suff_inflec:
                        word_forms.append(pre + stem + suf)
        elif suffix and not prefix:
            for suf in [s for s in vbd_suffixes if s != suffix]:
                word_forms.append(stem + suf)
            for pre in vbz_prefixes:
                word_forms.append(pre + stem)
                for suf in vbz_suff_inflec:
                    word_forms.append(pre + stem + suf)
    return stem, set(word_forms)


def make_alt_unin_verb_forms(parse):
    stem = extract_stem(parse)
    word_forms = []
    for pre in vbz_prefixes:
        word_forms.append(pre + stem)
        for suf in vbz_suff_inflec:
            word_forms.append(pre + stem + suf)
    for suf in vbd_suffixes:
        word_forms.append(stem + suf)
    return stem, set(word_forms)


def make_alt_unin_forms(parse):
    freq_dict = {}
    stem = extract_stem(parse)

    # test if it's an uninflected verb
    v_stem, verb_forms = make_alt_unin_verb_forms(parse)
    ave_verb_freq = compute_ave_freq(verb_forms)
    freq_dict['VBD'] = (ave_verb_freq, verb_forms)

    # test if it's an uninflected noun
    n_stem, noun_forms = make_alt_noun_forms(parse)
    ave_noun_freq = compute_ave_freq(noun_forms)
    freq_dict['UNIN_N'] = (ave_noun_freq, noun_forms)

    chosen_word_type = max(freq_dict, key=freq_dict.get)
    freq, word_forms = freq_dict.get(chosen_word_type)
    return stem, set(word_forms)


function_dict = {
    #nouns
    'NS' : make_alt_noun_forms,
    'C_N_PRO' : make_alt_noun_forms,
    'P_N_PRO' : make_alt_noun_forms,
    'C_P_N_PRO' : make_alt_noun_forms,
    'DET_N' : make_alt_noun_forms,
    'C_DET_N' : make_alt_noun_forms,
    'P_DET_N' : make_alt_noun_forms,
    'C_P_DET_N' : make_alt_noun_forms,
    #pronouns
    'NEG_PRO_NEG' : make_alt_affixed_pron_forms,
    'C_NEG_PRO_NEG' : make_alt_affixed_pron_forms,
    'INT_PRO' : make_alt_ind_pron_forms,
    'EMPH_PRO' : make_alt_affixed_pron_forms,
    'C_EMPH_PRO' : make_alt_affixed_pron_forms,
    'P_PRO' : make_alt_ind_pron_forms,
    'C_PRO' : make_alt_affixed_pron_forms,
    'C_P_PRO' : make_alt_affixed_pron_forms,
    #verbs
    'C_VBZ' : make_alt_verb_forms,
    'VBZ' : make_alt_verb_forms,
    'VBD' : make_alt_verb_forms,
    'C_VBD' : make_alt_verb_forms,
    'NEG_VBZ_NEG' : make_alt_verb_forms,
    'C_NEG_VBZ_NEG' : make_alt_verb_forms,
    'NEG_VBD' : make_alt_verb_forms,
    'C_NEG_VBD' : make_alt_verb_forms,
    #uninflected
    'UNIN' : make_alt_unin_forms,
    'C_UNIN' : make_alt_unin_forms,
    'P_UNIN' : make_alt_unin_forms,
    'C_P_UNIN' : make_alt_unin_forms,
    'UNINVBD_PRO' : make_alt_unin_verb_forms,
    'UNINVBD_P_PRO' : make_alt_unin_verb_forms,
    }


def choose_best_parse(parse_dict, debug=False):
    freq_dict = {}
    for word_type, parse in parse_dict.items():
        prefix = extract_prefix(parse)
        if debug: print("Prefix is ", prefix)
        if prefix and extract_prefix(parse)=='ال':   # automatically return noun if has def art
            if debug: print("Returning ", parse_dict[word_type], word_type)
            return parse_dict[word_type], word_type
        func = function_dict.get(word_type)
        # print("Word type is ", word_type)
        # print("VB in word type ", 'VB' in word_type)
        # if 'UNIN' in word_type:
        #     func = make_alt_unin_forms
        # elif 'VB' in word_type:
        #     func = make_alt_verb_forms()
        # elif 'P_PRO' or 'INT_PRO' in word_type:
        #     func = make_alt_ind_pron_forms()
        # elif 'PRO' in word_type:
        #     func = make_alt_affixed_pron_forms()
        # elif 'N' in word_type:
        #     func = make_alt_noun_forms()
        # else:
        #     func = None
        if debug: print("Function chosen is ", func)
        if func:
            stem, word_forms = func(parse)
            if debug: print("Stem, word_forms are ", stem, word_forms)
            ave_freq = compute_ave_freq(word_forms)
            if debug: print("Ave freq is ", ave_freq)
            freq_dict[word_type] = ave_freq
    try:
        chosen_word_type = max(freq_dict, key=freq_dict.get)
        if debug: print("Chosen word type is ", chosen_word_type)
    except TypeError: #if all are 0
        if debug: print("All freq zero, choosing UNIN")
        chosen_word_type = 'UNIN'
    if debug: print("Returning ", parse_dict[chosen_word_type], chosen_word_type)
    return parse_dict[chosen_word_type], chosen_word_type

