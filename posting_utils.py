# finds the intersection of two sorted numerical sets
def intersect(s1, s2):
    merged = []
    idx1 = idx2 = 0
    while (idx1 < len(s1) and idx2 < len(s2)):
        if (s1[idx1] == s2[idx2]):
            merged.append(s1[idx1])
            idx1 += 1
            idx2 += 1
        elif (s1[idx1] < s2[idx2]):
            idx1 += 1
        else:
            idx2 += 1
    return merged

# finds the intersection of an array of sorted numerical sets
def merge(docset):
    if (len(docset) == 0):
        return []
    if (len(docset) == 1):
        return docset[0]

    return intersect(docset[0], merge(docset[1:]))

# finds the positional intersection of two posting lists as ordered dictionaries
# from doc id to list of positions, sorted by doc id
def phrase_match(p1, p2):
    docset = []

    iter1 = iter(p1)
    iter2 = iter(p2)

    try:
        doc_id1 = iter1.next()
        doc_id2 = iter2.next()

        # break on StopIteration
        while(True):

            # iterate until we're comparing positional data for the same document
            if (doc_id1 == doc_id2):

                positions1 = p1[doc_id1]
                positions2 = p2[doc_id2]

                idx1 = idx2 = 0
                while (idx1 < len(positions1) and idx2 < len(positions2)):

                    # this distance indicates a phrase
                    if (positions1[idx1] == (positions2[idx2] - 1)):
                        # doesn't matter which
                        docset.append(doc_id1)
                        break
                    elif (positions1[idx1] < positions2[idx2]):
                        idx1 += 1
                    else:
                        idx2 += 1

                doc_id1 = iter1.next()
                doc_id2 = iter2.next()

            elif (doc_id1 < doc_id2):
                doc_id1 = iter1.next()
            else:
                doc_id2 = iter2.next()

    except StopIteration:
        pass

    return docset

def phrase_merge(postings_set):
    if (len(postings_set) == 0):
        return []
    elif (len(postings_set) == 1):
        return postings_set[0]
    elif (len(postings_set) == 2):
        return phrase_match(postings_set[0], postings_set[1])

    return intersect(phrase_match(postings_set[0], postings_set[1]), phrase_merge(postings_set[2:]))

