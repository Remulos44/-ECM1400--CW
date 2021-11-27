from flask import Flask, render_template, request
import sched, time
from covid_news_handling import news_API_request

app = flask(__name__)
s = sched.scheduler(time.time, time.sleep)
news = news_API_request()

@app.route('/index')
def initial():
    return render_template(
        'index.html',
        title = 'Daily Update,
        news_articles = news'
        )

if __name__ == "__main__":
    app.run()
