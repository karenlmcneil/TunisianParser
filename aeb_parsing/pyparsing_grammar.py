from pyparsing import StringEnd, oneOf, Optional, Or, Literal, SkipTo, FollowedBy, Combine

##################
# MORPHEME TYPES #
##################

endOfString = StringEnd()

conjunctions = ['و']

# affixed_prepositions = ['ل', 'ب', 'م']
prepositions = ['ل','ب', 'في', 'علي', 'من']

pronouns = ['انت', 'انتي', 'انا', 'اني', 'هو', 'هي', 'احنا', 'انتم', 'انتوما',
            'هم', 'هما', 'هوم', 'هوما']

emphatics = ['ها', 'را']

genitive = ['متاع', 'متع']


# Noun Clitics

def_art = ["ال"]
def_art_short = ["ل"]
poss_suffixes = ["ي", "يا", "نا", "ك", "كم", "و", "ه", "ها", "هم"]

N_SUFF = oneOf(poss_suffixes) + FollowedBy(endOfString)

# Verb Inflections and Clitics

vbz_pre_inflec = ['ان', 'ن', 'ت', 'ي']
key_vbz_prefixes = ['ي', 'ت', 'ن']
vbz_suff_inflec = ['وا', 'و']
vbd_suff_inflec = ["ت", "نا", "توا", "و", "وا"]
key_vbd_suffixes = ["ت", "نا", "و", "وا"]
dir_obj_suffixes = ["ني", "نا", "ك", "كم", "و", "ه", "هو", "ها", "هم"]
ind_obj_suffixes = ["ي", "نا", "كم", "و", "ه", "هو", "ها", "هم", "ك"]
pre_neg = ['م', 'ما']
post_neg = ['ش', 'شي']

VBZ_SUFF = oneOf(vbz_suff_inflec)
VBD_SUFF = oneOf(vbd_suff_inflec)
VB_DO = oneOf(dir_obj_suffixes)
VB_IDO = Literal("ل") + oneOf(ind_obj_suffixes)

VBD_CLIT = Or([VB_DO, Optional(VB_DO) + VB_IDO])
VBZ_CLIT = Or([
    VBZ_SUFF, VB_DO, VB_IDO,
    (VBZ_SUFF + VB_DO),
    (VBZ_SUFF + VB_IDO),
    (VBZ_SUFF + VB_DO + VB_IDO),
    (VB_DO + VB_IDO)
])
NEG_VBZ_CLIT = Or([oneOf(post_neg), VBZ_CLIT + oneOf(post_neg)])
NEG_VBD_CLIT = Or([oneOf(post_neg), VBD_CLIT + oneOf(post_neg)])

# Alternate way to make verb stems
    # from pyparsing import srange, Word
    # arabicChars = srange(r"[\0x0621-\0x0652,\0x067E,\0x06A4,\0x06A8]")
    # verbStem = Word(arabicChars, minimum=2).setName('stem')
    # vbz_pre = oneOf(['ان', 'ن', 'ت', 'ي']).setName('pre')
    # vbz_suff = oneOf(['وا', 'و']).setName('suff')
    # vbz = (vbz_pre + verbStem + vbz_suff).setName('vbz')


##############
# Word Types #
##############

C = oneOf(conjunctions)("stem")
C.setName('C')

PREP = oneOf(prepositions)("stem")
PREP.setName('PREP')

# Particles

GEN = oneOf(genitive)("stem")

GEN_PRO = oneOf(genitive)("stem") + oneOf(poss_suffixes)
GEN_PRO.setName('GEN_PRO')

# انني --> ان + ني
PART_PRO = Literal('ان')("stem") + oneOf(dir_obj_suffixes)
PART_PRO.setName('PART_PRO')

# Nouns

# كتابها --> كتاب + ها
N_PRO = SkipTo(N_SUFF)("stem") + N_SUFF("suffix")
N_PRO.setName('N_PRO')

# لكتابها --> ل + كتاب + ها
PREP_N_PRO = oneOf(prepositions)("prefix") + SkipTo(N_SUFF)("stem") + N_SUFF("suffix")
PREP_N_PRO.setName('PREP_N_PRO')

# الكتاب --> ال + كتاب
DET_N =  oneOf(def_art)("prefix") + SkipTo(endOfString)("stem")
DET_N.setName('DET_N')

# بالكتاب --> ب + ال + كتاب
PREP_DET_N = (oneOf(prepositions) + (oneOf(def_art) | oneOf(def_art_short)))("prefix") + SkipTo(endOfString)("stem")
PREP_DET_N.setName('PREP_DET_N')


# Pronouns

PRO = oneOf(pronouns).setName("stem")
PRO.setName('PRO')

ind = oneOf(ind_obj_suffixes)
prep = oneOf(prepositions)

PREP_PRO = prep("stem") + ind("suffix") + \
    FollowedBy(endOfString)
PREP_PRO.setName('PREP_PRO')


#################
    #VERBS#
#################

VBZ = Combine(oneOf(vbz_pre_inflec)("prefix") +
              SkipTo((VBZ_CLIT + endOfString) | endOfString)("stem") +
              Optional(VBZ_SUFF)("suffix"))
VBZ.setName('VBZ')

VBZ_PRO = VBZ + oneOf(dir_obj_suffixes)
VBZ_PRO.setName('VBZ_PRO')

VBZ_PREP_PRO = VBZ + VB_IDO
VBZ_PREP_PRO.setName('VBZ_PREP_PRO')

VBZ_PRO_PREP_PRO = VBZ + VB_DO + VB_IDO
VBZ_PRO_PREP_PRO.setName('VBZ_PRO_PREP_PRO')

VBD = Combine(SkipTo(VBD_SUFF +
                     Or([VBD_CLIT + endOfString, endOfString]))("stem") +
              VBD_SUFF("suffix"))
VBD.setName('VBD')

VBD_PRO = VBD + VB_DO
VBD_PRO.setName('VBD_PRO')

VBD_PREP_PRO = VBD + VB_IDO
VBD_PREP_PRO.setName('VBD_PREP_PRO')

VBD_PRO_PREP_PRO = VBD + VB_DO + VB_IDO
VBD_PRO_PREP_PRO.setName('VBD_PRO_PREP_PRO')


#################
   #NEG VERBS#
#################

NEG1 = oneOf(pre_neg)("neg1")
NEG2 = oneOf(post_neg)("neg2")

# negative vbz #

vbz_neg = Combine(oneOf(vbz_pre_inflec)("prefix") +
                  SkipTo((NEG_VBZ_CLIT + endOfString))("stem")) + \
                  Optional(VBZ_SUFF)("suffix")

VBZ_NEG = vbz_neg + NEG2
VBZ_NEG.setName('VBZ_NEG')

NEG_VBZ_NEG = NEG1 + VBZ_NEG
NEG_VBZ_NEG.setName('NEG_VBZ_NEG')

VBZ_PRO_NEG = vbz_neg + VB_DO + NEG2
VBZ_PRO_NEG.setName('VBZ_PRO_NEG')

NEG_VBZ_PRO_NEG = NEG1 + vbz_neg + \
                  VB_DO + NEG2
NEG_VBZ_PRO_NEG.setName('NEG_VBZ_PRO_NEG')

VBZ_PREP_PRO_NEG = vbz_neg + VB_IDO + NEG2
VBZ_PREP_PRO_NEG.setName('VBZ_PREP_PRO_NEG')

NEG_VBZ_PREP_PRO_NEG = NEG1 + vbz_neg + VB_IDO + NEG2
NEG_VBZ_PREP_PRO_NEG.setName('NEG_VBZ_PREP_PRO_NEG')

VBZ_PRO_PREP_PRO_NEG = vbz_neg + VB_DO + VB_IDO + NEG2
VBZ_PRO_PREP_PRO_NEG.setName('VBZ_PRO_PREP_PRO_NEG')

NEG_VBZ_PRO_PREP_PRO_NEG = NEG1 + VBZ_PRO_PREP_PRO_NEG
NEG_VBZ_PRO_PREP_PRO_NEG.setName('NEG_VBZ_PRO_PREP_PRO_NEG')


# negative vbd #

vbd_neg = Combine(SkipTo(VBD_SUFF + NEG_VBD_CLIT + endOfString)("stem") +
                  VBD_SUFF("suffix"))

VBD_NEG = vbd_neg + NEG2
VBD_NEG.setName('VBD_NEG')

NEG_VBD_NEG = NEG1 + VBD_NEG
NEG_VBD_NEG.setName('NEG_VBD_NEG')

VBD_PRO_NEG = vbd_neg + VB_DO + NEG2
VBD_PRO_NEG.setName('VBD_PRO_NEG')

NEG_VBD_PRO_NEG = NEG1 + VBD_PRO_NEG
NEG_VBD_PRO_NEG.setName('NEG_VBD_PRO_NEG')

VBD_PREP_PRO_NEG = vbd_neg + VB_IDO + NEG2
VBD_PREP_PRO_NEG.setName('VBD_PREP_PRO_NEG')

NEG_VBD_PREP_PRO_NEG = NEG1 + VBD_PREP_PRO_NEG
NEG_VBD_PREP_PRO_NEG.setName('NEG_VBD_PREP_PRO_NEG')

VBD_PRO_PREP_PRO_NEG = vbd_neg + VB_DO + VB_IDO + NEG2
VBD_PRO_PREP_PRO_NEG.setName('VBD_PRO_PREP_PRO_NEG')

NEG_VBD_PRO_PREP_PRO_NEG = NEG1 + VBD_PRO_PREP_PRO_NEG
NEG_VBD_PRO_PREP_PRO_NEG.setName('NEG_VBD_PRO_PREP_PRO_NEG')


# Uninflected

UNIN = SkipTo(endOfString)("stem")
UNIN.setName("UNIN")

PREP_UNIN = (oneOf(prepositions))("prefix") + SkipTo(endOfString)("stem")
PREP_UNIN.setName("PREP_UNIN")

# uninflected vbd #

UNINVBD_PRO = SkipTo(VB_DO + endOfString)("stem") + VB_DO("suffix")
UNINVBD_PRO.setName('UNINVBD_PRO')

UNINVBD_PREP_PRO = SkipTo(VB_IDO + endOfString)("stem") + VB_IDO("suffix")
UNINVBD_PREP_PRO.setName('UNINVBD_PREP_PRO')

UNINVBD_PRO_PREP_PRO = SkipTo(VBD_CLIT + endOfString)("stem") + VBD_CLIT("suffix")
UNINVBD_PRO_PREP_PRO.setName('UNINVBD_PRO_PREP_PRO')

# negative uninflected vbd #

UNINVBD_NEG = SkipTo(NEG2 + endOfString)("stem") + NEG2
UNINVBD_NEG.setName("UNINVBD_NEG")

UNINVBD_PRO_NEG = SkipTo(VB_DO + NEG2 + endOfString)("stem") + VB_DO + NEG2
UNINVBD_PRO_NEG.setName("UNINVBD_PRO_NEG")

UNINVBD_PREP_PRO_NEG = SkipTo(VB_IDO + NEG2 + endOfString)("stem") + VB_IDO + NEG2
UNINVBD_PREP_PRO_NEG.setName("UNINVBD_PREP_PRO_NEG")

UNINVBD_PRO_PREP_PRO_NEG = SkipTo(VB_DO + VB_IDO + NEG2 + endOfString)("stem") + VB_DO + VB_IDO + NEG2
UNINVBD_PRO_PREP_PRO_NEG.setName("UNINVBD_PRO_PREP_PRO_NEG")

NEG_UNINVBD_NEG = NEG1 + UNINVBD_NEG
NEG_UNINVBD_NEG.setName("NEG_UNINVBD_NEG")

NEG_UNINVBD_PRO_NEG = NEG1 + UNINVBD_PRO_NEG
NEG_UNINVBD_PRO_NEG.setName("NEG_UNINVBD_PRO_NEG")

NEG_UNINVBD_PREP_PRO_NEG = NEG1 + UNINVBD_PREP_PRO_NEG
NEG_UNINVBD_PREP_PRO_NEG.setName("NEG_UNINVBD_PREP_PRO_NEG")

NEG_UNINVBD_PRO_PREP_PRO_NEG = NEG1 + UNINVBD_PRO_PREP_PRO + NEG2
NEG_UNINVBD_PRO_PREP_PRO_NEG.setName("NEG_UNINVBD_PRO_PREP_PRO_NEG")


################
# WORD CLASSES #
################

# These word classes are passed to stemmer.py so that the parser knows which
# parse patterns to try.

verbs = [VBZ, VBZ_PRO, VBZ_PREP_PRO, VBZ_PRO_PREP_PRO,
         VBD, VBD_PRO, VBD_PREP_PRO, VBD_PRO_PREP_PRO]
neg_verbs = [NEG_VBD_NEG, NEG_VBD_PRO_NEG, NEG_VBD_PREP_PRO_NEG, NEG_VBD_PRO_PREP_PRO_NEG,
                 VBD_NEG,     VBD_PRO_NEG,     VBD_PREP_PRO_NEG,     VBD_PRO_PREP_PRO_NEG,
             NEG_VBZ_NEG, NEG_VBZ_PRO_NEG, NEG_VBZ_PREP_PRO_NEG, NEG_VBZ_PRO_PREP_PRO_NEG,
                 VBZ_NEG,     VBZ_PRO_NEG,     VBZ_PREP_PRO_NEG,     VBZ_PRO_PREP_PRO_NEG,]
nouns = [N_PRO, PREP_N_PRO, DET_N, PREP_DET_N]
conj = [C]
prons = [PRO, PREP_PRO]
parts = [PREP, PART_PRO, GEN, GEN_PRO]
unin = [UNIN, PREP_UNIN,
        UNINVBD_PRO, UNINVBD_PREP_PRO, UNINVBD_PRO_PREP_PRO,
        UNINVBD_NEG, UNINVBD_PRO_NEG, UNINVBD_PREP_PRO_NEG, UNINVBD_PRO_PREP_PRO_NEG,
        NEG_UNINVBD_NEG, NEG_UNINVBD_PRO_NEG, NEG_UNINVBD_PREP_PRO_NEG, NEG_UNINVBD_PRO_PREP_PRO_NEG]

word_types = conj + verbs + neg_verbs + nouns + prons + parts + unin


