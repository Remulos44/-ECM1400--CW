from covid_data_handler import schedule_covid_updates
import requests, json

def news_API_request(search_terms = "Covid COVID-19 coronavirus"):
    base_URL = "https://newsapi.org/v2/everything?"
    mentioning = search_terms.lower() + "&"

    f = open("config.json", "r")
    file = json.load(f)
    api_key = file["api_key"]
    f.close()

    final_URL = base_URL + "q=" + mentioning + "apikey=" + api_key
    response = requests.get(final_URL)
    return response.json()

def filtered_news(removed_articles):
    #Removes articles that have been deleted by the user
    news = news_API_request()
    for article in removed_articles:
        if article in news_API_request['articles']:
            news_API_request['articles'].remove(article)
    return news

def update_news():
    schedule_covid_updates(60**2, news_API_request())

if __name__ == "__main__":
    news_API_request()
