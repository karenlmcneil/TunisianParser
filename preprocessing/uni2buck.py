#!/usr/bin/python

# Based on the buckwalter2unicode.py script by
# Andrew Roberts (andyr [at] comp (dot) leeds [dot] ac (dot) uk)
# Project homepage: http://www.comp.leeds.ac.uk/andyr/software/
#
# Modified to make it work better with Tunisian Arabic, and
# to make it more RegEx friendly
# Specifically, I stripped out the short vowels, added the gaaf
# and reallocated some of the letters to the hamzas so that no
# symbols are necessary. This makes it so that you can do a \w
# search and get back full words

# Declare a dictionary with Buckwalter's ASCII symbols as the keys, and
# their unicode equivalents as values.


buck2uni = {u"c": u"\u0621", # hamza-on-the-line -------- was ' in original
            u"A": u"\u0622", # madda
            u"e": u"\u0623", # hamza-on-'alif
            u"W": u"\u0624", # hamza-on-waaw
            u"I": u"\u0625", # hamza-under-'alif
            u"i": u"\u0626", # hamza-on-yaa'
            u"a": u"\u0627", # bare 'alif
            u"b": u"\u0628", # baa'
            u"p": u"\u0629", # taa' marbuuTa
            u"t": u"\u062A", # taa'
            u"v": u"\u062B", # thaa'
            u"j": u"\u062C", # jiim
            u"H": u"\u062D", # Haa'
            u"x": u"\u062E", # khaa'
            u"d": u"\u062F", # daal
            u"V": u"\u0630", # dhaal ------ Was * in original script
            u"r": u"\u0631", # raa'
            u"z": u"\u0632", # zaay
            u"s": u"\u0633", # siin
            u"J": u"\u0634", # shiin ------ Was $ in original script
            u"S": u"\u0635", # Saad
            u"D": u"\u0636", # Daad
            u"T": u"\u0637", # Taa'
            u"Z": u"\u0638", # Zaa' (DHaa')
            u"C": u"\u0639", # cayn ------ Was E in original script
            u"G": u"\u063A", # ghayn ------ Was g in original script
            u"f": u"\u0641", # faa'
            u"q": u"\u0642", # qaaf
            u"g": u"\u06A8", # gaaf ------ Added
            u"k": u"\u0643", # kaaf
            u"l": u"\u0644", # laam
            u"m": u"\u0645", # miim
            u"n": u"\u0646", # nuun
            u"h": u"\u0647", # haa'
            u"w": u"\u0648", # waaw
            u"E": u"\u0649", # 'alif maqSuura ------ Was E in original script
            u"y": u"\u064A", # yaa'
            u"_": u"\u0651", # shaddah ------ Was ~ in original script
            u",": u"\u060C", # arabic comma
            u"?": u"\u061f", # arabic questionmark
}

def transString(uniString, reverse=False):
    '''Given a Unicode string, transliterate into Buckwalter. To go from
    Buckwalter back to Unicode, set reverse=1'''

    out = ''

    # For Buckwalter -> Unicode transliteration..
    if not reverse:
        # Loop over each character in the string, inString.
        for char in uniString:
            out = out + buck2uni.get(char, char)

    # Same as above, just in the other direction.
    else:
        uni2buck = {}
        for (key, value) in buck2uni.items():
                uni2buck[value] = key
        for char in uniString:
            out = out + uni2buck.get(char, char)

    return out
