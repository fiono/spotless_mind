import sys
import json
import os

from search import getMatches

if (len(sys.argv) < 2):
    print("Must supply a query term or phrase.")
    sys.exit()

try:
    index_file = open('indexes/data_index', "r")
except OSError:
    print("The index file is not valid.")
    sys.exit()

full_index = json.loads(index_file.read())
index_file.close()

query = sys.argv[1:]

results = getMatches(query, full_index)

for doc in results:
    print("\n")
    filename = full_index["id_map"][str(doc)]
    print(filename)

    fh = open("data/" + filename, 'r')

    print(fh.read())
    print("========")
    print("\n")

    fh.close()
