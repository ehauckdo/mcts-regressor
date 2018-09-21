from copy import deepcopy

# Return x normalized between min_value and max_value
# if min_value and max_value are invalid,return x
def normalize(x, min_value, max_value):
    if min_value < max_value:
        normalized = (x - min_value) / (max_value - min_value)
        return normalized
    else:
        return x

def print_log(text, shouldPrint):
    if shouldPrint:
        print(text)

def instantiateNewObject(obj):
    import importlib
    module_name = obj.__module__
    class_name = type(obj).__name__

    MyClass = getattr(importlib.import_module(module_name), class_name)
    instance = MyClass()
    return instance

