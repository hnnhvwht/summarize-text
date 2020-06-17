import math
from spacy.lang.pt.stop_words import STOP_WORDS
from sklearn.feature_extraction.text import CountVectorizer


def summarize(doc, pct_sentences, min_tokens):
    """
    Summarize a document by collecting the most important sentences.
    Sentences are ranked based on the weighted frequency of their 
    constituent tokens (words).
    
    Parameters
    ----------
    doc : spacy.tokens.doc.Doc
        Sequence of spaCy Token objects
    pct_sentences : float
        Percentage of the most highly ranked sentences to include
    min_tokens : int
        Minimum number of tokens needed for inclusion of a sentence
    
    Returns
    -------
    summary : list
    """
    corpus = [sent.text.lower() for sent in doc.sents]
    cv = CountVectorizer(stop_words=list(STOP_WORDS))   
    cv_fit = cv.fit_transform(corpus)    
    word_list = cv.get_feature_names();    
    count_list = cv_fit.toarray().sum(axis=0)    
    word_frequencies = dict(zip(word_list, count_list))
    top_frequency = max(word_frequencies.values())
    
    for word in word_frequencies.keys():
        word_frequencies[word] = word_frequencies[word] / top_frequency

    sentence_rank = dict()
    for sent in doc.sents:
        for word in sent:
            if word.text.lower() in word_frequencies.keys():
                if sent in sentence_rank.keys():
                    sentence_rank[sent] += word_frequencies[word.text.lower()]
                else:
                    sentence_rank[sent] = word_frequencies[word.text.lower()]

    top_ranks = [rank for rank in sentence_rank.values() if rank >= min_tokens]
    top_ranks = sorted(top_ranks, reverse=True)
    top_idx = math.ceil(pct_sentences / 100 * len(top_ranks))
    top_ranks = top_ranks[:top_idx]

    summary = [str(sent) for sent, rank in sentence_rank.items()
               if rank in top_ranks]
    
    return summary
