import matplotlib.pyplot as pyplot

import helpers


"""
Begin phase one - Read Input

Note: This phase will need slight tweaking for each data source as they do not follow a truly standard data format.
As a result, interfaces will likely need to be written for each source akin to read_ibrl_data()

Note: While I had originally intended to use Pandas DataFrame objects to store / manipulate the data I opted out as
it expects each column (sensor) to be of the same length (number of measurements) but that isn't the case with the IBRL
dataset. I could cast each column to a Pandas Series (1 dimensional vector object) and add each Series to the DataFrame
but that might be overkill. For know I am using a simple dictionary mapping each sensor to a list of tuples containing
temperature and humidity data.
"""
# location of IBRL sensor measurements dataset
ibrl_sensor_measurements_file = "./datasets/Reduced2530K.csv"


# Create dictionary of original sensors mapping to their measurements
# x1, x2, ..., xn where xi = (ti', hi') and X = (T, H)
raw_measurements = helpers.read_ibrl_data(ibrl_sensor_measurements_file)

"""
Begin phase two - Process Data
"""

# 1A - Transformation

# Shuffle measurements
shuffled_measurements = helpers.randomize_readings(raw_measurements)

# Calculate successive differences
differences, lookup_table = helpers.generate_differences(shuffled_measurements)

# Sensor One Test Data
sensor_one_data = raw_measurements['2']
sensor_one_shuffle = shuffled_measurements['2']
sensor_one_differences = differences['2']


pyplot.figure(1)

# Plot of Original Data
pyplot.subplot(311) # Num rows, num cols, figure num
for sensor in raw_measurements:
    pyplot.plot([reading[0] for reading in raw_measurements[sensor]],
                [reading[1] for reading in raw_measurements[sensor]],
                'ro')
pyplot.axis([0, 100, 0, 100]) # [xmin, xmax, ymin, ymax]
pyplot.xlabel('Temperature')
pyplot.ylabel('Humidity')
pyplot.title('Original Data')

# Plot of Shuffled   Sensor One Data
pyplot.subplot(312)
for sensor in shuffled_measurements:
    pyplot.plot([reading[0] for reading in shuffled_measurements[sensor]],
                [reading[1] for reading in shuffled_measurements[sensor]],
                'ro')
pyplot.axis([0, 100, 0, 100]) # [xmin, xmax, ymin, ymax]
pyplot.xlabel('Temperature')
pyplot.ylabel('Humidity')
pyplot.title('Randomized Data')

# Plot of Original Sensor One Data
pyplot.subplot(313)
for sensor in differences:
    pyplot.plot([reading[0] for reading in differences[sensor]],
                [reading[1] for reading in differences[sensor]],
                'ro')
pyplot.axis([-50, 50, -50, 50]) # [xmin, xmax, ymin, ymax]
pyplot.xlabel('Temperature')
pyplot.ylabel('Humidity')
pyplot.title('Successive Differences')

pyplot.tight_layout()

# Save the plot
pyplot.savefig('wsn_data_transformation.png')


# 1B - Ellipsoid Boundary Modeling
print len(differences['11'])
print len(shuffled_measurements['11'])

pyplot.figure(2)

min_temp, max_temp = helpers.get_min_max_temp(differences['3'])

pyplot.subplot(311)
pyplot.plot([reading[0] for reading in differences['5']],
            [reading[1] for reading in differences['5']])
pyplot.xlabel('Temperature')
pyplot.ylabel('Humidity')
pyplot.title('Successive Differences from Sensor 5')
pyplot.show()



# 1C - Inverse Transformation

"""
Begin phase four - Visually model data
"""

print "Completed..."