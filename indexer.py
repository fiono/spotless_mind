import argparse
import json
import os
import re
import sys

from tokenizer import tokenize
from stemmer import *

def index_dir(dirname):
  basename = os.path.basename(dirname.rstrip("/"))
  index_file = open('./indexes/%s_index' % basename, 'w');

  id_map = {}
  index_dict = {}
  doc_id = 0
  for (root, dirnames, filenames) in os.walk(dirname):
    for filename in filenames:
      if (re.search("\.sw[op]$", filename) == None):
        with open(os.path.join(root, filename), 'r') as fh:
          id_map[doc_id] = filename

          tokens = tokenize(fh)
          for (pos, token) in tokens:
            token = stem(alias(token))
            try:
              position_map = index_dict[token]
              try:
                position_map[doc_id].append(pos)
              except KeyError:
                position_map[doc_id] = [pos]
            except KeyError:
              index_dict[token] = {doc_id: [pos]}

          doc_id = doc_id + 1

  full_index = {"id_map" : id_map, "index" : index_dict}
  index_file.write(json.dumps(full_index))
  index_file.close()

if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument('--data-dir', type=str)
  args = parser.parse_args()

  if (not os.path.isdir(args.data_dir)):
    print("%s is not a valid directory" % (args.data_dir))
    sys.exit()
  else:
    index_dir(args.data_dir)
  
