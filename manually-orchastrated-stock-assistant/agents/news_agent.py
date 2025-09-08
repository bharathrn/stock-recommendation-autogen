from services.news import fetch_news

class NewsAgent:
    def __init__(self):
        self.name = "NewsAgent"

    def invoke(self, query: str, region: str = "IN", max_results: int = 10):
        news = fetch_news(query, region=region, max_results=max_results)
        return news
