import os
import time

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.common.exceptions import WebDriverException

MAX_WAIT = 10


class ValidatedFormTest(StaticLiveServerTestCase):
    def setUp(self):
        self.browser = webdriver.Firefox()
        staging_server = os.environ.get('STAGING_SERVER')
        print(self.live_server_url)
        if staging_server:
            print('\n\nSTAGING SERVER\n\n')
            self.live_server_url = 'http://' + staging_server
        print(self.live_server_url)

    def tearDown(self):
        self.browser.refresh()
        self.browser.quit()
        pass

    def wait_for_new_element(self, element_id):
        start_time = time.time()
        while True:
            try:
                element = self.browser.find_element_by_id(element_id)
                self.assertTrue(element is not None)
                return
            except (AssertionError, WebDriverException) as e:
                if time.time() - start_time > MAX_WAIT:
                    raise e
                time.sleep(0.5)

    def wait_for_modal_dialog(self):
        start_time = time.time()
        while True:
            try:
                element = self.browser.find_element_by_class_name("modal")
                self.assertTrue(element is not None)
                self.assertTrue(element.get_attribute("id").startswith("dialog-"))
                return element
            except (AssertionError, WebDriverException) as e:
                if time.time() - start_time > MAX_WAIT:
                    raise e
                time.sleep(0.5)

    def test_validated_list(self):
        self.browser.get(self.live_server_url + '/rest/validated.html')
        # Grem na validated html in preverim, če ima + Add button
        is_add = False
        header = self.browser.find_element_by_class_name("card-header")
        add_btn = header.find_element_by_class_name("btn")
        self.assertTrue(add_btn.text == "+ Add")

        # Preverim, če ima no data polje
        body = self.browser.find_element_by_class_name("card-body")
        table = body.find_element_by_tag_name("table")
        serializer_id = table.get_attribute("id").split('-', 1)[1]
        tbody = table.find_element_by_tag_name("tbody")
        rows = tbody.find_elements_by_tag_name("tr")
        self.assertTrue(len(rows) == 1)
        self.assertTrue(rows[0].find_element_by_tag_name("td").text == "No data")

        # ---------------------------------------------------------------------------------------------------------#
        # Spodaj je test, če je modalen dialog... lahko bi se naredil še test, če se urejanje pokaže na novi strani#
        # ---------------------------------------------------------------------------------------------------------#

        # Potem preko add buttona dodam en zapis in grem nazaj na validated.html in preverim, če je zapis dodan
        add_btn.click()
        dialog = self.wait_for_modal_dialog()
        modal_serializer_id = dialog.get_attribute("id").split("-", 1)[1]
        # dialog = self.browser.find_element_by_id('dialog-' + serializer_id)
        # preverim, če so v dialogu prikazana vsa polja... in če nobeden ni preveč
        field_count = 0

        form = dialog.find_element_by_id(modal_serializer_id)
        containers = form.find_elements_by_tag_name("div")
        for container in containers:
            container_id = container.get_attribute("id")
            if container_id.startswith("container-"):
                field_id = container_id.split('-', 1)[1]
                label = container.find_element_by_id("label-" + field_id)
                field = container.find_element_by_id(field_id)
                if label.text == "Code":
                    field_count += 1
                    self.assertTrue(field.text == "")
                    self.assertTrue(field.get_attribute("name") == "code")
                    self.assertTrue(field.get_attribute("type") == "text")
                    field.send_keys("12345")
                elif label.text == "Enabled":
                    field_count += 1
                    self.assertTrue(field.text == "")
                    self.assertTrue(field.get_attribute("name") == "enabled")
                    self.assertTrue(field.get_attribute("type") == "checkbox")
                    field.click()
                elif label.text == "Amount":
                    field_count += 1
                    self.assertTrue(field.text == "")
                    self.assertTrue(field.get_attribute("name") == "amount")
                    self.assertTrue(field.get_attribute("type") == "number")
                    field.send_keys("4423")
                elif label.text == "Item type":
                    field_count += 1
                    self.assertTrue(field.option == 0)
                    self.assertTrue(field.get_attribute("name") == "item_type")
                    self.assertTrue(field.tag_name == "select")
                    field.select(2)
                elif label.text == "Item flags":  # ta mora biti select2...
                    field_count += 1
                    self.assertTrue(field.option == 0)
                    self.assertTrue(field.get_attribute("name") == "item_flags")
                    self.assertTrue(field.tag_name == "select")
                    field.select(1)
                else:
                    self.assertTrue(False, f"Wrong field container - label: {label.text}")
        self.assertEqual(field_count, 5)

        # Potem kliknem na zapis in ga uredim. Grem nazaj na validated.html in preverim, če je zapis urejen
        # Grem šeenkrat na urejanje in ga prekinem
        pass
