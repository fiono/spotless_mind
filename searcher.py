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

    for doc in self.removeNailPolish(results):
      self.printResult(doc)

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

  def phraseSearch(self, terms):
    try:
      postingsLists = [self.indexDict[t] for t in terms]
    except KeyError:
      return []

    if len(postingsLists) == 1:
      return postingsLists[0].keys()

    matches = set()
    for i in range(0, len(postingsLists) - 1):
      m = set(phraseMatch(postingsLists[i], postingsLists[i + 1]))
      if i > 0:
        matches = matches.intersection(m)
      else:
        matches = m

    return matches

  def phraseMatch(p1, p2):
    matches = []
    candidates = set(p1.keys()).intersection(p2.keys())

    for doc_id in candidates:
      for pos in p1[doc_id]:
        if (pos + 1) in p2[doc_id]:
          matches.append(doc_id)

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

