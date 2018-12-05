import os
import time

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.common.exceptions import WebDriverException, ElementNotInteractableException, NoSuchElementException
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
                    self.assertFalse(element_id == f"dialog-{old_id}")
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
                if self.browser.find_element_by_id(f"dialog-{dialog_id}") is not None:
                    break
                self.assertFalse(time.time() - start_time > MAX_WAIT)
            except WebDriverException as e:
                break

    # noinspection PyMethodMayBeStatic
    def check_error_text(self, dialog):
        error_text = None
        try:
            error = dialog.find_element_by_class_name("text-danger")
            if error is not None:
                error_text = error.get_attribute("innerHTML")
        except WebDriverException as e:
            pass
        return error_text

    def get_table_body(self):
        body = self.browser.find_element_by_class_name("card-body")
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
        element = driver.find_element_by_xpath(f"//*[@id='{id}']/following-sibling::*[1]")
        element.click()

        if text:
            element = driver.find_element_by_xpath("//input[@type='search']")
            element.send_keys(text)

        try:
            element.send_keys(Keys.ENTER)
        except ElementNotInteractableException as e:
            actions = ActionChains(driver)
            a = actions.move_to_element_with_offset(element, 50, 30)
            a.send_keys(Keys.ENTER)
            a.perform()

    def test_validated_list(self):
        self.browser.get(self.live_server_url + '/validated.html')
        # Go to validated html and check if there's a "+ Add" button

        header = self.browser.find_element_by_class_name("card-header")
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
        self.assertTrue(self.check_error_text(dialog) is None)

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
                        self.assertTrue(initial_choice.text == "Choice 1")

                        select2_options = select2.find_elements_by_tag_name("option")
                        self.assertTrue(len(select2_options) == 4)
                        self.assertTrue(select2.get_attribute("name") == "item_type")
                        self.assertTrue(select2.tag_name == "select")
                        self.select_option_for_select2(container, field_id, text="Choice 4")
                    else:
                        select = Select(field)
                        selected_options = select.all_selected_options
                        self.assertTrue(len(selected_options) == 1)
                        self.assertTrue(selected_options[0].get_attribute("index") == "0")
                        self.assertTrue(selected_options[0].text == "Choice 1")
                        self.assertTrue(field.get_attribute("name") == "item_type")
                        self.assertTrue(field.tag_name == "select")
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
                    self.assertTrue(False, f"Wrong field container - label: '{label.text}' {check} {fname}")
        self.assertEqual(field_count, 6)
        dialog.find_element_by_id("save-" + modal_serializer_id).click()

        # There should be an error because of validator set in Model
        dialog, modal_serializer_id = self.wait_for_modal_dialog(modal_serializer_id)
        errors = dialog.find_elements_by_class_name("invalid-feedback")
        self.assertTrue(len(errors) == 1)
        self.assertTrue(errors[0].get_attribute("innerHTML") == "Ensure this value is greater than or equal to 5.")
        field = errors[0].parent.find_element_by_name("amount")
        field.clear()
        field.send_keys("8")
        dialog.find_element_by_id("save-" + modal_serializer_id).click()

        # There should be a field error because of validator set in serializer

        dialog, modal_serializer_id = self.wait_for_modal_dialog(modal_serializer_id)
        errors = dialog.find_elements_by_class_name("invalid-feedback")
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
        self.assertTrue(len(rows) == 1)
        self.check_row(rows[0], 7, ["1", "123", "false", "8", "2", "", None])

        # we delete the row we created
        del_btn = rows[0].find_elements_by_tag_name('td')[6].find_element_by_class_name('btn')
        del_btn.click()

        # TODO: remove following line when task for auto refresh is done.
        self.browser.refresh()
        rows = self.get_table_body()
        self.assertTrue(len(rows) == 1)
        self.assertTrue(rows[0].find_element_by_tag_name('td').text == 'No data')
