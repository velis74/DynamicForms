import time

from parameterized import parameterized
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from examples.models import Validated
from .select import Select
from .selenium_test_case import WaitingStaticLiveServerTestCase


class ValidatedFormTest(WaitingStaticLiveServerTestCase):

    def add_validated_record(self, btn_position, amount, add_second_record=None):
        header = self.find_element_by_classes(('card-header', 'panel-heading', 'ui-accordion-header'))
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
                label_text = self.get_element_text(label)

                if label_text == "Code":
                    self.initial_check(field, "", "code", "text")
                    field.send_keys("123")
                elif label_text == "Enabled":
                    self.initial_check(field, "", "enabled", "checkbox")
                    field.click()
                elif label_text == "Amount":
                    self.initial_check(field, "", "amount", "number")
                    field.send_keys(amount)
                elif label_text == "Item type":
                    select = Select(field)
                    select.select_by_value('0')
                elif label_text == "Item flags":
                    select = Select(field)
                    select.select_by_value('A')
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

        WebDriverWait(driver=self.browser, timeout=10, poll_frequency=0.2).until(EC.element_to_be_clickable(
            (By.ID, "save-" + modal_serializer_id))
        )

        dialog.find_element_by_id("save-" + modal_serializer_id).click()
        self.wait_for_modal_dialog_disapear(modal_serializer_id)

    @parameterized.expand(['html', 'component'])
    def test_validated_list(self, renderer='html'):
        self.browser.get(self.live_server_url + '/validated.' + renderer)
        # Go to validated html and check if there's a "+ Add" button

        header = self.find_element_by_classes(('card-header', 'panel-heading', 'ui-accordion-header'))
        add_btns = header.find_elements_by_class_name('btn')
        self.assertEqual(self.get_element_text(add_btns[0]), '+ Add (refresh record)')
        self.assertEqual(self.get_element_text(add_btns[1]), '+ Add (refresh table)')
        self.assertEqual(self.get_element_text(add_btns[2]), '+ Add (no refresh)')

        # Check if there's a "no data" table row
        rows = self.get_table_body()
        self.assertEqual(len(rows), 1)
        self.assertEqual(self.get_element_text(rows[0].find_element_by_tag_name('td')), 'No data')

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
                field_tag_name = self.get_tag_name(field)
                label_text = self.get_element_text(label)

                field_count += 1
                if label_text == "Code":
                    self.initial_check(field, "", "code", "text")
                    field.send_keys("12345")
                elif label_text == "Enabled":
                    self.initial_check(field, "", "enabled", "checkbox")
                    field.click()
                elif label_text == "Amount":
                    self.initial_check(field, "", "amount", "number")
                    field.send_keys("3")
                elif label_text == "Item type":
                    select = Select(field)
                    self.assertEqual(select.current_selection.single.value, '0')
                    self.assertEqual(len(select.options), 4)
                    self.assertEqual(field.get_attribute("name"), "item_type")
                    select.select_by_value('3')
                elif label_text == "Item flags":
                    select = Select(field)
                    self.assertEqual(select.current_selection.single.value, '')
                    self.assertEqual(len(select.options), 5)
                    self.assertEqual(field.get_attribute("name"), "item_flags")
                    select.select_by_value('C')
                elif field.get_attribute("name") in ('id',):
                    # Hidden fields
                    pass
                elif label_text == "Comment":
                    self.initial_check(field, "", "comment", "textarea")
                    field.send_keys("Some comment")
                else:
                    field_count -= 1
                    check = label_text == "Code"
                    fname = field.get_attribute("name")
                    self.assertTrue(
                        False, "Wrong field container - label: '{label_text}' {check} {fname}".format(**locals())
                    )
        self.assertEqual(field_count, 6)
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
        select = Select(form.find_element_by_name('item_type'))
        select.select_by_value('2')

        dialog.find_element_by_id("save-" + modal_serializer_id).click()
        self.wait_for_modal_dialog_disapear(modal_serializer_id)

        time.sleep(0.5)
        # Check if record was stored
        rows = self.get_table_body(expected_rows=1)
        self.assertEqual(len(rows), 1)
        cells = rows[0].find_elements_by_tag_name("td")
        self.assertEqual(len(cells), 8)

        # Then we click the record row to edit it. Go back to model_single.html and check if it had been edited
        cells[0].click()
        dialog, modal_serializer_id = self.wait_for_modal_dialog(modal_serializer_id)
        dialog.find_element_by_name("enabled").click()
        dialog.find_element_by_id("save-" + modal_serializer_id).click()
        self.wait_for_modal_dialog_disapear(modal_serializer_id)
        time.sleep(0.5)

        rows = self.get_table_body(expected_rows=1)
        self.assertEqual(len(rows), 1)
        cells = self.check_row(rows[0], 8, ['1', '123', 'false', '8', 'Choice 3', 'C', 'Some comment', None])

        # Once more to editing and cancel it
        cells[0].click()
        dialog, modal_serializer_id = self.wait_for_modal_dialog(modal_serializer_id)

        # Check if item_type field is select2 element
        form = dialog.find_element_by_id(modal_serializer_id)
        select = Select(form.find_element_by_name('item_type'))
        select.select_by_value('2')

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
        self.assertEqual(self.get_element_text(rows[0].find_element_by_tag_name('td')), 'No data')

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
        time.sleep(0.5)
        del_btns = rows[0].find_elements_by_tag_name('td')[7].find_elements_by_class_name('btn')
        del_btns[1].click()
        rows = self.get_table_body()
        self.assertEqual(len(rows), 2)

        time.sleep(0.5)
        del_btns = rows[0].find_elements_by_tag_name('td')[7].find_elements_by_class_name('btn')
        del_btns[1].click()
        rows = self.get_table_body()
        self.assertEqual(len(rows), 1)

        time.sleep(0.5)
        del_btns = rows[0].find_elements_by_tag_name('td')[7].find_elements_by_class_name('btn')
        del_btns[1].click()

        # Test that "no data" row is shown
        rows = self.get_table_body()
        self.assertEqual(len(rows), 1)
        self.assertEqual(self.get_element_text(rows[0].find_element_by_tag_name('td')), 'No data')

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
        try:
            dialog_title = dialog.find_element_by_class_name("modal-title")
        except NoSuchElementException:
            dialog_title = dialog.find_element_by_class_name("ui-dialog-title")
        self.assertEqual(self.get_element_text(dialog_title), 'Editing validated object')

        # Change Amount field value
        form = dialog.find_element_by_id(modal_serializer_id)
        field = form.find_elements_by_css_selector('input[name=amount]')[0]
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
        try:
            dialog_title = dialog.find_element_by_class_name("modal-title")
        except NoSuchElementException:
            dialog_title = dialog.find_element_by_class_name("ui-dialog-title")
        self.assertEqual(self.get_element_text(dialog_title), 'Editing validated object')

        # Change Amount field back to valid value
        form = dialog.find_element_by_id(modal_serializer_id)
        field = form.find_elements_by_css_selector('input[name=amount]')[0]
        field.clear()
        field.send_keys(6)

        # Submit form
        dialog.find_element_by_id("save-" + modal_serializer_id).click()

        # Check that edited record is updated
        self.wait_for_modal_dialog_disapear(modal_serializer_id)
        time.sleep(0.5)

        rows = self.get_table_body()
        self.assertEqual(len(rows), 1)
        cells = self.check_row(rows[0], 8, ['6', '123', 'true', '6', 'Choice 1', 'A', '', None])