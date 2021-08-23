from parameterized import parameterized
from selenium.common.exceptions import NoSuchElementException

from .select import Select
from .selenium_test_case import WaitingStaticLiveServerTestCase


class SingleDialogTest(WaitingStaticLiveServerTestCase):

    @parameterized.expand(['html', 'component'])
    def test_single_dialog(self, renderer):
        if renderer == 'component':
            self.browser.get(self.live_server_url + '/component')
        else:
            self.browser.get(self.live_server_url + '/refresh-types.' + renderer)

        hamburger = self.browser.find_element_by_id('hamburger')
        hamburger.click()

        self.wait_for_new_element(lambda: self.browser.find_element_by_link_text('Pop-up dialog'))
        pop_up_dialog = self.browser.find_element_by_link_text('Pop-up dialog')
        pop_up_dialog.click()

        dialog, modal_serializer_id = self.wait_for_modal_dialog()

        # check if all fields are in the dialog and no excessive fields too
        field_count = 0

        form = dialog.find_element_by_id(modal_serializer_id)
        children = form.find_elements_by_xpath("*")
        custom_paragraph = next((el for el in children if el.tag_name == 'p'), None)
        self.assertIsNotNone(custom_paragraph, "Custom paragraph not rendered")
        custom_list = next((el for el in children if el.tag_name == 'ul'), None)
        self.assertIsNotNone(custom_list, "Custom list not rendered")
        custom_list_items = custom_list.find_elements_by_tag_name("li")
        self.assertEqual(len(custom_list_items), 2, msg="Custom list items not rendered correctly")
        containers = form.find_elements_by_tag_name("div")
        for container in containers:
            container_id = container.get_attribute("id")
            if container_id.startswith("container-"):
                field_id = container_id.split('-', 1)[1]
                label = container.find_element_by_id("label-" + field_id)
                field = container.find_element_by_id(field_id)

                field_count += 1

                if label.text == "What should we say?":
                    select = Select(field)
                    self.assertEqual(len(select.current_selection), 1)
                    self.assertEqual(select.current_selection.single.value, "Today is sunny")
                    self.assertEqual(len(select.options), 2)
                    self.assertEqual(field.get_attribute("name"), "test")
                    select.select_by_value('Never-ending rain')

        try:
            dialog.find_element_by_class_name("btn-primary").click()
        except NoSuchElementException:
            dialog.find_element_by_class_name("ui-button").click()

        alert = self.get_alert(wait_time=15)
        self.assertEqual(self.get_element_text(alert), 'Never-ending rain')
        alert.accept()
