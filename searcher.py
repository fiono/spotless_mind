import sys
import json
import re
from collections import OrderedDict

import posting_utils
from stemmer import normalize

# searches an index file for a query
def search(query, full_index):
    results = []

    id_map = full_index["id_map"]
    index_dict = full_index["index"]

    is_phrase = (len(query) == 1 and re.search(' ', query[0]) != None)
    if (is_phrase):
        terms = [normalize(term) for term in query[0].split()]
        postings_lists = []
        for term in terms:
            sorted_postings = OrderedDict(sorted(index_dict[term].items(), key=lambda t:t[0]))
            postings_lists.append(sorted_postings)

        results = posting_utils.phrase_merge(postings_lists)

    else:
        terms = [normalize(term) for term in query]
        docset = []
        for term in terms:
            try:
                term_map = index_dict[term]
                doc_ids = sorted(term_map.keys())
            except KeyError:
                doc_ids = []
            docset.append(doc_ids)

        results = posting_utils.merge(docset)

    return results

if (len(sys.argv) < 2):
    print("Must supply a query term or phrase.")
    sys.exit()

try:
    index_file = open('indexes/test_data_index', "r")
except FileNotFoundError:
    print("The index file is not valid.")
    sys.exit()

full_index = json.loads(index_file.read())
index_file.close()

query = sys.argv[1:]

results = search(query, full_index)
for doc in results:
    print(full_index["id_map"][str(doc)])
