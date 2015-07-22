import json
from datetime import datetime
import random

with open('device-data.json') as data_file:    
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
    dates = {}
    cbg, parsed = [], []
    for entry in data:  
        if entry["type"] == 'cbg':
            relevant_data = {}
            relevant_data["time"] = convert_ISO_to_epoch(entry["time"], '%Y-%m-%dT%H:%M:%S.000Z')
            relevant_data["dose"] = entry["value"]
            
            if entry["time"][:10] not in dates:
                dates[entry["time"][:10]] = [relevant_data]
            else:
                dates[entry["time"][:10]].append(relevant_data)

    for date in dates:
        single_day_data = {}
        single_day_data["date"] = date
        single_day_data["steps"] = random.randint(6500, 12500) 
        single_day_data["cbg"] = dates[date]
        parsed.append(single_day_data)
    return parsed
        
parsed = parser(data)

file_object = open('exercise.json', mode='w')
json.dump(parsed, fp=file_object, sort_keys=True, indent=4) 
file_object.close()

