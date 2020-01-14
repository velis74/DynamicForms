import time

from django.urls import reverse

from examples.migrations import add_page_load
from examples.models import PageLoad
from .selenium_test_case import WaitingStaticLiveServerTestCase

MAX_WAIT = 10


class PageLoadFormTest(WaitingStaticLiveServerTestCase):

    def test_validated_list(self):
        # When running tests through github actions table PageLoad is empty, even though it gets filled up in
        # migrations initialisation
        if PageLoad.objects.count() == 0:
            add_page_load(None, None)

        self.browser.get(self.live_server_url + reverse('page-load-list', args=['html']))
        tbody = self.browser.find_element_by_tag_name('tbody')
        rows = tbody.find_elements_by_tag_name('tr')
        new_num_elements = num_elements = len(rows)
        self.assertTrue(num_elements > 0, 'Initial page load should contain data rows')

        def load_next():
            nonlocal new_num_elements, num_elements
            num_elements = new_num_elements
            tim = time.time()
            while time.time() < tim + 5 and new_num_elements == num_elements:
                # we wait for 5 seconds for number of elements to update on page
                time.sleep(.1)
                new_num_elements = len(tbody.find_elements_by_tag_name('tr'))

        load_next()
        self.assertGreater(new_num_elements, num_elements,
                           'The page was supposed to load next page of elements in a second after initial load')

        load_next()
        self.assertEqual(new_num_elements, num_elements,
                         'The page was supposed to stop loading following pages of elements after the initial addendum')

        self.browser.execute_script('window.scrollBy(0, 50000);')

        load_next()
        self.assertGreater(new_num_elements, num_elements,
                           'The page was supposed to load next page of elements in a second after scrolling to bottom')
