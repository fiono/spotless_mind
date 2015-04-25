def tokenize(fh):
    pos = 0
    for line in fh:
        tokens = line.split()
        for token in tokens:
            token = token.lower()
            yield(pos, token)
            pos += 1
