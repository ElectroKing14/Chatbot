import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
import spacy

nlp = spacy.load("de_core_news_lg")

while True:
    for token in nlp(input()):
        print(token.lemma_)