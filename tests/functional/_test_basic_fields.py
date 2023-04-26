import time

from parameterized import parameterized
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from .selenium_test_case import Browsers, MAX_WAIT, WaitingStaticLiveServerTestCase


class BasicFieldsTest(WaitingStaticLiveServerTestCase):
    @parameterized.expand(["html", "component"])
    def test_basic_fields(self, renderer):
        self.browser.get(self.live_server_url + "/basic-fields." + renderer)
        # Go to basic-fields html and check if there's a "Add" button

        header = self.find_element_by_classes(("card-header", "panel-heading", "ui-accordion-header"))
        add_btn = header.find_element(By.NAME, "btn-add")
        md_btn = header.find_element(By.NAME, "btn-modal_dialog")
        self.assertEqual(self.get_element_text(add_btn), "Add")

        # Check if there's a "no data" table row
        rows = self.get_table_body()
        self.assertEqual(len(rows), 1)
        self.assertEqual(self.get_element_text(rows[0].find_element(By.TAG_NAME, "td")), "No data")

        # ---------------------------------------------------------------------------------------------------------#
        # Following a test for modal dialog... we could also do a test for page-editing (not with dialog)          #
        # ---------------------------------------------------------------------------------------------------------#

        if renderer == "html":
            md_btn.click()
            dialog, modal_serializer_id = self.wait_for_modal_dialog()
            dialog.find_element(By.ID, "dlg-btn-ok").click()
            alert = self.browser.switch_to.alert
            self.assertEqual(alert.text, "Clicked OK button")
            alert.accept()
            self.wait_for_modal_dialog_disapear(modal_serializer_id)

        # Add a new record via the "Add" button and go back to model_single.html to check if the record had been added
        add_btn.click()
        dialog, modal_serializer_id = self.wait_for_modal_dialog()
        time.sleep(1)

        # check if all fields are in the dialog and no excessive fields too
        field_count = 0

        form = dialog.find_element(By.ID, modal_serializer_id)
        containers = form.find_elements(By.XPATH, '//div[starts-with(@id, "container-")]')
        for container in containers:
            container_id = container.get_attribute("id")
            if container_id.startswith("container-"):
                field_id = container_id.split("-", 1)[1]
                label = container.find_element(By.ID, "label-" + field_id)
                field = container.find_element(By.ID, field_id)

                field_count += 1
                label_text = self.get_element_text(label)

                if label_text == "Boolean field":
                    self.initial_check(field, "", "boolean_field", "checkbox")
                    self.assertTrue("form-check-input" in field.get_attribute("class"))
                    field.click()
                elif label_text == "Nullboolean field":
                    field_type = self.initial_check(field, "", "nullboolean_field", ("text", "checkbox"))
                    if field_type == "checkbox":
                        self.assertTrue("form-check-input" in field.get_attribute("class"))
                        field.click()
                    else:
                        field.send_keys("True")
                elif label_text == "Char field":
                    self.initial_check(field, "", "char_field", "text")
                    field.send_keys("Test")
                elif label_text == "Email field":
                    self.initial_check(field, "", "email_field", "email")
                    field.send_keys("test@test.com")
                elif label_text == "Slug field":
                    self.initial_check(field, "", "slug_field", "text")
                    field.send_keys("test-slug")
                elif label_text == "Url field":
                    self.initial_check(field, "", "url_field", "url")
                    field.send_keys("http://test.test")
                elif label_text == "Uuid field":
                    self.initial_check(field, "", "uuid_field", "text")
                    field.send_keys("123e4567-e89b-12d3-a456-426655440000")
                elif label_text == "Ipaddress field":
                    self.initial_check(field, "", "ipaddress_field", "text")
                    field.send_keys("145.17.154.1")
                elif label_text == "Integer field":
                    self.initial_check(field, "", "integer_field", "number")
                    field.send_keys(1)
                elif label_text == "Float field":
                    self.initial_check(field, "", "float_field", "number")
                    field.send_keys(15)
                elif label_text == "Decimal field":
                    self.initial_check(field, "", "decimal_field", "text")
                    field.send_keys("15.18")
                elif label_text == "Datetime field":
                    _field = field if renderer == "html" else field.find_element(by=By.TAG_NAME, value="input")
                    self.initial_check(
                        _field, "", "datetime_field" if renderer == "html" else "", ("datetime-local", "text")
                    )
                    if renderer == "html":
                        # datetime UI not supported
                        continue
                        if self.selected_browser in (Browsers.CHROME, Browsers.OPERA):
                            _field.send_keys("08122018")
                            _field.send_keys(Keys.TAB)
                            _field.send_keys("081500")
                            if self.github_actions:
                                _field.send_keys("AM")
                        elif self.selected_browser == Browsers.EDGE:
                            # There is a bug when sending keys to EDGE.
                            # https://stackoverflow.com/questions/38747126/selecting-calendar-control-in-edge-using-selenium
                            # Workaround is to do this with javascript using execute_script method
                            self.update_edge_field(field_id, "2018-12-08T08:15")
                        elif self.selected_browser == Browsers.FIREFOX:
                            _field.send_keys("08/12/2018")
                            _field.send_keys(Keys.TAB)
                            _field.send_keys("08:15")
                        else:
                            _field.send_keys("2018-12-08 08:15:00")
                    elif renderer == "component":
                        _field.click()
                        self.browser.find_element(
                            by=By.CLASS_NAME, value="vdatetime-popup__actions__button--confirm"
                        ).click()
                        time.sleep(0.5)
                        self.browser.find_element(
                            by=By.CLASS_NAME, value="vdatetime-popup__actions__button--confirm"
                        ).click()
                elif label_text == "Date field":
                    _field = field if renderer == "html" else field.find_element(by=By.TAG_NAME, value="input")
                    self.initial_check(
                        _field,
                        "",
                        "date_field" if renderer == "html" else "",
                        ("date", "text")
                        if self.selected_browser in (Browsers.IE, Browsers.SAFARI) or renderer == "component"
                        else "date",
                    )
                    if renderer == "html":
                        if self.selected_browser in (Browsers.CHROME, Browsers.OPERA):
                            _field.send_keys("08122018")
                        elif self.selected_browser == Browsers.EDGE:
                            _field.send_keys(Keys.ENTER)
                        else:
                            _field.send_keys("2018-12-08")
                    elif renderer == "component":
                        _field.click()
                        self.browser.find_element(
                            by=By.CLASS_NAME, value="vdatetime-popup__actions__button--confirm"
                        ).click()
                elif label_text == "Time field":
                    _field = field if renderer == "html" else field.find_element(by=By.TAG_NAME, value="input")
                    self.initial_check(
                        _field,
                        "",
                        "time_field" if renderer == "html" else "",
                        ("time", "text")
                        if self.selected_browser in (Browsers.IE, Browsers.SAFARI) or renderer == "component"
                        else "time",
                    )
                    if renderer == "html":
                        if self.selected_browser in (Browsers.CHROME, Browsers.OPERA):
                            _field.send_keys("081500")
                            if self.github_actions:
                                _field.send_keys("AM")
                        elif self.selected_browser == Browsers.EDGE:
                            _field.send_keys(Keys.ENTER)
                        else:
                            _field.send_keys("08:15:00")
                    elif renderer == "component":
                        _field.click()
                        self.browser.find_element(
                            by=By.CLASS_NAME, value="vdatetime-popup__actions__button--confirm"
                        ).click()
                elif label_text == "Duration field":
                    self.initial_check(field, "", "duration_field", "text")
                    field.send_keys("180")
                elif label_text == "Password field":
                    self.initial_check(field, "", "password_field", "password")
                    field.send_keys("password")
                    id_attr = field.get_attribute("id")
                    container.find_element(By.ID, "pwf-" + id_attr).click()
                    self.assertEqual("text", field.get_attribute("type"))
                else:
                    field_count -= 1

        self.assertEqual(field_count, 16)

        save_button_prefix = "save-" if renderer == "html" else "submit-"
        dialog.find_element(By.ID, save_button_prefix + modal_serializer_id).click()
        self.wait_for_modal_dialog_disapear(modal_serializer_id)
        time.sleep(1)  # Zato, da se lahko tabela osveži
        rows = self.get_table_body(expected_rows=1)
        self.assertEqual(len(rows), 1)
        cells = rows[0].find_elements(By.TAG_NAME, "td")
        self.assertEqual(len(cells), 18)
        # Then we click the record row to edit it. Go back to model_single.html and check if it had been edited
        cells[0].click()
        dialog, modal_serializer_id = self.wait_for_modal_dialog(modal_serializer_id)

        # Change email, url, uuid, number, datetime, date and time fields to throw errors
        dialog.find_element(By.NAME, "email_field").send_keys("Test error")
        dialog.find_element(By.NAME, "url_field").send_keys("Test error")
        dialog.find_element(By.NAME, "uuid_field").send_keys("Test error")
        dialog.find_element(By.NAME, "integer_field").send_keys("Test error")
        if self.selected_browser in (Browsers.CHROME, Browsers.OPERA):
            dialog.find_element(By.NAME, "datetime_field").send_keys("1111111111")
            dialog.find_element(By.NAME, "date_field").send_keys("1111111111")
            dialog.find_element(By.NAME, "time_field").send_keys(Keys.DELETE)
        elif self.selected_browser == Browsers.EDGE:
            self.update_edge_field(self.get_field_id_by_name(dialog, "datetime_field"), "1111111111")
            self.update_edge_field(self.get_field_id_by_name(dialog, "date_field"), "1111111111")
            self.update_edge_field(self.get_field_id_by_name(dialog, "time_field"), "1111111111")
        elif self.selected_browser in (Browsers.IE, Browsers.FIREFOX):
            # dt_field = dialog.find_element(By.NAME, "datetime_field")
            # dt_field.send_keys('09/1/2017')
            # dt_field.send_keys(Keys.TAB)
            # dt_field.send_keys('07:14')
            # self.clear_input(dt_field)
            # dt_field.send_keys(Keys.TAB)
            # self.clear_input(dt_field)
            # dt_field.send_keys(Keys.TAB)
            # self.clear_input(dt_field)
            # dt_field.send_keys(Keys.TAB)
            # self.clear_input(dt_field)
            # dt_field.send_keys(Keys.TAB)
            # self.clear_input(dt_field)
            date_field = dialog.find_element(By.NAME, "date_field")
            time_field = dialog.find_element(By.NAME, "time_field")
            if renderer == "component":
                date_field.find_element(By.CLASS_NAME, "clear-datetime").click()
                time_field.find_element(By.CLASS_NAME, "clear-datetime").click()
            else:
                self.clear_input(date_field)
                self.clear_input(time_field)
        else:
            dialog.find_element(By.NAME, "datetime_field").send_keys("Test error")
            dialog.find_element(By.NAME, "date_field").send_keys("Test error")
            dialog.find_element(By.NAME, "time_field").send_keys("Test error")

        # Submit
        dialog.find_element(By.ID, save_button_prefix + modal_serializer_id).click()
        if renderer == "html":
            self.wait_for_modal_dialog_disapear(modal_serializer_id)

            # Check for errors
            dialog, modal_serializer_id = self.wait_for_modal_dialog(modal_serializer_id)

        tim = time.time()
        while True:
            errors = dialog.find_elements(By.CLASS_NAME, "invalid-feedback")
            # Bootstrap v3
            if not errors:
                errors = dialog.find_elements(By.CLASS_NAME, "help-block")
            # jQueryUI
            if not errors:
                errors = dialog.find_elements(By.CLASS_NAME, "ui-error-span")

            if errors or renderer != "component" or time.time() > tim + MAX_WAIT:
                break

            time.sleep(0.01)

        self.assertEqual(len(errors), 6)
        self.assertEqual(errors[0].get_attribute("innerHTML"), "Enter a valid email address.")
        self.assertEqual(errors[1].get_attribute("innerHTML"), "Enter a valid URL.")
        self.assertIn(
            errors[2].get_attribute("innerHTML"),
            (
                "Must be a valid UUID.",
                '"123e4567-e89b-12d3-a456-426655440000Test error" is not a valid UUID.',
                '"Test error" is not a valid UUID.',
            ),
        )
        self.assertEqual(errors[3].get_attribute("innerHTML"), "A valid integer is required.")
        # self.assertEqual(errors[4].get_attribute("innerHTML"),
        #                  "Datetime has wrong format. Use one of these formats instead: YYYY-MM-DDThh:mm[:ss[.uuuuuu]]"
        #                  "[+HH:MM|-HH:MM|Z].")

        # reindexed error messages because of datetime field temporary suspension

        self.assertIn(
            errors[4].get_attribute("innerHTML"),
            (
                "Date has wrong format. Use one of these formats instead: YYYY-MM-DD.",
                "Date has wrong format. Use one of these formats instead: YYYY[-MM[-DD]].",
            ),
        )
        self.assertEqual(
            errors[5].get_attribute("innerHTML"),
            "Time has wrong format. Use one of these formats instead: hh:mm[:ss[.uuuuuu]].",
        )
