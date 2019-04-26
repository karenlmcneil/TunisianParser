from pyparsing import StringEnd, oneOf, Optional, Or, Literal, SkipTo, FollowedBy, Combine


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

noun_suffix = oneOf(poss_suffixes) + FollowedBy(endOfString)

# Verb Clitics
vbz_pre_inflec = ['ان', 'ن', 'ت', 'ي']
key_vbz_prefixes = ['ي', 'ت', 'ن']
vbz_suff_inflec = ['وا', 'و']
vbd_suff_inflec = ["ت", "نا", "توا", "و", "وا"]
key_vbd_suffixes = ["ت", "نا", "و", "وا"]
dir_obj_suffixes = ["ني", "نا", "ك", "كم", "و", "ه", "هو", "ها", "هم"]
ind_obj_suffixes = ["ي", "نا", "ن", "كم", "و", "ه", "هو", "ها", "هم"]

vb_do = oneOf(dir_obj_suffixes)
vb_ido = Literal("ل") + oneOf(ind_obj_suffixes)
vb_clit = Or([vb_do, Optional(vb_do) + vb_ido])

pre_neg = ['م', 'ما']
post_neg = ['ش', 'شي']


##############
# Word Types #
##############

# Nouns

# كتابها --> كتاب + ها
N_PRO = SkipTo(noun_suffix | endOfString)("stem") + noun_suffix("suffix")
N_PRO.setName('N_PRO')

# لكتابها --> ل + كتاب + ها
P_N_PRO = oneOf(prepositions) ("prefix") + SkipTo(noun_suffix | endOfString)("stem") + noun_suffix("suffix")
P_N_PRO.setName('P_N_PRO')

# الكتاب --> ال + كتاب
DET_N =  oneOf(def_art)("prefix") + SkipTo(endOfString)("stem")
DET_N.setName('DET_N')

# بالكتاب --> ب + ال + كتاب
P_DET_N = ( oneOf(prepositions) + ( oneOf(def_art) | oneOf(def_art_short) ) )("prefix") + SkipTo(endOfString)("stem")
P_DET_N.setName('P_DET_N')


# Pronouns

P_PRO = oneOf(prepositions)('prefix') + oneOf(ind_obj_suffixes)("stem") + \
    FollowedBy(endOfString)
P_PRO.setName('P_PRO')


#################
    #VERBS#
#################

VBZ = Combine(oneOf(vbz_pre_inflec)("prefix") +
              SkipTo(oneOf(vbz_suff_inflec, vb_clit) + endOfString | endOfString)("stem") +
              Optional(oneOf(vbz_suff_inflec))("suffix"))
VBZ.setName('VBZ')

VBZ_PRO = VBZ + oneOf(dir_obj_suffixes)
VBZ_PRO.setName('VBZ_PRO')

VBZ_P_PRO = VBZ + Literal('ل') + oneOf(ind_obj_suffixes)
VBZ_P_PRO.setName('VBZ_P_PRO')

VBZ_PRO_P_PRO = VBZ + oneOf(dir_obj_suffixes) + Literal('ل') + oneOf(ind_obj_suffixes)
VBZ_PRO_P_PRO.setName('VBZ_PRO_P_PRO')

VBD = Combine(SkipTo(oneOf(vbd_suff_inflec) + Or([vb_clit + endOfString, endOfString]))("stem") +
              oneOf(vbd_suff_inflec)("suffix"))
VBD.setName('VBD')

VBD_PRO = VBD + oneOf(dir_obj_suffixes)
VBD_PRO.setName('VBD_PRO')

VBD_P_PRO = VBD + Literal('ل') + oneOf(ind_obj_suffixes)
VBD_P_PRO.setName('VBD_P_PRO')

VBD_PRO_P_PRO = VBD + oneOf(dir_obj_suffixes) + Literal('ل') + oneOf(ind_obj_suffixes)
VBD_PRO_P_PRO.setName('VBD_PRO_P_PRO')

NEG_VBZ_NEG = oneOf(pre_neg) + VBZ + oneOf(post_neg)
NEG_VBZ_NEG.setName('NEG_VBZ_NEG')

NEG_VBD_NEG = oneOf(pre_neg) + VBD + oneOf(post_neg)
NEG_VBD_NEG.setName('NEG_VBD_NEG')



# Uninflected

UNIN = SkipTo(endOfString)("stem")
UNIN.setName("UNIN")

P_UNIN = ( oneOf(prepositions) )("prefix") + SkipTo(endOfString)("stem")
P_UNIN.setName("P_UNIN")

UNINVBD_PRO = SkipTo(vb_do + endOfString)("stem") + vb_do("suffix")
UNINVBD_PRO.setName('UNINVBD_PRO')

UNINVBD_PRO_P_PRO = SkipTo(vb_clit + endOfString)("stem") + vb_clit("suffix")
UNINVBD_PRO_P_PRO.setName('UNINVBD_PRO_P_PRO')

UNINVBD_P_PRO = SkipTo(vb_ido + endOfString)("stem") + vb_ido("suffix")
UNINVBD_P_PRO.setName('UNINVBD_P_PRO')


################
# WORD CLASSES #
################

verbs = [VBZ, VBZ_PRO, VBZ_P_PRO, VBZ_PRO_P_PRO, #VBZ
              VBD, VBD_PRO, VBD_P_PRO, VBD_PRO_P_PRO]

neg_verbs = [NEG_VBZ_NEG, NEG_VBD_NEG]

nouns = [N_PRO, P_N_PRO, DET_N, P_DET_N]

prons = [P_PRO]

unin = [UNIN, P_UNIN, UNINVBD_PRO, UNINVBD_P_PRO]

word_types = verbs + neg_verbs + nouns + prons + unin


