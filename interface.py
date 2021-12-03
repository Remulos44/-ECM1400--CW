from flask import Flask, render_template, request
import sched, time, json
from covid_news_handling import filtered_news
from covid_data_handler import process_covid_json_data

app = Flask(__name__)
s = sched.scheduler(time.time, time.sleep)

with open('removed_articles.json', 'r') as f:
    file = json.load(f)
    removed_articles = file["articles"]

news = filtered_news(removed_articles)

@app.route('/')
@app.route('/index')
def initial():

    #<<< Covid Data >>>#
    cases_last_7_days, current_hospital_cases, total_deaths = process_covid_json_data()

    #<<< News Data >>>#
    article_to_remove_title = str(request.args.get('notif'))
    remove_article(article_to_remove_title)

    #<<< Scheduler >>>#
    

    return render_template(
        'index.html',
        title = 'Daily Covid Update',
        location = 'Exeter',
        nation_location = 'UK',
        news_articles = news,
        image = 'covid19_image.jpg',
        local_7day_infections = cases_last_7_days,
        hospital_cases = current_hospital_cases,
        deaths_total = total_deaths
        )

def remove_article(title):
    print("Title: " + title)
    with open('removed_articles.json', 'r') as f:
        data = json.load(f)
    if title != 'None' and (title not in data['articles']):
        data['articles'].append(title)
        for article in news:
            if article['title'] == title:
                index = news.index(article)
                del news[index]
        with open('removed_articles.json', 'w') as f:
            json.dump(data, f, indent=4)

if __name__ == "__main__":
    app.run()
