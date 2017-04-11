import argparse
from collections import OrderedDict
from collections import Set
import json
import os
import re
import sys

from posting_utils import *
from stemmer import stem

class Searcher:
  def __init__(self):
    with open('indexes/data_index', "r") as index_file:
      self.index = json.loads(index_file.read())
      self.index_dict = self.index["index"]
      self.id_map = self.index["id_map"]

  def printResult(self, doc):
    print("\n")
    filename = self.id_map[str(doc)]
    print(filename)

    with open("data/" + filename, 'r') as doc:
      print(doc.read())
      print("========")
      print("\n")

  def search(self, query, is_phrase):
    results = []

    stemmed = [stem(t) for t in query.split(" ")]
    if (is_phrase):
      results = self.phraseSearch(stemmed)
    else:
      results = self.termSearch(stemmed)

    for doc in self.removeNailPolish(results):
      self.printResult(doc)

  def phraseSearch(self, terms):
    postings_lists = []

    for term in terms:
      try:
        sorted_postings = OrderedDict(sorted(self.index_dict[term].items(), key=lambda t:t[0]))
        postings_lists.append(sorted_postings)
      except KeyError:
        pass

    return phrase_merge(postings_lists)

  def termSearch(self, terms):
    docset = []

    for term in terms:
      try:
        term_map = self.index_dict[term]
        doc_ids = sorted(term_map.keys())
        docset.append(doc_ids)
      except KeyError:
        pass

    return merge(docset)

  def removeNailPolish(self, results):
    nail_polish_results = self.phraseSearch("nail polish".split())
    return difference(results, nail_polish_results)


if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument('--query', type=str)
  parser.add_argument('--phrase', action='store_true')
  args = parser.parse_args()

  s = Searcher()
  s.search(args.query, args.phrase)

