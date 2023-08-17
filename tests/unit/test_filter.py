import json

from django.urls import reverse
from jsonschema import validate
from rest_framework import status
from rest_framework.test import APITestCase

schema = {
    "type": "array",
    "items": {
        "type": "object",
        "properties": {
            "id": {"type": "number"},
            "df_control_data": {"type": "object"},
            "df_prev_id": {"type": "string"},
            "row_css_style": {"type": "string"},
            "name": {"type": ["null", "string"]},
            "rtf_field": {"type": ["null", "string"]},
            "datetime_field": {"type": "string"},
            "char_field": {"type": "string"},
            "int_field": {"type": "number"},
            "int_choice_field": {"type": "number"},
            "int_choice_field-display": {"type": "string"},
            "bool_field": {"type": "boolean"},
        },
        "additionalProperties": False,
    },
}


class FilterTest(APITestCase):
    def test_contains_filter(self):
        response = self.client.get(reverse("filter-list", args=["json"]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response["content-type"], "application/json")
        content = json.loads(response.content)
        validate(content, schema)
