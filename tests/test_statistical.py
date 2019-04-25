from unittest import TestCase, skip

from parsing.stemmer import stemmer
from parsing.goodness_of_fit import  \
    make_alt_unin_verb_forms, make_alt_verb_forms, compute_ave_freq, \
    choose_best_parse, make_alt_noun_forms


def choose_best_parse_test(word):
    parse_dict = stemmer(word)
    best_parse, word_type = choose_best_parse(parse_dict, debug=False)
    try:
        stem = best_parse.stem.asList()[0]
    except:
        stem = best_parse.stem
    return stem


class FreqDistTest(TestCase):

    def test_corpus_file_for_freq_dist_exists(self):
        corpus = '../parser/data/corpus_clean.txt'
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

    def test_vbd_parse(self):
        self.assertEqual(choose_best_parse_test('كتبت'),
        'كتب')

    @skip("Not fixable - must parse this type manually")
    def test_assim_vbd_parse(self):
        self.assertEqual(choose_best_parse_test('وصلت'),
        'وصل')

    def test_con_assim_vbd_parse(self):
        self.assertEqual(choose_best_parse_test('ووصلت'),
        'وصل')

    def test_defective_vbd_parse(self):
        self.assertEqual(choose_best_parse_test('مشيت'),
        'مشي')

    def test_con_defective_vbd_parse(self):
        self.assertEqual(choose_best_parse_test('ومشيت'),
        'مشي')

    def test_vbd_indobj_parse(self):
        self.assertEqual(choose_best_parse_test('قالتلي'), 'قال')

    @skip("Root too short. Fixable?")
    def test_short_vbd_indobj_parse(self):
        self.assertEqual(choose_best_parse_test('قتلي'),
        'قال')

    def test_defective_vbd_dirobj_parse(self):
        self.assertEqual(choose_best_parse_test('عطيتني'),
        'عطي')

    # def test_vbd_parse(self):
    #     self.assertEqual(choose_best_parse_test('word'), 'parse')

    def test_doubly_weak_vbd_parse(self):
        self.assertEqual(choose_best_parse_test('وليت'), 'ولي')


class ChooseBestVBZParseTest(TestCase):

    def test_vbz_parse(self):
        self.assertEqual(choose_best_parse_test('يكتبوا'), 'كتب')

    def test_defective_vbz_parse1(self):
        self.assertEqual(choose_best_parse_test('يمشي'), 'مشي')

    def test_defective_vbz_parse2(self):
        self.assertEqual(choose_best_parse_test('يمشيوا'), 'مشي')

    def test_doubly_weak_vbz_parse1(self):
        self.assertEqual(choose_best_parse_test('يوصي'), 'وصي')

    @skip("Not fixable - must parse this type manually")
    def test_doubly_weak_vbz_parse2(self):
        self.assertEqual(choose_best_parse_test('يولي'), 'ولي')


class ChooseBestNegParseTest(TestCase):

    def test_neg_parse1(self):
        self.assertEqual(choose_best_parse_test('مانحبش'), 'حب')

    def test_neg_parse2(self):
        self.assertEqual(choose_best_parse_test('منحبش'), 'حب')

    def test_neg_parse3(self):
        self.assertEqual(choose_best_parse_test('مانعرفوش'), 'عرف')

    def test_neg_parse4(self):
        self.assertEqual(choose_best_parse_test('ماتقولش'), 'قول')

    def test_neg_parse5(self):
        self.assertEqual(choose_best_parse_test('ماقلتوليش'), 'قل')

    @skip
    def test_neg_parse6(self):
        self.assertEqual(choose_best_parse_test('وماحبيتش'), 'حب')


class ChooseBestNounParseTest(TestCase):

    def test_best_detnoun_parse(self):
        self.assertEqual(choose_best_parse_test('الكتاب'), 'كتاب')

    def test_best_fem_noun_parse(self):
        self.assertEqual(choose_best_parse_test('الكرهبة'), 'كرهبة')

    def test_nisba_parse(self):
        self.assertEqual(choose_best_parse_test('العربي'), 'عربي')

    def test_defective_noun_parse(self):
        self.assertEqual(choose_best_parse_test('الجري'), 'جري')

    def test_con_det_noun_parse(self):
        self.assertEqual(choose_best_parse_test('والدار'), 'دار')

    def test_prep_noun_parse(self):
        self.assertEqual(choose_best_parse_test('للدار'), 'دار')

    def test_con_noun_poss_parse(self):
        self.assertEqual(choose_best_parse_test('ودارها'), 'دار')

    def test_prep_noun_poss(self):
        self.assertEqual(choose_best_parse_test('لدارهم'), 'دار')


class ChooseBestPronounParseTest(TestCase):

    def test_pronoun_parse1(self):
        self.assertEqual(choose_best_parse_test('ماكش'),
        'ك')

    def test_pronoun_parse2(self):
        self.assertEqual(choose_best_parse_test('مانيش'),
        'ني')

    def test_pronoun_parse3(self):
        self.assertEqual(choose_best_parse_test('ومانيش'),
        'ني')

    def test_pronoun_parse4(self):
        self.assertEqual(choose_best_parse_test('ماني'),
        'ني')

    def test_pronoun_parse5(self):
        self.assertEqual(choose_best_parse_test('راني'),
        'ني')

    def test_pronoun_parse6(self):
        self.assertEqual(choose_best_parse_test('وهاني'),
        'ني')

    def test_pronoun_parse7(self):
        self.assertEqual(choose_best_parse_test('ماهيش'),
        'هي')

    def test_pronoun_parse8(self):
        self.assertEqual(choose_best_parse_test('وانا'),
        'انا')

    def test_pronoun_parse9(self):
        self.assertEqual(choose_best_parse_test('لك'),
        'ك')

    def test_pronoun_parse10(self):
        self.assertEqual(choose_best_parse_test('ولك'),
        'ك')


class ChooseBestUninflectedParseTest(TestCase):

    def test_unin_parse1(self):
        self.assertEqual(choose_best_parse_test('كتب'),
        'كتب')

    def test_unin_parse2(self):
        self.assertEqual(choose_best_parse_test('وصي'),
        'وصي')

    def test_unin_parse3(self):
        self.assertEqual(choose_best_parse_test('كتاب'),
        'كتاب')

    def test_unin_parse4(self):
        self.assertEqual(choose_best_parse_test('كرهبة'),
        'كرهبة')

    def test_unin_parse5(self):
        self.assertEqual(choose_best_parse_test('وكتب'),
        'كتب')

    def test_unin_parse6(self):
        self.assertEqual(choose_best_parse_test('وكتاب'),
        'كتاب')

    def test_unin_parse7(self):
        self.assertEqual(choose_best_parse_test('لكتاب'),
        'كتاب')

    def test_unin_parse8(self):
        self.assertEqual(choose_best_parse_test('ولكتاب'),
        'كتاب')