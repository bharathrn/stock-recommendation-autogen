from autogen import GroupChat, GroupChatManager
from autogen.agentchat import UserProxyAgent
from .news_agent import build_news_agent
from .data_agent import build_data_agent
from .sentiment_agent import build_sentiment_agent
from .strategy_agent import StrategyAgent

def build_strategy_agent():
    return StrategyAgent()

def build_orchestrator():
    user = UserProxyAgent(
        name="Requester",
        human_input_mode="NEVER",
        code_execution_config={"use_docker": False}
    )
    news = build_news_agent()
    data = build_data_agent()
    sentiment = build_sentiment_agent()
    strategy = build_strategy_agent()

    agents = [user, news, data, sentiment, strategy]

    # ✅ explicitly pass empty transitions
    gc = GroupChat(
        agents=agents,
        messages=[],
        max_round=12,
        allowed_or_disallowed_speaker_transitions=None  # Explicitly set to None
    )

    manager = GroupChatManager(
        groupchat=gc,
        llm_config={"model": "ollama/qwen:1.5b"}
    )

    return manager, user, news, data, sentiment, strategy


def run_pipeline(ticker: str, company_query: str):
    manager, user, news, data, sentiment, strategy = build_orchestrator()
    query = f"Give me stock market analysis for {ticker} ({company_query})"
    result = user.initiate_chat(manager, message=query)
    return result
