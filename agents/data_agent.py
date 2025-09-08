from autogen import AssistantAgent
from services.market import fetch_history, compute_features

def build_data_agent():
    agent = AssistantAgent(
        name='DataAgent',
        system_message=(
            'You retrieve market data and compute technical indicators. '
            'Use the provided tools and return concise JSON.'
        )
    )

    agent.register_for_execution(fetch_history)
    agent.register_for_execution(compute_features)
    return agent

