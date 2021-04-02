from rest_framework.utils.encoders import JSONEncoder
import json


def convert_to_json_if(data, output_json: bool=True):
    if output_json:
        return json.dumps(data, cls=JSONEncoder)
    return data
