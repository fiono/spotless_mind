import re

blacklist = {
        "acetone"   : 0,
        "topcoat"   : 0,
        "basecoat"  : 0,
        "essie"     : 3,
        "opi"       : 3,
}

def normalize(token):
    return re.sub(r'\W+', '', token).lower()

def tokenize(fh):
    pos = 0
    blackout_counter = 0

    for line in fh:
        tokens = line.split()
        for token in tokens:
            token = normalize(token)

            if (token in blacklist):
                blackout_counter = blacklist[token]
            else:
                if (blackout_counter > 0):
                    blackout_counter = blackout_counter - 1
                else:
                    yield (pos, token)
            pos += 1
