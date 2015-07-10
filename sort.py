import json

with open('device-data.json') as data_file:    
    data = json.load(data_file)

def parser(data):
    """ Sort device data and parse only wizard iob and wizard time eventss"""
    parsed_data = []
    for entry in data:
        if entry["type"] == 'wizard':
            relevent_data = {
                "insulinOnBoard": entry["insulinOnBoard"],
                "time": entry["time"][:10] + " " + entry["time"][11:19] 
            }
            parsed_data.append(relevent_data)
    return parsed_data

parsed_data = parser(data)

file_object = open('data.json', mode='w')
json.dump(parsed_data, fp=file_object, sort_keys=True, indent=4) 
file_object.close()
