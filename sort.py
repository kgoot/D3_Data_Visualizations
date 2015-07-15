import json
from datetime import datetime

with open('bolus_wizard_data.json') as data_file:    
    data = json.load(data_file)


def convert_ISO_to_epoch(datetime_string, date_format):
    """ Takes a datetime string and returns an epoch time in seconds
        Only works when datetime_string is in UTC 
    """
    datetime_object = datetime.strptime(datetime_string, date_format)
    epoch = datetime.utcfromtimestamp(0)
    delta = datetime_object - epoch
    return int(delta.total_seconds())

def parser(data):
    """ Sort device data and parse only wizard iob and wizard time eventss"""
    parsed_data = []
    for entry in data:
        if entry["type"] == 'bolus':
            relevent_data = {}
            relevent_data["time"] = convert_ISO_to_epoch(entry["time"], '%Y-%m-%dT%H:%M:%S.000Z')
            if entry["subType"] == 'normal':
                relevent_data["insulin"] = entry["normal"]              
            elif entry["subType"] == 'dual/square':
                relevent_data["insulin"] = entry["normal"] + entry["extended"]
            else:
                relevent_data["insulin"] = entry["extended"]
            parsed_data.append(relevent_data)
    ordered = sorted(parsed_data, key=lambda t: t["time"])
    return ordered

parsed_data = parser(data)

file_object = open('sorted_data.json', mode='w')
json.dump(parsed_data, fp=file_object, sort_keys=True, indent=4) 
file_object.close()
