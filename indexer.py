import argparse
import json
import os
import re
import sys

from tokenizer import tokenize
from stemmer import *

def indexDir(dirname):
  basename = os.path.basename(dirname.rstrip("/"))
  indexFile = open('./indexes/%s_index' % basename, 'w');

  idMap = {}
  indexDict = {}
  docId = 0
  for (root, dirnames, filenames) in os.walk(dirname):
    for filename in filenames:
      if (re.search("\.sw[op]$", filename) == None):
        with open(os.path.join(root, filename), 'r') as fh:
          idMap[docId] = filename

          tokens = tokenize(fh)
          for (pos, token) in tokens:
            token = stem(alias(token))
            try:
              positionMap = indexDict[token]
              try:
                positionMap[docId].append(pos)
              except KeyError:
                positionMap[docId] = [pos]
            except KeyError:
              indexDict[token] = {docId: [pos]}

          docId += 1

  fullIndex = {"id_map" : idMap, "index" : indexDict}
  indexFile.write(json.dumps(fullIndex))
  indexFile.close()

if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument('--data-dir', type=str)
  args = parser.parse_args()

  if (not os.path.isdir(args.data_dir)):
    print("%s is not a valid directory" % (args.data_dir))
    sys.exit()
  else:
    indexDir(args.data_dir)
  
