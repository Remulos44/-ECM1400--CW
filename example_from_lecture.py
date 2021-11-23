from flask import Flask
from flask import render_template
import sched, time
from flask import request

app = Flask(__name__)
s = sched.scheduler(time.time, time.sleep)
news = [
    {
        "title": "TITLE EXAMPLE",
        "content": "CONTENT EXAMPLE"
    },
    {
        "title": "TITLE 2",
        "content": "content 2"
    }
]

def add_news_article():
    news.append({
        'title': "T",
        'content': "C"
    })

def sched_add_news():
        e1 = s.enter(5,1,add_news_article)

@app.route('/index')
def hello():
    s.run(blocking=False) #blocking=False means it only runs the scheduler if the time has elapsed
    text_field = request.args.get('two') #gets what's written in text field on website
    print(text_field)
    if text_field: #checks if text_field has text, if it does, triggers scheduled event
        sched_add_news()
    return render_template('index.html',
    title = 'Daily update',
    news_articles = news)

if __name__ == "__main__":
    app.run()
