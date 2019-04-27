from pyparsing import StringEnd, oneOf, Optional, Or, Literal, SkipTo, FollowedBy, Combine

##################
# MORPHEME TYPES #
##################

endOfString = StringEnd()

conjunctions = ['و']
# affixed_prepositions = ['ل', 'ب', 'م']
prepositions = ['ل','ب', 'في', 'علي', 'من']

pronouns = ['انت', 'انتي', 'انا', 'اني', 'هو', 'هي', 'هوّ', 'هيّ'
             'احنا', 'انتم', 'انتوما', 'هم', 'هما', 'هوم', 'هوما']

emphatics = ['ها', 'را']

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
ind_obj_suffixes = ["ي", "نا", "ن", "كم", "و", "ه", "هو", "ها", "هم"]
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
    # verbStem = Word(arabicChars, exact=3).setName('stem')
    # vbz_pre = oneOf(['ان', 'ن', 'ت', 'ي']).setName('pre')
    # vbz_suff = oneOf(['وا', 'و']).setName('suff')
    # vbz = (vbz_pre + verbStem + vbz_suff).setName('vbz')


##############
# Word Types #
##############

# Nouns

# كتابها --> كتاب + ها
N_PRO = SkipTo(N_SUFF | endOfString)("stem") + N_SUFF("suffix")
N_PRO.setName('N_PRO')

# لكتابها --> ل + كتاب + ها
P_N_PRO = oneOf(prepositions) ("prefix") + SkipTo(N_SUFF | endOfString)("stem") + N_SUFF("suffix")
P_N_PRO.setName('P_N_PRO')

# الكتاب --> ال + كتاب
DET_N =  oneOf(def_art)("prefix") + SkipTo(endOfString)("stem")
DET_N.setName('DET_N')

# بالكتاب --> ب + ال + كتاب
P_DET_N = ( oneOf(prepositions) + ( oneOf(def_art) | oneOf(def_art_short) ) )("prefix") + SkipTo(endOfString)("stem")
P_DET_N.setName('P_DET_N')


# Pronouns

PRO = oneOf(pronouns)
PRO.setName('PRO')

P_PRO = oneOf(prepositions)('prefix') + oneOf(ind_obj_suffixes)("stem") + \
    FollowedBy(endOfString)
P_PRO.setName('P_PRO')


#################
    #VERBS#
#################

VBZ = Combine(oneOf(vbz_pre_inflec)("prefix") +
              SkipTo((VBZ_CLIT + endOfString) | endOfString)("stem") +
              Optional(VBZ_SUFF)("suffix"))
VBZ.setName('VBZ')

VBZ_PRO = VBZ + oneOf(dir_obj_suffixes)
VBZ_PRO.setName('VBZ_PRO')

VBZ_P_PRO = VBZ + VB_IDO
VBZ_P_PRO.setName('VBZ_P_PRO')

VBZ_PRO_P_PRO = VBZ + VB_DO + VB_IDO
VBZ_PRO_P_PRO.setName('VBZ_PRO_P_PRO')

VBD = Combine(SkipTo(VBD_SUFF +
                     Or([VBD_CLIT + endOfString, endOfString]))("stem") +
              VBD_SUFF("suffix"))
VBD.setName('VBD')

VBD_PRO = VBD + VB_DO
VBD_PRO.setName('VBD_PRO')

VBD_P_PRO = VBD + VB_IDO
VBD_P_PRO.setName('VBD_P_PRO')

VBD_PRO_P_PRO = VBD + VB_DO + VB_IDO
VBD_PRO_P_PRO.setName('VBD_PRO_P_PRO')


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

VBZ_P_PRO_NEG = vbz_neg + VB_IDO + NEG2
VBZ_P_PRO_NEG.setName('VBZ_P_PRO_NEG')

NEG_VBZ_P_PRO_NEG = NEG1 + vbz_neg + VB_IDO + NEG2
NEG_VBZ_P_PRO_NEG.setName('NEG_VBZ_P_PRO_NEG')

VBZ_PRO_P_PRO_NEG = vbz_neg + VB_DO + VB_IDO + NEG2
VBZ_PRO_P_PRO_NEG.setName('VBZ_PRO_P_PRO_NEG')

NEG_VBZ_PRO_P_PRO_NEG = NEG1 + VBZ_PRO_P_PRO_NEG
NEG_VBZ_PRO_P_PRO_NEG.setName('NEG_VBZ_PRO_P_PRO_NEG')


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

VBD_P_PRO_NEG = vbd_neg + VB_IDO + NEG2
VBD_P_PRO_NEG.setName('VBD_P_PRO_NEG')

NEG_VBD_P_PRO_NEG = NEG1 + VBD_P_PRO_NEG
NEG_VBD_P_PRO_NEG.setName('NEG_VBD_P_PRO_NEG')

VBD_PRO_P_PRO_NEG = vbd_neg + VB_DO + VB_IDO + NEG2
VBD_PRO_P_PRO_NEG.setName('VBD_PRO_P_PRO_NEG')

NEG_VBD_PRO_P_PRO_NEG = NEG1 + VBD_PRO_P_PRO_NEG
NEG_VBD_PRO_P_PRO_NEG.setName('NEG_VBD_PRO_P_PRO_NEG')


# Uninflected

UNIN = SkipTo(endOfString)("stem")
UNIN.setName("UNIN")

P_UNIN = ( oneOf(prepositions) )("prefix") + SkipTo(endOfString)("stem")
P_UNIN.setName("P_UNIN")

# uninflected vbd #

UNINVBD_PRO = SkipTo(VB_DO + endOfString)("stem") + VB_DO("suffix")
UNINVBD_PRO.setName('UNINVBD_PRO')

UNINVBD_P_PRO = SkipTo(VB_IDO + endOfString)("stem") + VB_IDO("suffix")
UNINVBD_P_PRO.setName('UNINVBD_P_PRO')

UNINVBD_PRO_P_PRO = SkipTo(VBD_CLIT + endOfString)("stem") + VBD_CLIT("suffix")
UNINVBD_PRO_P_PRO.setName('UNINVBD_PRO_P_PRO')

# negative uninflected vbd #

UNINVBD_NEG = SkipTo(NEG2 + endOfString)("stem") + NEG2
UNINVBD_NEG.setName("UNINVBD_NEG")

UNINVBD_PRO_NEG = SkipTo(VB_DO + NEG2 + endOfString)("stem") + VB_DO + NEG2
UNINVBD_PRO_NEG.setName("UNINVBD_PRO_NEG")

UNINVBD_P_PRO_NEG = SkipTo(VB_IDO + NEG2 + endOfString)("stem") + VB_IDO + NEG2
UNINVBD_P_PRO_NEG.setName("UNINVBD_P_PRO_NEG")

UNINVBD_PRO_P_PRO_NEG = SkipTo(VB_DO + VB_IDO + NEG2 + endOfString)("stem") + VB_DO + VB_IDO + NEG2
UNINVBD_PRO_P_PRO_NEG.setName("UNINVBD_PRO_P_PRO_NEG")

NEG_UNINVBD_NEG = NEG1 + UNINVBD_NEG
NEG_UNINVBD_NEG.setName("NEG_UNINVBD_NEG")

NEG_UNINVBD_PRO_NEG = NEG1 + UNINVBD_PRO_NEG
NEG_UNINVBD_PRO_NEG.setName("NEG_UNINVBD_PRO_NEG")

NEG_UNINVBD_P_PRO_NEG = NEG1 + UNINVBD_P_PRO_NEG
NEG_UNINVBD_P_PRO_NEG.setName("NEG_UNINVBD_P_PRO_NEG")

NEG_UNINVBD_PRO_P_PRO_NEG = NEG1 + UNINVBD_PRO_P_PRO + NEG2
NEG_UNINVBD_PRO_P_PRO_NEG.setName("NEG_UNINVBD_PRO_P_PRO_NEG")


################
# WORD CLASSES #
################

# These word classes are passed to stemmer.py so that the parser knows which
# parse patterns to try.

verbs = [VBZ, VBZ_PRO, VBZ_P_PRO, VBZ_PRO_P_PRO,
         VBD, VBD_PRO, VBD_P_PRO, VBD_PRO_P_PRO]
neg_verbs = [NEG_VBD_NEG, NEG_VBD_PRO_NEG, NEG_VBD_P_PRO_NEG, NEG_VBD_PRO_P_PRO_NEG,
                 VBD_NEG,     VBD_PRO_NEG,     VBD_P_PRO_NEG,     VBD_PRO_P_PRO_NEG,
             NEG_VBZ_NEG, NEG_VBZ_PRO_NEG, NEG_VBZ_P_PRO_NEG, NEG_VBZ_PRO_P_PRO_NEG,
                 VBZ_NEG,     VBZ_PRO_NEG,     VBZ_P_PRO_NEG,     VBZ_PRO_P_PRO_NEG,]
nouns = [N_PRO, P_N_PRO, DET_N, P_DET_N]
prons = [P_PRO]
unin = [UNIN, P_UNIN,
        UNINVBD_PRO, UNINVBD_P_PRO, UNINVBD_PRO_P_PRO,
        UNINVBD_NEG, UNINVBD_PRO_NEG, UNINVBD_P_PRO_NEG, UNINVBD_PRO_P_PRO_NEG,
        NEG_UNINVBD_NEG, NEG_UNINVBD_PRO_NEG, NEG_UNINVBD_P_PRO_NEG, NEG_UNINVBD_PRO_P_PRO_NEG]

word_types = verbs + neg_verbs + nouns + prons + unin


