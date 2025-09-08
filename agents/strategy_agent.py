import os

USE_OLLAMA = os.getenv("USE_OLLAMA", "False").lower() in ["true", "1", "yes"]

if USE_OLLAMA:
    from langchain_ollama import ChatOllama
    llm = ChatOllama(
        model=os.getenv("OLLAMA_MODEL", "qwen/qwen-1.5b"),
        host=os.getenv("OLLAMA_HOST", "http://localhost:11434")
    )

class StrategyAgent:
    def __init__(self):
        self.name = "StrategyAgent"
        self.system_prompt = (
            "You are a financial strategy assistant. "
            "Given stock data, news, and sentiment, provide a concise "
            "recommendation and reasoning for short-term trading decisions."
        )

        if not USE_OLLAMA:
            from autogen.agentchat import AssistantAgent
            self.agent = AssistantAgent(
                name=self.name,
                system_message=self.system_prompt
            )

    def analyze(self, ticker, news_summary="", sentiment_summary="", market_data=""):
        prompt = (
            f"{self.system_prompt}\n"
            f"Ticker: {ticker}\n"
            f"News: {news_summary}\n"
            f"Sentiment: {sentiment_summary}\n"
            f"Market Data: {market_data}\n"
            "Provide a trading recommendation (Buy/Hold/Sell) with reasoning."
        )

        if USE_OLLAMA:
            return llm.invoke(prompt)
        else:
            return self.agent.invoke(prompt)
