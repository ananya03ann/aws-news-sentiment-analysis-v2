import requests
from config import URL

def fetch_news():

    response = requests.get(URL)

    if response.status_code != 200:
        print("Failed to fetch news")
        print(response.text)
        return None

    return response.json()