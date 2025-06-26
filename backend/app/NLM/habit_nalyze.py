import spacy
from langdetect import detect

# Carica i modelli una volta sola
nlp_en = spacy.load("en_core_web_lg")
nlp_it = spacy.load("it_core_news_sm")

texts = [
    "I plan to meditate every morning for 10 minutes.",
    "I wish to learn a new language this year.",
    "I plan to cook a new recipe once a month.",
    "I wish to save $1000 every month.",
    "I hope to volunteer at the shelter once a week.",
    "Voglio leggere 10 pagine al giorno.",
    "Desidero fare esercizio fisico tre volte alla settimana.",
    "Vorrei imparare a suonare uno strumento musicale quest'anno.",
    "Intendo bere 2 litri d'acqua ogni giorno.",
    "Desidero risparmiare 500 euro ogni mese.",
]

def detect_language(text: str) -> spacy.language.Language:
    try:
        lang = detect(text)
        return nlp_it if lang == "it" else nlp_en
    except Exception as e:
        print(f"Language detection error: {e}")
        return nlp_en

def extract_habits(text: str) -> dict:
    habit_verb = None
    quantity = None
    obj = None
    repetition = None

    lang = detect_language(text)
    doc = lang(text)

    for token in doc:
        if token.dep_ in ("xcomp", "ccomp") and token.pos_ == "VERB":
            habit_verb = token.lemma_

            for tok in token.subtree:
                if tok.pos_ == "NUM":
                    for right in tok.rights:
                        if right.pos_ == "NOUN":
                            quantity = f"{tok.text} {right.text}"
                            break
                    if not quantity and tok.head.pos_ == "NOUN":
                        quantity = f"{tok.text} {tok.head.text}"

            for tok in token.subtree:
                if tok.dep_ == "pobj" and tok.head.text.lower() in ("of", "di"):
                    obj = tok.text
                elif tok.dep_ == "dobj" and tok.pos_ == "NOUN":
                    obj = tok.text

            for tok in doc:
                if tok.text.lower() in ("daily", "nightly", "weekly", "monthly",  "mensilmente", "giornalmente", "settimanalmente"):
                    repetition = tok.text

                elif tok.text.lower() in ("every", "each", "once", "per", "ogni", "una"):
                    next_tok = doc[tok.i + 1] if tok.i + 1 < len(doc) else None
                    if next_tok and next_tok.pos_ in ("NOUN", "PROPN"):
                        repetition = f"{tok.text} {next_tok.text}"
                elif tok.ent_type_ in ("DATE", "TIME") and tok.dep_ != "npadvmod":
                    repetition = tok.text

            break

    return {
        "text": text,
        "language": "it" if lang == nlp_it else "en",
        "verb": habit_verb,
        "quantity": quantity,
        "object": obj,
        "repetition": repetition
    }

if __name__ == "__main__":
    for text in texts:
        habits = extract_habits(text)
        print(f"Text: {habits['text']}")
        print(f"Language: {habits['language']}")
        print(f"Verb: {habits['verb']}")
        print(f"Quantity: {habits['quantity']}")
        print(f"Object: {habits['object']}")
        print(f"Repetition: {habits['repetition']}")
        print("-" * 40)
    print("Processing complete.")
