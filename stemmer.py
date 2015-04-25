# insane "snowball" stemmer based on documentation here: http://snowball.tartarus.org/algorithms/english/stemmer.html
# "the least fun i've ever had at a computer"

import re

vowels = "[aeiouy]"
nonvowels = "[^aeiouy]"
doubles = "(bb|dd|ff|gg|mm|nn|pp|rr|tt)"
li_ending = "[cdeghkmnrt]"

suffix_mappings_1 = {
        "tional": "tion",
        "enci": "ence",
        "anci": "ance",
        "abli": "able",
        "entli": "ent",
        "izer": "ize",
        "ization": "ize",
        "ational": "ate",
        "ation": "ate",
        "ator": "ate",
        "alism": "al",
        "aliti": "al",
        "alli": "al",
        "fulness": "ful",
        "ousli": "ous",
        "ousness": "ous",
        "iveness": "ive",
        "iviti": "ive",
        "biliti": "ble",
        "bli": "ble",
        "logi": "og",
        "fulli": "ful",
        "lessli": "less",
}

suffix_mappings_2 = {
        "tional": "tion",
        "ational": "ate",
        "alize": "al",
        "icate": "ic",
        "iciti": "ic",
        "ical": "ic",
        "ful": "",
        "ness": "",
}

# defines a "short" syllable
def isShort(token):
    if (re.search("({1}{0}[^aeiouywxY]|^{0}{1})$".format(vowels,nonvowels),token)):
        return True
    return False

# finds the longest suffix given a word and a list of candidates
def longestSuffix(token, suffixes):
    suffix_regex = "({0})$".format("|".join(suffixes));
    suffix_match = re.search(suffix_regex, token)
    if (suffix_match):
        return suffix_match.group(0)
    return ""

# marks ys which appear to serve as consonants
def yMark(token):
    return re.sub("^(y)|(y)(?={0})".format(vowels),"Y",token)

# removes suffixes
def desuffix(token, r1, r2, is_short):
    # step 0
    # remove the longest of ', 's, 's'
    token = re.sub(r'(\'|\'s|\'s\')$',"",token)

    # step 1a
    # find longest of sses, ied, ies, s, us, ss
    longest_suffix = longestSuffix(token, ["sses", "ied", "ies", "s", "us", "ss"])
    if (longest_suffix != ""):
        if (longest_suffix == "sses"):
            # sses -> ss
            token = re.sub(r'sses$',"",token)
        elif (longest_suffix == "ied" or longest_suffix == "ies"):
            # replace by i if preceded by more than one letter, otherwise by ie
            if (re.search(r'..ie[ds]$',token)):
                token = re.sub(r'ie[ds]$',"i", token)
            else:
                token = re.sub(r'ie[ds]$',"ie", token)
        elif (longest_suffix == "s"):
            # delete if the preceding word part contains a vowel not immediately before the s
            if (re.search("{0}.+s$".format(vowels),token)):
                token = re.sub(r's$',"",token)

    # step 1b
    # find longest of eed, eedly, ed, edly, ing, ingly
    longest_suffix = longestSuffix(token, ["eed", "eedly", "ed", "edly", "ing", "ingly"])
    if (longest_suffix != ""):
        if (longest_suffix == "eed" or longest_suffix == "eedly"):
            # replace by ee if suffix in R1
            if (re.search("{0}$".format(longest_suffix),token[r1:])):
                token = re.sub("{0}$".format(longest_suffix),"ee",token)
        else:
            # delete if the preceding word part contains a vowel
            if (re.search("{0}.*{1}$".format(vowels, longest_suffix), token)):
                token = re.sub("{0}$".format(longest_suffix),"",token)

                # if the word ends at, bl or iz, or if the word is short, add e
                if (re.search(r'(at|bl|iz)$',token) or is_short):
                    token += "e"

                # if the word ends with a double remove the last letter
                elif (re.search("{0}$".format(doubles),token)):
                    token = token[:-1]

    # step 1c
    # replace suffix y or Y by i if preceded by a non-vowel which is not the first letter of the word
    if (re.search(".+{0}[yY]".format(nonvowels),token)):
        token = re.sub("[yY]$","i",token)

    # step 2
    # find and sub the longest of the first set of suffixes in r1
    longest_suffix = longestSuffix(token[r1:], suffix_mappings_1.keys())

    if (longest_suffix != ""):
        token = re.sub("{0}$".format(longest_suffix),suffix_mappings_1[longest_suffix],token)
    elif (re.search("{0}li$".format(li_ending),token)):
        # delete li if preceded by a valid li-ending
        token = re.sub(r'li$',"",token)

    # step 3
    # find and sub the longest of the second set of suffixes in r1
    longest_suffix = longestSuffix(token[r1:], suffix_mappings_2.keys())

    if (longest_suffix != ""):
        token = re.sub("{0}$".format(longest_suffix),suffix_mappings_2[longest_suffix],token)
    elif (re.search(r'ative$',token[r2:])):
        token = re.sub(r'ative$',"",token)

    # step 4
    # find and delete the longest of the third set of suffixes in r2
    longest_suffix = longestSuffix(token[r2:], ["al","ance","ence","er","ic","able","ible","ant",
                                        "ement","ment","ent","ism","ate","iti","ous","ive","ize"])

    if (longest_suffix != ""):
        token = re.sub("{0}$".format(longest_suffix),"",token)
    elif (re.search(r'[st]ion$',token[r2:])):
        token = re.sub(r'ion$',"",token)

    # step 5
    # maybe delete a trailing "l" or "e"
    if (re.search(r'e$',token[r2:])):
        token = re.sub(r'e$',"",token)
    elif (re.search(r'e$',token[r1:])):
        prefix = re.search(r'(?P<region>)e$',token[r1:])
        if (prefix and prefix.group("region") and not isShort(prefix.group("region"))):
            token = re.sub(r'e$',"",token)
    elif (re.search(r'll$',token[r2:])):
        token = re.sub(r'l$',"",token)

    return token


def stem(token):
    token = token.lower()

    if (len(token) <= 2):
        return token

    # strip leading quotes
    token = token.lstrip("'\"")

    token = yMark(token)

    # define R1 and R2
    r1 = r2 = len(token)

    # R1 is the the region after the first non-vowel following a vowel
    r1_match = re.search("{0}{1}(?P<region>.*$)".format(vowels,nonvowels),token)
    if (r1_match and r1_match.group("region")):
        r1 = token.rfind(r1_match.group("region"))

        # R2 is the region after the first non-vowel following a vowel in R1
        r2_match = re.search("{0}{1}(?P<region>.*$)".format(vowels,nonvowels),token[r1:])
        if (r2_match and r2_match.group("region")):
            r2 = token.rfind(r2_match.group("region"))

    is_short = (isShort(token) and token[r1:] == len(token))

    token = desuffix(token, r1, r2, is_short)

    # turn any remaining Y letters in the word back into lower case
    token = token.lower()

    return token
