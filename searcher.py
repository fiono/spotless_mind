import argparse
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

    #for doc in self.removeNailPolish(results):
    for doc in results:
      self.printResult(doc)

  def termSearch(self, terms):
    try:
      postingsLists = [set(self.indexDict[t].keys()) for t in terms]
    except KeyError:
      return []

    return set.intersection(*postingsLists)

  def phraseSearch(self, terms):
    if len(terms) == 1:
      return self.termSearch(terms[0])

    try:
      candidates = set.intersection(*[set(self.indexDict[t].keys()) for t in terms])
    except KeyError:
      return []

    matches = []
    for docId in candidates:
      positions = [self.indexDict[t][docId] for t in terms]

      for init in positions[0]:
        checks = []
        for i in range(0, len(positions)):
          checks.append((init + i) in positions[i])
        if all(checks):
          matches.append(docId)
          break

    return matches

  def removeNailPolish(self, results):
    npResults = self.phraseSearch("nail polish".split())
    return set(results) - set(npResults)


if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument('--query', type=str)
  parser.add_argument('--phrase', action='store_true')
  args = parser.parse_args()

  s = Searcher()
  s.search(args.query, args.phrase)

