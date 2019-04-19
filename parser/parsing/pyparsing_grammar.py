from pyparsing import StringEnd, oneOf, Optional, Literal, SkipTo, FollowedBy


endOfString = StringEnd()

conjunctions = ['و']
#affixed_prepositions = ['ل', 'ب', 'م']
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
vbz_prefixes = ['ان','ن','ت','ي']
key_vbz_prefixes = ['ي', 'ت', 'ن']
vbz_suffixes = ['وا', 'و']
vbd_suffixes = ["ت", "نا", "توا", "و", "وا"]
key_vbd_suffixes = ["ت", "نا", "و", "وا"]
dir_obj_suffixes = ["ني", "نا", "ك", "كم", "و", "ه", "هو", "ها", "هم"]
ind_obj_suffixes = ["ي", "نا", "ن", "كم", "و", "ه", "هو", "ها", "هم"]

vbz_suffix = Optional( oneOf(vbz_suffixes) ) + Optional( oneOf(dir_obj_suffixes) ) + \
                     Optional( Literal("ل") + oneOf(ind_obj_suffixes) )

vbd_suffix = oneOf(vbd_suffixes)  + Optional( oneOf(dir_obj_suffixes) ) + \
                Optional( Literal("ل") + oneOf(ind_obj_suffixes) )


##############
# Word Types #
##############

# Nouns

# كتابها --> كتاب + ها
NS = SkipTo(noun_suffix | endOfString)("stem") + noun_suffix("suffix")
NS.setName('NS')

# وكتابها --> و + كتاب + ها
C_NS = oneOf(conjunctions) ("prefix") + SkipTo(noun_suffix | endOfString)("stem") + noun_suffix("suffix")
C_NS.setName('C_NS')

# لكتابها --> ل + كتاب + ها
P_NS = oneOf(prepositions) ("prefix") + SkipTo(noun_suffix | endOfString)("stem") + noun_suffix("suffix")
P_NS.setName('P_NS')

# ولكتابها --> و + ل + كتاب + ها
C_P_NS = ( oneOf(conjunctions) + oneOf(prepositions) )("prefix") + SkipTo(noun_suffix | endOfString)("stem") + \
    noun_suffix("suffix")
C_P_NS.setName('C_P_NS')

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

# مانيش --> ما + ني + ش
NEG_PRO = ( Literal("ما")('prefix') + oneOf(dir_obj_suffixes)("stem") + \
    Optional( Literal("ش") )('suffix') ) + FollowedBy(endOfString)
NEG_PRO.setName('NEG_PRO')

C_NEG_PRO = ( oneOf(conjunctions) + Literal("ما") ) ("prefix") + \
    oneOf(dir_obj_suffixes)('stem') + Optional( Literal("ش") )('suffix') + \
    FollowedBy(endOfString)
C_NEG_PRO.setName('C_NEG_PRO')

# ماهيش --> ما + هي + ش
INT_PRO = Optional ( Literal("ما") )("prefix") + oneOf(pronouns)("stem") + \
    ( Literal("ش") + Optional( Literal("ي") ) + \
    FollowedBy(endOfString) )("suffix")
INT_PRO.setName('INT_PRO')

EMPH = oneOf(emphatics)('prefix') + oneOf(dir_obj_suffixes)("stem") + \
    Optional( Literal("ش") )('suffix')  + FollowedBy(endOfString)
EMPH.setName('EMPH')

C_EMPH = oneOf(conjunctions)("prefix") + oneOf(emphatics)('prefix') +  \
    oneOf(dir_obj_suffixes)("stem") + Optional( Literal("ش") )('suffix') + \
    FollowedBy(endOfString)
C_EMPH.setName('C_EMPH')

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

VBZ = oneOf(vbz_prefixes)("prefix") + SkipTo( vbz_suffix + endOfString | endOfString)("stem") + Optional( (vbz_suffix)("suffix") )
VBZ.setName('VBZ')

C_VBZ = ( oneOf(conjunctions) + oneOf(vbz_prefixes) )("prefix") + SkipTo( vbz_suffix + endOfString | endOfString)("stem") + \
    Optional(vbz_suffix)("suffix")
C_VBZ.setName('C_VBZ')

VBD = SkipTo( vbd_suffix + endOfString )("stem") + (vbd_suffix + endOfString)("suffix")
VBD.setName('VBD')

C_VBD = oneOf(conjunctions)("prefix") + SkipTo( vbd_suffix + endOfString )("stem") + (vbd_suffix + endOfString)("suffix")
C_VBD.setName('C_VBD')

NEG_VBZ = ( Optional( oneOf("م ما") ) + oneOf(vbz_prefixes)  )("prefix") + \
            SkipTo( vbz_suffix + Literal("ش") + endOfString | Literal("ش") + endOfString )("stem") + \
            ( Optional(vbz_suffix) + Literal("ش") + endOfString )("suffix")
NEG_VBZ.setName('NEG_VBZ')

C_NEG_VBZ = ( oneOf(conjunctions) + Optional( oneOf("م ما" ) + oneOf(vbz_prefixes)  )("prefix") + \
            SkipTo( vbz_suffix + Literal("ش") + endOfString | Literal("ش") + endOfString )("stem") + \
            ( Optional(vbz_suffix) + Literal("ش") + endOfString )("suffix") )
C_NEG_VBZ.setName('C_NEG_VBZ')

NEG_VBD = ( Optional( oneOf("م ما" ) )("prefix") + \
            SkipTo( vbd_suffix + Literal("ش") + endOfString | Literal("ش") + endOfString )("stem") + \
            (Optional(vbd_suffix) + Literal("ش") + endOfString)("suffix") )
NEG_VBD.setName('NEG_VBD')

C_NEG_VBD = ( Optional(oneOf(conjunctions)) + Optional( oneOf("م ما" ) )("prefix") + \
            SkipTo( vbd_suffix + Literal("ش") + endOfString | Literal("ش") + endOfString )("stem") + \
            (Optional(vbd_suffix) + Literal("ش") + endOfString)("suffix") )
C_NEG_VBD.setName('C_NEG_VBD')


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



word_types = [ NS, C_NS, P_NS, C_P_NS, DET_N, C_DET_N, P_DET_N, C_P_DET_N,              # Nouns
              NEG_PRO, C_NEG_PRO, INT_PRO, EMPH, C_EMPH, P_PRO, C_PRO, C_P_PRO,         # Pronouns
              VBZ, C_VBZ, VBD, C_VBD, NEG_VBZ, C_NEG_VBZ, NEG_VBD, C_NEG_VBD,           # Verbs
              UNIN, C_UNIN, P_UNIN, C_P_UNIN,]                                          # Uninflected


