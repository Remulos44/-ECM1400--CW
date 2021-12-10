"""Handle and process covid news data."""

import datetime
import json
import sched
import time
import requests
from covid_data_handler import remove_update_item

s = sched.scheduler(time.time, time.sleep)


def news_API_request(search_terms="Covid COVID-19 coronavirus"):
    """Retrieve news articles from 'newsapi.org'."""
    print("TESTING: Initiating news_API_request function")
    base_url = "https://newsapi.org/v2/everything?"
    mentioning = search_terms.lower() + "&"

    with open("config.json", "r", encoding="utf-8") as file:
        data = json.load(file)
        api_key = data[0]["api_key"]

    final_url = base_url + "q=" + mentioning + "apikey=" + api_key
    response = requests.get(final_url)
    return response.json()


def filtered_news():
    """Remove articles from news dictionary."""
    print("TESTING: Initiating filtered_news function")
    with open('removed_articles.json', 'r', encoding='utf-8') as file:
        removed_article_titles = json.load(file)
        removed_articles = removed_article_titles["articles"]

    news = news_API_request()
    for article_title in removed_articles:
        for article in news['articles']:
            if article_title == article['title']:
                index = news['articles'].index(article)
                del news['articles'][index]

    with open('news_data.json', 'w', encoding='utf-8') as file:
        json.dump(news['articles'], file, indent=4)


def update_news(update_name, update_interval=10, repeat="False"):
    """Schedual covid news updates."""
    print("TESTING: Initiating update_news function")
    with open('updates_list.json', 'r', encoding='utf-8') as file:
        updates_list = json.load(file)

    time_scheduled = datetime.datetime.now(
        ) + datetime.timedelta(seconds=update_interval)
    print("TESTING: Time scheduled: " + str(time_scheduled))
    time_scheduled_str = datetime.datetime.strftime(time_scheduled, "%H:%M")
    print("TESTING: Time scheduled string: " + time_scheduled_str)
    content = "Covid News Update, Scheduled for: " + \
        time_scheduled_str + ", Repeat: " + repeat
    print("TESTING: content: " + str(content))

    print("TESTING: appending updates_list")
    updates_list.append(
        {'title': update_name, 'content': content, 'repeat': repeat})

    with open('updates_list.json', 'w', encoding='utf-8') as file:
        json.dump(updates_list, file, indent=4)

    print("TESTING: Scheduling news update events")
    s.enter(update_interval, 1, filtered_news)
    s.enter(update_interval, 2, remove_update_item, update_name)
    if repeat == "True":
        print("TESTING: repeat=True, scheduling repeat event")
        s.enter(update_interval, 3, repeat_news_update, update_name)
    s.run(blocking=False)


def repeat_news_update(update_name):
    """Schedual repeating data updates."""
    print("TESTING: Initiating repeat_news_update function")
    with open('updates_list.json', 'r', encoding='utf-8') as file:
        updates_list = json.load(file)
    for item in updates_list:
        if item['title'] == update_name and item['repeat'] == "True":
            print("TESTING: Found match in updates_list json file")
            update_news(update_name=update_name,
                        update_interval=24*60*60, repeat="True")


def remove_article(title):
    """Remove article from news list."""
    print("TESTING: Initiating remove_article function")
    with open('removed_articles.json', 'r', encoding='utf-8') as file:
        removed_articles = json.load(file)
    with open('news_data.json', 'r', encoding='utf-8') as file:
        news = json.load(file)
    if title != 'None' and (title not in removed_articles['articles']):
        removed_articles['articles'].append(title)
        for article in news:
            if article['title'] == title:
                print("TESTING: Match found")
                index = news.index(article)
                del news[index]
        with open('removed_articles.json', 'w', encoding='utf-8') as file:
            json.dump(removed_articles, file, indent=4)
        with open('news_data.json', 'w', encoding='utf-8') as file:
            json.dump(news, file, indent=4)
