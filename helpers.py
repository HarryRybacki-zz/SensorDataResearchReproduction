import numpy
import math

"""Helper classes."""

"""Begin data input functions"""
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
            tokens = line.split(',') # segregate each section

            try:
                if len(tokens) != 5: # dump incomplete sensor readings
                    bad_count = bad_count + 1
                elif tokens[3] in measurements: # if sensor id is in the sensor dict
                    # append new temp/humidity tuple
                    measurements[tokens[3]].append((float(tokens[0]), float(tokens[1])))
                else:
                    # else create a new entry in sensor_dict and add it's respective sensor data
                    measurements[tokens[3]] = [(float(tokens[0]), float(tokens[1]))]
            except Exception as e:
                raise e
        print "Total rows: %s" % row_count
        print "Total incomplete rows: %s" % bad_count
    return measurements

"""Begin data transformation functions"""
def randomize_readings(dictionary):
    """For each list mapped to a sensor, randomize the tuples within and returns the resulting dictionary

    :param dictionary: Dictionary of sensors whose lists will be shuffled
    :return: Dictionary mapping sensors to randomized lists of temp. and humidity readings
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

def standardize_readings(sensor_readings):
    """Standardize sensor readings

    :param dictionary: dictionary of sensors whose readings need to be normalized
    :return: dictionary mapping sensors to normalized lists of temp .and humidity readings
    """
    for sensor, readings in sensor_readings.iteritems():
        # Calculate temperature and humidity means
        temp_mean = numpy.mean([reading[0] for reading in readings])
        humidity_mean = numpy.mean([reading[1] for reading in readings])
        # Calculate tempeature and humidity standard deviations
        temp_sd = numpy.std([reading[0] for reading in readings])
        humidity_sd = numpy.std([reading[0] for reading in readings])

        standardized_readings = []

        for reading in readings:
            standardized_readings.append(
                (((reading[0] - temp_mean) / temp_sd),
                 ((reading[1] - humidity_mean) / humidity_sd)))

        sensor_readings[sensor] = standardized_readings

    return sensor_readings

"""Begin ellipsoid modeling functions"""
def generate_regional_ellipsoid_parameters(sensors_ellipsoid_parameters):
    """ Generates the aggregate ellipsoid parameters from a list of ellipsoids
     within a region

    :param ellipsoid_parameters: list of dictionaries representing ellipsoid
    parameters from individual sensors
    :return: dictionary representing the aggregate ellipsoid parameters for a
    given region
    """
    num_of_ellipsoids = len(sensors_ellipsoid_parameters)
    ave_a = sum([sensors_ellipsoid_parameters[ellipsoid]['a'] for ellipsoid in sensors_ellipsoid_parameters]) / num_of_ellipsoids
    ave_b = sum([sensors_ellipsoid_parameters[ellipsoid]['b'] for ellipsoid in sensors_ellipsoid_parameters]) / num_of_ellipsoids
    ave_theta = sum([sensors_ellipsoid_parameters[ellipsoid]['theta'] for ellipsoid in sensors_ellipsoid_parameters]) / num_of_ellipsoids

    return (ave_a, ave_b, ave_theta)

def generate_ellipsoid(sensor_readings, a, b, theta=None):
    """Calculates points representing an ellipsoid for a given a and b
    over a set of sensor readings.

    :param sensor_readings: list of tuples representing sensor readings
    :param a: a parameter used in calculating ellipsoid parameters
    :param b: b parameter used in calculating ellipsoid parameters
    :param theta: optional hardcoded theta value
    :return: ellipsoid_parameters: dictionary containing parameters used in creation of
    as well as results from modeling ellipsoid boundaries
    """
    if theta is None:
        theta = calculate_ellipsoid_orientation(sensor_readings)
    A = calc_A(a, b, theta) # A is independent of the temperatures

    ellipsoid_parameters = {
        'a': a,
        'b': b,
        'theta': theta,
        'original_sensor_readings': sensor_readings,
        'ellipsoid_points': []
    }

    for reading in sensor_readings:
        #print "Temp: %s" % temp
        B = calc_B(a, b, reading[0], theta)
        C = calc_C(a, b, reading[0], theta)
        hi1 = calc_hi1(A, B, C)
        ellipsoid_parameters['ellipsoid_points'].append((reading[0], hi1))
        hi2 = calc_hi2(A, B, C)
        ellipsoid_parameters['ellipsoid_points'].append((reading[0], hi2))

    return ellipsoid_parameters

def calculate_ellipsoid_orientation(sensor_readings):
    """
    :param sensor_readings: list of tuples (temp., humidity) representing readings
    :return: float, theta of ellipsoid orientation
    """

    n = len(sensor_readings)
    temperature_readings = [reading[0] for reading in sensor_readings]
    humidity_readings = [reading[1] for reading in sensor_readings]

    #FIXME(hrybacki): Come up with a better way of breaking this components down

    # part_one
    part_one_multiplicands = [temperature_readings[i]*humidity_readings[i] for i in range(n)]
    part_one_value = n * sum(part_one_multiplicands)

    # part two
    part_two_value = sum(temperature_readings) * sum(humidity_readings)

    # part three
    part_three_value = n * sum([math.pow(temp, 2) for temp in temperature_readings])

    # part four
    part_four_value = math.pow(sum(temperature_readings), 2)

    # arctan(theta)
    tan_theta = (part_one_value - part_two_value) / (part_three_value - part_four_value)

    #return math.atan(tan_theta)
    # @FIXME(hrybacki): Dr. Shan want's this to be absolute value. Do we need that? WHy?
    return math.fabs(math.atan(tan_theta))

def calc_A(a, b, theta):
    """ Returns the A value used in ellipsoid boundary modeling

    :param a: represents the major axis of the ellipsoid
    :param b: represents the mini axis os the ellipsoid
    :param theta: represents the orientation of the raw measurements
    :return: A value used in ellipsoid boundary modeling
    """
    A = (math.pow(math.sin(theta), 2) / math.pow(a, 2)) + (math.pow(math.cos(theta), 2) / math.pow(b, 2))

    return A

def calc_B(a, b, ti, theta):
    """ Returns the B value used in ellipsoid boundary modeling

    :param a: represents the major axis of the ellipsoid
    :param b: represents the mini axis os the ellipsoid
    :param ti: temperature (independent variable) used in calculation
    :param theta: represents the orientation of the raw measurements
    :return: B value used in ellipsoid boundary modeling
    """
    B = ((1/math.pow(a, 2)) - (1/math.pow(b, 2))) * ti * math.sin(2*theta)

    return B

def calc_C(a, b, ti, theta):
    """ Returns the C value used in ellipsoid boundary modeling

    :param a: represents the major axis of the ellipsoid
    :param b: represents the mini axis os the ellipsoid
    :param ti: temperature (independent variable) used in calculation
    :param theta: represents the orientation of the raw measurements
    :return: C value used in ellipsoid boundary modeling
    """
    C = ((math.pow(ti, 2) * math.pow(math.cos(theta), 2)) / math.pow(a, 2)) + \
        ((math.pow(ti, 2) * math.pow(math.sin(theta), 2)) / math.pow(b, 2)) - 1

    return C

def calc_hi1(A, B, C):
    """ Calculates the upper point for a given temp modeling an ellipsoid

    :param A: A value used in ellipsoid boundary modeling
    :param B: B value used in ellipsoid boundary modeling
    :param C: C value used in ellipsoid boundary modeling
    :return: Upper point for given temperature
    """
    try:
        return (-B + math.sqrt(math.pow(B, 2) - (4*A*C))) / (2*A)
    except ValueError:
        pass # skip domain errors

def calc_hi2(A, B, C):
    """ Calculates the lower point for a given temp modeling an ellipsoid

    :param A: A value used in ellipsoid boundary modeling
    :param B: B value used in ellipsoid boundary modeling
    :param C: C value used in ellipsoid boundary modeling
    :return: Lower point for given temperature
    """
    try:
        return (-B - math.sqrt(math.pow(B, 2) - (4*A*C))) / (2*A)
    except ValueError:
        pass # ignore domain errors


"""Begin misc. functions"""
# FIXME: Are we picking the correct values here? Why are the sigmas
# FIXME: 'swapped' in the calculations?
# FIXME: Flip the h's and t's
def calculate_dist(point_one, point_two, sigma_one, sigma_two):
    """ Calculates the distance between two points
    d(pi, pj) = (h1-h2)^2*sigma_one+(t1-t2)^2*sigma_two + 2*(h1-h2)(t1-t2)*sigma_one*sigma_two
    :param point_one: first tuple (temp., humidity)
    :param point_two: second tuple (temp., humidity)
    :param sigma_one: std. dev. of temperature readings
    :param sigma_two: std. dev. of humidity readings
    :return: distance
    """
    t1, h1 = point_one
    t2, h2 = point_two

    return math.fabs(math.pow(h1-h2, 2)*sigma_one + math.pow(t1-t2, 2)*sigma_two + 2*(h1-h2)*(t1-t2)*sigma_one*sigma_two)

def calculate_humidity_mean(sensor_readings):
    """Calculates the mean humidity of a given sensors list of readings

    :param list: list of tuples representing sensor readings (temp., humidity)
    :return: mean
    """

    return numpy.mean([reading[1] for reading in sensor_readings])

def calculate_temp_mean(sensor_readings):
    """Calculates the mean temp. of a given sensors list of readings

    :param list: list of tuples representing sensor readings (humidity, temp.)
    :return: mean
    """

    return numpy.mean([reading[0] for reading in sensor_readings])

"""Begin incomplete functions"""
def model_ellipsoid(sensor_data):
    """Generates and returns a three tuple of ellipsoid parameter for a single sensor

    :param sensor_data: Dictionary mapping a sensor to it's normalized readings
    :return: 3-tuple with ellipsoid parameters
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