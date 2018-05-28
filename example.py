#!/usr/bin/python
# -*- coding: utf-8 -*-

from takahe import takahe
import spacy

################################################################################
raw_sentences = [
    "The wife of a former U.S. president Bill \
Clinton Hillary Clinton visited China last Monday.",
    "Hillary Clinton wanted to visit China \
last month but postponed her plans till Monday \
last week.", "Hillary Clinton paid a visit to \
the People Republic of China on Monday.",
    "Last week the Secretary of State Ms. Clinton \
visited Chinese officials."
]
################################################################################

nlp = spacy.load('en')
sentences = [nlp(s) for s in raw_sentences]


def token_to_tagged(token):
    if token.pos_ == 'PUNCT':
        return f"{token.text}/{token.pos_}"
    return f"{token.text}/{token.tag_}"


sentences = [
    ' '.join([token_to_tagged(token) for token in sent]) for sent in sentences
]
print(sentences)

# Create a word graph from the set of sentences with parameters :
# - minimal number of words in the compression : 6
# - language of the input sentences : en (english)
# - POS tag for punctuation marks : PUNCT
compresser = takahe.word_graph(
    sentences, nb_words=6, lang='en', punct_tag="PUNCT")

# Get the 50 best paths
candidates = compresser.get_compression(50)

# 1. Rerank compressions by path length (Filippova's method)
for cummulative_score, path in candidates:

    # Normalize path score by path length
    normalized_score = cummulative_score / len(path)

    # Print normalized score and compression
    print(round(normalized_score, 3), ' '.join([u[0] for u in path]))

# Write the word graph in the dot format
compresser.write_dot('test.dot')

# 2. Rerank compressions by keyphrases (Boudin and Morin's method)
reranker = takahe.keyphrase_reranker(sentences, candidates, lang='en')

reranked_candidates = reranker.rerank_nbest_compressions()

# Loop over the best reranked candidates
for score, path in reranked_candidates:

    # Print the best reranked candidates
    print(round(score, 3), ' '.join([u[0] for u in path]))
