import datetime, json
from uk_covid19 import Cov19API

def parse_csv_data(csv_filename: str) -> list:
    data = []
    f = open(csv_filename)
    for line in f:
        data.append(line)
    f.close()
    return data

def process_covid_csv_data(covid_csv_data: list):
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
        if date >= (date_now - datetime.timedelta(days=7)) and date < date_now:
            cases_last_7_days += int(split_line[6])
    return cases_last_7_days, current_hospital_cases, total_deaths

def covid_API_request(location = "Exeter", location_type = "ltla"):
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
    data = api.get_json(save_as="./data.json")
    return data

def process_covid_json_data(file_name):
    today = datetime.datetime.today()
    f = open("data.json", "r")
    file = json.load(f)
    data = file["data"]
    cases_last_7_days = 0
    current_hospital_cases = data[0]["hospital_cases"]
    total_deaths = data[0]["cummulative_deaths"]
    for line in data:
        date = datetime.datetime.strptime(line["date"], "%Y-%m-%d")
        if date >= today - datetime.timedelta(days=7):
            cases_last_7_days += line["new_cases"]
    f.close()
    return cases_last_7_days, current_hospital_cases, total_deaths

print(process_covid_json_data("data.json"))