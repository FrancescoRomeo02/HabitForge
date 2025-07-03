import spacy
from langdetect import detect
import re
from transformers import AutoTokenizer, AutoModelForTokenClassification
from transformers.pipelines import pipeline
from typing import Dict, List

# Carica i modelli una volta sola
try:
    nlp_en = spacy.load("en_core_web_lg")
except OSError:
    nlp_en = spacy.load("en_core_web_sm")

try:
    nlp_it = spacy.load("it_core_news_sm")
except OSError:
    nlp_it = None

# Inizializza i modelli transformer
try:
    # Per inglese - modello BERT fine-tuned
    tokenizer_en = AutoTokenizer.from_pretrained("dbmdz/bert-large-cased-finetuned-conll03-english")
    model_en = AutoModelForTokenClassification.from_pretrained("dbmdz/bert-large-cased-finetuned-conll03-english")
    ner_pipeline_en = pipeline("ner", model=model_en, tokenizer=tokenizer_en, aggregation_strategy="simple")
    # Per italiano - modello BERT fine-tuned
    tokenizer_it = AutoTokenizer.from_pretrained("Davlan/bert-base-multilingual-cased-ner-hrl")
    model_it = AutoModelForTokenClassification.from_pretrained("Davlan/bert-base-multilingual-cased-ner-hrl")
    ner_pipeline_it = pipeline("ner", model=model_it, tokenizer=tokenizer_it, aggregation_strategy="simple")

    print("✅ Modelli transformer caricati con successo")
except Exception as e:
    print(f"⚠️ Errore nel caricamento dei modelli transformer: {e}")
    ner_pipeline_en = None
    ner_pipeline_it = None

def detect_language(text: str) -> spacy.language.Language:
    try:
        lang = detect(text)
        if lang == "it" and nlp_it is not None:
            return nlp_it
        else:
            return nlp_en
    except Exception as e:
        print(f"Language detection error: {e}")
        return nlp_en

class HabitExtractorML:
    def __init__(self):
        self.frequency_patterns = {
            "daily": {"frequency": 7, "period": 7},
            "weekly": {"frequency": 1, "period": 7},
            "monthly": {"frequency": 1, "period": 30},
            "giornalmente": {"frequency": 7, "period": 7},
            "settimanalmente": {"frequency": 1, "period": 7},
            "mensilmente": {"frequency": 1, "period": 30},
        }
    
    def extract_with_transformer(self, text: str, lang_code: str) -> Dict:
        """Usa modelli transformer per estrazione entità"""
        entities = {"PERSON": [], "ORG": [], "LOC": [], "MISC": [], "numbers": [], "temporal": []}
        
        try:
            # Seleziona il pipeline giusto in base alla lingua
            pipeline = ner_pipeline_it if lang_code == "it" else ner_pipeline_en
            
            if pipeline:
                ner_results = pipeline(text)
                
                for entity in ner_results:
                    entity_type = entity["entity_group"]
                    entity_text = entity["word"]
                    
                    if entity_type in entities:
                        entities[entity_type].append({
                            "text": entity_text,
                            "score": entity["score"],
                            "start": entity["start"],
                            "end": entity["end"]
                        })
        except Exception as e:
            print(f"Errore transformer NER: {e}")
        
        return entities
    
    def extract_numbers_and_units(self, doc) -> List[Dict]:
        """Estrae numeri e relative unità usando spaCy + pattern"""
        quantities = []
        
        for token in doc:
            if token.pos_ == "NUM" or token.like_num:
                quantity_info = {
                    "number": token.text,
                    "unit": None,
                    "context": "unknown"
                }
                
                # Cerca unità nelle vicinanze
                for i in range(token.i + 1, min(token.i + 4, len(doc))):
                    next_token = doc[i]
                    if next_token.pos_ in ("NOUN", "PROPN", "SYM"):
                        # Classifica il tipo di unità
                        unit_text = next_token.text.lower()
                        
                        if any(unit in unit_text for unit in ["km", "metri", "m", "litri", "l", "kg", "g"]):
                            quantity_info["context"] = "physical_measure"
                        elif any(unit in unit_text for unit in ["pagine", "page", "minuti", "minute", "ore", "hour"]):
                            quantity_info["context"] = "time_or_quantity"
                        elif any(unit in unit_text for unit in ["euro", "dollar", "$"]):
                            quantity_info["context"] = "money"
                        else:
                            quantity_info["context"] = "general"
                        
                        quantity_info["unit"] = next_token.text
                        break
                
                quantities.append(quantity_info)
        
        return quantities
    
    def extract_frequency_with_ml(self, text: str, doc) -> Dict:
        """Estrae frequenza usando pattern ML + linguistici"""
        frequency_info = {"count": None, "period": None, "confidence": 0.0}
        
        # Pattern regex avanzati per frequenze
        patterns = {
            "times_per_week": r"(\d+)\s*(?:volte?|times?)\s*(?:alla|per|a)\s*settimana|week",
            "times_per_month": r"(\d+)\s*(?:volte?|times?)\s*(?:al|per|a)\s*mese|month",
            "daily_pattern": r"(?:tutti\s*i\s*giorni|every\s*day|al\s*giorno|per\s*day)",
            "weekly_pattern": r"(?:ogni\s*settimana|every\s*week|alla\s*settimana)",
            "monthly_pattern": r"(?:ogni\s*mese|every\s*month|al\s*mese)",
        }
        
        text_lower = text.lower()
        
        for pattern_name, pattern in patterns.items():
            match = re.search(pattern, text_lower)
            if match:
                if "times_per_week" in pattern_name:
                    frequency_info = {"count": int(match.group(1)), "period": 7, "confidence": 0.9}
                elif "times_per_month" in pattern_name:
                    frequency_info = {"count": int(match.group(1)), "period": 30, "confidence": 0.9}
                elif "daily" in pattern_name:
                    frequency_info = {"count": 7, "period": 7, "confidence": 0.8}
                elif "weekly" in pattern_name:
                    frequency_info = {"count": 1, "period": 7, "confidence": 0.8}
                elif "monthly" in pattern_name:
                    frequency_info = {"count": 1, "period": 30, "confidence": 0.8}
                break
        
        # Fallback usando dependency parsing
        if frequency_info["count"] is None:
            for token in doc:
                if token.text.lower() in self.frequency_patterns:
                    pattern_data = self.frequency_patterns[token.text.lower()]
                    frequency_info = {
                        "count": pattern_data["frequency"], 
                        "period": pattern_data["period"], 
                        "confidence": 0.7
                    }
                    break
        
        return frequency_info
    
    def extract_action_with_ml(self, doc, entities: Dict) -> Dict:
        """Estrae l'azione principale usando analisi sintattica avanzata"""
        action_candidates = []
        
        # Metodo 1: Dependency parsing per verbi principali
        for token in doc:
            if token.pos_ == "VERB":
                action_score = 0.0
                
                # Punteggio base per tipo di dipendenza
                if token.dep_ == "ROOT":
                    action_score += 0.4
                elif token.dep_ in ("xcomp", "ccomp"):
                    action_score += 0.3
                elif token.dep_ in ("acl", "relcl"):
                    action_score += 0.2
                
                # Bonus se non è un verbo modale
                modal_verbs = {"volere", "dovere", "potere", "want", "wish", "plan", "hope", "intend"}
                if token.lemma_.lower() not in modal_verbs:
                    action_score += 0.3
                
                # Bonus se ha oggetti diretti
                if any(child.dep_ == "dobj" for child in token.children):
                    action_score += 0.2
                
                action_candidates.append({
                    "verb": token.lemma_,
                    "score": action_score,
                    "token": token
                })
        
        # Ordina per punteggio e restituisce il migliore
        action_candidates.sort(key=lambda x: x["score"], reverse=True)
        
        return action_candidates[0] if action_candidates else {"verb": None, "score": 0.0}

def extract_habits_ml(text: str) -> dict:
    """Funzione principale che usa ML per estrazione abitudini"""
    lang = detect_language(text)
    lang_code = "it" if lang == nlp_it else "en"
    doc = lang(text)
    
    # Inizializza l'estrattore ML
    extractor = HabitExtractorML()
    
    # Estrai entità con transformer
    entities = extractor.extract_with_transformer(text, lang_code)
    
    # Estrai componenti usando ML + NLP
    action_info = extractor.extract_action_with_ml(doc, entities)
    quantities = extractor.extract_numbers_and_units(doc)
    frequency_info = extractor.extract_frequency_with_ml(text, doc)
    
    # Estrai target/oggetto
    target = None
    for token in doc:
        if token.dep_ == "dobj" and token.pos_ in ("NOUN", "PROPN"):
            target = token.text
            break
        elif token.dep_ == "pobj" and token.pos_ in ("NOUN", "PROPN"):
            if token.head.text.lower() in ("in", "a", "al", "alla", "to", "at"):
                target = token.text
                break
    
    # Se non trova target, usa entità riconosciute
    if not target and entities["ORG"]:
        target = entities["ORG"][0]["text"]
    elif not target and entities["LOC"]:
        target = entities["LOC"][0]["text"]
    
    return {
        "text": text,
        "language": lang_code,
        "action": action_info["verb"],
        "action_confidence": action_info["score"],
        "quantities": quantities,
        "main_quantity": quantities[0] if quantities else None,
        "target": target,
        "frequency_count": frequency_info["count"],
        "frequency_period": frequency_info["period"],
        "frequency_confidence": frequency_info["confidence"],
        "frequency_text": f"{frequency_info['count']} su {frequency_info['period']}" if frequency_info["count"] and frequency_info["period"] else None,
        "entities_detected": entities,
        "ml_confidence": (action_info["score"] + frequency_info["confidence"]) / 2
    }
