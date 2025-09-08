from transformers import pipeline
from loguru import logger

class LocalSentiment:
    def __init__(self):
        logger.info('[Sentiment] Loading transformers sentiment pipeline (may download model to cache)')
        # Use a small sentiment model to keep CPU usage reasonable
        self.nlp = pipeline('sentiment-analysis', model='distilbert-base-uncased-finetuned-sst-2-english', device=-1)

    def score(self, texts):
        if not texts:
            return []
        out = self.nlp(texts, truncation=True)
        scored = []
        for t, r in zip(texts, out):
            scored.append({
                'text': t,
                'label': r.get('label'),
                'score': float(r.get('score', 0.0)),
            })
        return scored
