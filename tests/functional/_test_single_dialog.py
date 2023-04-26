from parameterized import parameterized
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By

from .select import Select
from .selenium_test_case import WaitingStaticLiveServerTestCase


class SingleDialogTest(WaitingStaticLiveServerTestCase):
    @parameterized.expand(["html", "component"])
    def test_single_dialog(self, renderer):
        if renderer == "component":
            # for now viewmode version of dynamicforms does not support dynamicforms.dialog and dialog creation
            # outside single page app is not supported
            return
        else:
            self.browser.get(self.live_server_url + "/refresh-types." + renderer)

        hamburger = self.browser.find_element(By.ID, "hamburger")
        hamburger.click()

        self.wait_for_new_element(lambda: self.browser.find_element(By.LINK_TEXT, "Pop-up dialog"))
        pop_up_dialog = self.browser.find_element(By.LINK_TEXT, "Pop-up dialog")
        pop_up_dialog.click()

        dialog, modal_serializer_id = self.wait_for_modal_dialog()

        # we verify that the dialog is set to large size and that dialog's title bar is set to info
        # both tests are really crude: we just look for ANY child with the class. They should suffice though except
        # if someone decides to hack some stuff of his own in there using these classes
        dialog.find_elements(By.CLASS_NAME, "modal-lg")
        dialog.find_elements(By.CLASS_NAME, "bg-info")
        # check if all fields are in the dialog and no excessive fields too
        field_count = 0

        form = dialog.find_element(By.ID, modal_serializer_id)
        custom_paragraph = dialog.find_element(By.ID, "single_dialog_instructions")
        self.assertIsNotNone(custom_paragraph, "Custom paragraph not rendered")
        custom_list = dialog.find_element(By.ID, "single_dialog_instructions_list")
        self.assertIsNotNone(custom_list, "Custom list not rendered")
        custom_list_items = custom_list.find_elements(By.TAG_NAME, "li")
        self.assertEqual(len(custom_list_items), 2, msg="Custom list items not rendered correctly")
        containers = form.find_elements(By.TAG_NAME, "div")
        for container in containers:
            container_id = container.get_attribute("id")
            if container_id.startswith("container-"):
                field_id = container_id.split("-", 1)[1]
                label = container.find_element(By.ID, "label-" + field_id)
                field = container.find_element(By.ID, field_id)

                field_count += 1

                if label.text == "What should we say?":
                    select = Select(field)
                    self.assertEqual(len(select.current_selection), 1)
                    self.assertEqual(select.current_selection.single.value, "Today is sunny")
                    self.assertEqual(len(select.options), 2)
                    self.assertEqual(field.get_attribute("name"), "test")
                    select.select_by_value("Never-ending rain")

        try:
            dialog.find_element(By.CLASS_NAME, "btn-primary").click()
        except NoSuchElementException:
            dialog.find_element(By.CLASS_NAME, "ui-button").click()

        alert = self.get_alert(wait_time=15)
        self.assertEqual(self.get_element_text(alert), "Never-ending rain")
        alert.accept()
