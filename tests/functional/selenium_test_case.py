import json
import os
import time

from enum import Enum
from typing import Iterable

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.common.exceptions import (
    ElementNotInteractableException,
    NoSuchElementException,
    TimeoutException,
    WebDriverException,
)
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

MAX_WAIT = 10
MAX_WAIT_ALERT = 5


class Browsers(Enum):
    FIREFOX = "FIREFOX"
    CHROME = "CHROME"
    OPERA = "OPERA"
    EDGE = "EDGE"
    SAFARI = "SAFARI"
    IE = "INTERNETEXPLORER"


# noinspection PyMethodMayBeStatic
class WaitingStaticLiveServerTestCase(StaticLiveServerTestCase):
    # host = '0.0.0.0'

    binary_location = ""
    github_actions = False

    def get_browser(self, opts=None):
        if self.selected_browser == Browsers.FIREFOX:
            return webdriver.Firefox(options=opts)
        elif self.selected_browser == Browsers.CHROME:
            return webdriver.Chrome(options=opts)
        elif self.selected_browser == Browsers.OPERA:
            return webdriver.Opera(options=opts)
        elif self.selected_browser == Browsers.EDGE:
            return webdriver.Edge()
        elif self.selected_browser == Browsers.SAFARI:
            return webdriver.Safari()
        elif self.selected_browser == Browsers.IE:
            return webdriver.Ie(options=opts)

        self.selected_browser = Browsers.FIREFOX
        return webdriver.Firefox(options=opts)

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
        opts = json.loads(opts)
        for key, val in opts.items():
            setattr(options, key, val)
        return options

    def setUp(self):
        # When running tests through github actions sometimes tables are empty, even though they are filled up in
        # migrations initialisation
        from examples.migrations import add_filter, add_page_load, add_relation
        from examples.models import Filter, PageLoad, Relation

        if not Filter.objects.count():
            add_filter(Filter)

        if not PageLoad.objects.count():
            add_page_load(PageLoad)

        if not Relation.objects.count():
            add_relation(Relation)

        self.github_actions = os.environ.get("GITHUB_ACTIONS", False)

        # first parameter: remote server
        # second parameter: "my" server

        # remote_selenium = 'MAC-SERVER:4444,myserver,SAFARI'
        # remote_selenium = 'WIN-SERVER:4444,myserver,FIREFOX|{"binary_location": "C:\\\\Program Files\\\\Mozilla
        #      Firefox\\\\firefox.exe"{comma} "headless": true}'
        remote_selenium = os.environ.get("REMOTE_SELENIUM", ",")

        # first parameter: selected browser
        # second parameter (optional): browser options in JSON format.
        browser_selenium = os.environ.get("BROWSER_SELENIUM", ";")
        # browser_selenium = 'CHROME;{"no-sandbox": true, "window-size": "1420,1080", "headless": true, ' \
        #                    '"disable-gpu": true}'
        # browser_selenium = 'FIREFOX;{"headless": true, ' \
        #                    '"binary_location": "C:\\\\Program Files\\\\Mozilla Firefox\\\\firefox.exe"}'

        browser_options = browser_selenium.split(";", 1)
        browser = browser_options[0]
        if browser:
            self.selected_browser = Browsers(browser)
        else:
            self.selected_browser = Browsers.FIREFOX

        # Spodaj je poizkus, da bi naložil driverje za EDGE... Inštalacija je bila sicer uspešna, ampak še vedno dobim
        # selenium.common.exceptions.WebDriverException: Message: Unknown error
        #
        # Bom počakal, da najprej zaključijo issue https://github.com/actions/virtual-environments/issues/99
        #
        # if self.github_actions and self.selected_browser == Browsers.EDGE:
        #     import sys
        #     driver_file = sys.exec_prefix + "\\Scripts\\msedgedriver.exe"
        #     if not os.path.isfile(driver_file):
        #         win_temp = os.environ.get('TEMP', '') + '\\'
        #         import urllib.request
        #         urllib.request.urlretrieve("https://msedgedriver.azureedge.net/81.0.394.0/edgedriver_win64.zip",
        #                                    win_temp + "edgedriver_win64.zip")
        #         import zipfile
        #         with zipfile.ZipFile(win_temp + "edgedriver_win64.zip", 'r') as zip_ref:
        #             zip_ref.extractall(win_temp)
        #         from shutil import copyfile
        #         copyfile(win_temp + "msedgedriver.exe", sys.exec_prefix + "\\Scripts\\msedgedriver.exe")
        #
        #         urllib.request.urlretrieve("https://download.microsoft.com/download/F/8/A/"
        #                                    "F8AF50AB-3C3A-4BC4-8773-DC27B32988DD/MicrosoftWebDriver.exe",
        #                                    win_temp + "MicrosoftWebDriver.exe")
        #         copyfile(win_temp + "MicrosoftWebDriver.exe", sys.exec_prefix + "\\Scripts\\MicrosoftWebDriver.exe")

        opts = None
        try:
            opts = self.get_browser_options(browser_options[1])
        except:
            pass

        remote, this_server = remote_selenium.split(",")
        if remote:
            self.browser = webdriver.Remote(
                command_executor="http://{remote}/wd/hub".format(remote=remote),
                desired_capabilities=dict(javascriptEnabled=True, **getattr(webdriver.DesiredCapabilities, browser)),
                options=opts,
            )

            olsu = self.live_server_url
            self.live_server_url = "http://{this_server}:{port}".format(
                this_server=this_server, port=self.live_server_url.split(":")[2]
            )
            print("Listen: ", olsu, " --> Remotely accessible on: ", self.live_server_url)
        else:
            self.browser = self.get_browser(opts)

    def tearDown(self):
        self.browser.refresh()
        self.browser.quit()

    def wait_for_new_element(self, element_id):
        if not callable(element_id):
            elid = element_id

            def element_id():
                return self.browser.find_element(By.ID, elid)

        start_time = time.time()
        while True:
            try:
                time.sleep(0.01)
                element = element_id()
                self.assertIsNotNone(element)
                return
            except (AssertionError, WebDriverException) as e:
                if time.time() - start_time > MAX_WAIT:
                    raise e

    def wait_for_modal_dialog(self, old_id=None):
        start_time = time.time()
        while True:
            try:
                time.sleep(0.01)
                element = None
                for el in self.browser.find_elements(By.CLASS_NAME, "modal"):
                    if el.is_displayed():
                        element = el
                        break
                self.assertIsNotNone(element)
                element_id = element.get_attribute("id")
                if old_id and element_id == "dialog-{old_id}".format(**locals()):
                    # The new dialog must not have same id as the old one
                    # if it does, this means that we're still looking at the old dialog - let's wait for it to go away
                    if time.time() - start_time > MAX_WAIT:
                        raise Exception("Timeout for old dialog to go away expired")
                    continue
                self.assertTrue(element_id.startswith("dialog-"))
                element_id = element_id.split("-", 1)[1]

                # this is a dialog - let's wait for its animations to stop
                try:
                    WebDriverWait(driver=self.browser, timeout=10, poll_frequency=0.2).until(
                        EC.element_to_be_clickable((By.CLASS_NAME, "btn"))
                    )
                except TimeoutException as e:
                    # dialog not ready yet or we found a bad dialog with no buttons
                    if time.time() - start_time > MAX_WAIT:
                        raise e
                    continue

                return element, element_id
            except (AssertionError, WebDriverException) as e:
                if time.time() - start_time > MAX_WAIT:
                    raise e

    def wait_for_modal_dialog_disapear(self, dialog_id):
        start_time = time.time()
        while True:
            try:
                time.sleep(0.01)
                if self.browser.find_element(By.ID, "dialog-{dialog_id}".format(**locals())) is None:
                    break
                self.assertFalse(time.time() - start_time > MAX_WAIT)
            except WebDriverException:
                break

    def get_alert(self, wait_time=None):
        if not wait_time:
            wait_time = MAX_WAIT_ALERT
        WebDriverWait(self.browser, wait_time).until(EC.alert_is_present(), "No alert dialog.")
        alert = self.browser.switch_to.alert
        return alert

    # noinspection PyMethodMayBeStatic
    def check_error_text(self, dialog):
        error_text = None
        try:
            error = dialog.find_element(By.CLASS_NAME, "text-danger")
            if error is not None:
                error_text = error.get_attribute("innerHTML")
        except WebDriverException:
            pass
        return error_text

    def initial_check(self, field, fld_text, fld_name, fld_type):
        self.assertEqual(self.get_element_text(field), fld_text)
        self.assertEqual(field.get_attribute("name"), fld_name)

        field_type = field.get_attribute("type")
        if isinstance(fld_type, tuple):
            self.assertIn(field_type, fld_type)
        else:
            self.assertEqual(field_type, fld_type)
        return field_type

    def get_table_body(self, whole_table=False, expected_rows: int = None):
        start_time = time.time()
        body = None
        while True:
            for cls in ["card-body", "panel-body", "ui-accordion-content"]:
                try:
                    body = self.browser.find_element(By.CLASS_NAME, cls)
                    if body:
                        break
                except NoSuchElementException:
                    self.assertFalse(time.time() - start_time > MAX_WAIT, "Wait time exceeded for table to appear")
                    time.sleep(0.01)
            if body:
                break

        table = body.find_element(By.TAG_NAME, "table")
        if whole_table:
            return table

        while True:
            rows = table.find_element(By.TAG_NAME, "tbody").find_elements(By.TAG_NAME, "tr")
            if not rows:
                # component renders "no data" in tfoot
                rows = table.find_element(By.TAG_NAME, "tfoot").find_elements(By.TAG_NAME, "tr")

            if expected_rows is not None and len(rows) != expected_rows:
                self.assertFalse(time.time() - start_time > MAX_WAIT, "Wait time exceeded for table rows to appear")
                time.sleep(0.01)
                continue
            else:
                break
        return rows

    def select_option_for_select2(self, driver, element_id, text=None):
        element = driver.find_element(By.XPATH, "//*[@id='{element_id}']/following-sibling::*[1]".format(**locals()))
        element.click()

        if text:
            element = element.parent.switch_to.active_element
            element.send_keys(text)

        try:
            element.send_keys(Keys.ENTER)
        except ElementNotInteractableException:
            actions = ActionChains(driver)
            a = actions.move_to_element_with_offset(element, 50, 30)
            a.send_keys(Keys.ENTER)
            a.perform()

    def check_row(self, row, cell_cnt, cell_values):
        cells = row.find_elements(By.TAG_NAME, "td")
        self.assertEqual(len(cells), cell_cnt)
        for i in range(len(cell_values)):
            if callable(cell_values[i]):
                cell_values[i](self.get_element_text(cells[i]))
            elif cell_values[i] is not None:
                self.assertEqual(self.get_element_text(cells[i]), cell_values[i])
        return cells

    def get_current_url(self):
        time.sleep(0.05)
        return self.browser.current_url

    def update_edge_field(self, field_id, value):
        self.browser.execute_script(
            """
        $('#%s').val('%s');
        dynamicforms.fieldChange('%s', 'final');
            """
            % (field_id, value, field_id)
        )

    @staticmethod
    def get_field_id_by_name(dialog, name):
        return dialog.find_element(By.NAME, name).get_attribute("id")

    @staticmethod
    def get_tag_name(el):
        return el.tag_name.lower()

    @staticmethod
    def get_element_text(el):
        tim = time.time()
        while True:
            res = el.text.strip()
            if "…" not in res or time.time() > tim + MAX_WAIT:
                break
            time.sleep(0.01)
        return res

    def clear_input(self, element):
        element.click()
        while len(element.get_attribute("value")):
            element.send_keys(Keys.BACKSPACE)
        element.clear()

    def find_element_by_classes(self, classes: Iterable):
        for cls in classes:
            try:
                return self.browser.find_element(By.CLASS_NAME, cls)
            except NoSuchElementException:
                pass
