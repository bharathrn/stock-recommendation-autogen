from autogen import AssistantAgent
from services.sentiment import LocalSentiment

_sent = None
def _lazy_sent():
    global _sent
    if _sent is None:
        _sent = LocalSentiment()
    return _sent

def sentiment_tool(texts: list):
    return _lazy_sent().score(texts)

def build_sentiment_agent():
    agent = AssistantAgent(
        name='SentimentAgent',
        system_message=(
            'You run local sentiment analysis on headlines. '
            'Use the sentiment_tool and return a list of {text, label, score}.'
        )
    )

    agent.register_for_execution(sentiment_tool)
    return agent
