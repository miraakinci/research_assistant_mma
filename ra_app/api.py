import requests
from django.conf import settings


def fetch_articles_from_google_scholar(query, api_key):
    url = "https://serpapi.com/search"
    params = {
        "engine" : "google_scholar",
        "q": query,
        "api_key": settings.SERP_API_KEY,
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        # hata mesajı
        response.raise_for_status()
