import re
from .arabic_const import *


HARAKAT_pat =re.compile(r'|'.join([FATHATAN,DAMMATAN,KASRATAN,FATHA,DAMMA,KASRA,SUKUN,SHADDA]))
HAMZAT_pat =re.compile(r'|'.join([WAW_HAMZA,YEH_HAMZA]))
ALEFAT_pat =re.compile(r'|'.join([ALEF_MADDA,ALEF_HAMZA_ABOVE,ALEF_HAMZA_BELOW,HAMZA_ABOVE,HAMZA_BELOW]))
LAMALEFAT_pat =re.compile(r'|'.join([LAM_ALEF,LAM_ALEF_HAMZA_ABOVE,LAM_ALEF_HAMZA_BELOW,LAM_ALEF_MADDA_ABOVE]))

def strip_tashkeel(w):
	"strip vowels from a word and return a result word"
	return HARAKAT_pat.sub('', w)

def strip_tatweel(w):
	"strip tatweel from a word and return a result word"
	return re.sub(TATWEEL, '', w)

def normalize_hamza(w):
	"replace various alef-hamza combinations with plain alef"
	w=ALEFAT_pat.sub(ALEF, w)
	return HAMZAT_pat.sub(HAMZA, w)

def normalize_lamalef(w):
	"standardize lam-alef ligatures"
	return LAMALEFAT_pat.sub(u'%s%s'%(LAM,ALEF), w)

def normalize_spellerrors(w):
	"change all tah marboutas to ha's"
	return re.sub(TEH_MARBUTA,	HEH, w)
	#return re.sub(ur'[%s]' % ALEF_MAKSURA,	YEH, w)


def normalize(text):
    text=strip_tashkeel(text);
    text=strip_tatweel(text);
    text=normalize_lamalef(text);
    text=normalize_hamza(text);
    #text=normalize_spellerrors(text);
    return text;
