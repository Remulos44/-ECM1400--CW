"""
Module for handling covid news articles
"""

import json
import requests
from covid_data_handler import schedule_covid_updates


def news_API_request(search_terms="Covid COVID-19 coronavirus"):
    """
    Function for retrieving news articles from the 'newsapi.org' api
    """
    base_url = "https://newsapi.org/v2/everything?"
    mentioning = search_terms.lower() + "&"

    with open("config.json", "r", encoding="utf-8") as file:
        data = json.load(file)
        api_key = data["api_key"]

    final_url = base_url + "q=" + mentioning + "apikey=" + api_key
    response = requests.get(final_url)
    return response.json()


def filtered_news(removed_articles):
    """
    Function for removing articles from the list
    """
    news = news_API_request()
    for article_title in removed_articles:
        for article in news['articles']:
            if article_title == article['title']:
                index = news['articles'].index(article)
                del news['articles'][index]
    return news['articles']


def update_news():
    """
    Function for updating the news list
    """
    schedule_covid_updates(60**2, news_API_request())


if __name__ == "__main__":
    news_API_request()
