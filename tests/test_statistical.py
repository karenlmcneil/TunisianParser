from unittest import TestCase, skip

from parsing.stemmer import stemmer, extract_stem
from parsing.goodness_of_fit import  \
    make_alt_unin_verb_forms, make_alt_verb_forms, compute_ave_freq, \
    choose_best_parse, make_alt_noun_forms


def choose_best_stem_test(word, debug=False):
    parse_dict = stemmer(word)
    if debug: print("Parse dict is", parse_dict)
    best_parse, word_type = choose_best_parse(parse_dict, debug=debug)
    stem = extract_stem(best_parse)
    return stem


class FreqDistTest(TestCase):

    def test_corpus_file_for_freq_dist_exists(self):
        corpus = 'data/corpus_clean.txt'
        self.assertEqual(str(type(corpus)), "<class 'str'>")


class CreateAltFormsTest(TestCase):

    def test_make_alt_vbd_forms(self):
        vbd = 'كتبت'
        parse_dict = stemmer(vbd)
        parse = parse_dict.get('VBD')
        stem, word_forms = make_alt_verb_forms(parse)
        self.assertEqual(sorted(word_forms), sorted(
            ['كتبنا', 'كتبو', 'كتبوا', 'يكتب', 'يكتبوا', 'يكتبو', 'تكتب', 'تكتبوا', 'تكتبو', 'نكتب', 'نكتبوا', 'نكتبو', 'كتب']
            ))

    def test_make_alt_noun_forms(self):
        n = 'الكتاب'
        parse_dict = stemmer(n)
        parse = parse_dict.get('DET_N')
        stem, word_forms = make_alt_noun_forms(parse)
        self.assertEqual(sorted(word_forms), sorted(
            ['كتابك','كتابكم','كتابنا','كتابه','كتابها','كتابهم','كتابو','كتابي','كتابيا','لكتاب', 'كتاب']
            ))

    def test_make_unin_verb_forms(self):
        verb = 'كتب'
        parse_dict = stemmer(verb)
        parse = parse_dict.get('UNIN')
        stem, verb_forms = make_alt_unin_verb_forms(parse)
        all_verb_forms = ['يكتب', 'يكتبوا', 'يكتبو', 'تكتب', 'تكتبوا', 'تكتبو', 'نكتب', 'نكتبوا',
        'نكتبو', 'كتبت', 'كتبنا', 'كتبو', 'كتبوا']
        self.assertEqual(sorted(verb_forms), sorted(all_verb_forms))

    def make_alt_verb_forms(self):
        vbd = 'كتبت'
        parse_dict = stemmer(vbd)
        parse = parse_dict.get('VBD')
        stem, word_forms = make_alt_verb_forms(parse)
        ave_freq = compute_ave_freq(word_forms)
        self.assertNotEqual(ave_freq, 0)


class ComputeAveFreqTest(TestCase):

    def test_ave_vbz_freq(self):
        vbz = 'يكتبوا'
        parse_dict = stemmer(vbz)
        parse = parse_dict.get('VBZ')
        stem, word_forms = make_alt_verb_forms(parse)
        ave_freq = compute_ave_freq(word_forms)
        self.assertNotEqual(ave_freq, 0)

    def test_ave_noun_freq(self):
        noun = 'الكتاب'
        parse_dict = stemmer(noun)
        parse = parse_dict.get('DET_N')
        stem, word_forms = make_alt_noun_forms(parse)
        ave_freq = compute_ave_freq(word_forms)
        self.assertNotEqual(ave_freq, 0)

    def test_ave_unin_vbd_freq(self):
        vbd = 'كتب'
        parse_dict = stemmer(vbd)
        parse = parse_dict.get('UNIN')
        stem, word_forms = make_alt_unin_verb_forms(parse)
        ave_freq = compute_ave_freq(word_forms)
        self.assertNotEqual(ave_freq, 0)


class ChooseBestVBDParseTest(TestCase):
    """
    Test suite for evaluating parses of past tense verbs of various types (sound,
    assimilated, defective, hollow) with various affixes. Tests that correct stem
    (i.e. uninflected verb) is returned, e.g. wktbthA --> ktb.
    """

    def test_vbd_parse(self):
        p = choose_best_stem_test('كتبت')
        self.assertEqual('كتب', p)

    def test_assim_vbd_parse(self):
        p = choose_best_stem_test('وصلت')
        self.assertEqual('وصل', p)

    def test_con_assim_vbd_parse(self):
        p = choose_best_stem_test('ووصلت')
        self.assertEqual('وصل', p)

    def test_defective_vbd_parse(self):
        p = choose_best_stem_test('مشيت')
        self.assertEqual('مشي', p)

    def test_con_defective_vbd_parse(self):
        p = choose_best_stem_test('ومشيت')
        self.assertEqual('مشي', p)

    def test_vbd_indobj_parse(self):
        p = choose_best_stem_test('قالتلي')
        self.assertEqual('قال', p)

    # @skip("Root too short.")
    # def test_short_vbd_indobj_parse(self):
    #     self.assertEqual('قال', choose_best_stem_test('قتلي'))

    def test_defective_vbd_dirobj_parse(self):
        p = choose_best_stem_test('عطيتني')
        self.assertEqual('عطي', p)

    def test_uninf_vbd_dirobj(self):
        p = choose_best_stem_test('كتبها')
        self.assertEqual('كتب', p)

    def test_doubly_weak_vbd_parse(self):
        p = choose_best_stem_test('وليت')
        self.assertEqual('ولي', p)


class ChooseBestVBZParseTest(TestCase):

    def test_vbz_parse(self):
        self.assertEqual('كتب', choose_best_stem_test('يكتب'))

    def test_vbz_pl_parse(self):
        self.assertEqual('كتب', choose_best_stem_test('يكتبوا'))

    def test_defective_vbz_def_parse(self):
        self.assertEqual('مشي', choose_best_stem_test('يمشي'))

    def test_defective_vbz_def_pl_0arse(self):
        self.assertEqual('مشي', choose_best_stem_test('يمشيوا'))

    def test_doubly_weak_vbz_parse1(self):
        self.assertEqual('وصي', choose_best_stem_test('يوصي'))

    def test_doubly_weak_vbz_parse2(self):
        self.assertEqual('ولي', choose_best_stem_test('يولي'))

    def test_vbz_do(self):
        self.assertEqual('كتب', choose_best_stem_test('يكتبها'))

    def test_vbz_pl_do(self):
        self.assertEqual('كتب', choose_best_stem_test('يكتبوها'))

    def test_vbz_ind(self):
        self.assertEqual('كتب', choose_best_stem_test('يكتبلها'))

    def test_vbz_do_ind(self):
        self.assertEqual('كتب', choose_best_stem_test('يكتبهالي'))

    def test_vbz_pl_ind(self):
        self.assertEqual('كتب', choose_best_stem_test('يكتبولها'))

    def test_vbz_pl_do_ind(self):
        self.assertEqual('كتب', choose_best_stem_test('يكتبوهالي'))

@skip
class ChooseBestNegParseTest(TestCase):

    def test_neg_parse1(self):
        self.assertEqual('حب', choose_best_stem_test('مانحبش'))

    def test_neg_parse2(self):
        self.assertEqual('حب', choose_best_stem_test('منحبش'))

    def test_neg_parse3(self):
        self.assertEqual('عرف', choose_best_stem_test('مانعرفوش'))

    def test_neg_parse4(self):
        self.assertEqual('قول', choose_best_stem_test('ماتقولش'))

    def test_neg_parse5(self):
        self.assertEqual('قل', choose_best_stem_test('ماقلتوليش'))

    @skip
    def test_neg_parse6(self):
        self.assertEqual('حب', choose_best_stem_test('وماحبيتش'))


class ChooseBestNounParseTest(TestCase):

    def test_best_detnoun_parse(self):
        self.assertEqual('كتاب', choose_best_stem_test('الكتاب'))

    def test_best_fem_noun_parse(self):
        self.assertEqual('كرهبة', choose_best_stem_test('الكرهبة'))

    def test_nisba_parse(self):
        self.assertEqual('عربي', choose_best_stem_test('العربي'))

    def test_defective_noun_parse(self):
        self.assertEqual('جري', choose_best_stem_test('الجري'))

    def test_con_det_noun_parse(self):
        self.assertEqual('دار', choose_best_stem_test('والدار'))

    def test_prep_noun_parse(self):
        self.assertEqual('دار', choose_best_stem_test('للدار'))

    def test_con_noun_poss_parse(self):
        self.assertEqual('دار', choose_best_stem_test('ودارها'))

    def test_prep_noun_poss(self):
        self.assertEqual('دار', choose_best_stem_test('لدارهم'))


class ChooseBestUninflectedParseTest(TestCase):

    def test_unin_parse1(self):
        self.assertEqual('كتب', choose_best_stem_test('كتب'))

    def test_unin_parse2(self):
        self.assertEqual('وصي', choose_best_stem_test('وصي'))

    def test_unin_parse3(self):
        self.assertEqual('كتاب', choose_best_stem_test('كتاب'))

    def test_unin_parse4(self):
        self.assertEqual('كرهبة', choose_best_stem_test('كرهبة'))

    def test_unin_parse5(self):
        self.assertEqual('كتب', choose_best_stem_test('وكتب'), )

    def test_unin_parse6(self):
        self.assertEqual('كتاب', choose_best_stem_test('وكتاب'))

    def test_unin_parse7(self):
        self.assertEqual('كتاب', choose_best_stem_test('لكتاب'))

    def test_unin_parse8(self):
        self.assertEqual('كتاب', choose_best_stem_test('ولكتاب'))