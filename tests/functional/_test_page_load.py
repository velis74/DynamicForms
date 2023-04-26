import time

from django.urls import reverse
from parameterized import parameterized
from selenium.webdriver.common.by import By

from tests.functional.selenium_test_case import WaitingStaticLiveServerTestCase
from tests.request_sync import RequestSyncMiddleware

MAX_WAIT = 10


class PageLoadFormTest(WaitingStaticLiveServerTestCase):
    @parameterized.expand(["html", "component"])
    def test_validated_list(self, renderer):
        with RequestSyncMiddleware.add_sync_url_mutex("page-load", 1):
            self.browser.get(self.live_server_url + reverse("page-load-list", args=[renderer]))
            tbody = self.browser.find_element(By.TAG_NAME, "tbody")
            new_num_elements = num_elements = len(tbody.find_elements(By.TAG_NAME, "tr"))
            self.assertEqual(num_elements, 30, "Initial page load should contain 30 data rows")

        def load_next():
            nonlocal new_num_elements, num_elements
            num_elements = new_num_elements
            tim = time.time()
            while time.time() < tim + 2 and new_num_elements == num_elements:
                # we wait for 5 seconds for number of elements to update on page
                time.sleep(0.1)
                new_num_elements = len(tbody.find_elements(By.TAG_NAME, "tr"))

        load_next()
        self.assertGreater(
            new_num_elements,
            num_elements,
            "The page was supposed to load next page of elements within a second after initial load",
        )

        load_next()
        self.assertEqual(
            new_num_elements,
            num_elements,
            "The page was supposed to stop loading following pages of elements after the initial addendum",
        )

        self.browser.execute_script("window.scrollBy(0, 50000);")

        load_next()
        self.assertGreater(
            new_num_elements,
            num_elements,
            "The page was supposed to load next page of elements in a second after scrolling to bottom",
        )
