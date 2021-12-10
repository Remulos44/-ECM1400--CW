"""Render HTML interface."""

import json
import datetime
from flask import Flask, render_template, request
from covid_news_handling import filtered_news
from covid_news_handling import update_news
from covid_news_handling import remove_article
from covid_data_handler import process_covid_json_data
from covid_data_handler import schedule_covid_updates
from covid_data_handler import remove_update_item

# <<< GLOBAL VARIABLES >>> #
app = Flask(__name__)  # Initiates Flask app

# <<< UPDATE ALL DATA ON STARTUP >>> #
filtered_news()
print("TESTING: Startup News Update")
process_covid_json_data()
print("TESTING: Startup Covid Update")


@app.route('/')
@app.route('/index')
def initial():
    """Initiate web interface."""
    print("TESTING: Initiating HTML interface")
    # <<< REMOVING NEWS ARTICLE >>> #
    article_to_remove_title = str(request.args.get('notif'))
    print("TESTING: Removing article title: " + str(article_to_remove_title))
    remove_article(article_to_remove_title)

    # <<< REMOVING UPDATE ITEM >>> #
    update_item_to_remove = str(request.args.get('update_item'))
    print("TESTING: Removing update item title: " + str(update_item_to_remove))
    remove_update_item(update_item_to_remove)

    # <<< SCHEDULING UPDATES >>> #
    update_label = request.args.get('two')
    print("TESTING: update_label: " + str(update_label))
    if update_label:
        print("TESTING: Adding new update item")
        # < calculate update time > #
        update_time = datetime.datetime.strptime(
            request.args.get('update'), "%H:%M")
        print("TESTING: Update scheduled for: " + str(update_time))
        time_now = datetime.datetime.now()
        delta_hours = (update_time.hour - time_now.hour) & 24
        delta_minutes = (update_time.minute - time_now.minute) % 60
        update_time_seconds = (datetime.timedelta(
            hours=delta_hours, minutes=delta_minutes)).seconds
        print("TESTING: Update triggers in "
              + str(update_time_seconds) + " seconds")
        # < --------------------- > #
        update_repeat = request.args.get('repeat', default='None')
        print("TESTING: update_repeat: " + str(update_repeat))
        if update_repeat == "repeat":
            update_repeat = "True"
        else:
            update_repeat = "False"
        print("TESTING: update_repeat: " + str(update_repeat))
        update_covid_data = request.args.get('covid-data', default='None')
        print("TESTING: update_covid_data: " + str(update_covid_data))
        update_news_data = request.args.get('news', default='None')
        print("TESTING: update_news_data: " + str(update_news_data))
        if update_covid_data == "covid-data":
            print("TESTING: scheduling covid data update, name: "
                  + update_label + ", interval: " + str(update_time_seconds)
                  + ", repeat: " + update_repeat)
            schedule_covid_updates(update_name=update_label,
                                   update_interval=update_time_seconds,
                                   repeat=update_repeat)

        if update_news_data == "news":
            print("TESTING: scheduling covid news update, name: "
                  + update_label + ", interval: " + str(update_time_seconds)
                  + ", repeat: " + update_repeat)
            update_news(update_name=update_label,
                        update_interval=update_time_seconds,
                        repeat=update_repeat)

    # <<< READING FROM FILES >>> #
    with open('covid_data.json', 'r', encoding='utf-8') as file:
        print("TESTING: loading covid_data json file")
        covid_data = json.load(file)

    with open('news_data.json', 'r', encoding='utf-8') as file:
        print("TESTING: loading news json file")
        news = json.load(file)

    with open('updates_list.json', 'r', encoding='utf-8') as file:
        print("TESTING: loading updates_list json file")
        updates_list = json.load(file)

    # <<< RENDERING HTML PAGE >>> #
    print("TESTING: rendering template")
    return render_template(
        'index.html',
        title='Daily Covid Update',
        location='Exeter',
        nation_location='UK',
        news_articles=news,
        image='covid19_image.jpg',
        local_7day_infections=covid_data['cases_last_7_days'],
        hospital_cases=covid_data['current_hospital_cases'],
        deaths_total=covid_data['total_deaths'],
        updates=updates_list
        )


if __name__ == "__main__":
    print("TESTING: Loading app")
    app.run()
