import requests

from modules.config import NEWS_API_KEY

def fetch_news():

    url = (
        f"https://newsapi.org/v2/top-headlines"
        f"?country=us&apiKey={NEWS_API_KEY}"
    )

    response = requests.get(url)

    data = response.json()

    return data.get("articles", [])