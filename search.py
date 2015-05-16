import re
from collections import OrderedDict
from collections import Set

import posting_utils
from stemmer import stem

def phraseSearch(terms, index_dict):
    postings_lists = []

    for term in terms:
        try:
            sorted_postings = OrderedDict(sorted(index_dict[term].items(), key=lambda t:t[0]))
            postings_lists.append(sorted_postings)
        except KeyError:
            pass

    return posting_utils.phrase_merge(postings_lists)

def termSearch(terms, index_dict):
    docset = []

    for term in terms:
        try:
            term_map = index_dict[term]
            doc_ids = sorted(term_map.keys())
            docset.append(doc_ids)
        except KeyError:
            pass

    return posting_utils.merge(docset)

def noNailPolish(results, index_dict):
    nail_polish_results = phraseSearch("nail polish".split(), index_dict)
    return set(results).difference(set(nail_polish_results))

# searches an index file for a query
def getMatches(query, full_index):
    results = []

    index_dict = full_index["index"]

    is_phrase = (len(query) == 1 and re.search(' ', query[0]) != None)

    if (is_phrase):
        terms = [stem(term) for term in query[0].split()]
        results = phraseSearch(terms, index_dict)

    else:
        terms = [stem(term) for term in query]
        results = termSearch(terms, index_dict)

    results = noNailPolish(results, index_dict)

    return results
