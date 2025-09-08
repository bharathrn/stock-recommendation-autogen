from agents.news_agent import NewsAgent
from agents.data_agent import DataAgent
from agents.sentiment_agent import SentimentAgent
from agents.strategy_agent import StrategyAgent

class StockOrchestrator:
    def __init__(self):
        self.news_agent = NewsAgent()
        self.data_agent = DataAgent()
        self.sentiment_agent = SentimentAgent()
        self.strategy_agent = StrategyAgent()

    def run(self, ticker: str, query: str = None):
        # 1️⃣ Fetch news
        news = self.news_agent.invoke(query or ticker)
        headlines = [n["title"] for n in news]

        # 2️⃣ Sentiment
        sentiment = self.sentiment_agent.invoke(headlines)

        # 3️⃣ Market data
        market_data = self.data_agent.invoke(ticker)

        # 4️⃣ Strategy decision
        recommendation = self.strategy_agent.invoke(
            ticker=ticker,
            news_summary=headlines,
            sentiment_summary=sentiment,
            market_data=market_data
        )
        return recommendation
