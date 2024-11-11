import os
import json


def read_file(filename):
    absolute_path = os.path.abspath(filename)

    with open(absolute_path, 'r') as f:
        return json.load(f)


def write_file(filename, data):
    absolute_path = os.path.abspath(filename)

    with open(absolute_path, 'w') as f:
        json.dump(data, f, indent=4)
