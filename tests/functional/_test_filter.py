import time

from django.urls import reverse
from parameterized import parameterized
from selenium.webdriver.common.by import By

from .selenium_test_case import WaitingStaticLiveServerTestCase


class FilterFormTest(WaitingStaticLiveServerTestCase):
    reset_sequences = True

    # noinspection PyMethodMayBeStatic
    def wait_data_loading(self, loading_row, skip=False):
        time.sleep(0.5)
        if skip:
            return
        # noinspection PyTypeChecker
        while (
            dict(
                [
                    tuple(y.strip() for y in x.split(":"))
                    for x in loading_row.get_attribute("style").split(";")
                    if len(x)
                ]
            ).get("display", "")
            != "none"
        ):
            time.sleep(0.1)

    def check_data(self, data_id):
        try:
            self.browser.find_element(By.CSS_SELECTOR, 'tbody tr[data-id="%s"' % data_id)
            return True
        except:
            return False

    @parameterized.expand(["html", "component"])
    def test_filter_list(self, renderer):
        is_component_renderer = renderer == "component"
        self.browser.get(self.live_server_url + reverse("filter-list", args=[renderer]))

        filter_btn = None
        for button in self.browser.find_elements(
            By.CSS_SELECTOR, ".dynamicforms-actioncontrol" + (" button" if not is_component_renderer else ".button")
        ):
            if button.text == "Filter":
                filter_btn = button
                break
        self.assertIsNotNone(filter_btn, "Page should contain filter button")

        filter_row = self.browser.find_elements(By.CLASS_NAME, "dynamicforms-filterrow")
        self.assertTrue(len(filter_row) > 0, "Page should contain filter")
        filter_row = filter_row[0]
        loading_row = (
            self.browser.find_element(By.CSS_SELECTOR, 'tfoot tr[id*="loading-"') if not is_component_renderer else None
        )

        char_field = filter_row.find_element(By.CSS_SELECTOR, 'input[name="char_field"]')
        datetime_field = (
            filter_row.find_element(By.CSS_SELECTOR, 'input[name="datetime_field"]')
            if not is_component_renderer
            else filter_row.find_element(By.CLASS_NAME, "vdatetime-input")
        )
        int_field = filter_row.find_element(By.CSS_SELECTOR, 'input[name="int_field"]')
        rtf_field = filter_row.find_element(By.CSS_SELECTOR, 'input[name="rtf_field"]')
        if not is_component_renderer:
            int_choices_field = filter_row.find_element(By.CSS_SELECTOR, 'select[name="int_choice_field"]')
        bool_field = filter_row.find_element(By.CSS_SELECTOR, 'input[name="bool_field"]')

        self.wait_data_loading(loading_row, skip=is_component_renderer)
        rtf_field.send_keys("def")
        filter_btn.click()
        self.wait_data_loading(loading_row, skip=is_component_renderer)
        self.assertFalse(self.check_data("1"), "Row 1 shouldn't be shown")
        self.clear_input(rtf_field)
        filter_btn.click()

        self.wait_data_loading(loading_row, skip=is_component_renderer)
        char_field.send_keys("def")
        filter_btn.click()
        self.wait_data_loading(loading_row, skip=is_component_renderer)
        self.assertTrue(self.check_data("2"), "No row 2")
        self.assertTrue(self.check_data("4"), "No row 4")
        self.assertTrue(self.check_data("14"), "No row 14")
        self.assertFalse(self.check_data("1"), "Row 1 shouldn't be shown")
        # char_field.clear()
        self.clear_input(char_field)

        # from examples.models import Filter
        # date_field = Filter.objects.filter(
        # datetime_field__gt=timezone.now() + timedelta(days=1)).order_by('id').first()
        # tomorrow = date_field.datetime_field.strftime("%Y-%m-%dT%H:%M")
        # tomorrow_check = localize(date_field.datetime_field.date())

        if renderer == "html":
            pass
            # commented out datetime field because of missing UI
            # if self.selected_browser in (Browsers.CHROME, Browsers.OPERA):
            #     datetime_field.send_keys(date_field.datetime_field.strftime(
            #         "%m%d%Y" if self.github_actions else "%d%m%Y"))
            #     datetime_field.send_keys(Keys.TAB)
            #     datetime_field.send_keys(date_field.datetime_field.strftime("%H%M%S"))
            #     if self.github_actions:
            #         datetime_field.send_keys("AM")
            # elif self.selected_browser in (Browsers.FIREFOX,):
            #     datetime_field.send_keys(date_field.datetime_field.strftime("%d/%m/%Y"))
            #     datetime_field.send_keys(Keys.TAB)
            #     datetime_field.send_keys(date_field.datetime_field.strftime("%H:%M"))
            # else:
            #     datetime_field.send_keys(tomorrow)

        filter_btn.click()
        self.wait_data_loading(loading_row, skip=is_component_renderer)

        if is_component_renderer:
            datetime_field.click()
            self.browser.find_element(by=By.CLASS_NAME, value="vdatetime-popup__actions__button--confirm").click()
            time.sleep(0.5)
            self.browser.find_element(by=By.CLASS_NAME, value="vdatetime-popup__actions__button--confirm").click()
            time.sleep(0.5)
            self.assertEqual(0, len(self.browser.find_elements(By.CSS_SELECTOR, "tbody tr")))
            self.browser.find_element(by=By.CLASS_NAME, value="clear-datetime").click()

        # commented out datetime field because of missing UI

        # input_val = data_rows[0].find_element(By.CSS_SELECTOR, 'td[data-name="datetime_field"').text
        # self.assertTrue(input_val.startswith(tomorrow_check),
        #                 'First row date not matching [%s] != [%s]' % (input_val, tomorrow_check))
        # input_val = data_rows[-1].find_element(By.CSS_SELECTOR, 'td[data-name="datetime_field"').text
        # self.assertTrue(input_val.startswith(tomorrow_check),
        #                 'Last row date not matching [%s] != [%s]' % (input_val, tomorrow_check))

        int_field.send_keys("2")
        # datetime_field.clear()
        # self.clear_input(datetime_field)
        filter_btn.click()
        self.wait_data_loading(loading_row, skip=is_component_renderer)
        self.assertTrue(self.check_data("2"), "No row 2")
        self.assertTrue(self.check_data("12"), "No row 12")
        self.assertTrue(self.check_data("22"), "No row 22")
        self.assertFalse(self.check_data("1"), "Row 1 shouldn't be shown")
        # int_field.clear()
        self.clear_input(int_field)

        if not is_component_renderer:
            self.select_option_for_select2(filter_row, int_choices_field.get_attribute("id"), text="Choice 2")

        filter_btn.click()
        if not is_component_renderer:
            # todo: wait for choice field to WORK
            self.wait_data_loading(loading_row, skip=is_component_renderer)
            self.assertTrue(self.check_data("2"), "No row 2")
            self.assertTrue(self.check_data("6"), "No row 6")
            self.assertTrue(self.check_data("10"), "No row 10")
            self.assertTrue(self.check_data("14"), "No row 14")
            self.assertFalse(self.check_data("1"), "Row 1 shouldn't be shown")
            self.assertFalse(self.check_data("3"), "Row 3 shouldn't be shown")
            self.assertFalse(self.check_data("9"), "Row 9 shouldn't be shown")
            self.assertFalse(self.check_data("11"), "Row 11 shouldn't be shown")
            self.select_option_for_select2(filter_row, int_choices_field.get_attribute("id"), text="--------")
        self.wait_data_loading(loading_row, skip=is_component_renderer)

        bool_field.click()

        time.sleep(0.2)
        filter_btn.click()
        self.wait_data_loading(loading_row, skip=is_component_renderer)
        self.assertTrue(self.check_data("1"), "No row 1")
        self.assertTrue(self.check_data("5"), "No row 5")
        self.assertTrue(self.check_data("11"), "No row 11")
        self.assertTrue(self.check_data("15"), "No row 15")
        self.assertFalse(self.check_data("6"), "Row 6 shouldn't be shown")
        self.assertFalse(self.check_data("10"), "Row 10 shouldn't be shown")
        self.assertFalse(self.check_data("16"), "Row 16 shouldn't be shown")
        self.assertFalse(self.check_data("20"), "Row 20 shouldn't be shown")

        if is_component_renderer:
            bool_field = filter_row.find_element(By.CSS_SELECTOR, 'input[name="bool_field"]')

        bool_field.click()
        time.sleep(0.2)
        filter_btn.click()
        self.wait_data_loading(loading_row, skip=is_component_renderer)
        self.assertTrue(self.check_data("6"), "No row 6")
        self.assertTrue(self.check_data("10"), "No row 10")
        self.assertTrue(self.check_data("16"), "No row 16")
        self.assertTrue(self.check_data("20"), "No row 20")
        self.assertFalse(self.check_data("1"), "Row 1 shouldn't be shown")
        self.assertFalse(self.check_data("5"), "Row 5 shouldn't be shown")
        self.assertFalse(self.check_data("11"), "Row 11 shouldn't be shown")
        self.assertFalse(self.check_data("15"), "Row 15 shouldn't be shown")

        char_field.send_keys("jkl")
        if not is_component_renderer:
            pass
            # commented out datetime field because of missing UI
            # datetime_field.send_keys(tomorrow)
        int_field.send_keys("11")
        if not is_component_renderer:
            self.select_option_for_select2(filter_row, int_choices_field.get_attribute("id"), text="Choice 3")
        if is_component_renderer:
            # todo: fix select to complete tests
            return
        filter_btn.click()
        self.wait_data_loading(loading_row, skip=is_component_renderer)
        data_rows = self.browser.find_elements(By.CSS_SELECTOR, "tbody tr")
        self.assertTrue(len(data_rows) == 1, "There should be no data. Only one row (no data row) in table body")
        self.assertTrue(data_rows[0].find_element(By.TAG_NAME, "td").text == "No data", 'No "No data" row')
