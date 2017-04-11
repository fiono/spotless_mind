import re
from collections import OrderedDict
from collections import Set

from posting_utils import *
from stemmer import stem

def phraseSearch(terms, index_dict):
    postings_lists = []

    for term in terms:
        try:
            sorted_postings = OrderedDict(sorted(index_dict[term].items(), key=lambda t:t[0]))
            postings_lists.append(sorted_postings)
        except KeyError:
            pass

    return phrase_merge(postings_lists)

def termSearch(terms, index_dict):
    docset = []

    for term in terms:
        try:
            term_map = index_dict[term]
            doc_ids = sorted(term_map.keys())
            docset.append(doc_ids)
        except KeyError:
            pass

    return merge(docset)

def noNailPolish(results, index_dict):
    nail_polish_results = phraseSearch("nail polish".split(), index_dict)
    return difference(results, nail_polish_results)

# searches an index file for a query
def getMatches(terms, is_phrase, full_index):
    results = []

    index_dict = full_index["index"]

    stemmed = [stem(term) for term in terms]
    if (is_phrase):
        results = phraseSearch(stemmed, index_dict)
    else:
        results = termSearch(stemmed, index_dict)

    results = noNailPolish(results, index_dict)

    return results
