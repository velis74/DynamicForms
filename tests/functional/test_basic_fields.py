import time

from parameterized import parameterized
from selenium.webdriver.common.keys import Keys

from .selenium_test_case import Browsers, MAX_WAIT, WaitingStaticLiveServerTestCase


class BasicFieldsTest(WaitingStaticLiveServerTestCase):

    @parameterized.expand(['html', 'component'])
    def test_basic_fields(self, renderer):
        self.browser.get(self.live_server_url + '/basic-fields.' + renderer)
        # Go to basic-fields html and check if there's a "+ Add" button

        header = self.find_element_by_classes(('card-header', 'panel-heading', 'ui-accordion-header'))
        add_btn = header.find_element_by_name('btn-add')
        md_btn = header.find_element_by_name('btn-modal_dialog')
        self.assertEqual(self.get_element_text(add_btn), '+ Add')

        # Check if there's a "no data" table row
        rows = self.get_table_body()
        self.assertEqual(len(rows), 1)
        self.assertEqual(self.get_element_text(rows[0].find_element_by_tag_name('td')), 'No data')

        # ---------------------------------------------------------------------------------------------------------#
        # Following a test for modal dialog... we could also do a test for page-editing (not with dialog)          #
        # ---------------------------------------------------------------------------------------------------------#

        # TODO: Currently there is no modal dialog for .component, skipping test
        if renderer == 'html':
            md_btn.click()
            dialog, modal_serializer_id = self.wait_for_modal_dialog()
            dialog.find_element_by_id('dlg-btn-ok').click()
            alert = self.browser.switch_to.alert
            self.assertEqual(alert.text, 'Clicked OK button')
            alert.accept()
            self.wait_for_modal_dialog_disapear(modal_serializer_id)

        # Add a new record via the "+ Add" button and go back to model_single.html to check if the record had been added
        add_btn.click()
        dialog, modal_serializer_id = self.wait_for_modal_dialog()

        # check if all fields are in the dialog and no excessive fields too
        field_count = 0

        form = dialog.find_element_by_id(modal_serializer_id)
        containers = form.find_elements_by_xpath('//div[starts-with(@id, "container-")]')
        for container in containers:
            container_id = container.get_attribute('id')
            if container_id.startswith('container-'):
                field_id = container_id.split('-', 1)[1]
                label = container.find_element_by_id("label-" + field_id)
                field = container.find_element_by_id(field_id)

                field_count += 1
                label_text = self.get_element_text(label)

                if label_text == 'Boolean field':
                    self.initial_check(field, '', 'boolean_field', 'checkbox')
                    self.assertEqual(field.get_attribute('class'), 'form-check-input')
                    field.click()
                elif label_text == 'Nullboolean field':
                    field_type = self.initial_check(field, '', 'nullboolean_field', ('text', 'checkbox'))
                    if field_type == 'checkbox':
                        self.assertEqual(field.get_attribute('class'), 'form-check-input')
                        field.click()
                    else:
                        field.send_keys('True')
                elif label_text == 'Char field':
                    self.initial_check(field, '', 'char_field', 'text')
                    field.send_keys('Test')
                elif label_text == 'Email field':
                    self.initial_check(field, '', 'email_field', 'email')
                    field.send_keys('test@test.com')
                elif label_text == 'Slug field':
                    self.initial_check(field, '', 'slug_field', 'text')
                    field.send_keys('test-slug')
                elif label_text == 'Url field':
                    self.initial_check(field, '', 'url_field', 'url')
                    field.send_keys('http://test.test')
                elif label_text == 'Uuid field':
                    self.initial_check(field, '', 'uuid_field', 'text')
                    field.send_keys('123e4567-e89b-12d3-a456-426655440000')
                elif label_text == 'Ipaddress field':
                    self.initial_check(field, '', 'ipaddress_field', 'text')
                    field.send_keys('145.17.154.1')
                elif label_text == 'Integer field':
                    self.initial_check(field, '', 'integer_field', 'number')
                    field.send_keys(1)
                elif label_text == 'Float field':
                    self.initial_check(field, '', 'float_field', 'number')
                    field.send_keys(15)
                elif label_text == 'Decimal field':
                    self.initial_check(field, '', 'decimal_field', 'text')
                    field.send_keys('15.18')
                elif label_text == 'Datetime field':
                    self.initial_check(field, '', 'datetime_field', ('datetime-local', 'text'))
                    if self.selected_browser in (Browsers.CHROME, Browsers.OPERA):
                        field.send_keys('08122018')
                        field.send_keys(Keys.TAB)
                        field.send_keys('081500')
                        if self.github_actions:
                            field.send_keys('AM')
                    elif self.selected_browser == Browsers.EDGE:
                        # There is a bug when sending keys to EDGE.
                        # https://stackoverflow.com/questions/38747126/selecting-calendar-control-in-edge-using-selenium
                        # Workaround is to do this with javascript using execute_script method
                        self.update_edge_field(field_id, '2018-12-08T08:15')
                    else:
                        field.send_keys('2018-12-08 08:15:00')
                elif label_text == 'Date field':
                    self.initial_check(field, '', 'date_field',
                                       ('date', 'text') if self.selected_browser in (
                                           Browsers.IE, Browsers.SAFARI) else 'date')
                    if self.selected_browser in (Browsers.CHROME, Browsers.OPERA):
                        field.send_keys('08122018')
                    elif self.selected_browser == Browsers.EDGE:
                        field.send_keys(Keys.ENTER)
                    else:
                        field.send_keys('2018-12-08')
                elif label_text == 'Time field':
                    self.initial_check(field, '', 'time_field',
                                       ('time', 'text') if self.selected_browser in (
                                           Browsers.IE, Browsers.SAFARI) else 'time')
                    if self.selected_browser in (Browsers.CHROME, Browsers.OPERA):
                        field.send_keys('081500')
                        if self.github_actions:
                            field.send_keys('AM')
                    elif self.selected_browser == Browsers.EDGE:
                        field.send_keys(Keys.ENTER)
                    else:
                        field.send_keys('08:15:00')
                elif label_text == 'Duration field':
                    self.initial_check(field, '', 'duration_field', 'text')
                    field.send_keys('180')
                elif label_text == 'Password field':
                    self.initial_check(field, '', 'password_field', 'password')
                    field.send_keys('password')
                    id_attr = field.get_attribute('id')
                    container.find_element_by_id('pwf-' + id_attr).click()
                    self.assertEqual('text', field.get_attribute('type'))
                else:
                    field_count -= 1

        self.assertEqual(field_count, 16)

        save_button_prefix = "save-" if renderer == 'html' else 'submit-'
        dialog.find_element_by_id(save_button_prefix + modal_serializer_id).click()
        self.wait_for_modal_dialog_disapear(modal_serializer_id)
        time.sleep(1)  # Zato, da se lahko tabela osveži
        rows = self.get_table_body()
        self.assertEqual(len(rows), 1)
        cells = rows[0].find_elements_by_tag_name("td")
        self.assertEqual(len(cells), 18)

        # Then we click the record row to edit it. Go back to model_single.html and check if it had been edited
        cells[0].click()
        dialog, modal_serializer_id = self.wait_for_modal_dialog(modal_serializer_id)

        # Change email, url, uuid, number, datetime, date and time fields to throw errors
        dialog.find_element_by_name("email_field").send_keys("Test error")
        dialog.find_element_by_name("url_field").send_keys("Test error")
        dialog.find_element_by_name("uuid_field").send_keys("Test error")
        dialog.find_element_by_name("integer_field").send_keys("Test error")
        if self.selected_browser in (Browsers.CHROME, Browsers.OPERA):
            dialog.find_element_by_name("datetime_field").send_keys("1111111111")
            dialog.find_element_by_name("date_field").send_keys("1111111111")
            dialog.find_element_by_name("time_field").send_keys(Keys.DELETE)
        elif self.selected_browser == Browsers.EDGE:
            self.update_edge_field(self.get_field_id_by_name(dialog, "datetime_field"), "1111111111")
            self.update_edge_field(self.get_field_id_by_name(dialog, "date_field"), "1111111111")
            self.update_edge_field(self.get_field_id_by_name(dialog, "time_field"), "1111111111")
        elif self.selected_browser == Browsers.IE:
            dialog.find_element_by_name("datetime_field").clear()
            dialog.find_element_by_name("date_field").clear()
            dialog.find_element_by_name("time_field").clear()
        else:
            dialog.find_element_by_name("datetime_field").send_keys("Test error")
            dialog.find_element_by_name("date_field").send_keys("Test error")
            dialog.find_element_by_name("time_field").send_keys("Test error")

        # Submit
        dialog.find_element_by_id(save_button_prefix + modal_serializer_id).click()
        if renderer == 'html':
            self.wait_for_modal_dialog_disapear(modal_serializer_id)

            # Check for errors
            dialog, modal_serializer_id = self.wait_for_modal_dialog(modal_serializer_id)

        tim = time.time()
        while True:
            errors = dialog.find_elements_by_class_name("invalid-feedback")
            # Bootstrap v3
            if not errors:
                errors = dialog.find_elements_by_class_name("help-block")
            # jQueryUI
            if not errors:
                errors = dialog.find_elements_by_class_name("ui-error-span")

            if errors or renderer != 'component' or time.time() > tim + MAX_WAIT:
                break

            time.sleep(0.01)

        self.assertEqual(len(errors), 7)
        self.assertEqual(errors[0].get_attribute("innerHTML"), "Enter a valid email address.")
        self.assertEqual(errors[1].get_attribute("innerHTML"), "Enter a valid URL.")
        self.assertIn(errors[2].get_attribute("innerHTML"),
                      ("Must be a valid UUID.", '"123e4567-e89b-12d3-a456-426655440000Test error" is not a valid UUID.',
                       '"Test error" is not a valid UUID.')
                      )
        self.assertEqual(errors[3].get_attribute("innerHTML"), "A valid integer is required.")
        self.assertEqual(errors[4].get_attribute("innerHTML"),
                         "Datetime has wrong format. Use one of these formats instead: YYYY-MM-DDThh:mm[:ss[.uuuuuu]]"
                         "[+HH:MM|-HH:MM|Z].")
        self.assertIn(errors[5].get_attribute("innerHTML"),
                      ("Date has wrong format. Use one of these formats instead: YYYY-MM-DD.",
                       "Date has wrong format. Use one of these formats instead: YYYY[-MM[-DD]].",)
                      )
        self.assertEqual(errors[6].get_attribute("innerHTML"),
                         "Time has wrong format. Use one of these formats instead: hh:mm[:ss[.uuuuuu]].")
