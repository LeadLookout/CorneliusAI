# FILE: cornelius_os/app/modules/nlp_engine.py
import spacy

class NLPEngine:
    def __init__(self, model_name='en_core_web_sm'):
        self.nlp = spacy.load(model_name)

    def process(self, text):
        """Processes text and returns NLP information."""
        doc = self.nlp(text)

        # Extract entities
        entities = []
        for ent in doc.ents:
            entities.append({"text": ent.text, "label": ent.label_})

        # Basic intent classification (very simple for the MVP)
        intent = "unknown"
        if "create" in text.lower() or "add" in text.lower():
            intent = "create_widget"  # Example intent
        elif "save" in text.lower():
            intent = "save_file"

        return {
            "intent": intent,
            "entities": entities,
            # You can add other information from the spaCy Doc object here
            # For example:  dependencies, tokens, etc.
        }

    # Add other NLP methods as needed (e.g., question answering, summarization)