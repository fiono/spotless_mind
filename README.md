A local search engine in python for those of us who wouldn't like to hear about nail polish.

Three mods:

- Tokenizer drops nail polish-specific tokens and attempts to drop full nail polish names when prepended by a
  brand name

- Stemmer aliases nail polish-relevant terms to a rhyming alias to encourage conscious searching

- Searcher drops any document containing the phrase "nail polish"
