import argparse
import json
import os
import sys

from search import getMatches

class Searcher:
  def __init__(self):
    with open('indexes/data_index', "r") as index_file:
      self.index = json.loads(index_file.read())

  def print_res(self, doc):
    print("\n")
    filename = self.index["id_map"][str(doc)]
    print(filename)

    with open("data/" + filename, 'r') as doc:
      print(doc.read())
      print("========")
      print("\n")

  def search(self, query, is_phrase):
    terms = query.split(" ")
    results = getMatches(terms, is_phrase, self.index)

    for doc in results:
      self.print_res(doc)

if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument('--query', type=str)
  parser.add_argument('--phrase', action='store_true')
  args = parser.parse_args()

  s = Searcher()
  s.search(args.query, args.phrase)

