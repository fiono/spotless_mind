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
    with open('indexes/data_index', "r") as indexFile:
      self.index = json.loads(indexFile.read())
      self.indexDict = self.index["index"]
      self.idMap = self.index["id_map"]

  def printResult(self, doc):
    print("\n")
    filename = self.idMap[str(doc)]
    print(filename)

    with open("data/" + filename, 'r') as doc:
      print(doc.read())
      print("========")
      print("\n")

  def search(self, query, isPhrase):
    results = []

    stemmed = [stem(t) for t in query.split(" ")]
    if (isPhrase):
      results = self.phraseSearch(stemmed)
    else:
      results = self.termSearch(stemmed)

    for doc in self.removeNailPolish(results):
      self.printResult(doc)

  def phraseSearch(self, terms):
    postingsLists = []

    for term in terms:
      try:
        sortedPostings = OrderedDict(sorted(self.indexDict[term].items(), key=lambda t:t[0]))
        postingsLists.append(sortedPostings)
      except KeyError:
        pass

    return phraseMerge(postingsLists)

  def termSearch(self, terms):
    docset = []

    for term in terms:
      try:
        termMap = self.indexDict[term]
        docIds = sorted(termMap.keys())
        docset.append(docIds)
      except KeyError:
        pass

    return merge(docset)

  def removeNailPolish(self, results):
    npResults = self.phraseSearch("nail polish".split())
    return difference(results, npResults)


if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument('--query', type=str)
  parser.add_argument('--phrase', action='store_true')
  args = parser.parse_args()

  s = Searcher()
  s.search(args.query, args.phrase)

