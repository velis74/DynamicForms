import json

from django.urls import reverse
from jsonschema import validate
from rest_framework import status
from rest_framework.test import APITestCase

response_schema = {
    "type": "array",
    "items": {
        "type": "object",
        "properties": {
            "id": {"type": "number"},
            "description": {"type": "string"},
            "df_control_data": {"type": "object"},
            "df_prev_id": {"type": "string"},
            "choice": {"type": "number"},
            "choice-display": {"type": "string"},
            "row_css_style": {"type": "string"},
        },
        "required": ["id", "description", "df_control_data", "df_prev_id", "choice", "row_css_style"],
        "additionalProperties": False,
    },
}

next_schema = {
    "type": "object",
    "properties": {
        "next": {"type": "string"},
        "previous": {"type": "string"},
        "results": response_schema,
    },
}


class PageLoadTest(APITestCase):
    def test_fetch_first_page(self):
        response = self.client.get(reverse("page-load-list", args=["json"]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response["content-type"], "application/json")
        content = json.loads(response.content)
        validate(content, schema=response_schema)

    def test_fetch_next_page(self):
        response = self.client.get(reverse("page-load-list", args=["json"]), HTTP_X_PAGINATION=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response["content-type"], "application/json")
        content = json.loads(response.content.decode("utf-8"))
        cursor_next = content["next"]

        response = self.client.get(cursor_next, HTTP_X_DF_RENDER_TYPE="table rows")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response["content-type"], "application/json")
        content = json.loads(response.content.decode("utf-8"))
        validate(content, schema=next_schema)
