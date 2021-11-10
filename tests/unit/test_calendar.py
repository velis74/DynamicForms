import datetime
import json

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from dynamicforms.template_render.mixins.util import convert_to_json_if


class CalendarEventTest(APITestCase):

    def test_basic_operations(self):

        def get_json(response, expected_status):
            self.assertEqual(expected_status, response.status_code)
            if expected_status == status.HTTP_204_NO_CONTENT:
                return None
            self.assertEqual('application/json', response['content-type'])
            return json.loads(response.content.decode('utf-8'))

        def encode_json(data):
            return convert_to_json_if(event, True).encode('utf-8')

        # check that table is empty and the API is working
        event_url = reverse('calendar-event-list', args=['json'])
        response = get_json(self.client.get(event_url), status.HTTP_200_OK)
        self.assertTrue(not response)  # we are expecting that there are no records in the events table

        # Insert a new event
        event = dict(
            title='Party time', colour=0x000008,
            date_from=datetime.date(2020, 1, 30), time_from=datetime.time(10,0),
            date_to=datetime.date(2020, 1, 30), time_to=datetime.time(11, 0),
        )

        response = get_json(
            self.client.post(event_url, data=encode_json(event), content_type='application/json'),
            status.HTTP_201_CREATED
        )
        expected_response = dict(
            title='Party time', description=None, colour=0x000008,
            date_from='2020-01-30', time_from='10:00:00', date_to='2020-01-30', time_to='11:00:00',
            recurrence=None
        )
        trimmed_response = {k: response[k] for k in expected_response.keys()}
        self.assertEqual(expected_response, trimmed_response)
        self.assertIn('id', response)
        inserted_id = response['id']
        self.assertIsInstance(inserted_id, int)

        # retrieve the new event
        event_url = reverse('calendar-event-detail', kwargs=dict(pk=inserted_id, format='json'))
        response = get_json(self.client.get(event_url), status.HTTP_200_OK)
        self.assertTrue(response)
        trimmed_response = {k: response[k] for k in expected_response.keys()}  # we reuse the expected result from above
        self.assertEqual(expected_response, trimmed_response)

        # patch the event, change only description
        event = dict(description='Let\'s rock this place!')
        response = get_json(
            self.client.patch(event_url, data=encode_json(event), content_type='application/json'),
            status.HTTP_200_OK
        )
        expected_response['description'] = event['description']
        trimmed_response = {k: response[k] for k in expected_response.keys()}
        self.assertEqual(expected_response, trimmed_response)

        response = get_json(
            self.client.delete(event_url),
            status.HTTP_204_NO_CONTENT
        )
        self.assertIsNone(response)
