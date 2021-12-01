from flask import Flask, render_template, request
import sched, time, json
from covid_news_handling import news_API_request
from covid_data_handler import process_covid_json_data

app = Flask(__name__)
s = sched.scheduler(time.time, time.sleep)
news = news_API_request()

@app.route('/')
@app.route('/home')
@app.route('/index')
def initial():
    cases_last_7_days, current_hospital_cases, total_deaths = process_covid_json_data()
    return render_template(
        'index.html',
        title = 'Daily Covid Update',
        location = 'Exeter',
        nation_location = 'UK',
        news_articles = news['articles'],
        image = 'covid19_image.jpg',
        local_7day_infections = cases_last_7_days,
        hospital_cases = current_hospital_cases,
        deaths_total = total_deaths
        )

if __name__ == "__main__":
    app.run()
