"""
This is a test module
"""

from uk_covid19 import Cov19API

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
    print(str(type(data)))
    return data

if __name__ == "__main__":
    covid_API_request()
