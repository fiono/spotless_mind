import re
from collections import OrderedDict

import posting_utils
from stemmer import stem

# searches an index file for a query
def getMatches(query, full_index):
    results = []

    id_map = full_index["id_map"]
    index_dict = full_index["index"]

    is_phrase = (len(query) == 1 and re.search(' ', query[0]) != None)

    if (is_phrase):
        terms = [stem(term) for term in query[0].split()]
        postings_lists = []

        for term in terms:
            try:
                sorted_postings = OrderedDict(sorted(index_dict[term].items(), key=lambda t:t[0]))
                postings_lists.append(sorted_postings)
            except KeyError:
                pass

        results = posting_utils.phrase_merge(postings_lists)

    else:
        terms = [stem(term) for term in query]
        docset = []

        for term in terms:
            try:
                term_map = index_dict[term]
                doc_ids = sorted(term_map.keys())
                docset.append(doc_ids)
            except KeyError:
                pass

        results = posting_utils.merge(docset)

    return results
