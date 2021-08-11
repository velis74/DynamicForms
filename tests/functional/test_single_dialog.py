from parameterized import parameterized
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.select import Select

from .selenium_test_case import WaitingStaticLiveServerTestCase


class SingleDialogTest(WaitingStaticLiveServerTestCase):

    @parameterized.expand(['html', 'component'])
    def test_single_dialog(self, renderer):
        self.browser.get(self.live_server_url + '/refresh-types.' + renderer)

        hamburger = self.browser.find_element_by_id('hamburger')
        hamburger.click()

        self.browser.execute_script(f'window.singleDialogFormat = "{renderer}";')
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

                        initial_choice = container.find_element_by_class_name("select2-selection__rendered")
                        self.assertEqual(self.get_element_text(initial_choice), "Today is sunny")

                        select2_options = select2.find_elements_by_tag_name("option")
                        self.assertEqual(len(select2_options), 2)
                        self.assertEqual(select2.get_attribute("name"), "test")
                        self.assertEqual(self.get_tag_name(select2), "select")
                        self.select_option_for_select2(container, field_id, text="Never-ending rain")
                    except NoSuchElementException:
                        try:
                            select2 = container.find_element_by_class_name("df-select-class")
                            selected_options = select2.get_attribute('data-value').split(',')
                            self.assertEqual(len(selected_options), 1)
                            self.assertEqual(selected_options[0], "Today is sunny")
                            self.assertEqual(field.get_attribute("name"), "test")
                            self.assertEqual(self.get_tag_name(field), "div")
                            self.browser.execute_script(f"window['setSelectValue {field_id}']('Never-ending rain');")
                        except NoSuchElementException:
                            select = Select(field)
                            selected_options = select.all_selected_options
                            self.assertEqual(len(selected_options), 1)
                            self.assertEqual(selected_options[0].get_attribute("index"), "0")
                            self.assertEqual(self.get_element_text(selected_options[0]), "Today is sunny")
                            self.assertEqual(field.get_attribute("name"), "test")
                            self.assertEqual(self.get_tag_name(field), "select")
                            select.select_by_index(1)


        try:
            dialog.find_element_by_class_name("btn-primary").click()
        except NoSuchElementException:
            dialog.find_element_by_class_name("ui-button").click()

        alert = self.get_alert(wait_time=15)
        self.assertEqual(self.get_element_text(alert), 'Never-ending rain')
        alert.accept()
