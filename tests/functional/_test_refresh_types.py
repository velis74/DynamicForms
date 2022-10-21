import time

from selenium.webdriver.common.by import By

from examples.models import RefreshType
from .selenium_test_case import WaitingStaticLiveServerTestCase


class RefreshTypesTest(WaitingStaticLiveServerTestCase):

    def add_refresh_types_record(self, btn_position, text, add_second_record=None):
        header = self.find_element_by_classes(('card-header', 'panel-heading', 'ui-accordion-header'))
        add_btns = header.find_elements(By.CLASS_NAME, 'btn')
        add_btns[btn_position].click()

        dialog, modal_serializer_id = self.wait_for_modal_dialog()

        form = dialog.find_element(By.ID, modal_serializer_id)
        containers = form.find_elements(By.CSS_SELECTOR, "div[id^=container-]")
        for container in containers:
            container_id = container.get_attribute("id")
            if container_id.startswith("container-"):
                field_id = container_id.split('-', 1)[1]
                label = container.find_element(By.ID, "label-" + field_id)
                field = container.find_element(By.ID, field_id)

                if self.get_element_text(label) == "Description":
                    self.initial_check(field, "", "description", "text")
                    field.send_keys(text)
                elif field.get_attribute("name") in ('id',):
                    # Hidden fields
                    pass

        if add_second_record:
            RefreshType.objects.create(
                description="Refresh type extra"
            )

        dialog.find_element(By.ID, "save-" + modal_serializer_id).click()

        if btn_position == 5:  # Custom function only
            alert = self.get_alert()
            self.assertEqual(self.get_element_text(alert), 'Custom function refresh type.')
            alert.accept()

        self.wait_for_modal_dialog_disapear(modal_serializer_id)

    # components don't need custom refreshing because everything works as it's supposed to (full refresh)
    # @parameterized.expand(['html', 'component'])
    def test_refresh_types_list(self, renderer='html'):
        self.browser.get(self.live_server_url + '/refresh-types.' + renderer)

        header = self.find_element_by_classes(('card-header', 'panel-heading', 'ui-accordion-header'))

        add_btns = header.find_elements(By.CLASS_NAME, 'btn')
        self.assertEqual(self.get_element_text(add_btns[0]), '+ Add (refresh record)')
        self.assertEqual(self.get_element_text(add_btns[1]), '+ Add (refresh table)')
        self.assertEqual(self.get_element_text(add_btns[2]), '+ Add (no refresh)')
        self.assertEqual(self.get_element_text(add_btns[3]), '+ Add (page reload)')
        self.assertEqual(self.get_element_text(add_btns[4]), '+ Add (redirect)')
        self.assertEqual(self.get_element_text(add_btns[5]), '+ Add (custom function)')

        # Check if there's a "no data" table row
        rows = self.get_table_body()
        self.assertEqual(len(rows), 1)
        self.assertEqual(self.get_element_text(rows[0].find_element(By.TAG_NAME, 'td')), 'No data')

        # Test Add action with refreshType='record'
        self.add_refresh_types_record(0, 'Refresh record')
        time.sleep(1)
        rows = self.get_table_body()
        self.assertEqual(len(rows), 1)
        cells = rows[0].find_elements(By.TAG_NAME, "td")
        self.assertEqual(len(cells), 4)

        # Test Add action with refreshType='table'
        self.add_refresh_types_record(1, 'Refresh table')
        rows = self.get_table_body()
        self.assertEqual(len(rows), 2)
        rows[0].find_elements(By.TAG_NAME, "td")

        self.add_refresh_types_record(1, 'Refresh table 2', add_second_record=True)
        time.sleep(1)
        rows = self.get_table_body()
        self.assertEqual(len(rows), 4)

        # Test Add action with refreshType='no refresh'
        self.add_refresh_types_record(2, 'No refresh')
        rows = self.get_table_body()
        self.assertEqual(len(rows), 4)

        self.browser.refresh()

        rows = self.get_table_body()
        self.assertEqual(len(rows), 5)

        # Test Add action with refreshType='reload'
        self.add_refresh_types_record(3, 'Page reload')
        rows = self.get_table_body()
        self.assertEqual(len(rows), 6)

        # Test Add action with refreshType='redirect'
        self.add_refresh_types_record(4, 'Redirect')
        # Redirection to /validated.html defined in action happens
        redirect_url = self.get_current_url()
        self.assertRegex(redirect_url, '/validated.' + renderer)
        # Back to /refresh-types.html
        self.browser.get(self.live_server_url + '/refresh-types.' + renderer)
        rows = self.get_table_body()
        self.assertEqual(len(rows), 7)

        # Test Add action with refreshType='custom function'
        self.add_refresh_types_record(5, 'Custom function')
        # Alert is processed in add_record function

        self.browser.refresh()

        rows = self.get_table_body()
        self.assertEqual(len(rows), 8)

        # Test Delete action with refreshType='record'
        del_btns = rows[0].find_elements(By.TAG_NAME, 'td')[3].find_elements(By.CLASS_NAME, 'btn')
        del_btns[0].click()
        rows = self.get_table_body()
        self.assertEqual(len(rows), 7)

        # Test Delete action with refreshType='table'
        del_btns = rows[0].find_elements(By.TAG_NAME, 'td')[3].find_elements(By.CLASS_NAME, 'btn')
        del_btns[1].click()
        rows = self.get_table_body()
        self.assertEqual(len(rows), 6)

        # Test Delete action with refreshType='no refresh'
        del_btns = rows[0].find_elements(By.TAG_NAME, 'td')[3].find_elements(By.CLASS_NAME, 'btn')
        del_btns[2].click()
        rows = self.get_table_body()
        self.assertEqual(len(rows), 6)

        self.browser.refresh()

        rows = self.get_table_body()
        self.assertEqual(len(rows), 5)

        # Test Delete action with refreshType='reload'
        del_btns = rows[0].find_elements(By.TAG_NAME, 'td')[3].find_elements(By.CLASS_NAME, 'btn')
        del_btns[3].click()
        rows = self.get_table_body()
        self.assertEqual(len(rows), 4)

        # Test Delete action with refreshType='redirect'
        del_btns = rows[0].find_elements(By.TAG_NAME, 'td')[3].find_elements(By.CLASS_NAME, 'btn')
        del_btns[4].click()
        # Redirection to /validated.html defined in action happens
        redirect_url = self.get_current_url()
        self.assertRegex(redirect_url, '/validated.' + renderer)
        # Back to /refresh-types.html
        self.browser.get(self.live_server_url + '/refresh-types.' + renderer)
        rows = self.get_table_body()
        self.assertEqual(len(rows), 3)

        # Test Delete action with refreshType='custom function'
        del_btns = rows[0].find_elements(By.TAG_NAME, 'td')[3].find_elements(By.CLASS_NAME, 'btn')
        del_btns[5].click()

        alert = self.get_alert()
        self.assertEqual(self.get_element_text(alert), 'Custom function refresh type.')
        alert.accept()

        self.browser.refresh()

        rows = self.get_table_body()
        self.assertEqual(len(rows), 2)
