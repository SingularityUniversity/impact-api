import json
from requests import get
from os.path import expanduser


def download_json_data():
    url = "http://127.0.0.1:8000/json_data"
    filename = expanduser("~/src/singularity-impact-dashboard/assets/json/data.json")

    json_data = get(url).json()

    print('==============')
    print('No of people:', json_data['community']['no_of_people'])
    print('No of locations:', json_data['community']['no_of_locations'])
    print('No of events:', json_data['community']['no_of_engagements'])
    print('Total educated:', json_data['education']['total_educated'])
    print('No of initiatives:', json_data['initiatives']['no_of_initiatives'])
    print('No of categories:', json_data['initiatives']['no_of_categories'])
    print('==============')

    file = open(filename, "w")
    file.write(json.dumps(json_data))
    file.close()

download_json_data()



