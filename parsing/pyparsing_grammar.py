from pyparsing import StringEnd, oneOf, Optional, Or, Literal, SkipTo, FollowedBy, Combine, And


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
vb_clit = Or(vb_do, Optional(vb_do) + vb_ido)

pre_neg = ['م', 'ما']
post_neg = ['ش', 'شي']

##############
# Word Types #
##############

# Nouns

# كتابها --> كتاب + ها
N_PRO = SkipTo(noun_suffix | endOfString)("stem") + noun_suffix("suffix")
N_PRO.setName('N_PRO')

# وكتابها --> و + كتاب + ها
C_N_PRO = oneOf(conjunctions) ("prefix") + SkipTo(noun_suffix | endOfString)("stem") + noun_suffix("suffix")
C_N_PRO.setName('C_N_PRO')

# لكتابها --> ل + كتاب + ها
P_N_PRO = oneOf(prepositions) ("prefix") + SkipTo(noun_suffix | endOfString)("stem") + noun_suffix("suffix")
P_N_PRO.setName('P_N_PRO')

# ولكتابها --> و + ل + كتاب + ها
C_P_N_PRO = (oneOf(conjunctions) + oneOf(prepositions))("prefix") + SkipTo(noun_suffix | endOfString)("stem") + \
            noun_suffix("suffix")
C_P_N_PRO.setName('C_P_N_PRO')

# الكتاب --> ال + كتاب
DET_N =  oneOf(def_art)("prefix") + SkipTo(endOfString)("stem")
DET_N.setName('DET_N')

# والكتاب --> و + ال + كتاب
C_DET_N =  ( oneOf(conjunctions) + oneOf(def_art) )("prefix") + \
    SkipTo(endOfString)("stem")
C_DET_N.setName('C_DET_N')

# بالكتاب --> ب + ال + كتاب
P_DET_N = ( oneOf(prepositions) + ( oneOf(def_art) | oneOf(def_art_short) ) )("prefix") + SkipTo(endOfString)("stem")
P_DET_N.setName('P_DET_N')

# وبالكتاب --> و + ب + ال + كتاب
C_P_DET_N =  ( oneOf(conjunctions) + oneOf(prepositions) + ( oneOf(def_art) | oneOf(def_art_short) ) )("prefix") + \
    SkipTo(endOfString)("stem")
C_P_DET_N.setName('C_P_DET_N')


# Pronouns

# مانيش --> ما + ني + ش  #TODO remove these and add unanalyzed to pronouns
NEG_PRO_NEG = (Literal("ما")('prefix') + oneOf(dir_obj_suffixes)("stem") +
               Optional( Literal("ش"))('suffix')) + FollowedBy(endOfString)
NEG_PRO_NEG.setName('NEG_PRO_NEG')

C_NEG_PRO_NEG = (oneOf(conjunctions) + Literal("ما")) ("prefix") + \
                oneOf(dir_obj_suffixes)('stem') + Optional( Literal("ش"))('suffix') + \
                FollowedBy(endOfString)
C_NEG_PRO_NEG.setName('C_NEG_PRO_NEG')

# ماهيش --> ما + هي + ش
INT_PRO = Optional ( Literal("ما") )("prefix") + oneOf(pronouns)("stem") + \
    ( Literal("ش") + Optional( Literal("ي") ) +
    FollowedBy(endOfString) )("suffix")
INT_PRO.setName('INT_PRO')

EMPH_PRO = (oneOf(emphatics)('prefix') + oneOf(dir_obj_suffixes)("stem") +
           #Optional( Literal("ش") )('suffix') + \
           FollowedBy(endOfString))
EMPH_PRO.setName('EMPH_PRO')

C_EMPH_PRO = (oneOf(conjunctions)("prefix") + oneOf(emphatics)('prefix') +
             oneOf(dir_obj_suffixes)("stem") +
             #Optional( Literal("ش") )('suffix') + \
             FollowedBy(endOfString))
C_EMPH_PRO.setName('C_EMPH_PRO')

C_PRO = oneOf(conjunctions)("prefix") + oneOf(pronouns)("stem") + \
    FollowedBy(endOfString)
C_PRO.setName('C_PRO')

P_PRO = oneOf(prepositions)('prefix') + oneOf(dir_obj_suffixes)("stem") + \
    FollowedBy(endOfString)
P_PRO.setName('P_PRO')

C_P_PRO = ( oneOf(conjunctions) + oneOf(prepositions) )('prefix') + \
    oneOf(dir_obj_suffixes)("stem") + FollowedBy(endOfString)
C_P_PRO.setName('C_P_PRO')

# Verbs

VBZ = Combine(oneOf(vbz_pre_inflec)("prefix") +
              SkipTo(oneOf(vbz_suff_inflec, vb_clit) + endOfString | endOfString)("stem") +
              Optional(oneOf(vbz_suff_inflec))("suffix"))
VBZ.setName('VBZ')

VBZ_PRO = VBZ + oneOf(dir_obj_suffixes)
VBZ_PRO.setName('VBZ_PRO')

VBZ_P_PRO = VBZ + Literal('ل') + oneOf(ind_obj_suffixes)
VBZ_P_PRO.setName('VBZ_P_PRO')

C_VBZ = oneOf(conjunctions) + VBZ
C_VBZ.setName('C_VBZ')

C_VBZ_PRO = oneOf(conjunctions) + VBZ_PRO
C_VBZ_PRO.setName('C_VBZ_PRO')

VBD = Combine(SkipTo(oneOf(vbd_suff_inflec) + endOfString)("stem") +
              And(oneOf(vbd_suff_inflec), endOfString)("suffix"))
VBD.setName('VBD')

C_VBD = oneOf(conjunctions) + VBD
C_VBD.setName('C_VBD')

NEG_VBZ_NEG = oneOf(pre_neg) + VBZ + oneOf(post_neg)
NEG_VBZ_NEG.setName('NEG_VBZ_NEG')

C_NEG_VBZ_NEG = oneOf(conjunctions) + NEG_VBZ_NEG
C_NEG_VBZ_NEG.setName('C_NEG_VBZ_NEG')

NEG_VBD_NEG = oneOf(pre_neg) + VBD + oneOf(post_neg)
NEG_VBD_NEG.setName('NEG_VBD_NEG')

C_NEG_VBD_NEG = oneOf(conjunctions) + NEG_VBD_NEG
C_NEG_VBD_NEG.setName('C_NEG_VBD_NEG')



# Uninflected

UNIN = SkipTo(endOfString)("stem")
UNIN.setName("UNIN")

C_UNIN = ( oneOf(conjunctions) )("prefix") + SkipTo(endOfString)("stem")
C_UNIN.setName("C_UNIN")

P_UNIN = ( oneOf(prepositions) )("prefix") + SkipTo(endOfString)("stem")
P_UNIN.setName("P_UNIN")

C_P_UNIN = ( oneOf(conjunctions) + oneOf(prepositions) )("prefix") + \
    SkipTo(endOfString)("stem")
C_P_UNIN.setName("C_P_UNIN")



word_types = [N_PRO, C_N_PRO, P_N_PRO, C_P_N_PRO, DET_N, C_DET_N, P_DET_N, C_P_DET_N,  # Nouns
              NEG_PRO_NEG, C_NEG_PRO_NEG, INT_PRO, EMPH_PRO, C_EMPH_PRO, P_PRO, C_PRO, C_P_PRO,  # Pronouns
              VBZ, C_VBZ, VBD, C_VBD, NEG_VBZ_NEG, C_NEG_VBZ_NEG, NEG_VBD_NEG, C_NEG_VBD_NEG,  # Verbs
              UNIN, C_UNIN, P_UNIN, C_P_UNIN, ]                                          # Uninflected


