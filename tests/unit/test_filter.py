from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class FilterTest(APITestCase):

    def test_contains_filter(self):
        response = self.client.get(reverse('filter-list', args=['html']))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response['content-type'], 'text/html; charset=utf-8')
        content = response.content.decode('utf-8')
        self.assertTrue(
            all(x in content for x in ['<html', '<body', '<table', '<tbody', '<tr class="dynamicforms-filterrow"',
                                       'dynamicforms.defaultFilter(event)']))
