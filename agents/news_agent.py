from autogen import AssistantAgent
from services.news import fetch_news

def build_news_agent():
    agent =  AssistantAgent(
        name='NewsAgent',
        system_message=(
            'You fetch latest financial and company-related news. '
            'Only return concise JSON with keys: title, source, date, url, snippet.'
        )
    )
    agent.register_for_execution(fetch_news)
    return agent
