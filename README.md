
# Stock Market Assistant: Manual, Simple AutoAgent, and AutoGen Approaches

This project demonstrates three approaches to building a stock market assistant using multi-agent orchestration and LLMs:

1. **Manual Orchestration** (`manually-orchastrated-stock-assistant/`)
2. **Simple AutoAgent** (`simple-autoagent.py`)
3. **AutoGen Stock Assistant** (`autogen-stock-assistant.py`)

---

## 1. Manual Orchestration

The `manually-orchastrated-stock-assistant/` folder contains a classic, explicit pipeline where each agent is called in sequence by a central orchestrator. The flow is as follows:

1. **NewsAgent** fetches news headlines for a given stock ticker or query.
2. **SentimentAgent** analyzes the sentiment of the news headlines.
3. **DataAgent** retrieves recent market data for the ticker.
4. **StrategyAgent** synthesizes a recommendation (buy/hold/sell) using the news, sentiment, and data.

The orchestrator (`main.py` and `agents/orchestrator.py`) manages this step-by-step process, passing outputs from one agent to the next. This approach is transparent and easy to debug, but requires manual wiring and is less flexible for complex workflows.

---

## 2. Simple AutoAgent

The `simple-autoagent.py` script demonstrates a minimal multi-agent setup using the AutoGen framework. Here, agents (e.g., math and chemistry experts) are defined with their own system prompts and can be composed as tools for a general assistant agent. The assistant can delegate tasks to the expert agents as needed, showing how AutoGen enables modular, tool-based agent collaboration with minimal code.

This script is a template for building more complex agent systems, but does not implement the full stock assistant pipeline.

---

## 3. AutoGen Stock Assistant

The `autogen-stock-assistant.py` script implements the stock assistant pipeline using the AutoGen framework and Ollama for local LLM inference. The flow is:

1. **Tool Functions**: News, stock data, and sentiment analysis are defined as callable Python functions.
2. **Agents**: Each agent (news, data, sentiment, strategy) is defined as an AutoGen agent, with the strategy agent using an LLM (e.g., Qwen3 via Ollama) to synthesize recommendations.
3. **Orchestration**: A group chat manager coordinates the agents, allowing the strategy agent to autonomously request information from the others as needed.

This approach is highly flexible and efficient:
- Agents can communicate and collaborate dynamically, without hardcoded pipelines.
- The LLM-powered strategy agent can decide which information to request, making the system more adaptive.
- Adding or modifying agents/tools is easy, supporting rapid experimentation.

---

## Why AutoGen Stock Assistant is More Efficient

- **Less Manual Wiring**: The orchestration logic is handled by the AutoGen framework, reducing boilerplate and making the codebase easier to extend.
- **Dynamic Collaboration**: Agents can interact in a group chat, enabling more natural and context-aware decision making.
- **LLM-Driven Reasoning**: The strategy agent leverages a local LLM (via Ollama) for advanced reasoning, using evidence from news, sentiment, and data.
- **Easier to Scale**: New agents or tools can be added with minimal changes to the orchestration logic.

---

## Setup (Windows)

1. Install Python 3.11 (recommended) or 3.12. Avoid 3.13 for ML packages.
2. Create and activate a virtual environment:

	```powershell
	py -3.11 -m venv .venv
	.\.venv\Scripts\Activate.ps1
	pip install -r requirements.txt
	```

3. Configure Ollama and environment variables:

	```powershell
	copy .env.example .env
	# Edit .env if needed. For Ollama (local):
	# OPENAI_API_BASE=http://localhost:11434/v1
	# OPENAI_MODEL=qwen/qwen-1.5b
	```
	# OPENAI_MODEL=qwen3:1.7b
	```

4. Run Ollama locally:

	```powershell
	ollama pull qwen3:1.7b
	ollama serve
	```

5. Run the desired assistant:

	- **Manual Orchestration:**
	  ```powershell
	  python manually-orchastrated-stock-assistant/main.py --ticker AAPL --query "Apple earnings"
	  ```
	- **AutoGen Stock Assistant:**
	  ```powershell
	  python autogen-stock-assistant.py
	  ```

---

## Notes
- If you can't install torch on your Python version, try CPU/nightly builds or adjust requirements as needed.
- This project is for research/education only; not financial advice.
