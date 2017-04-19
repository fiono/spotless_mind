def phraseMatch(p1, p2):
  matches = []
  candidates = set(p1.keys()).intersection(p2.keys())

  for doc_id in candidates:
    for pos in p1[doc_id]:
      if (pos + 1) in p2[doc_id]:
        matches.append(doc_id)

  return matches

# returns a phrase match across sorted postings lists
def phraseMerge(postingsSet):
  if len(postingsSet) == 0:
    return []
  if len(postingsSet) < 2:
    return postingsSet[0].keys()

  matches = set()

  for i in range(0, len(postingsSet) - 1):
    m = set(phraseMatch(postingsSet[i], postingsSet[i + 1]))
    if i > 0:
      matches = matches.intersection(m)
    else:
      matches = m

  return matches
