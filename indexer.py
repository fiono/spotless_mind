import sys
import os
import json

from tokenizer import tokenize
from stemmer import stem

if (len(sys.argv) != 2):
    print("Must supply one directory for indexing.")
    sys.exit()

dirname = sys.argv[1]
if (not os.path.isdir(sys.argv[1])):
    print("%s is not a valid directory" % (dirname))
    sys.exit()

basename = os.path.basename(dirname.rstrip("/"))
index_file = open('./indexes/%s_index' % basename, 'w');

id_map = {}
index_dict = {}
doc_id = 0
for (root, dirnames, filenames) in os.walk(dirname):
    for filename in filenames:
        file = open(os.path.join(root, filename), 'r')
        id_map[doc_id] = filename

        tokens = tokenize(file)
        for (pos, token) in tokens:
            token = stem(token)
            try:
                bucket = index_dict[token]
                found = False
                for doc in bucket:
                    if (doc["id"] == doc_id):
                        doc["positions"].append(pos)
                        found = True
                if (not found):
                    bucket.append({"id" : doc_id, "positions" : [pos]})
            except KeyError:
                index_dict[token] = [{"id" : doc_id, "positions" : [pos]}]

        doc_id = doc_id + 1
        file.close()

full_index = {"id_map" : id_map, "index" : index_dict}
index_file.write(json.dumps(full_index))
index_file.close()
