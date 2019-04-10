import os
import time

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.common.exceptions import (
    ElementNotInteractableException, NoSuchElementException, WebDriverException, TimeoutException
)
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from dynamicforms.settings import DYNAMICFORMS

MAX_WAIT = 10


# noinspection PyMethodMayBeStatic
class WaitingStaticLiveServerTestCase(StaticLiveServerTestCase):
    host = '0.0.0.0'

    def setUp(self):
        remote, this_server, browser = os.environ.get('REMOTE_SELENIUM', ',,').split(',')
        if remote:
            self.browser = webdriver.Remote(
                command_executor='http://{remote}/wd/hub'.format(remote=remote),
                desired_capabilities=dict(**getattr(webdriver.DesiredCapabilities, browser), javascriptEnabled=True)
            )
            olsu = self.live_server_url
            self.live_server_url = 'http://{this_server}:{port}'.format(this_server=this_server,
                                                                        port=self.live_server_url.split(':')[2])
            print('Listen: ', olsu, ' --> Remotely accessible on: ', self.live_server_url)
        else:
            self.live_server_url = self.live_server_url.replace('0.0.0.0', 'localhost')
            self.browser = webdriver.Firefox()

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
                if old_id and element_id == "dialog-{old_id}".format(**locals()):
                    # The new dialog must not have same id as the old one
                    # if it does, this means that we're still looking at the old dialog - let's wait for it to go away
                    continue
                self.assertTrue(element_id.startswith('dialog-'))
                element_id = element_id.split('-', 1)[1]

                # this is a dialog - let's wait for its animations to stop
                try:
                    WebDriverWait(element, .5).until(EC.element_to_be_clickable(
                        (By.CLASS_NAME, 'ui-button' if DYNAMICFORMS.jquery_ui else 'btn'))
                    )
                except TimeoutException:
                    # dialog not ready yet or we found a bad dialog with no buttons
                    continue

                return element, element_id
            except (AssertionError, WebDriverException) as e:
                if time.time() - start_time > MAX_WAIT:
                    raise e

    def wait_for_modal_dialog_disapear(self, dialog_id):
        start_time = time.time()
        while True:
            try:
                time.sleep(0.1)
                if self.browser.find_element_by_id('dialog-{dialog_id}'.format(**locals())) is None:
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
        if isinstance(fld_type, tuple):
            self.assertIn(field.get_attribute('type'), fld_type)
        else:
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

    def select_option_for_select2(self, driver, element_id, text=None):
        element = driver.find_element_by_xpath("//*[@id='{element_id}']/following-sibling::*[1]".format(**locals()))
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
