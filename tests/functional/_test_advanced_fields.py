import os

from parameterized import parameterized
from selenium.webdriver.common.by import By

from setup.settings import BASE_DIR, MEDIA_ROOT

from .select import Select
from .selenium_test_case import WaitingStaticLiveServerTestCase


class AdvancedFieldsTest(WaitingStaticLiveServerTestCase):
    upload_file_name = "0_3142.prj"
    file_for_upload = os.path.join(BASE_DIR, "tests", "static_files", upload_file_name)

    def tearDown(self):
        super().tearDown()
        uploaded_file = "%s/examples/%s" % (MEDIA_ROOT, self.upload_file_name)
        if os.path.exists(uploaded_file):
            os.remove(uploaded_file)

    @parameterized.expand(["html", "component"])
    def test_advanced_fields(self, renderer="component"):
        self.browser.get(self.live_server_url + "/advanced-fields." + renderer)
        # Go to advanced-fields html and check if there's a "Add" button

        header = self.find_element_by_classes(("card-header", "panel-heading", "ui-accordion-header"))
        add_btn = header.find_element(By.CLASS_NAME, "btn")
        if add_btn.tag_name == "div":
            btn_text = self.get_element_text(add_btn.find_element(By.TAG_NAME, "span"))
        else:
            btn_text = self.get_element_text(add_btn)
        self.assertEqual(btn_text, "Add")

        # Check if there's a "no data" table row
        rows = self.get_table_body()
        self.assertEqual(len(rows), 1)
        self.assertEqual(self.get_element_text(rows[0].find_element(By.TAG_NAME, "td")), "No data")

        # ---------------------------------------------------------------------------------------------------------#
        # Following a test for modal dialog... we could also do a test for page-editing (not with dialog)          #
        # ---------------------------------------------------------------------------------------------------------#

        # Add a new record via the "Add" button and go back to model_single.html to check if the record had been added
        add_btn.click()
        dialog, modal_serializer_id = self.wait_for_modal_dialog()

        # check if all fields are in the dialog and no excessive fields too
        field_count = 0

        form = dialog.find_element(By.ID, modal_serializer_id)
        containers = form.find_elements(By.TAG_NAME, "div")
        for container in containers:
            container_id = container.get_attribute("id")
            if container_id.startswith("container-"):
                field_id = container_id.split("-", 1)[1]
                field = container.find_element(By.ID, field_id)
                label = container.find_element(By.ID, "label-" + field_id)

                field_count += 1
                label_text = self.get_element_text(label)

                if label_text == "Regex field":
                    self.initial_check(field, "", "regex_field", "text")
                    field.send_keys("abcdef")
                elif label_text == "Choice field":
                    select = Select(field)
                    self.assertEqual(select.current_selection.single.value, "0")
                    self.assertEqual(len(select.options), 4)
                    self.assertEqual(field.get_attribute("name"), "choice_field")
                    select.select_by_value("3")
                elif label_text == "Readonly field":
                    self.initial_check(field, "", "readonly_field", "checkbox")
                    self.assertEqual(field.get_attribute("checked"), "true")
                elif label_text == "Filepath field":
                    select = Select(field)
                    self.assertEqual(select.current_selection.single.value, "")
                    self.assertEqual(field.get_attribute("name"), "filepath_field")
                    select.select_by_value(select.value_from_text("admin.py"))
                # Hidden field is not shown in dialog
                elif label_text == "Primary key related field":
                    select = Select(field)
                    self.assertEqual(select.current_selection.single.value, select.value_from_text("Relation object 1"))
                    self.assertEqual(len(select.options), 10)
                    self.assertEqual(field.get_attribute("name"), "primary_key_related_field")
                    select.select_by_value(select.value_from_text("Relation object 7"))
                elif label_text == "Slug related field":
                    select = Select(field)
                    self.assertEqual(select.current_selection.single.value, select.value_from_text("Relation object 1"))
                    self.assertEqual(len(select.options), 10)
                    self.assertEqual(field.get_attribute("name"), "slug_related_field")
                    select.select_by_value(select.value_from_text("Relation object 5"))
                # StringRelatedField is read only with primary_key_related_field as source and is not shown in dialog
                elif label_text == "File field" and renderer == "html":
                    container.find_element(By.NAME, "file_field").send_keys(self.file_for_upload)
                elif label_text == "File field two" and renderer == "component":
                    container.find_element(By.NAME, "file_field_two").send_keys(self.file_for_upload)
                else:
                    field_count -= 1

        self.assertEqual(field_count, 7)
        dialog.find_element(By.ID, ("save-" if renderer == "html" else "submit-") + modal_serializer_id).click()
        self.wait_for_modal_dialog_disapear(modal_serializer_id)

        # TODO: remove following line when task for auto refresh is done.
        if renderer == "html":
            self.browser.refresh()

        rows = self.get_table_body()
        self.assertEqual(len(rows), 1)
        cells = rows[0].find_elements(By.TAG_NAME, "td")
        self.assertEqual(len(cells), 12)

        # Check for relations
        self.assertEqual(self.get_element_text(cells[6]), "Relation object 7")
        self.assertEqual(self.get_element_text(cells[7]), "Relation object 7")
        self.assertEqual(self.get_element_text(cells[8]), "Relation object 5")

        # Then we click the record row to edit it. Go back to model_single.html and check if it had been edited
        cells[0].click()
        dialog, modal_serializer_id = self.wait_for_modal_dialog(modal_serializer_id)

        select = Select(dialog.find_element(By.NAME, "choice_field"))
        select.select_by_value(select.value_from_text("Choice 2"))

        select = Select(dialog.find_element(By.NAME, "primary_key_related_field"))
        select.select_by_value(select.value_from_text("Relation object 9"))

        # Submit
        dialog.find_element(By.ID, ("save-" if renderer == "html" else "submit-") + modal_serializer_id).click()
        self.wait_for_modal_dialog_disapear(modal_serializer_id)

        # TODO: remove following line when task for auto refresh is done.
        self.browser.refresh()
        rows = self.get_table_body()
        self.assertEqual(len(rows), 1)
        cells = rows[0].find_elements(By.TAG_NAME, "td")
        self.assertEqual(len(cells), 12)

        # Check for changed values
        self.assertEqual(self.get_element_text(cells[2]), "Choice 2")
        self.assertEqual(self.get_element_text(cells[6]), "Relation object 9")
        self.assertEqual(self.get_element_text(cells[7]), "Relation object 9")

        # Then we click the record row to edit it. Go back to model_single.html and check if it had been edited
        cells[0].click()
        dialog, modal_serializer_id = self.wait_for_modal_dialog(modal_serializer_id)

        # Change regex field to throw error
        regex_field = dialog.find_element(By.NAME, "regex_field")
        regex_field.clear()
        regex_field.send_keys("Test error")

        # Submit
        dialog.find_element(By.ID, ("save-" if renderer == "html" else "submit-") + modal_serializer_id).click()

        if renderer == "html":
            self.wait_for_modal_dialog_disapear(modal_serializer_id)
        # Check for errors
        dialog, modal_serializer_id = self.wait_for_modal_dialog()

        errors = dialog.find_elements(By.CLASS_NAME, "invalid-feedback")
        # Bootstrap v3
        if not errors:
            errors = dialog.find_elements(By.CLASS_NAME, "help-block")

        # jQueryUI
        if not errors:
            errors = dialog.find_elements(By.CLASS_NAME, "ui-error-span")
        self.assertEqual(len(errors), 1)
        self.assertEqual(
            errors[0].get_attribute("innerHTML"), "This value does not match the required pattern (?&lt;=abc)def."
        )
