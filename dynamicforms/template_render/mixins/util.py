import json

from rest_framework.utils.encoders import JSONEncoder


def convert_to_json_if(data, output_json: bool = True):
    if output_json:
        return json.dumps(data, cls=JSONEncoder)
    return data
