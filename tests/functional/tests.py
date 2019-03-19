import os
import time

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.common.exceptions import (ElementNotInteractableException, NoSuchElementException, WebDriverException,
                                        NoAlertPresentException)
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
from examples.models import Validated, RefreshType

MAX_WAIT = 10


class WaitingStaticLiveServerTestCase(StaticLiveServerTestCase):

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

    def wait_for_new_element(self, element_id):
        start_time = time.time()
        while True:
            try:
                time.sleep(0.1)
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
                time.sleep(0.1)
                element = self.browser.find_element_by_class_name('modal')
                self.assertTrue(element is not None)
                element_id = element.get_attribute('id')
                # if old_id:
                #    self.assertFalse(element_id == "dialog-{old_id}".format(**locals()))
                self.assertTrue(element_id.startswith('dialog-'))
                element_id = element_id.split('-', 1)[1]
                return element, element_id
            except (AssertionError, WebDriverException) as e:
                if time.time() - start_time > MAX_WAIT:
                    raise e

    def wait_for_modal_dialog_disapear(self, dialog_id):
        start_time = time.time()
        while True:
            try:
                time.sleep(0.1)
                if self.browser.find_element_by_id('dialog-{dialog_id}'.format(**locals())) is not None:
                    break
                self.assertFalse(time.time() - start_time > MAX_WAIT)
            except WebDriverException:
                break

    # noinspection PyMethodMayBeStatic
    def check_error_text(self, dialog):
        error_text = None
        try:
            error = dialog.find_element_by_class_name('text-danger')
            if error is not None:
                error_text = error.get_attribute('innerHTML')
        except WebDriverException:
            pass
        return error_text

    def initial_check(self, field, fld_text, fld_name, fld_type):
        self.assertEqual(field.text, fld_text)
        self.assertEqual(field.get_attribute('name'), fld_name)
        self.assertEqual(field.get_attribute('type'), fld_type)

    def get_table_body(self):
        try:
            body = self.browser.find_element_by_class_name('card-body')
        except NoSuchElementException:
            try:
                # Bootstrap 3
                body = self.browser.find_element_by_class_name('panel-body')
            except NoSuchElementException:
                # jQueryUI
                body = self.browser.find_element_by_class_name('ui-accordion-content')

        table = body.find_element_by_tag_name('table')

        tbody = table.find_element_by_tag_name('tbody')
        return tbody.find_elements_by_tag_name('tr')

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

    def check_row(self, row, cell_cnt, cell_values):
        cells = row.find_elements_by_tag_name('td')
        self.assertEqual(len(cells), cell_cnt)
        for i in range(len(cell_values)):
            if cell_values[i] is not None:
                self.assertEqual(cells[i].text, cell_values[i])
        return cells


class ValidatedFormTest(WaitingStaticLiveServerTestCase):

    def add_validated_record(self, btn_position, amount, add_second_record=None):
        try:
            header = self.browser.find_element_by_class_name('card-header')
        except NoSuchElementException:
            try:
                # Bootstrap v3
                header = self.browser.find_element_by_class_name("panel-heading")
            except NoSuchElementException:
                # jQueryUI
                header = self.browser.find_element_by_class_name("ui-accordion-header")

        add_btns = header.find_elements_by_class_name('btn')

        add_btns[btn_position].click()

        dialog, modal_serializer_id = self.wait_for_modal_dialog()

        form = dialog.find_element_by_id(modal_serializer_id)
        containers = form.find_elements_by_tag_name("div")
        for container in containers:
            container_id = container.get_attribute("id")
            if container_id.startswith("container-"):
                field_id = container_id.split('-', 1)[1]
                label = container.find_element_by_id("label-" + field_id)
                field = container.find_element_by_id(field_id)

                if label.text == "Code":
                    self.initial_check(field, "", "code", "text")
                    field.send_keys("123")
                elif label.text == "Enabled":
                    self.initial_check(field, "", "enabled", "checkbox")
                    field.click()
                elif label.text == "Amount":
                    self.initial_check(field, "", "amount", "number")
                    field.send_keys(amount)
                elif label.text == "Item type":
                    # Check if item_type field is select2 element
                    try:
                        select2 = container.find_element_by_class_name("select2-field")
                    except NoSuchElementException:
                        select2 = None

                    if select2:
                        self.select_option_for_select2(container, field_id, text="Choice 1")
                    else:
                        select = Select(field)
                        select.select_by_index(0)
                elif label.text == "Item flags":
                    # Check if item_flags field is select2 element
                    try:
                        select2 = container.find_element_by_class_name("select2-field")
                    except NoSuchElementException:
                        select2 = None

                    if select2:
                        self.select_option_for_select2(container, field_id, text="A")
                    else:
                        select = Select(field)
                        select.select_by_index(0)
                elif field.get_attribute("name") in ('id',):
                    # Hidden fields
                    pass

        if add_second_record:
            Validated.objects.create(
                code="123",
                enabled=True,
                amount=6,
                item_type=0,
                item_flags='A'
            )

        dialog.find_element_by_id("save-" + modal_serializer_id).click()
        self.wait_for_modal_dialog_disapear(modal_serializer_id)

    def test_validated_list(self):
        self.browser.get(self.live_server_url + '/validated.html')
        # Go to validated html and check if there's a "+ Add" button

        try:
            header = self.browser.find_element_by_class_name('card-header')
        except NoSuchElementException:
            try:
                # Bootstrap v3
                header = self.browser.find_element_by_class_name("panel-heading")
            except NoSuchElementException:
                # jQueryUI
                header = self.browser.find_element_by_class_name("ui-accordion-header")

        add_btns = header.find_elements_by_class_name('btn')
        self.assertEqual(add_btns[0].text, '+ Add (refresh record)')
        self.assertEqual(add_btns[1].text, '+ Add (refresh table)')
        self.assertEqual(add_btns[2].text, '+ Add (no refresh)')

        # Check if there's a "no data" table row
        rows = self.get_table_body()
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0].find_element_by_tag_name('td').text, 'No data')

        # ---------------------------------------------------------------------------------------------------------#
        # Following a test for modal dialog... we could also do a test for page-editing (not with dialog)          #
        # ---------------------------------------------------------------------------------------------------------#

        # Add a new record via the "+ Add (record refresh)" button and go back to model_single.html to check if the
        # record had been added
        # Test Add action with refreshType='record'
        add_btns[0].click()
        dialog, modal_serializer_id = self.wait_for_modal_dialog()

        # Check if all fields are in the dialog and no excessive fields too
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
                elif label.text == "Comment":
                    self.initial_check(field, "", "comment", "textarea")
                    field.send_keys("Some comment")
                else:
                    field_count -= 1
                    check = label.text == "Code"
                    fname = field.get_attribute("name")
                    self.assertTrue(
                        False, "Wrong field container - label: '{label.text}' {check} {fname}".format(**locals())
                    )
        self.assertEqual(field_count, 7)
        dialog.find_element_by_id("save-" + modal_serializer_id).click()

        # There should be an error because of validator set in Model

        dialog, modal_serializer_id = self.wait_for_modal_dialog(modal_serializer_id)

        errors = dialog.find_elements_by_class_name("invalid-feedback")
        # Bootstrap v3
        if not errors:
            errors = dialog.find_elements_by_class_name("help-block")
        # jQueryUI
        if not errors:
            errors = dialog.find_elements_by_class_name("ui-error-span")

        self.assertEqual(len(errors), 1)
        self.assertEqual(errors[0].get_attribute("innerHTML"), "Ensure this value is greater than or equal to 5.")
        field = errors[0].parent.find_element_by_name("amount")
        field.clear()
        field.send_keys("8")
        dialog.find_element_by_id("save-" + modal_serializer_id).click()

        # There should be a field error because of validator set in serializer
        try:
            # jQueryUI
            body = self.browser.find_element_by_class_name("ui-accordion-content")
            dialog, modal_serializer_id = self.wait_for_modal_dialog()
        except NoSuchElementException:
            dialog, modal_serializer_id = self.wait_for_modal_dialog(modal_serializer_id)

        errors = dialog.find_elements_by_class_name("invalid-feedback")

        # Bootstrap v3
        if not errors:
            errors = dialog.find_elements_by_class_name("help-block")

        # jQueryUI
        if not errors:
            errors = dialog.find_elements_by_class_name("ui-error-span")

        self.assertEqual(len(errors), 1)
        self.assertEqual(errors[0].get_attribute("innerHTML"), 'amount can only be different than 5 if code is "123"')
        field = errors[0].parent.find_element_by_name("code")
        field.clear()
        field.send_keys("123")
        dialog.find_element_by_id("save-" + modal_serializer_id).click()

        # There should be a general/form error because of validator set in serializer
        dialog, modal_serializer_id = self.wait_for_modal_dialog(modal_serializer_id)
        self.assertEqual(self.check_error_text(dialog), "When enabled you can only choose from first three item types")

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

        # Check if record was stored
        rows = self.get_table_body()
        self.assertEqual(len(rows), 1)
        cells = rows[0].find_elements_by_tag_name("td")
        self.assertEqual(len(cells), 8)

        # Then we click the record row to edit it. Go back to model_single.html and check if it had been edited
        cells[0].click()
        dialog, modal_serializer_id = self.wait_for_modal_dialog(modal_serializer_id)
        dialog.find_element_by_name("enabled").click()
        dialog.find_element_by_id("save-" + modal_serializer_id).click()
        self.wait_for_modal_dialog_disapear(modal_serializer_id)

        rows = self.get_table_body()
        self.assertEqual(len(rows), 1)
        cells = self.check_row(rows[0], 8, ['1', '123', 'false', '8', 'Choice 3', 'C', 'Some comment', None])

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

        try:
            # Bootstrap
            close_dialog = dialog.find_element_by_css_selector("[data-dismiss=modal]")
        except NoSuchElementException:
            # jQueryUI
            close_dialog = dialog.find_element_by_class_name("close-btn")
        close_dialog.click()

        rows = self.get_table_body()
        self.assertEqual(len(rows), 1)
        self.check_row(rows[0], 8, ['1', '123', 'false', '8', 'Choice 3', 'C', 'Some comment', None])

        self.wait_for_modal_dialog_disapear(modal_serializer_id)

        # We delete the row we created
        # Test Delete action with refreshType='record'
        del_btns = rows[0].find_elements_by_tag_name('td')[7].find_elements_by_class_name('btn')
        del_btns[0].click()

        rows = self.get_table_body()
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0].find_element_by_tag_name('td').text, 'No data')

        # ----------------------------------------------------------#
        # Tests for refreshType='table' and refreshType='no refresh #'
        # ----------------------------------------------------------#

        self.browser.refresh()

        # Test Add action with refreshType='table'
        self.add_validated_record(1, 5)
        rows = self.get_table_body()
        self.assertEqual(len(rows), 1)
        cells = rows[0].find_elements_by_tag_name("td")
        self.assertEqual(len(cells), 8)

        self.add_validated_record(1, 7, add_second_record=True)
        rows = self.get_table_body()
        self.assertEqual(len(rows), 3)

        # Test Delete action with refreshType='table'
        del_btns = rows[0].find_elements_by_tag_name('td')[7].find_elements_by_class_name('btn')
        del_btns[1].click()
        rows = self.get_table_body()
        self.assertEqual(len(rows), 2)

        del_btns = rows[0].find_elements_by_tag_name('td')[7].find_elements_by_class_name('btn')
        del_btns[1].click()
        rows = self.get_table_body()
        self.assertEqual(len(rows), 1)

        del_btns = rows[0].find_elements_by_tag_name('td')[7].find_elements_by_class_name('btn')
        del_btns[1].click()

        # Test that "no data" row is shown
        rows = self.get_table_body()
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0].find_element_by_tag_name('td').text, 'No data')

        # Test Add action with refreshType='no refresh'
        self.add_validated_record(2, 5, add_second_record=True)

        self.browser.refresh()

        rows = self.get_table_body()
        self.assertEqual(len(rows), 2)
        cells = rows[0].find_elements_by_tag_name("td")
        self.assertEqual(len(cells), 8)

        # Test Delete action with refreshType='no refresh'
        del_btns = rows[0].find_elements_by_tag_name('td')[7].find_elements_by_class_name('btn')
        del_btns[2].click()

        self.browser.refresh()

        rows = self.get_table_body()
        self.assertEqual(len(rows), 1)

        # -------------------------------------------#
        # Tests for editing record and dialog update #'
        # -------------------------------------------#

        self.browser.refresh()

        # Click on record for editing
        rows = self.get_table_body()
        cells = rows[0].find_elements_by_tag_name("td")
        cells[0].click()

        dialog, modal_serializer_id = self.wait_for_modal_dialog()
        dialog_one_id = dialog.get_attribute("id")

        # Check that dialog has Editing in title
        dialog_title = dialog.find_element_by_class_name("modal-title")
        if not dialog_title:
            dialog_title = dialog.find_element_by_class_name("ui-dialog-title")
        self.assertEqual(dialog_title.text, 'Editing validated object')

        # Change Amount field value
        form = dialog.find_element_by_id(modal_serializer_id)
        containers = form.find_elements_by_tag_name("div")
        container_id = containers[3].get_attribute("id")
        field_id = container_id.split('-', 1)[1]
        field = containers[3].find_element_by_id(field_id)
        field.clear()
        field.send_keys(11)

        # Submit form
        dialog.find_element_by_id("save-" + modal_serializer_id).click()

        dialog, modal_serializer_id = self.wait_for_modal_dialog()
        # Check for errors
        errors = dialog.find_elements_by_class_name("invalid-feedback")
        # Bootstrap v3
        if not errors:
            errors = dialog.find_elements_by_class_name("help-block")
        # jQueryUI
        if not errors:
            errors = dialog.find_elements_by_class_name("ui-error-span")

        self.assertEqual(len(errors), 1)
        self.assertEqual(errors[0].get_attribute("innerHTML"), "Ensure this value is less than or equal to 10.")

        # Check that dialog still has Editing in title
        dialog_title = dialog.find_element_by_class_name("modal-title")
        if not dialog_title:
            dialog_title = dialog.find_element_by_class_name("ui-dialog-title")
        self.assertEqual(dialog_title.text, 'Editing validated object')

        # Change Amount field back to valid value
        form = dialog.find_element_by_id(modal_serializer_id)
        containers = form.find_elements_by_tag_name("div")
        container_id = containers[3].get_attribute("id")
        field_id = container_id.split('-', 1)[1]
        field = containers[3].find_element_by_id(field_id)
        field.clear()
        field.send_keys(6)

        # Submit form
        dialog.find_element_by_id("save-" + modal_serializer_id).click()

        # Check that edited record is updated
        self.wait_for_modal_dialog_disapear(modal_serializer_id)

        rows = self.get_table_body()
        self.assertEqual(len(rows), 1)
        cells = self.check_row(rows[0], 8, ['6', '123', 'true', '6', 'Choice 1', 'A', '', None])

    def test_basic_fields(self):
        self.browser.get(self.live_server_url + '/basic-fields.html')
        # Go to basic-fields html and check if there's a "+ Add" button

        try:
            header = self.browser.find_element_by_class_name("card-header")
        except NoSuchElementException:
            try:
                # Bootstrap v3
                header = self.browser.find_element_by_class_name("panel-heading")
            except NoSuchElementException:
                # jQueryUI
                header = self.browser.find_element_by_class_name("ui-accordion-header")

        add_btn = header.find_element_by_class_name("btn")
        self.assertTrue(add_btn.text == "+ Add")

        # Check if there's a "no data" table row
        rows = self.get_table_body()
        self.assertEqual(len(rows), 1)
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
        self.assertEqual(len(rows), 1)
        cells = rows[0].find_elements_by_tag_name("td")
        self.assertEqual(len(cells), 17)

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

        # jQueryUI
        if not errors:
            errors = dialog.find_elements_by_class_name("ui-error-span")

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

    def test_advanced_fields(self):
        self.browser.get(self.live_server_url + '/advanced-fields.html')
        # Go to advanced-fields html and check if there's a "+ Add" button

        try:
            header = self.browser.find_element_by_class_name("card-header")
        except NoSuchElementException:
            try:
                # Bootstrap v3
                header = self.browser.find_element_by_class_name("panel-heading")
            except NoSuchElementException:
                # jQueryUI
                header = self.browser.find_element_by_class_name("ui-accordion-header")

        add_btn = header.find_element_by_class_name("btn")
        self.assertTrue(add_btn.text == "+ Add")

        # Check if there's a "no data" table row
        rows = self.get_table_body()
        self.assertEqual(len(rows), 1)
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
                        self.assertEqual(initial_choice.text, "Relation object 1")

                        select2_options = select2.find_elements_by_tag_name("option")
                        self.assertEqual(len(select2_options), 10)
                        self.assertEqual(select2.get_attribute("name"), "primary_key_related_field")
                        self.assertEqual(select2.tag_name, "select")
                        self.select_option_for_select2(container, field_id, text="Relation object 7")
                    else:
                        select = Select(field)
                        selected_options = select.all_selected_options
                        self.assertEqual(len(selected_options), 1)
                        self.assertEqual(selected_options[0].get_attribute("index"), "0")
                        self.assertEqual(selected_options[0].text, "Relation object 1")
                        self.assertEqual(field.get_attribute("name"), "primary_key_related_field")
                        self.assertEqual(field.tag_name, "select")
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
        self.assertEqual(len(rows), 1)
        cells = rows[0].find_elements_by_tag_name("td")
        self.assertEqual(len(cells), 9)

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
        self.assertEqual(len(rows), 1)
        cells = rows[0].find_elements_by_tag_name("td")
        self.assertEqual(len(cells), 9)

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

        # jQueryUI
        if not errors:
            errors = dialog.find_elements_by_class_name("ui-error-span")
        self.assertEqual(len(errors), 1)
        self.assertEqual(errors[0].get_attribute("innerHTML"),
                         "This value does not match the required pattern (?&lt;=abc)def.")

    def add_refresh_types_record(self, btn_position, text, add_second_record=None):
        try:
            header = self.browser.find_element_by_class_name('card-header')
        except NoSuchElementException:
            try:
                # Bootstrap v3
                header = self.browser.find_element_by_class_name("panel-heading")
            except NoSuchElementException:
                # jQueryUI
                header = self.browser.find_element_by_class_name("ui-accordion-header")

        add_btns = header.find_elements_by_class_name('btn')

        add_btns[btn_position].click()

        dialog, modal_serializer_id = self.wait_for_modal_dialog()

        form = dialog.find_element_by_id(modal_serializer_id)
        containers = form.find_elements_by_tag_name("div")
        for container in containers:
            container_id = container.get_attribute("id")
            if container_id.startswith("container-"):
                field_id = container_id.split('-', 1)[1]
                label = container.find_element_by_id("label-" + field_id)
                field = container.find_element_by_id(field_id)

                if label.text == "Description":
                    self.initial_check(field, "", "description", "text")
                    field.send_keys(text)
                elif field.get_attribute("name") in ('id',):
                    # Hidden fields
                    pass

        if add_second_record:
            RefreshType.objects.create(
                description="Refresh type extra"
            )

        dialog.find_element_by_id("save-" + modal_serializer_id).click()

        try:
            alert = self.browser.switch_to.alert
            self.assertEqual(alert.text, 'Custom function refresh type.')
            alert.accept()
        except NoAlertPresentException:
            pass

        self.wait_for_modal_dialog_disapear(modal_serializer_id)

    def test_refresh_types_list(self):
        self.browser.get(self.live_server_url + '/refresh-types.html')

        try:
            header = self.browser.find_element_by_class_name('card-header')
        except NoSuchElementException:
            try:
                # Bootstrap v3
                header = self.browser.find_element_by_class_name("panel-heading")
            except NoSuchElementException:
                # jQueryUI
                header = self.browser.find_element_by_class_name("ui-accordion-header")

        add_btns = header.find_elements_by_class_name('btn')
        self.assertEqual(add_btns[0].text, '+ Add (refresh record)')
        self.assertEqual(add_btns[1].text, '+ Add (refresh table)')
        self.assertEqual(add_btns[2].text, '+ Add (no refresh)')
        self.assertEqual(add_btns[3].text, '+ Add (page reload)')
        self.assertEqual(add_btns[4].text, '+ Add (redirect)')
        self.assertEqual(add_btns[5].text, '+ Add (custom function)')

        # Check if there's a "no data" table row
        rows = self.get_table_body()
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0].find_element_by_tag_name('td').text, 'No data')

        # Test Add action with refreshType='record'
        self.add_refresh_types_record(0, 'Refresh record')
        rows = self.get_table_body()
        self.assertEqual(len(rows), 1)
        cells = rows[0].find_elements_by_tag_name("td")
        self.assertEqual(len(cells), 3)

        # Test Add action with refreshType='table'
        self.add_refresh_types_record(1, 'Refresh table')
        rows = self.get_table_body()
        self.assertEqual(len(rows), 2)
        cells = rows[0].find_elements_by_tag_name("td")

        self.add_refresh_types_record(1, 'Refresh table 2', add_second_record=True)
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
        redirect_url = self.browser.current_url
        self.assertRegex(redirect_url, '/validated.html')
        # Back to /refresh-types.html
        self.browser.get(self.live_server_url + '/refresh-types.html')
        rows = self.get_table_body()
        self.assertEqual(len(rows), 7)

        # Test Add action with refreshType='custom function'
        self.add_refresh_types_record(5, 'Custom function')
        # Alert is processed in add_record function

        self.browser.refresh()

        rows = self.get_table_body()
        self.assertEqual(len(rows), 8)

        # Test Delete action with refreshType='record'
        del_btns = rows[0].find_elements_by_tag_name('td')[2].find_elements_by_class_name('btn')
        del_btns[0].click()
        rows = self.get_table_body()
        self.assertEqual(len(rows), 7)

        # Test Delete action with refreshType='table'
        del_btns = rows[0].find_elements_by_tag_name('td')[2].find_elements_by_class_name('btn')
        del_btns[1].click()
        rows = self.get_table_body()
        self.assertEqual(len(rows), 6)

        # Test Delete action with refreshType='no refresh'
        del_btns = rows[0].find_elements_by_tag_name('td')[2].find_elements_by_class_name('btn')
        del_btns[2].click()
        rows = self.get_table_body()
        self.assertEqual(len(rows), 6)

        self.browser.refresh()

        rows = self.get_table_body()
        self.assertEqual(len(rows), 5)

        # Test Delete action with refreshType='reload'
        del_btns = rows[0].find_elements_by_tag_name('td')[2].find_elements_by_class_name('btn')
        del_btns[3].click()
        rows = self.get_table_body()
        self.assertEqual(len(rows), 4)

        # Test Delete action with refreshType='redirect'
        del_btns = rows[0].find_elements_by_tag_name('td')[2].find_elements_by_class_name('btn')
        del_btns[4].click()
        # Redirection to /validated.html defined in action happens
        redirect_url = self.browser.current_url
        self.assertRegex(redirect_url, '/validated.html')
        # Back to /refresh-types.html
        self.browser.get(self.live_server_url + '/refresh-types.html')
        rows = self.get_table_body()
        self.assertEqual(len(rows), 3)

        # Test Delete action with refreshType='custom function'
        del_btns = rows[0].find_elements_by_tag_name('td')[2].find_elements_by_class_name('btn')
        del_btns[5].click()

        alert = self.browser.switch_to.alert
        self.assertEqual(alert.text, 'Custom function refresh type.')
        alert.accept()

        self.browser.refresh()

        rows = self.get_table_body()
        self.assertEqual(len(rows), 2)

    def test_single_dialog(self):
        self.browser.get(self.live_server_url + '/refresh-types.html')

        hamburger = self.browser.find_element_by_id('hamburger')
        hamburger.click()

        pop_up_dialog = self.browser.find_element_by_link_text('Pop-up dialog')
        pop_up_dialog.click()

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

                if label.text == "What should we say?":
                    # Check if choice_field field is select2 element
                    try:
                        select2 = container.find_element_by_class_name("select2-field")
                    except NoSuchElementException:
                        select2 = None

                    if select2:
                        initial_choice = container.find_element_by_class_name("select2-selection__rendered")
                        self.assertEqual(initial_choice.text, "Today is sunny")

                        select2_options = select2.find_elements_by_tag_name("option")
                        self.assertEqual(len(select2_options), 2)
                        self.assertEqual(select2.get_attribute("name"), "test")
                        self.assertEqual(select2.tag_name, "select")
                        self.select_option_for_select2(container, field_id, text="Never-ending rain")
                    else:
                        select = Select(field)
                        selected_options = select.all_selected_options
                        self.assertEqual(len(selected_options), 1)
                        self.assertEqual(selected_options[0].get_attribute("index"), "0")
                        self.assertEqual(selected_options[0].text, "Today is sunny")
                        self.assertEqual(field.get_attribute("name"), "test")
                        self.assertEqual(field.tag_name, "select")
                        select.select_by_index(1)

        try:
            dialog.find_element_by_class_name("btn").click()
        except NoSuchElementException:
            dialog.find_element_by_class_name("ui-button").click()

        try:
            alert = self.browser.switch_to.alert
            self.assertEqual(alert.text, 'Never-ending rain')
            alert.accept()
        except NoAlertPresentException:
            pass
