from copy import deepcopy

# Return x normalized between min_value and max_value
# if min_value and max_value are invalid,return x
def normalize(x, min_value, max_value):
    if min_value < max_value:
        normalized = (x - min_value) / (max_value - min_value)
        return normalized
    else:
        return x

# LAZY WORKAROUND!! Fix this later!
def instantiateNewObject(obj):
    new_instance = deepcopy(obj)
    new_instance.value = {}
    return new_instance
