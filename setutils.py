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
    merge_set = []
    if (len(docset) > 0):
        if (len(docset) == 1):
            merge_set = docset[0]
        else:
            for (idx, term_docs) in enumerate(docset):
                if (idx == 0):
                    merge_set = intersect(docset[idx], docset[idx + 1])
                else:
                    if ((idx + 1) < len(docset)):
                        merge_set = intersect(merge_set, docset[idx + 1])
    return merge_set
