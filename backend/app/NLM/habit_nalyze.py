import spacy

nlp = spacy.load('en_core_web_lg')


doc = nlp(u"i want to read 10 pages per day. I wnat to do 5km every week")
azione, oggetto, frequenza = "", "", ""
for token in doc:
    if token.pos == "VERB":
        azione = token.pos
    print(token.pos_, token.lemma_, token.dep_)