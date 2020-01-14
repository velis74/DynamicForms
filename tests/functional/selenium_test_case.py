import json
import os
import time
from enum import Enum

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.common.exceptions import (
    ElementNotInteractableException, NoAlertPresentException, NoSuchElementException, TimeoutException,
    WebDriverException
)
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.opera.options import Options as OperaOptions
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from dynamicforms.settings import DYNAMICFORMS

MAX_WAIT = 10
MAX_WAIT_ALERT = 0.3


class Browsers(Enum):
    FIREFOX = 'FIREFOX'
    CHROME = 'CHROME'
    OPERA = 'OPERA'
    EDGE = 'EDGE'
    SAFARI = 'SAFARI'
    IE = 'INTERNETEXPLORER'


# noinspection PyMethodMayBeStatic
class WaitingStaticLiveServerTestCase(StaticLiveServerTestCase):
    # host = '0.0.0.0'

    binary_location = ''

    def get_browser(self):
        if self.selected_browser == Browsers.FIREFOX:
            opts = FirefoxOptions()
            opts.binary_location = '/usr/bin/firefox'
            opts.headless = True
            return webdriver.Firefox(options=opts)
        elif self.selected_browser == Browsers.CHROME:
            return webdriver.Chrome()
        elif self.selected_browser == Browsers.OPERA:
            opts = OperaOptions()
            opts.binary_location = self.binary_location
            return webdriver.Opera(options=opts)
        elif self.selected_browser == Browsers.EDGE:
            return webdriver.Edge()
        elif self.selected_browser == Browsers.SAFARI:
            return webdriver.Safari()
        elif self.selected_browser == Browsers.IE:
            return webdriver.Ie()

        self.selected_browser = Browsers.FIREFOX
        return webdriver.Firefox

    def get_browser_options(self, opts):
        if not opts:
            return None

        if self.selected_browser == Browsers.FIREFOX:
            from selenium.webdriver.firefox.options import Options
        elif self.selected_browser == Browsers.CHROME:
            from selenium.webdriver.chrome.options import Options
        elif self.selected_browser == Browsers.OPERA:
            from selenium.webdriver.opera.options import Options
        elif self.selected_browser == Browsers.EDGE:
            from selenium.webdriver.edge.options import Options
        elif self.selected_browser == Browsers.IE:
            from selenium.webdriver.ie.options import Options
        else:  # Safari doesn't have Options
            return None

        options = Options()
        opts = json.loads(opts.replace('{comma}', ','))
        for key, val in opts.items():
            setattr(options, key, val)
        return options

    def setUp(self):
        remote_selenium = os.environ.get('REMOTE_SELENIUM', ',,')
        # first parameter: remote server
        # second parameter: "my" server
        # third parameter: browser with optional additional options (behind vertical bar)
        #  Options are in JSON format. All commas must be replaced with '{comma}' string (see example below)
        #
        # remote_selenium = 'MAC-SERVER:4444,myserver,SAFARI'
        # remote_selenium = 'WIN-SERVER:4444,myserver,FIREFOX|{"binary_location": "C:\\\\Program Files\\\\Mozilla
        #      Firefox\\\\firefox.exe"{comma} "headless": true}'

        remote, this_server, browser_options = remote_selenium.split(',')
        if remote:

            browser_options = browser_options.split('|', 1)
            browser = browser_options[0]
            self.selected_browser = Browsers(browser)
            opts = None
            try:
                opts = self.get_browser_options(browser_options[1])
            except:
                pass

            self.browser = webdriver.Remote(
                command_executor='http://{remote}/wd/hub'.format(remote=remote),
                desired_capabilities=dict(javascriptEnabled=True, **getattr(webdriver.DesiredCapabilities, browser)),
                options=opts
            )

            olsu = self.live_server_url
            self.live_server_url = 'http://{this_server}:{port}'.format(this_server=this_server,
                                                                        port=self.live_server_url.split(':')[2])
            print('Listen: ', olsu, ' --> Remotely accessible on: ', self.live_server_url)
        else:
            # self.live_server_url = self.live_server_url.replace('0.0.0.0', 'localhost')
            # self.binary_location = 'C:\\Users\\kleme\\AppData\\Local\\Programs\\Opera\\60.0.3255.170\\opera.exe'
            self.selected_browser = Browsers.FIREFOX
            self.browser = self.get_browser()

    def tearDown(self):
        self.browser.refresh()
        self.browser.quit()

    def wait_for_new_element(self, element_id):
        start_time = time.time()
        while True:
            try:
                time.sleep(0.1)
                element = self.browser.find_element_by_id(element_id)
                self.assertIsNotNone(element)
                return
            except (AssertionError, WebDriverException) as e:
                if time.time() - start_time > MAX_WAIT:
                    raise e

    def wait_for_modal_dialog(self, old_id=None):
        start_time = time.time()
        while True:
            try:
                time.sleep(0.1)
                element = None
                for el in self.browser.find_elements_by_class_name('modal'):
                    if el.is_displayed():
                        element = el
                        break
                self.assertIsNotNone(element)
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

    def get_alert(self):
        start_time = time.time()
        while True:
            try:
                time.sleep(0.05)
                alert = self.browser.switch_to.alert
                break
            except NoAlertPresentException:
                pass
            if time.time() - start_time > MAX_WAIT_ALERT:
                raise NoAlertPresentException
        return alert

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
        self.assertEqual(self.get_element_text(field), fld_text)
        self.assertEqual(field.get_attribute('name'), fld_name)
        if isinstance(fld_type, tuple):
            self.assertIn(field.get_attribute('type'), fld_type)
        else:
            self.assertEqual(field.get_attribute('type'), fld_type)

    def get_table_body(self, whole_table=False):
        time.sleep(0.1)
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
        if whole_table:
            return table

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
                self.assertEqual(self.get_element_text(cells[i]), cell_values[i])
        return cells

    def get_current_url(self):
        time.sleep(0.05)
        return self.browser.current_url

    def update_edge_field(self, field_id, value):
        self.browser.execute_script('''
        $('#%s').val('%s');
        dynamicforms.fieldChange('%s', 'final');
            ''' % (field_id, value, field_id))

    @staticmethod
    def get_field_id_by_name(dialog, name):
        return dialog.find_element_by_name(name).get_attribute('id')

    @staticmethod
    def get_tag_name(el):
        return el.tag_name.lower()

    @staticmethod
    def get_element_text(el):
        return el.text.strip()
