from math import log10


def convert_to_IU_per_ml(value, constant):
    if not isinstance(constant, float):
        raise TypeError("Constant has to be a float")
    if constant == 0:
        raise ValueError("Constant cannot be zero")
    
    conversion = value / constant
    return conversion

def get_value_log(value):
    if not isinstance(value, (float, int)):
        raise TypeError("value has to be an Integer or float")
    
    return log10(value)
    