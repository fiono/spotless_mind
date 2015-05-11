import sys
import json
from collections import OrderedDict

import posting_utils
from stemmer import normalize

if (len(sys.argv) != 3):
    print("Must supply an index name and one quoted search term or phrase.")
    sys.exit()

index_path = 'indexes/%s_index' % sys.argv[1]
query = sys.argv[2]
is_phrase_match = True

try:
    index_file = open(index_path, "r")
except FileNotFoundError:
    print("The index name provided is not valid.")
    sys.exit()

full_index = json.loads(index_file.read())
index_file.close()

id_map = full_index["id_map"]
index_dict = full_index["index"]

terms = [normalize(term) for term in query.split()]

results = []
if (is_phrase_match):
    postings_lists = []
    for term in terms:
        sorted_postings = OrderedDict(sorted(index_dict[term].items(), key=lambda t:t[0]))
        postings_lists.append(sorted_postings)

    results = posting_utils.phrase_merge(postings_lists)

else:
    docset = []
    for term in terms:
        try:
            term_map = index_dict[term]
            doc_ids = sorted(term_map.keys())
        except KeyError:
            doc_ids = []
        docset.append(doc_ids)

    results = posting_utils.merge(docset)

for doc in results:
    print(id_map[str(doc)])
