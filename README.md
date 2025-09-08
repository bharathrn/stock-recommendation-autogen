# Stock Market Assistant (AutoGen, Ollama qwen1.5b, CPU-friendly)

Multi-agent pipeline:
- News via DuckDuckGo (no API key)
- Prices via yfinance
- Sentiment via transformers (CPU)
- Strategy synthesis via local Ollama model (qwen1.5b) via OpenAI-compatible API

## Setup (Windows)

1. Install Python 3.11 (recommended) or 3.12. Avoid 3.13 for ML packages.
2. Create venv and activate (PowerShell):

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1   # or .\.venv\Scripts\activate for cmd
pip install -r requirements.txt
```

3. Copy env and configure Ollama:

```powershell
copy .env.example .env
# Edit .env if needed. For Ollama (local):
# OPENAI_API_BASE=http://localhost:11434/v1
# OPENAI_MODEL=qwen/qwen-1.5b
```

4. Run Ollama locally and serve (example):

```powershell
ollama pull qwen/qwen-1.5b
ollama serve
```

5. Run the app:

```powershell
python main.py --ticker AAPL --query "Apple earnings"
```

## Notes
- If you can't install torch on your Python version, remove or install CPU/nightly builds as needed.
- This tool is for research/education only; not financial advice.
