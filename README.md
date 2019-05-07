# Tunisian Arabic Morphological Segmenter and POS Tagger

## Description
This package performs morphological segmentation and part of speech
tagging for Tunisian Arabic.

This package contains the following main elements:
* `preprocessor.py` (and supporting files): normalizes Tunisian Arabic
text
* `aeb_parser.py`: a rules-based parser that performs morphological 
segmentation and assigns a part-of-speech tag (Note: "aeb" 
is the Ethnologue language code for Tunisian Arabic and is 
used in some of the file names to avoid name conflicts with
other Python packages)
* `parse_eval.py`: evaluates the output of aeb_parser
* `aeb_tagging.py`: uses a hand-annotated gold-standard file to train 
and evaluate several NLTK supervised learning POS taggers.

## Results
The hand-rolled parser (`aeb_parser.py`) segments words with a 92.0% accuracy. The part-of-speech 
tagging performed by the parser has an accuracy of approximately 84.3%,
after correcting mis-segmentations.

The supervised learning POS taggers (TrigramTagging and BrillTagging)
perform nearly as well, achieving a top accuracy of 83.9% for the
BrillTagger with Leave One Out cross-validation. (This, of course, was
on the already segmented data.)

There are three interesting conclusions for this project.
1. Supervised learning methods can be valuable, even for under-
resourced languages with very small annotated resources. The total
training and test data size was for this project was just 452 sentences,
about 6,000 words / 70 Kilobytes).
2. For tiny data sets like this, Leave One Out performs 
better than 10-fold cross validation, improving the accuracy by over 
0.5%.
3. In this specific case, the supervised learning taggers are not
particularly useful, since they require that the data be previously
segmented, and the laboriously-created rules-based segmenter used here 
determines the part of speech of each word as a consequence of finding 
the correct parse. However, this work is still exciting in 
demonstrating that, if a similarly easy method (that does not return
the POS) for segmentation can be developed, the part of speech tagging
can be performed afterwards 
at a fair accuracy.

## preprocessing/preprocessor.py
### Description
This prepares Tunisian Arabic text for parsing. Specifically,
it:
* Inserts a space between Arabic characters and foreign
(English or French) characters (it is common for Tunisians 
to code-switch, even in the middle of a word, for example by
using a French word with an Arabic definite article). To do 
this it relies on a helper function, `test_lang` that 
exploits Arabic characters' lack of case to determine if a
character is in Arabic or Latin script.
* Normalizes some spelling features (hamzas, for example)
* Tokenizes the text

## aeb_parser.py

### Description
This parser is a rules-based morphological segmentator (also called a light stemmer) for 
Tunisian Arabic. In the process of segmentation, it also assigns
POS tags.

### Usage
As input, the parser takes a string of Arabic, writen in Arabic script 
(no transliteration is necessary). It does this by defining an
extensive grammar of affixes and word types, then uses the
`pyparsing` module to create a list of possible parses. 
(Because Tunisian Arabic is highly inflectional and the 
script does not represent short vowels, word surface forms
tend to be ambiguous and have several possible parses). It
then uses the concept of "suffix-level similarity" (Dasgupta 
and Ng 2007) to determine the correct parse.

All clitics are removed, but verb inflections are kept with the verb.
For example, the complex word mā-ktib-at-hā-l-ī-š 
(neg-wrote-3f-it-to-me-neg, 'She didn't write it to me') would be
parsed as: `[('mā', 'NEG'), ('ktibat', 'VBD'), ('hā', 'PRO'), ('l', 'PREP'), 
('ī', 'PRO'), ('š', 'NEG')]`

The string to be parsed can be entered as an argument on the command line:
```text
$ python aeb_parser.py --string "ماكتبتهاليش"

[('ما', 'NEG'), ('كتبت', 'VBD'), ('ها', 'PRO'), ('ل', 'P'), ('ي', 'PRO'), ('ش', 'NEG')]

```

Multiword strings can also be parsed. Here is the sentence, 

    min  waqtāš rejʕ-at     te-ḥkī  mʕā-hu   al-mudīr?
    from when   returned-2p 2p-talk with-him the-boss?
    'Since when are you back to talking to the boss?'

```text
$ python parser.py --string "من وقتاش رجعت تحكي معاه المدير؟"

[('من', 'PREP'), ('وقتاش', 'INTEROG'), ('رجعت', 'VBD'), ('تحكي', 'VBZ'), 
('معا', 'N') ,('ه', 'PRO'), ('ال', 'DET'), ('مدير', 'N'), ('؟', 'PUNCT')]
```
This sentence shows some of the shortcomings of the parser: the 
preposition `mʕā` is mislabeled here as a noun.

In addition to the `parse_string` function shown above, the module
contains a `parse_file` function, but this is not accessible from the command line.

## parse_eval.py

### Description
This module evaluates the accuracy of the output of aeb_parser.py. The
accuracy is given in three measures:
1. Accuracy on the word-level, i.e. whether the word was parsed correctly. 
2. Segmentation precision at the character level.
3. Segmentation recall at the character level.

The evaluation is performed using `data/segmentation_gold.txt`, a 
gold-standard file of 2,000 words, 
which were randomly selected (in groups of five) from the corpus text
and segmented by hand.

### Usage
```text
$ python parse_eval.py --filename "data/segmentation_gold.txt"

Word-level segmentation accuracy is 92.08% 
Character-level segmentation precision is 97.62% 
Character-level segmentation recall is 93.44%
```

## aeb_tagging.py

This module takes a gold standard tsv file of the format
```csv
word \t tag
word \t tag
word \t tag
...

```
and uses it to train several NLTK part-of-speech taggers:
UnigramTagger, BigramTagger, TrigramTagger, and BrillTagger.
It then evaluates each tagger and returns a dictionary with
the score for each tagger.

The data is split into training and testing sets using 
k-fold cross validation. Leave One Out cross validation is
also available (in which k equals the length of the total
data set minus one).

### Usage and Results
```text
$ python aeb_tagging.py --filename 'data/gold_standard_403.tsv' --n_folds 10
DefaultTagger : 26.61%
UnigramTagger : 82.53%
BigramTagger : 83.12%
TrigramTagger : 83.24%
BrillTagger : 83.30%

$ python aeb_tagging.py --filename 'data/gold_standard_403.tsv' --loo True
DefaultTagger : 26.98%
UnigramTagger : 82.59%
BigramTagger : 83.37%
TrigramTagger : 83.81%
BrillTagger : 83.93%

```

The best-performing tagger--barely--was the Brill tagger, used with
Leave One Out cross-validation. Interestingly, of the 89 
rule possibilities, the Brill tagger only used between two 
and six, depending on the run. The most useful 
features were the two previous words, and the part
 of speech of the previous and following word:
```text
>>> brill_tagger.print_template_statistics(printunused=False)
TEMPLATE STATISTICS (TRAIN)  4 templates, 4 rules)
TRAIN (   5516 tokens) initial    83 0.9850 final:    74 0.9866 
#ID | Score (train) |  #Rules     | Template
--------------------------------------------
080 |     3   0.333 |   1   0.250 | Template(Pos([-1]),Pos([1]))
083 |     2   0.222 |   1   0.250 | Template(Word([-2]))
081 |     2   0.222 |   1   0.250 | Template(Word([-1]))
073 |     2   0.222 |   1   0.250 | Template(Pos([1]))
```