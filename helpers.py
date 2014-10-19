"""Helper classes."""

def read_ibrl_data(data_file):
    """Reads IBRL data from file and returns dict mapping
    temp./humidity sensor data to the node that collected them

    :param data_file: string representing path to ibrl dataset
    :return: dictionary mapping sensor node to list of tuples containing sensor data
    """
    with open(data_file, 'r') as fp:
        row_count = 0
        bad_count = 0
        measurements = {}
        for line in fp:
            row_count = row_count + 1
            line = line.strip() # remove edge whitespace
            tokens = line.split() # segregate each section
            #if len(tokens) != 8:
            #    pass
            try:
                if len(tokens) != 8: # dump incomplete sensor readings
                    bad_count = bad_count + 1
                elif tokens[3] in measurements: # if sensor id is in the sensor dict
                    # append new temp/humidity tuple
                    measurements[tokens[3]].append((float(tokens[4]), float(tokens[4])))
                else:
                    # else create a new entry in sensor_dict and add it's respective sensor data
                    measurements[tokens[3]] = [(float(tokens[4]), float(tokens[5]))]
            except Exception as e:
                raise e
        print "Total rows: %s" % row_count
        print "Total incomplete rows: %s" % bad_count
    return measurements

def randomize_readings(dictionary):
    """For each list mapped to a sensor, randomize the tuples within and returns the resulting dictionary

    :param dictionary: Dictionary of sensors whose lists will be shuffled
    :return: Dictionary mapping sensors to randomized list of temp. and humidity readings
    """
    import random
    for sensor in dictionary:
        random.shuffle(dictionary[sensor])

    return dictionary

def generate_differences(dictionary):
    """Generates a dictionary that maps each sensor to a list of length n and containing tuples of temp. and humidity
    data to a new list of tuples size n-1 where each tuple is the differnce between the original list at index n+1 and
    the original list at index n

    :param dictionary: dictionary mapping sensors to original tuples of temp. and humidty data.
    :return: dictionary mapping sensors to new list of tuple differences
    """
    differences = {}

    for sensor in dictionary:
        for index in range(len(dictionary) - 1):
            difference_tuple =  (
                dictionary[sensor][index + 1][0] - dictionary[sensor][index][0],
                dictionary[sensor][index + 1][1] - dictionary[sensor][index][1]
            )
            if sensor in differences:
                differences[sensor].append(difference_tuple)
            else:
                differences[sensor] = [difference_tuple]

    return differences

