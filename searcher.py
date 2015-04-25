import sys
import json

from stemmer import stem

# finds the intersection of two sorted numerical sets
def intersect(s1, s2):
    merged = []
    idx1 = idx2 = 0
    while (idx1 < len(s1) and idx2 < len(s2)):
        if (s1[idx1] == s2[idx2]):
            merged.append(s1[idx1])
            idx1 += 1
            idx2 += 1
        elif (s1[idx1] < s2[idx2]):
            idx1 += 1
        else:
            idx2 += 1
    return merged

# finds the intersection of an array of sorted numerical sets
def merge(docset):
    merge_set = []
    if (len(docset) > 0):
        if (len(docset) == 1):
            merge_set = docset[0]
        else:
            for (idx, term_docs) in enumerate(docset):
                if (idx == 0):
                    merge_set = intersect(docset[idx], docset[idx + 1])
                else:
                    if ((idx + 1) < len(docset)):
                        merge_set = intersect(merge_set, docset[idx + 1])
    return merge_set



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

merge_set = merge(docset)

for doc in merge_set:
    print(id_map[str(doc)])
