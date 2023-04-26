from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class ValidateAllowNullForFieldWithSourceEqualToStarTest(APITestCase):
    def setUp(self):
        super().setUp()
        self.record_data = dict(
            name="",
            char_field="something",
            datetime_field="2019-11-06T00:35:00.771476",
            int_field=5,
            int_choice_field=0,
            bool_field=False,
            rtf_field="string value",
        )

    def __make_post_request(self, data):
        return self.client.post(reverse("filter-list", args=["json"]), data=data)

    def test_validate_allow_null_with_empty_string_for_field_with_source_equal_to_star(self):
        response = self.__make_post_request(self.record_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_validate_allow_null_with_null_for_field_with_source_equal_to_star(self):
        self.record_data.pop("name")
        response = self.__make_post_request(self.record_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_record_for_field_with_source_equal_to_star(self):
        name = "test"
        self.record_data["name"] = name
        response = self.__make_post_request(self.record_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data.get("name"), name)

    def test_update_record_for_field_with_source_equal_to_star(self):
        name = "test"
        self.record_data["name"] = "xy"
        response = self.__make_post_request(self.record_data)
        id = response.data.get("id")
        self.record_data["name"] = name
        update_response = self.client.put(reverse("filter-detail", kwargs=dict(pk=id)), data=self.record_data)
        self.assertEqual(update_response.status_code, status.HTTP_200_OK)
        self.assertEqual(update_response.data.get("name"), name)
