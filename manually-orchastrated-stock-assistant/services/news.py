from ddgs import DDGS
from typing import List, Dict
from tenacity import retry, stop_after_attempt, wait_fixed
from loguru import logger

@retry(stop=stop_after_attempt(3), wait=wait_fixed(1))
def fetch_news(query: str, region: str = "IN", max_results: int = 10) -> List[Dict]:
    logger.info(f"[News] fetching news for query={query} region={region} n={max_results}")
    results = []
    if not query:
        return results
    with DDGS() as ddgs:
        for item in ddgs.news(query, max_results=max_results, region=region):
            results.append({
                "title": item.get("title"),
                "snippet": item.get("body"),
                "source": item.get("source"),
                "date": item.get("date"),
                "url": item.get("url"),
            })
    return results
