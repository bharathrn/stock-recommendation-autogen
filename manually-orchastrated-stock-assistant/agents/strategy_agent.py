import os
import asyncio
from autogen_core.models import UserMessage
from autogen_ext.models.ollama import OllamaChatCompletionClient

class StrategyAgent:
    def __init__(self):
        self.name = "StrategyAgent"
        self.client = OllamaChatCompletionClient(
            model=os.getenv("OLLAMA_MODEL", "qwen3:1.7b")
        )
        self.system_prompt = (
            "You are a financial strategy assistant. "
            "Given stock market features, news headlines, and sentiment scores, "
            "provide a concise Buy/Hold/Sell recommendation with reasoning."
        )

    def invoke(self, ticker, news_summary, sentiment_summary, market_data):
        prompt = (
            f"{self.system_prompt}\n"
            f"Ticker: {ticker}\n"
            f"News: {news_summary}\n"
            f"Sentiment: {sentiment_summary}\n"
            f"Market Data: {market_data}\n"
            "Provide a clear recommendation and reasoning."
        )
        return asyncio.run(self._call_ollama(prompt))

    async def _call_ollama(self, prompt: str) -> str:
        response = await self.client.create([
            UserMessage(content=prompt, source="user")
        ])
        # FIX: no output_text, use message.content
        if hasattr(response, "message") and response.message:
            return response.message.content
        elif hasattr(response, "messages"):
            return "".join([m.content for m in response.messages if m.content])
        else:
            return str(response)

