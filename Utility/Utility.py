from copy import deepcopy
import os
# Return x normalized between min_value and max_value
# if min_value and max_value are invalid,return x
def normalize(x, min_value, max_value):
    if min_value < max_value:
        normalized = (x - min_value) / (max_value - min_value)
        return normalized
    else:
        return x

# Creates (or clean) a certain directory used for logging
def prepareLogDirectory(folderPath):
        directory = os.path.dirname(folderPath)
        # if directory does not exit, create it
        if not os.path.exists(directory):
            os.makedirs(directory)
        # if exists, try to clean any old log files inside it
        else:
            for myFile in os.listdir(folderPath):
                filePath = os.path.join(folderPath, myFile)
                try:
                    if os.path.isfile(filePath):
                        os.remove(filePath)
                except Exception as e:
                    print("Error")
                    pass

def getFilesFromDirectory(folderPath):
    files = []
    for myFile in os.listdir(folderPath):
        filePath = os.path.join(folderPath, myFile)
        files.append(filePath)
    return sorted(files)

# Creates a new instance of dynamic unkown object
def instantiateNewObject(obj):
    import importlib
    module_name = obj.__module__
    class_name = type(obj).__name__

    MyClass = getattr(importlib.import_module(module_name), class_name)
    instance = MyClass()
    return instance

