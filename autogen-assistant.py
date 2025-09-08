# agents/autogen_stock.py
from autogen import AssistantAgent, UserProxyAgent
from autogen_ext.models.ollama import OllamaChatCompletionClient
import yfinance as yf

########################################
# 1. Define Tool Functions
########################################
def fetch_news(query: str, region: str = "US", n: int = 5):
    from duckduckgo_search import DDGS
    with DDGS() as ddgs:
        results = [r for r in ddgs.news(query, region=region, max_results=n)]
    return results

def fetch_stock_data(ticker: str):
    df = yf.download(ticker, period="6mo")
    return df.tail(5).to_dict()

def analyze_sentiment(text: str):
    if "growth" in text.lower():
        return {"sentiment": "positive"}
    elif "loss" in text.lower():
        return {"sentiment": "negative"}
    else:
        return {"sentiment": "neutral"}

########################################
# 2. Define Agents
########################################
ollama_client = OllamaChatCompletionClient(model="qwen3:1.7b")

# Strategy agent (LLM)
strategy_agent = AssistantAgent(
    name="strategy_agent",
    llm_config={
        "config_list": [
            {
                "model": "qwen3:1.7b",
                "base_url": "http://localhost:11434/v1",  # Ollama OpenAI-compatible endpoint
                "api_key": "NA",  # Ollama ignores this, but required by schema
            }
        ]
    },
    system_message="""You are a stock strategy expert.
    - Ask other agents for data, news, or sentiment when needed.
    - Provide a clear buy/hold/sell recommendation.
    - Justify your reasoning with evidence from news & stock data.
    """
)


# News agent
news_agent = UserProxyAgent(
    name="news_agent",
    code_execution_config={"use_docker": False}  # ✅ disables docker
)

news_agent.register_for_execution(fetch_news)

# Data agent
data_agent = UserProxyAgent(
    name="data_agent",
    code_execution_config={"use_docker": False}
)
data_agent.register_for_execution(fetch_stock_data)

# Sentiment agent
sentiment_agent = UserProxyAgent(
    name="sentiment_agent",
    code_execution_config={"use_docker": False}
    )
sentiment_agent.register_for_execution(analyze_sentiment)

# Orchestrator (acts like the user)
orchestrator = UserProxyAgent(name="orchestrator",
                              code_execution_config={"use_docker": False},
                              human_input_mode="NEVER")

########################################
# 3. Run Orchestration
########################################
if __name__ == "__main__":
    ticker = "INTC"
    query = f"What should I do with {ticker} stock?"

    orchestrator.initiate_chat(
        strategy_agent,
        max_turns = 2,
        message=f"Analyze {ticker} and give me a recommendation. You can ask news_agent, data_agent, and sentiment_agent for help."
    )
