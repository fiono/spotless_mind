import sys
import json

import setutils
from stemmer import stem

if (len(sys.argv) != 3):
    print("Must supply an index name and one quoted search term or phrase.")
    sys.exit()

index_path = 'indexes/%s_index' % sys.argv[1]
query = sys.argv[2]

try:
    index_file = open(index_path, "r")
except FileNotFoundError:
    print("The index name provided is not valid.")
    sys.exit()

full_index = json.loads(index_file.read())
index_file.close()

id_map = full_index["id_map"]
index_dict = full_index["index"]

docset = []
for term in query.split():
    term = stem(term)
    try:
        term_docs = index_dict[term]
        doc_ids = []
        for doc in term_docs:
            doc_ids.append(doc["id"])
    except KeyError:
        doc_ids = []
    docset.append(doc_ids)

merge_set = setutils.merge(docset)

for doc in merge_set:
    print(id_map[str(doc)])
