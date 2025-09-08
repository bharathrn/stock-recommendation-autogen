import os
from dotenv import load_dotenv
from pydantic import BaseModel
from loguru import logger

load_dotenv()

class AppConfig(BaseModel):
    openai_api_key: str | None = os.getenv("OPENAI_API_KEY") or None
    openai_api_base: str | None = os.getenv("OPENAI_API_BASE") or None
    openai_model: str | None = os.getenv("OPENAI_MODEL") or None

    default_region: str = os.getenv("DEFAULT_REGION", "IN")
    news_items: int = int(os.getenv("NEWS_ITEMS", "10"))
    max_lookback_days: int = int(os.getenv("MAX_LOOKBACK_DAYS", "180"))
    log_level: str = os.getenv("LOG_LEVEL", "INFO")

    @property
    def llm_enabled(self) -> bool:
        ok = bool(self.openai_api_base and self.openai_model)
        if not ok:
            logger.warning("LLM not configured. Falling back to rules-based Strategy.")
        return ok

config = AppConfig()
logger.remove()
logger.add(lambda msg: print(msg, end=''), level=config.log_level)
