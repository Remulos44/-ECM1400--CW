"""Handle and process covid data."""

import datetime
import sched
import time
import json
from uk_covid19 import Cov19API

s = sched.scheduler(time.time, time.sleep)


def parse_csv_data(csv_filename: str) -> list:
    """Read and return data from 'nation_2021-10-28.csv' file."""
    data = []
    with open(csv_filename, 'r', encoding='utf-8') as file:
        for line in file:
            data.append(line)
    return data


def process_covid_csv_data(covid_csv_data: list):
    """Process and return data returned by 'parse_csv_data'."""
    del covid_csv_data[0]
    cases_last_7_days = 0
    current_hospital_cases = int(covid_csv_data[0].split(",")[5])
    total_deaths = 0
    date_now = datetime.datetime.strptime("2021-10-27", "%Y-%m-%d")
    for line in covid_csv_data:
        split_line = line.split(",")
        if split_line[4] != "":
            if total_deaths < int(split_line[4]):
                total_deaths = int(split_line[4])
        date = datetime.datetime.strptime(split_line[3], "%Y-%m-%d")
        if (date_now - datetime.timedelta(days=7)) <= date < date_now:
            cases_last_7_days += int(split_line[6])
    return cases_last_7_days, current_hospital_cases, total_deaths


def covid_API_request(location="Exeter", location_type="ltla"):
    """Retrieve data from covid19API."""
    print("TESTING: Initiating covid_API_request function")
    location_filter = [
        'areaType=' + location_type,
        'areaName=' + location
        ]
    structure_filter = {
        "area_code": "areaCode",
        "area_name": "areaName",
        "area_type": "areaType",
        "date": "date",
        "cummulative_deaths": "cumDailyNsoDeathsByDeathDate",
        "hospital_cases": "hospitalCases",
        "new_cases": "newCasesBySpecimenDate"
        }
    api = Cov19API(filters=location_filter, structure=structure_filter)
    data = api.get_json()
    return data


def process_covid_json_data():
    """Process the data retrieved from 'covid_API_request'."""
    file_data = {}
    today = datetime.datetime.today()
    print("TESTING: Calling covid_API_request function")
    all_data = covid_API_request()
    data = all_data['data']
    file_data['cases_last_7_days'] = 0
    file_data['current_hospital_cases'] = data[0]["hospital_cases"]
    file_data['total_deaths'] = data[0]["cummulative_deaths"]
    for line in data:
        date = datetime.datetime.strptime(line["date"], "%Y-%m-%d")
        if date >= today - datetime.timedelta(days=7):
            file_data['cases_last_7_days'] += line["new_cases"]

    print("TESTING: Writing to covid_data json file")
    with open('covid_data.json', 'w', encoding='utf-8') as file:
        json.dump(file_data, file, indent=4)


def schedule_covid_updates(update_name, update_interval=10, repeat="False"):
    """Schedual covid data updates."""
    print("TESTING: Initiating schedule_covid_updates module")
    with open('updates_list.json', 'r', encoding='utf-8') as file:
        updates_list = json.load(file)

    time_scheduled = datetime.datetime.now(
        ) + datetime.timedelta(seconds=update_interval)
    print("TESTING: Time scheduled: " + str(time_scheduled))
    time_scheduled_str = datetime.datetime.strftime(time_scheduled, "%H:%M")
    print("TESTING: Time scheduled string: " + time_scheduled_str)
    content = "Covid Data Update, Scheduled for: " + \
        time_scheduled_str + ", Repeat: " + repeat
    print("TESTING: content: " + str(content))

    print("TESTING: appending updates_list")
    updates_list.append(
        {'title': update_name, 'content': content, 'repeat': repeat})

    with open('updates_list.json', 'w', encoding='utf-8') as file:
        json.dump(updates_list, file, indent=4)

    print("TESTING: Scheduling covid update events")
    s.enter(update_interval, 1, process_covid_json_data)
    s.enter(update_interval, 2, remove_update_item, update_name)
    if repeat == "True":
        print("TESTING: repeat=True, scheduling repeat event")
        s.enter(update_interval, 3, repeat_schedule_updates, update_name)
    s.run(blocking=False)


def repeat_schedule_updates(update_name):
    """Schedual repeating data updates."""
    print("TESTING: Initiating repeat_schedule_updates function")
    with open('updates_list.json', 'r', encoding='utf-8') as file:
        updates_list = json.load(file)
    for item in updates_list:
        if item['title'] == update_name and item['repeat'] == "True":
            print("TESTING: Found match in updates_list json file")
            schedule_covid_updates(update_name=update_name,
                                   update_interval=24*60*60, repeat="True")


def remove_update_item(title):
    """Remove item from updates list."""
    print("TESTING: Initiating remove_update_item function")
    with open('updates_list.json', 'r', encoding='utf-8') as file:
        updates_list = json.load(file)
    for item in updates_list:
        if item['title'] == title:
            print("TESTING: Match found")
            index = updates_list.index(item)
            del updates_list[index]
    with open('updates_list.json', 'w', encoding='utf-8') as file:
        json.dump(updates_list, file, indent=4)
