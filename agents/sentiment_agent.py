from services.sentiment import LocalSentiment

class SentimentAgent:
    def __init__(self):
        self.name = "SentimentAgent"
        self.model = LocalSentiment()

    def invoke(self, headlines: list):
        return self.model.score(headlines)
