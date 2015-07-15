import json
import collections 

with open('sorted_data.json') as data_file:    
    data = json.load(data_file)

def parser(data):
    """ Sort device data and parse only iob and  time eventss"""
    parsed_data = []
    for key, value in data.items():
        insulin = value[0]
        iob = value[1]
        relevent_data = {
                "insulinOnBoard": iob,
                "insulin": insulin,
                "time": key * 1000
            }
        parsed_data.append(relevent_data)
    return parsed_data

def combine_close_itmes(iob_dict):
    close = 60
    previous_time = 0
    for entry in iob_dict: 
        iob_value = iob_dict[entry]
        if abs(entry - previous_time) < close:
            del iob_dict[entry]
            iob_dict[previous_time] += iob_value
        else:
            previous_time = entry
    return iob_dict  

def create_iob_dict(data, action_time):
    iob_dict = {}
    for entry in data:
        time = entry["time"]
        dose = entry["insulin"]
        remaining_time = action_time * 60 #in minutes
        step = 0 
        decay_rate = 0
        iob_dict = add_iob(iob_dict, time, dose, step, decay_rate)
        while remaining_time > 5: #continue to calculate iob values until complete decay
            if decay_rate < 0.0035:
                decay_rate += 0.00009
            step += 1
            time += 1 * 60 
            iob_dict = add_iob(iob_dict, time, dose, step, decay_rate)
            remaining_time -= 1 
    ordered = collections.OrderedDict(sorted(iob_dict.items(), key=lambda t: t[0]))
    ordered_list = parser(ordered)
    return ordered_list

def add_iob(curr_dict, time, dose, step, decay_rate):
    """ Add a single iob amount to the iob_dict based on linear decay equation"""
    growth_eqn = dose * (1 - pow(2.7, - 0.05 * step))
    decay_eqn = dose * (1 - pow(2.7, decay_rate * step))
    iob_amount = growth_eqn + decay_eqn
    if iob_amount >= 0:
        if time not in curr_dict:
            curr_dict[time] = [dose, iob_amount]
        else: 
            curr_dict[time] += [dose, iob_amount]
    return curr_dict

iob = create_iob_dict(data, 4)

file_object = open('parsed_iob.json', mode='w')
json.dump(iob, fp=file_object, sort_keys=True, indent=4) 
file_object.close()