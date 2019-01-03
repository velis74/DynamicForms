import os
import time

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.common.exceptions import ElementNotInteractableException, NoSuchElementException, WebDriverException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select

MAX_WAIT = 10


class ValidatedFormTest(StaticLiveServerTestCase):
    def setUp(self):
        self.browser = webdriver.Firefox()
        staging_server = os.environ.get('STAGING_SERVER')
        # print(self.live_server_url)
        if staging_server:
            # print('\n\nSTAGING SERVER\n\n')
            self.live_server_url = 'http://' + staging_server
        # print(self.live_server_url)

    def tearDown(self):
        self.browser.refresh()
        self.browser.quit()
        pass

    def wait_for_new_element(self, element_id):
        start_time = time.time()
        while True:
            try:
                time.sleep(0.5)
                element = self.browser.find_element_by_id(element_id)
                self.assertTrue(element is not None)
                return
            except (AssertionError, WebDriverException) as e:
                if time.time() - start_time > MAX_WAIT:
                    raise e

    def wait_for_modal_dialog(self, old_id=None):
        start_time = time.time()
        while True:
            try:
                time.sleep(0.5)
                element = self.browser.find_element_by_class_name("modal")
                self.assertTrue(element is not None)
                element_id = element.get_attribute("id")
                if old_id:
                    self.assertFalse(element_id == "dialog-{old_id}".format(**locals()))
                self.assertTrue(element_id.startswith("dialog-"))
                element_id = element_id.split("-", 1)[1]
                return element, element_id
            except (AssertionError, WebDriverException) as e:
                if time.time() - start_time > MAX_WAIT:
                    raise e

    def wait_for_modal_dialog_disapear(self, dialog_id):
        start_time = time.time()
        while True:
            try:
                time.sleep(0.5)
                if self.browser.find_element_by_id("dialog-{dialog_id}".format(**locals())) is not None:
                    break
                self.assertFalse(time.time() - start_time > MAX_WAIT)
            except WebDriverException:
                break

    # noinspection PyMethodMayBeStatic
    def check_error_text(self, dialog):
        error_text = None
        try:
            error = dialog.find_element_by_class_name("text-danger")
            if error is not None:
                error_text = error.get_attribute("innerHTML")
        except WebDriverException:
            pass
        return error_text

    def get_table_body(self):
        try:
            body = self.browser.find_element_by_class_name("card-body")
        except NoSuchElementException:
            # Bootstrap 3
            body = self.browser.find_element_by_class_name("panel-body")

        table = body.find_element_by_tag_name("table")

        tbody = table.find_element_by_tag_name("tbody")
        return tbody.find_elements_by_tag_name("tr")

    def initial_check(self, field, fld_text, fld_name, fld_type):
        self.assertEqual(field.text, fld_text)
        self.assertEqual(field.get_attribute("name"), fld_name)
        self.assertEqual(field.get_attribute("type"), fld_type)

    def check_row(self, row, cell_cnt, cell_values):
        cells = row.find_elements_by_tag_name("td")
        self.assertEqual(len(cells), cell_cnt)
        for i in range(len(cell_values)):
            if cell_values[i] is not None:
                self.assertTrue(cells[i], cell_values[i])
        return cells

    def select_option_for_select2(self, driver, id, text=None):
        element = driver.find_element_by_xpath("//*[@id='{id}']/following-sibling::*[1]".format(**locals()))
        element.click()

        if text:
            element = driver.find_element_by_xpath("//input[@type='search']")
            element.send_keys(text)

        try:
            element.send_keys(Keys.ENTER)
        except ElementNotInteractableException:
            actions = ActionChains(driver)
            a = actions.move_to_element_with_offset(element, 50, 30)
            a.send_keys(Keys.ENTER)
            a.perform()

    def test_validated_list(self):
        self.browser.get(self.live_server_url + '/validated.html')
        # Go to validated html and check if there's a "+ Add" button

        try:
            header = self.browser.find_element_by_class_name('card-header')
        except NoSuchElementException:
            # Bootstrap v3
            header = self.browser.find_element_by_class_name('panel-heading')

        add_btn = header.find_element_by_class_name('btn')
        self.assertEqual(add_btn.text, '+ Add')

        # Check if there's a "no data" table row
        rows = self.get_table_body()
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0].find_element_by_tag_name('td').text, 'No data')

        # ---------------------------------------------------------------------------------------------------------#
        # Following a test for modal dialog... we could also do a test for page-editing (not with dialog)          #
        # ---------------------------------------------------------------------------------------------------------#

        # Add a new record via the "+ Add" button and go back to model_single.html to check if the record had been added
        add_btn.click()
        dialog, modal_serializer_id = self.wait_for_modal_dialog()

        # check if all fields are in the dialog and no excessive fields too
        field_count = 0
        self.assertIsNone(self.check_error_text(dialog))

        form = dialog.find_element_by_id(modal_serializer_id)
        containers = form.find_elements_by_tag_name("div")
        for container in containers:
            container_id = container.get_attribute("id")
            if container_id.startswith("container-"):
                field_id = container_id.split('-', 1)[1]
                label = container.find_element_by_id("label-" + field_id)
                field = container.find_element_by_id(field_id)

                field_count += 1
                if label.text == "Code":
                    self.initial_check(field, "", "code", "text")
                    field.send_keys("12345")
                elif label.text == "Enabled":
                    self.initial_check(field, "", "enabled", "checkbox")
                    field.click()
                elif label.text == "Amount":
                    self.initial_check(field, "", "amount", "number")
                    field.send_keys("3")
                elif label.text == "Item type":
                    # Check if item_type field is select2 element
                    try:
                        select2 = container.find_element_by_class_name("select2-field")
                    except NoSuchElementException:
                        select2 = None

                    if select2:
                        initial_choice = container.find_element_by_class_name("select2-selection__rendered")
                        self.assertEqual(initial_choice.text, "Choice 1")

                        select2_options = select2.find_elements_by_tag_name("option")
                        self.assertEqual(len(select2_options), 4)
                        self.assertEqual(select2.get_attribute("name"), "item_type")
                        self.assertEqual(select2.tag_name, "select")
                        self.select_option_for_select2(container, field_id, text="Choice 4")
                    else:
                        select = Select(field)
                        selected_options = select.all_selected_options
                        self.assertEqual(len(selected_options), 1)
                        self.assertEqual(selected_options[0].get_attribute("index"), "0")
                        self.assertEqual(selected_options[0].text, "Choice 1")
                        self.assertEqual(field.get_attribute("name"), "item_type")
                        self.assertEqual(field.tag_name, "select")
                        select.select_by_index(3)
                elif label.text == "Item flags":
                    # Check if item_flags field is select2 element
                    try:
                        select2 = container.find_element_by_class_name("select2-field")
                    except NoSuchElementException:
                        select2 = None

                    if select2:
                        empty_choice = container.find_element_by_class_name("select2-selection__rendered")
                        self.assertTrue(empty_choice.text == "--------")

                        select2_options = select2.find_elements_by_tag_name("option")
                        self.assertTrue(len(select2_options) == 5)
                        self.assertTrue(select2.get_attribute("name") == "item_flags")
                        self.assertTrue(select2.tag_name == "select")
                        self.select_option_for_select2(container, field_id, text="C")
                    else:
                        select = Select(field)
                        selected_options = select.all_selected_options
                        self.assertTrue(len(selected_options) == 1)
                        self.assertTrue(selected_options[0].get_attribute("index") == "0")
                        self.assertTrue(selected_options[0].text == "--------")
                        self.assertTrue(field.get_attribute("name") == "item_flags")
                        self.assertTrue(field.tag_name == "select")
                        select.select_by_index(3)
                elif field.get_attribute("name") in ('id',):
                    # Hidden fields
                    pass
                else:
                    field_count -= 1
                    check = label.text == "Code"
                    fname = field.get_attribute("name")
                    self.assertTrue(
                        False, "Wrong field container - label: '{label.text}' {check} {fname}".format(**locals())
                    )
        self.assertEqual(field_count, 6)
        dialog.find_element_by_id("save-" + modal_serializer_id).click()

        # There should be an error because of validator set in Model
        dialog, modal_serializer_id = self.wait_for_modal_dialog(modal_serializer_id)

        errors = dialog.find_elements_by_class_name("invalid-feedback")
        # Bootstrap v3
        if not errors:
            errors = dialog.find_elements_by_class_name("help-block")

        self.assertTrue(len(errors) == 1)
        self.assertTrue(errors[0].get_attribute("innerHTML") == "Ensure this value is greater than or equal to 5.")
        field = errors[0].parent.find_element_by_name("amount")
        field.clear()
        field.send_keys("8")
        dialog.find_element_by_id("save-" + modal_serializer_id).click()

        # There should be a field error because of validator set in serializer

        dialog, modal_serializer_id = self.wait_for_modal_dialog(modal_serializer_id)

        errors = dialog.find_elements_by_class_name("invalid-feedback")
        # Bootstrap v3
        if not errors:
            errors = dialog.find_elements_by_class_name("help-block")

        self.assertTrue(len(errors) == 1)
        self.assertTrue(errors[0].get_attribute("innerHTML") == 'amount can only be different than 5 if code is "123"')
        field = errors[0].parent.find_element_by_name("code")
        field.clear()
        field.send_keys("123")
        dialog.find_element_by_id("save-" + modal_serializer_id).click()

        # There should be a general/form error because of validator set in serializer
        dialog, modal_serializer_id = self.wait_for_modal_dialog(modal_serializer_id)
        self.assertTrue(self.check_error_text(dialog) == "When enabled you can only choose from first three item types")

        # Check if item_type field is select2 element
        form = dialog.find_element_by_id(modal_serializer_id)
        try:
            select2_elements = form.find_elements_by_class_name("select2-field")
        except NoSuchElementException:
            select2_elements = None

        if select2_elements:
            select2_element_id = select2_elements[0].get_attribute("id")
            self.select_option_for_select2(select2_elements[0], select2_element_id, text="Choice 3")
        else:
            Select(dialog.find_element_by_name("item_type")).select_by_index(2)

        dialog.find_element_by_id("save-" + modal_serializer_id).click()
        self.wait_for_modal_dialog_disapear(modal_serializer_id)

        # TODO: remove following line when task for auto refresh is done.
        self.browser.refresh()
        # check if record was stored
        rows = self.get_table_body()
        self.assertTrue(len(rows) == 1)
        cells = rows[0].find_elements_by_tag_name("td")
        self.assertTrue(len(cells) == 7)

        # Then we click the record row to edit it. Go back to model_single.html and check if it had been edited
        cells[0].click()
        dialog, modal_serializer_id = self.wait_for_modal_dialog(modal_serializer_id)
        dialog.find_element_by_name("enabled").click()
        dialog.find_element_by_id("save-" + modal_serializer_id).click()
        self.wait_for_modal_dialog_disapear(modal_serializer_id)

        # TODO: remove following line when task for auto refresh is done.
        self.browser.refresh()
        rows = self.get_table_body()
        self.assertTrue(len(rows) == 1)
        cells = self.check_row(rows[0], 7, ["1", "123", "false", "8", "2", "", None])

        # Once more to editing and cancel it
        cells[0].click()
        dialog, modal_serializer_id = self.wait_for_modal_dialog(modal_serializer_id)

        # Check if item_type field is select2 element
        form = dialog.find_element_by_id(modal_serializer_id)
        try:
            select2_elements = form.find_elements_by_class_name("select2-field")
        except NoSuchElementException:
            select2_elements = None

        if select2_elements:
            select2_element_id = select2_elements[1].get_attribute("id")
            self.select_option_for_select2(select2_elements[1], select2_element_id, text="Choice 3")
        else:
            Select(dialog.find_element_by_name("item_type")).select_by_index(2)

        dialog.find_element_by_css_selector("[data-dismiss=modal]").click()

        # TODO: remove following line when task for auto refresh is done.
        self.browser.refresh()
        rows = self.get_table_body()
        self.assertEqual(len(rows), 1)
        self.check_row(rows[0], 7, ["1", "123", "false", "8", "2", "", None])

        # we delete the row we created
        del_btn = rows[0].find_elements_by_tag_name('td')[6].find_element_by_class_name('btn')
        del_btn.click()

        # TODO: remove following line when task for auto refresh is done.
        self.browser.refresh()
        rows = self.get_table_body()
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0].find_element_by_tag_name('td').text, 'No data')


class BasicFieldsTest(StaticLiveServerTestCase):
    def setUp(self):
        self.browser = webdriver.Firefox()
        staging_server = os.environ.get('STAGING_SERVER')
        # print(self.live_server_url)
        if staging_server:
            # print('\n\nSTAGING SERVER\n\n')
            self.live_server_url = 'http://' + staging_server
        # print(self.live_server_url)

    def tearDown(self):
        self.browser.refresh()
        self.browser.quit()
        pass

    def wait_for_modal_dialog(self, old_id=None):
        start_time = time.time()
        while True:
            try:
                time.sleep(0.5)
                element = self.browser.find_element_by_class_name("modal")
                self.assertTrue(element is not None)
                element_id = element.get_attribute("id")
                if old_id:
                    self.assertFalse(element_id == "dialog-{old_id}".format(**locals()))
                self.assertTrue(element_id.startswith("dialog-"))
                element_id = element_id.split("-", 1)[1]
                return element, element_id
            except (AssertionError, WebDriverException) as e:
                if time.time() - start_time > MAX_WAIT:
                    raise e

    def wait_for_modal_dialog_disapear(self, dialog_id):
        start_time = time.time()
        while True:
            try:
                time.sleep(0.5)
                if self.browser.find_element_by_id("dialog-{dialog_id}".format(**locals())) is not None:
                    break
                self.assertFalse(time.time() - start_time > MAX_WAIT)
            except WebDriverException:
                break

    def get_table_body(self):
        try:
            body = self.browser.find_element_by_class_name("card-body")
        except NoSuchElementException:
            # Bootstrap 3
            body = self.browser.find_element_by_class_name("panel-body")

        table = body.find_element_by_tag_name("table")

        tbody = table.find_element_by_tag_name("tbody")
        return tbody.find_elements_by_tag_name("tr")

    def initial_check(self, field, fld_text, fld_name, fld_type):
        self.assertTrue(field.text == fld_text)
        self.assertTrue(field.get_attribute("name") == fld_name)
        self.assertTrue(field.get_attribute("type") == fld_type)

    def test_basic_fields(self):
        self.browser.get(self.live_server_url + '/basic-fields.html')
        # Go to basic-fields html and check if there's a "+ Add" button

        try:
            header = self.browser.find_element_by_class_name("card-header")
        except NoSuchElementException:
            # Bootstrap v3
            header = self.browser.find_element_by_class_name("panel-heading")

        add_btn = header.find_element_by_class_name("btn")
        self.assertTrue(add_btn.text == "+ Add")

        # Check if there's a "no data" table row
        rows = self.get_table_body()
        self.assertTrue(len(rows) == 1)
        self.assertTrue(rows[0].find_element_by_tag_name("td").text == "No data")

        # ---------------------------------------------------------------------------------------------------------#
        # Following a test for modal dialog... we could also do a test for page-editing (not with dialog)          #
        # ---------------------------------------------------------------------------------------------------------#

        # Add a new record via the "+ Add" button and go back to model_single.html to check if the record had been added
        add_btn.click()
        dialog, modal_serializer_id = self.wait_for_modal_dialog()

        # check if all fields are in the dialog and no excessive fields too
        field_count = 0

        form = dialog.find_element_by_id(modal_serializer_id)
        containers = form.find_elements_by_tag_name("div")
        for container in containers:
            container_id = container.get_attribute("id")
            if container_id.startswith("container-"):
                field_id = container_id.split('-', 1)[1]
                label = container.find_element_by_id("label-" + field_id)
                field = container.find_element_by_id(field_id)

                field_count += 1

                if label.text == "Boolean field":
                    self.initial_check(field, "", "boolean_field", "checkbox")
                    field.click()
                elif label.text == "Nullboolean field":
                    self.initial_check(field, "", "nullboolean_field", "text")
                    field.send_keys("True")
                elif label.text == "Char field":
                    self.initial_check(field, "", "char_field", "text")
                    field.send_keys("Test")
                elif label.text == "Email field":
                    self.initial_check(field, "", "email_field", "email")
                    field.send_keys("test@test.com")
                elif label.text == "Slug field":
                    self.initial_check(field, "", "slug_field", "text")
                    field.send_keys("test-slug")
                elif label.text == "Url field":
                    self.initial_check(field, "", "url_field", "url")
                    field.send_keys("http://test.test")
                elif label.text == "Uuid field":
                    self.initial_check(field, "", "uuid_field", "text")
                    field.send_keys("123e4567-e89b-12d3-a456-426655440000")
                elif label.text == "Ipaddress field":
                    self.initial_check(field, "", "ipaddress_field", "text")
                    field.send_keys("145.17.154.1")
                elif label.text == "Integer field":
                    self.initial_check(field, "", "integer_field", "number")
                    field.send_keys(1)
                elif label.text == "Float field":
                    self.initial_check(field, "", "float_field", "number")
                    field.send_keys(15)
                elif label.text == "Decimal field":
                    self.initial_check(field, "", "decimal_field", "text")
                    field.send_keys("15.18")
                elif label.text == "Datetime field":
                    self.initial_check(field, "", "datetime_field", "text")
                    field.send_keys("2018-12-08 08:15:00")
                elif label.text == "Date field":
                    self.initial_check(field, "", "date_field", "date")
                    field.send_keys("2018-12-08")
                elif label.text == "Time field":
                    self.initial_check(field, "", "time_field", "time")
                    field.send_keys("08:15:00")
                elif label.text == "Duration field":
                    self.initial_check(field, "", "duration_field", "text")
                    field.send_keys("180")
                else:
                    field_count -= 1

        self.assertEqual(field_count, 15)
        dialog.find_element_by_id("save-" + modal_serializer_id).click()
        self.wait_for_modal_dialog_disapear(modal_serializer_id)

        # TODO: remove following line when task for auto refresh is done.
        self.browser.refresh()
        rows = self.get_table_body()
        self.assertTrue(len(rows) == 1)
        cells = rows[0].find_elements_by_tag_name("td")
        self.assertTrue(len(cells) == 17)

        # Then we click the record row to edit it. Go back to model_single.html and check if it had been edited
        cells[0].click()
        dialog, modal_serializer_id = self.wait_for_modal_dialog(modal_serializer_id)

        # Change email, url, uuid, number, datetime, date and time fields to throw errors
        dialog.find_element_by_name("email_field").send_keys("Test error")
        dialog.find_element_by_name("url_field").send_keys("Test error")
        dialog.find_element_by_name("uuid_field").send_keys("Test error")
        dialog.find_element_by_name("integer_field").send_keys("Test error")
        dialog.find_element_by_name("datetime_field").send_keys("Test error")
        dialog.find_element_by_name("date_field").send_keys("Test error")
        dialog.find_element_by_name("time_field").send_keys("Test error")

        # Submit
        dialog.find_element_by_id("save-" + modal_serializer_id).click()
        self.wait_for_modal_dialog_disapear(modal_serializer_id)

        # Check for errors
        dialog, modal_serializer_id = self.wait_for_modal_dialog(modal_serializer_id)
        errors = dialog.find_elements_by_class_name("invalid-feedback")
        # Bootstrap v3
        if not errors:
            errors = dialog.find_elements_by_class_name("help-block")
        self.assertEqual(len(errors), 7)
        self.assertEqual(errors[0].get_attribute("innerHTML"), "Enter a valid email address.")
        self.assertEqual(errors[1].get_attribute("innerHTML"), "Enter a valid URL.")
        self.assertIn(errors[2].get_attribute("innerHTML"),
                      ("Must be a valid UUID.", '"123e4567-e89b-12d3-a456-426655440000Test error" is not a valid UUID.')
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


class AdvancedFieldsTest(StaticLiveServerTestCase):
    def setUp(self):
        self.browser = webdriver.Firefox()
        staging_server = os.environ.get('STAGING_SERVER')
        # print(self.live_server_url)
        if staging_server:
            # print('\n\nSTAGING SERVER\n\n')
            self.live_server_url = 'http://' + staging_server
        # print(self.live_server_url)

    def tearDown(self):
        self.browser.refresh()
        self.browser.quit()
        pass

    def wait_for_modal_dialog(self, old_id=None):
        start_time = time.time()
        while True:
            try:
                time.sleep(0.5)
                element = self.browser.find_element_by_class_name("modal")
                self.assertTrue(element is not None)
                element_id = element.get_attribute("id")
                if old_id:
                    self.assertFalse(element_id == "dialog-{old_id}".format(**locals()))
                self.assertTrue(element_id.startswith("dialog-"))
                element_id = element_id.split("-", 1)[1]
                return element, element_id
            except (AssertionError, WebDriverException) as e:
                if time.time() - start_time > MAX_WAIT:
                    raise e

    def wait_for_modal_dialog_disapear(self, dialog_id):
        start_time = time.time()
        while True:
            try:
                time.sleep(0.5)
                if self.browser.find_element_by_id("dialog-{dialog_id}".format(**locals())) is not None:
                    break
                self.assertFalse(time.time() - start_time > MAX_WAIT)
            except WebDriverException:
                break

    def get_table_body(self):
        try:
            body = self.browser.find_element_by_class_name("card-body")
        except NoSuchElementException:
            # Bootstrap 3
            body = self.browser.find_element_by_class_name("panel-body")

        table = body.find_element_by_tag_name("table")

        tbody = table.find_element_by_tag_name("tbody")
        return tbody.find_elements_by_tag_name("tr")

    def initial_check(self, field, fld_text, fld_name, fld_type):
        self.assertTrue(field.text == fld_text)
        self.assertTrue(field.get_attribute("name") == fld_name)
        self.assertTrue(field.get_attribute("type") == fld_type)

    def check_row(self, row, cell_cnt, cell_values):
        cells = row.find_elements_by_tag_name("td")
        self.assertTrue(len(cells) == cell_cnt)
        for i in range(len(cell_values)):
            if cell_values[i] is not None:
                self.assertTrue(cells[i], cell_values[i])
        return cells

    def select_option_for_select2(self, driver, id, text=None):
        element = driver.find_element_by_xpath("//*[@id='{id}']/following-sibling::*[1]".format(**locals()))
        element.click()

        if text:
            element = driver.find_element_by_xpath("//input[@type='search']")
            element.send_keys(text)

        try:
            element.send_keys(Keys.ENTER)
        except ElementNotInteractableException:
            actions = ActionChains(driver)
            a = actions.move_to_element_with_offset(element, 50, 30)
            a.send_keys(Keys.ENTER)
            a.perform()

    def test_advanced_fields(self):
        self.browser.get(self.live_server_url + '/advanced-fields.html')
        # Go to advanced-fields html and check if there's a "+ Add" button

        try:
            header = self.browser.find_element_by_class_name("card-header")
        except NoSuchElementException:
            # Bootstrap v3
            header = self.browser.find_element_by_class_name("panel-heading")

        add_btn = header.find_element_by_class_name("btn")
        self.assertTrue(add_btn.text == "+ Add")

        # Check if there's a "no data" table row
        rows = self.get_table_body()
        self.assertTrue(len(rows) == 1)
        self.assertTrue(rows[0].find_element_by_tag_name("td").text == "No data")

        # ---------------------------------------------------------------------------------------------------------#
        # Following a test for modal dialog... we could also do a test for page-editing (not with dialog)          #
        # ---------------------------------------------------------------------------------------------------------#

        # Add a new record via the "+ Add" button and go back to model_single.html to check if the record had been added
        add_btn.click()
        dialog, modal_serializer_id = self.wait_for_modal_dialog()

        # check if all fields are in the dialog and no excessive fields too
        field_count = 0

        form = dialog.find_element_by_id(modal_serializer_id)
        containers = form.find_elements_by_tag_name("div")
        for container in containers:
            container_id = container.get_attribute("id")
            if container_id.startswith("container-"):
                field_id = container_id.split('-', 1)[1]
                label = container.find_element_by_id("label-" + field_id)
                field = container.find_element_by_id(field_id)

                field_count += 1

                if label.text == "Regex field":
                    self.initial_check(field, "", "regex_field", "text")
                    field.send_keys("abcdef")
                elif label.text == "Choice field":
                    # Check if choice_field field is select2 element
                    try:
                        select2 = container.find_element_by_class_name("select2-field")
                    except NoSuchElementException:
                        select2 = None

                    if select2:
                        initial_choice = container.find_element_by_class_name("select2-selection__rendered")
                        self.assertTrue(initial_choice.text == "Choice 1")

                        select2_options = select2.find_elements_by_tag_name("option")
                        self.assertTrue(len(select2_options) == 4)
                        self.assertTrue(select2.get_attribute("name") == "choice_field")
                        self.assertTrue(select2.tag_name == "select")
                        self.select_option_for_select2(container, field_id, text="Choice 4")
                    else:
                        select = Select(field)
                        selected_options = select.all_selected_options
                        self.assertTrue(len(selected_options) == 1)
                        self.assertTrue(selected_options[0].get_attribute("index") == "0")
                        self.assertTrue(selected_options[0].text == "Choice 1")
                        self.assertTrue(field.get_attribute("name") == "choice_field")
                        self.assertTrue(field.tag_name == "select")
                        select.select_by_index(3)
                elif label.text == "Readonly field":
                    self.initial_check(field, "", "readonly_field", "text")
                    self.assertTrue(field.text == "true")
                elif label.text == "Filepath field":
                    # Check if filepath_field field is select2 element
                    try:
                        select2 = container.find_element_by_class_name("select2-field")
                    except NoSuchElementException:
                        select2 = None

                    if select2:
                        initial_choice = container.find_element_by_class_name("select2-selection__rendered")
                        self.assertTrue(initial_choice.text == "---------")

                        # Checking number of items seems to yield different values for each different way of running
                        # tests (tox, manual, etc)
                        # select2_options = select2.find_elements_by_tag_name("option")
                        # self.assertEqual(len(select2_options), 8)
                        self.assertEqual(select2.get_attribute("name"), "filepath_field")
                        self.assertEqual(select2.tag_name, "select")
                        self.select_option_for_select2(container, field_id, text="admin.py")
                    else:
                        select = Select(field)
                        selected_options = select.all_selected_options
                        self.assertEqual(len(selected_options), 1)
                        self.assertEqual(selected_options[0].get_attribute("index"), "0")
                        self.assertEqual(selected_options[0].text, "---------")
                        self.assertEqual(field.get_attribute("name"), "filepath_field")
                        self.assertEqual(field.tag_name, "select")
                        select.select_by_index(3)
                # Hidden field is not shown in dialog
                elif label.text == "Primary key related field":
                    # Check if primary_key_related_field field is select2 element
                    try:
                        select2 = container.find_element_by_class_name("select2-field")
                    except NoSuchElementException:
                        select2 = None

                    if select2:
                        initial_choice = container.find_element_by_class_name("select2-selection__rendered")
                        self.assertTrue(initial_choice.text == "Relation object 1")

                        select2_options = select2.find_elements_by_tag_name("option")
                        self.assertTrue(len(select2_options) == 10)
                        self.assertTrue(select2.get_attribute("name") == "primary_key_related_field")
                        self.assertTrue(select2.tag_name == "select")
                        self.select_option_for_select2(container, field_id, text="Relation object 7")
                    else:
                        select = Select(field)
                        selected_options = select.all_selected_options
                        self.assertTrue(len(selected_options) == 1)
                        self.assertTrue(selected_options[0].get_attribute("index") == "0")
                        self.assertTrue(selected_options[0].text == "Relation object 1")
                        self.assertTrue(field.get_attribute("name") == "primary_key_related_field")
                        self.assertTrue(field.tag_name == "select")
                        select.select_by_index(6)
                elif label.text == "Slug related field":
                    # Check if slug_related_field field is select2 element
                    try:
                        select2 = container.find_element_by_class_name("select2-field")
                    except NoSuchElementException:
                        select2 = None

                    if select2:
                        initial_choice = container.find_element_by_class_name("select2-selection__rendered")
                        self.assertTrue(initial_choice.text == "Relation object 1")

                        select2_options = select2.find_elements_by_tag_name("option")
                        self.assertTrue(len(select2_options) == 10)
                        self.assertTrue(select2.get_attribute("name") == "slug_related_field")
                        self.assertTrue(select2.tag_name == "select")
                        self.select_option_for_select2(container, field_id, text="Relation object 5")
                    else:
                        select = Select(field)
                        selected_options = select.all_selected_options
                        self.assertTrue(len(selected_options) == 1)
                        self.assertTrue(selected_options[0].get_attribute("index") == "0")
                        self.assertTrue(selected_options[0].text == "Relation object 1")
                        self.assertTrue(field.get_attribute("name") == "slug_related_field")
                        self.assertTrue(field.tag_name == "select")
                        select.select_by_index(4)
                # StringRelatedField is read only with primary_key_related_field as source and is not shown in dialog
                else:
                    field_count -= 1

        self.assertEqual(field_count, 5)
        dialog.find_element_by_id("save-" + modal_serializer_id).click()
        self.wait_for_modal_dialog_disapear(modal_serializer_id)

        # TODO: remove following line when task for auto refresh is done.
        self.browser.refresh()
        rows = self.get_table_body()
        self.assertTrue(len(rows) == 1)
        cells = rows[0].find_elements_by_tag_name("td")
        self.assertTrue(len(cells) == 9)

        # Check for relations
        self.assertTrue(cells[5].text == "Relation object 7")
        self.assertTrue(cells[6].text == "Relation object 7")
        self.assertTrue(cells[7].text == "Relation object 5")

        # Then we click the record row to edit it. Go back to model_single.html and check if it had been edited
        cells[0].click()
        dialog, modal_serializer_id = self.wait_for_modal_dialog(modal_serializer_id)

        # Change choice fields
        form = dialog.find_element_by_id(modal_serializer_id)
        try:
            select2_elements = form.find_elements_by_class_name("select2-field")
        except NoSuchElementException:
            select2_elements = None

        if select2_elements:
            self.select_option_for_select2(
                select2_elements[0], select2_elements[0].get_attribute("id"), text="Choice 2"
            )
            self.select_option_for_select2(
                select2_elements[3], select2_elements[3].get_attribute("id"), text="Relation object 9"
            )
        else:
            Select(dialog.find_element_by_name("choice_field")).select_by_index(1)
            Select(dialog.find_element_by_name("primary_key_related_field")).select_by_index(8)

        # Submit
        dialog.find_element_by_id("save-" + modal_serializer_id).click()
        self.wait_for_modal_dialog_disapear(modal_serializer_id)

        # TODO: remove following line when task for auto refresh is done.
        self.browser.refresh()
        rows = self.get_table_body()
        self.assertTrue(len(rows) == 1)
        cells = rows[0].find_elements_by_tag_name("td")
        self.assertTrue(len(cells) == 9)

        # Check for changed values
        self.assertTrue(cells[2].text == "Choice 2")
        self.assertTrue(cells[5].text == "Relation object 9")
        self.assertTrue(cells[6].text == "Relation object 9")

        # Then we click the record row to edit it. Go back to model_single.html and check if it had been edited
        cells[0].click()
        dialog, modal_serializer_id = self.wait_for_modal_dialog(modal_serializer_id)

        # Change regex field to throw error
        regex_field = dialog.find_element_by_name("regex_field")
        regex_field.clear()
        regex_field.send_keys("Test error")

        # Submit
        dialog.find_element_by_id("save-" + modal_serializer_id).click()
        self.wait_for_modal_dialog_disapear(modal_serializer_id)

        # Check for errors
        dialog, modal_serializer_id = self.wait_for_modal_dialog(modal_serializer_id)
        errors = dialog.find_elements_by_class_name("invalid-feedback")
        # Bootstrap v3
        if not errors:
            errors = dialog.find_elements_by_class_name("help-block")
        self.assertEqual(len(errors), 1)
        self.assertEqual(errors[0].get_attribute("innerHTML"),
                         "This value does not match the required pattern (?&lt;=abc)def.")
