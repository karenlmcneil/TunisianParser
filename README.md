# Tunisian Arabic Morphological Segmenter and POS Tagger

## Description
This package performs morphological segmentation and part of speech
tagging for Tunisian Arabic.

## aeb_parser.py

### Usage
As input, the parser takes a string of Arabic, writen in Arabic script 
(no transliteration is necessary).

For example, the complex word `mā-ktib-at-hā-l-ī-š 
(neg-wrote-3pf-it-to-me-neg, 'She didn't write it to me') would be
parsed as follows:
```text
$ python parser.py --string "ماكتبتهاليش"

[('ما', 'NEG'), ('كتبت', 'VBD'), ('ها', 'PRO'), ('ل', 'P'), ('ي', 'PRO'), ('ش', 'NEG')]

```

Multiword strings can also be parsed. Here is the sentence, 
min waqtāš rejʕ-at te-ḥkī mʕā-hu al-mudīr?
from when returned-2p 2p-talk with-him the-boss?
'Since when are you back to talking to the boss?'

```text
$ python parser.py --string "من وقتاش رجعت تحكي معاه المدير؟"

[('من', 'P'), ('وقتاش', 'INTEROG'), ('رجعت', 'VBD'), ('تحكي', 'VBZ'), ('معا', 'N'), ('ه', 'PRO'), ('ال', 'DET'), ('مدير', 'N'), ('؟', 'PUNCT')]
```

## parse_eval.py

### Usage
```text
$ python parse_eval.py

Word-level segmentation accuracy is 92.08% 
Character-level segmentation precision is 97.62% 
Character-level segmentation recall is 93.44%


```

## aeb_tagging.py

### Usage
```text
$ python aeb_tagging.py --n_folds 10
{'DefaultTagger': 0.2661379031035197, 'UnigramTagger': 0.8252707356105378, 'BigramTagger': 0.8311627137602488, 'TrigramTagger': 0.8324412327452249}

$ python aeb_tagging.py --loo True
{'DefaultTagger': 0.26979523430344154, 'UnigramTagger': 0.8259191576444443, 'BigramTagger': 0.8337195775813869, 'TrigramTagger': 0.8381413203179351}

```