from services.market import fetch_history, compute_features

class DataAgent:
    def __init__(self):
        self.name = "DataAgent"

    def invoke(self, ticker: str):
        df = fetch_history(ticker)
        features = compute_features(df)
        return features
