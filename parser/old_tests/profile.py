# from: https://zapier.com/engineering/profiling-python-boss/

from aeb_parser.parser import parser
from aeb_parser.parsing.stemmer import stemmer
from aeb_parser.parsing.goodness_of_fit import choose_best_parse, compute_ave_freq, \
        make_alt_verb_forms, make_alt_noun_forms, make_alt_affixed_pron_forms, \
        make_alt_unin_forms, make_alt_unin_verb_forms



try:
    from line_profiler import LineProfiler

    def do_profile(follow=[]):
        def inner(func):
            def profiled_func(*args, **kwargs):
                try:
                    profiler = LineProfiler()
                    profiler.add_function(func)
                    for f in follow:
                        profiler.add_function(f)
                    profiler.enable_by_count()
                    return func(*args, **kwargs)
                finally:
                    profiler.print_stats()
            return profiled_func
        return inner

except ImportError:
    def do_profile(follow=[]):
        "Helpful if you accidentally leave in production!"
        def inner(func):
            def nothing(*args, **kwargs):
                return func(*args, **kwargs)
            return nothing
        return inner


@do_profile(follow=[parser])
def parse_test_sentence():
    test_sent = 'ومن وقتاش رجعت تحكي معاه المدير؟'
    parse = parser(test_sent)
    return parse


@do_profile(follow=[choose_best_parse])
def choose_parse():
    words = ['كتاب', 'الكتاب', 'كتبت', 'يكتب']
    chosen_parses = []
    for word in words:
        parse_dict = stemmer(word)
        best_parse = choose_best_parse(parse_dict)
        chosen_parses.append(best_parse)
    return chosen_parses


@do_profile(follow=[compute_ave_freq])
def calculate_freq():
    wordforms = ['كتبوا', 'كتبو', 'كتبنا', 'كتبت']
    freq = compute_ave_freq(wordforms)
    return freq


@do_profile(follow=[make_alt_verb_forms, make_alt_noun_forms, \
            make_alt_affixed_pron_forms, make_alt_unin_forms])
def make_word_forms():
    word_form_list = []
    words = {
        'يكتب' : make_alt_verb_forms,
        'الكتاب' : make_alt_noun_forms,
        'راني' : make_alt_affixed_pron_forms,
        'كرهبة' : make_alt_unin_forms,
        }
    for word, func in words.items():
        parse_dict = stemmer(word)
        for word_type, parse in parse_dict.items():
            stem, word_forms = func(parse)
            word_form_list.append(word_forms)
    return word_form_list


@do_profile(follow=[compute_ave_freq])
def make_unin_forms():
    word_form_list = []
    word = 'كرهبة'
    parse_dict = stemmer(word)
    for word_type, parse in parse_dict.items():
        freq_dict = {}

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
        word_form_list.append(set(word_forms))
    return word_form_list




# Line #      Hits         Time  Per Hit   % Time  Line Contents
# ==============================================================
#   192                                           def choose_best_parse(parse_dict, debug=False):
#   193         4            8      2.0      0.0      freq_dict = {}
#   194        11           26      2.4      0.0      for word_type, parse in parse_dict.items():
#   195         7           18      2.6      0.0          func = function_dict.get(word_type)
#   196         7           12      1.7      0.0          if func:
#   197         7       467824  66832.0     55.2              stem, word_forms = func(parse)
#   198         7       379322  54188.9     44.8              ave_freq = compute_ave_freq(word_forms)
#   199         7           33      4.7      0.0              freq_dict[word_type] = ave_freq
#   200         4            6      1.5      0.0      try:
#   201         4           47     11.8      0.0          chosen_word_type = max(freq_dict, key=freq_dict.get)
#   202                                               except TypeError: #if all are 0
#   203                                                   chosen_word_type = 'UNIN'
#   204         4            6      1.5      0.0      return parse_dict[chosen_word_type], chosen_word_type
# Total time: 0.86362 s
# File: /home/larapsodia/development/aeb_parser/old_tests/profile.py
# Function: choose_parse at line 44
# Line #      Hits         Time  Per Hit   % Time  Line Contents
# ==============================================================
#     44                                           @do_profile(follow=[choose_best_parse])
#     45                                           def choose_parse():
#     46         1            4      4.0      0.0      words = ['كتاب', 'الكتاب', 'كتبت', 'يكتب']
#     47         1            2      2.0      0.0      chosen_parses = []
#     48         5            9      1.8      0.0      for word in words:
#     49         4        16143   4035.8      1.9          parse_dict = stemmer(word)
#     50         4       847450 211862.5     98.1          best_parse = choose_best_parse(parse_dict)
#     51         4           11      2.8      0.0          chosen_parses.append(best_parse)
#     52         1            1      1.0      0.0      return chosen_parses