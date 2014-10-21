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
    data to a new list of tuples size n-1 where each tuple is the difference between the original list at index n+1 and
    the original list at index n

    :param dictionary: dictionary mapping sensors to original tuples of temp. and humidity data.
    :return: tuple containing dictionary mapping sensors to new list of tuple differences and a lookup table containing
    back references to the raw measurements used to calculate the new measurements in the differences dict
    """
    differences = {}
    lookup_table = {}

    for sensor in dictionary:
        for index in range(len(dictionary[sensor]) - 1):
            difference_tuple =  (
                dictionary[sensor][index + 1][0] - dictionary[sensor][index][0],
                dictionary[sensor][index + 1][1] - dictionary[sensor][index][1]
            )
            if sensor in differences:
                differences[sensor].append(difference_tuple)
            else:
                differences[sensor] = [difference_tuple]

    return (differences, lookup_table)

def calculate_humidity_mean(sensor_readings):
    """Calculates the mean humidity of a given sensors list of readings

    :param list: list of tuples representing sensor readings (humidity, temp.)
    :return: mean
    """

    total_count = 0

    for index, reading in enumerate(sensor_readings):
        total_count = total_count + reading[0] # humidity portion of tuple

    return total_count / len(sensor_readings)

def calculate_temp_mean(sensor_readings):
    """Calculates the mean temp. of a given sensors list of readings

    :param list: list of tuples representing sensor readings (humidity, temp.)
    :return: mean
    """

    total_count = 0

    for index, reading in enumerate(sensor_readings):
        total_count = total_count + reading[1] # temp. portion of tuple

    return total_count / len(sensor_readings)

def model_ellipsoid(sensor_data):
    """Generates and returns a three tuple of ellipsoid parameter for a single sensor

    :param sensor_data: Dictionary mapping a sensor to it's normalized readings
    :return: 3-tuple with ellipsoid parameters
    """
    pass

def model_region_ellipsoid(sensor_ellipsoids):
    """Generates and returns a three tuple of ellipsoid parameter aggregate

    :param sensor_data: Dictionary mapping sensors to their respective ellipsoids
    :return: 3-tuple with ellipsoid aggregate parameters
    """
    pass

def inverse_transformation(lookup_table, aggregate_ellipsoid):
    """ Generates a tuple of two dicts mapping sensors to anomalies and true measurements

    :param lookup_table: dictionary mapping difference readings to their raw measurements
    :param aggregate_ellipsoid: 3-tuple containing aggregate ellipsoid parameters
    :return: tuple containing two dicts, one of true measurements and another of anomalies
    each mapped to their original sensors
    """
    true_measurements = {}
    anomalies = {}

    for sensor in lookup_table:
        for reading in sensor:
            if is_anomaly(reading):
                anomalies[sensor] = reading
            else:
                true_measurements[sensor] = reading

    return (true_measurements, anomalies)

def is_anomaly(reading, aggregate_ellipsoid):
    """ Determines if reading is anomaly with respect to an ellipsoid

    :param reading: temperature and humidity readings
    :param aggregate_ellipsoid: parameters for aggregate ellipsoid
    :return: True if an anomaly, else False
    """
    pass