# a helper utility that iterates through two sorted collections and finds elements that
# match a specified predicate
def findMatchesAcrossCollections(c1, c2, findCondition):
    results = []

    iter1 = iter(c1)
    iter2 = iter(c2)

    try:
        el1 = iter1.next()
        el2 = iter2.next()

        while(True):
            if findCondition(el1, el2):
                results.append(el1)
                el1 = iter1.next()
                el2 = iter2.next()

            elif (el1 < el2):
                el1 = iter1.next()

            else:
                el2 = iter2.next()
    except StopIteration:
        pass

    return results

# finds the intersection of two sorted numerical lists
def intersect(docset1, docset2):
    return findMatchesAcrossCollections(docset1, docset2, lambda id1, id2: id1 == id2)

# calculates difference between two sorted numerical lists
def difference(docset1, docset2):
    results = []

    intersection = intersect(docset1, docset2)
    if (len(intersection) == 0):
        return docset1

    iter1 = iter(docset1)
    iter2 = iter(intersection)

    try:
        id1 = iter1.next()
        id2 = iter2.next()

        while(True):
            if (id1 != id2):
                results.append(id1)
                id1 = iter1.next()
            else:
                try:
                    id2 = iter2.next()
                except StopIteration:
                    id2 = None
                id1 = iter1.next()
    except StopIteration:
        pass

    return results

# finds the intersection of an array of sorted numerical sets
def merge(docset):
    if (len(docset) == 0):
        return []
    if (len(docset) == 1):
        return docset[0]

    return intersect(
                docset[0],
                merge(docset[1:])
           )

# finds the positional intersection of two posting lists as ordered dictionaries
# from doc id to list of positions, sorted by doc id
def phrase_match(p1, p2):
    return findMatchesAcrossCollections(p1, p2, lambda id1, id2:
            (id1 == id2) and len(findMatchesAcrossCollections(p1[id1], p2[id2], lambda p1, p2:
                # the position of term 1 must directly precede the position of term 2
                (p1 == (p2 - 1))
            )) > 0
           )

# returns a phrase match across sorted postings lists
def phrase_merge(postings_set):
    if (len(postings_set) == 0):
        return []
    elif (len(postings_set) == 1):
        return postings_set[0].keys()

    return intersect(
                phrase_match(postings_set[0], postings_set[1]),
                phrase_merge(postings_set[1:])
           )
