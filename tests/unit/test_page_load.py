import json

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class PageLoadTest(APITestCase):

    def test_fetch_first_page(self):
        response = self.client.get(reverse('page-load-list', args=['html']))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response['content-type'], 'text/html; charset=utf-8')
        content = response.content.decode('utf-8')
        self.assertTrue(all(x in content for x in ['<html', '<body', '<table', '<tbody', '<tr']))

    def test_fetch_next_page(self):
        response = self.client.get(reverse('page-load-list', args=['json']), HTTP_X_PAGINATION=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response['content-type'], 'application/json')
        content = json.loads(response.content.decode('utf-8'))
        cursor_next = content['next'].replace('json', 'html')  # a little hack to obtain the cursor for HTML renderer

        response = self.client.get(cursor_next, HTTP_X_DF_RENDER_TYPE='table rows')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response['content-type'], 'text/html; charset=utf-8')
        content = response.content.decode('utf-8')
        self.assertFalse(any(x in content for x in ['<html', '<body', '<table']))
        self.assertTrue(all(x in content for x in ['<tr', '<td', 'data-next=']))
