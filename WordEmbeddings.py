import os
import pandas as pd
import numpy
import matplotlib.pyplot as plt
import string
import json
import re
from gensim import corpora
from pprint import pprint
from gensim.models import Phrases
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer

from ds_voc.text_processing import TextProcessing

FILE = "TextCorpus.json"
FileJson = json.load(open(FILE))
RawSentences = [FileJson[sentenceID] for sentenceID in FileJson]
pprint(RawSentences)

if __name__ == "__main__":
  #Creating list of lists. Word2Vec expects tokens of each sentence. 
  te = TextProcessing()
  
  cleaned = [te.default_clean(d) for d in RawSentences]
  sentences = [te.stop_and_stem(d) for d in cleaned]
  print(sentences)