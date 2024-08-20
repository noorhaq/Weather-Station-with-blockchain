###
# For now we are using random values for the temperature and humidity as we didn't have any sensor specified. But the below functions can be modified to get the data from sensor
#
###
import random

def get_temperature():
    return round(random.uniform(20.0, 30.0), 2) 

def get_humidity():
    return round(random.uniform(50.0, 70.0), 2)