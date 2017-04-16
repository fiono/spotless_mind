import re

blacklist = {
    "acetone"   : 0,
    "topcoat"   : 0,
    "basecoat"  : 0,
    "essie"   : 3,
    "opi"     : 3,
}

def normalize(token):
  return re.sub(r'\W+', '', token).lower()

def tokenize(fh):
  pos = 0
  blackoutCounter = 0

  for line in fh:
    for token in line.split():
      token = normalize(token)

      if (token in blacklist):
        blackoutCounter = blacklist[token]
      elif (blackoutCounter > 0):
        blackoutCounter -= 1
      else:
        yield (pos, token)
      pos += 1
