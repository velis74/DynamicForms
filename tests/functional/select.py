import json

from collections import namedtuple
from enum import IntEnum
from typing import List, Union

from selenium.common.exceptions import ElementNotInteractableException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.select import Select as SeleniumSelect


class SelectType(IntEnum):
    GENERIC = 0
    SELECT2 = 1
    COMPONENT = 2


SelectOption = namedtuple("SelectOption", ("value, text"))


class SelectOptions(dict):
    """Contains data values of currently selected select options"""

    @property
    def single(self):
        """returns the only selected element after confirming it actually is the only one"""
        assert len(self) == 1
        return SelectOption(*next(iter(self.items())))

    @property
    def empty(self):
        return len(self) == 0 or self.single.value == ""


class Select:
    def __init__(self, field: WebElement):
        self.element = field

    @property
    def id(self):
        return self.element.get_attribute("id")

    @property
    def _browser(self) -> WebDriver:
        return self.element.parent

    @property
    def select_type(self) -> SelectType:
        if "select2-field" in self.element.get_attribute("class"):
            return SelectType.SELECT2
        elif "df-select-class" in self.element.get_attribute("class"):
            return SelectType.COMPONENT
        return SelectType.GENERIC

    @property
    def current_selection(self):
        if self.select_type == SelectType.COMPONENT:
            return SelectOptions(
                {k: v for k, v in self.options.items() if str(k) in self.element.get_attribute("data-value").split(",")}
            )
        select = SeleniumSelect(self.element)
        selected_options = select.all_selected_options
        return SelectOptions(map(lambda x: (x.get_attribute("value").strip(), x.text.strip()), selected_options))

    @property
    def options(self):
        if self.select_type == SelectType.COMPONENT:
            options = json.loads(self.element.get_attribute("data-options"))
            return SelectOptions(map(lambda x: (x["id"], x["text"]), options))

        select = SeleniumSelect(self.element)
        options = select.options
        return SelectOptions(map(lambda x: (x.get_attribute("value").strip(), x.text.strip()), options))

    def select_by_value(self, value: Union[str, List[str]]):
        if self.select_type == SelectType.COMPONENT:
            value = repr(value) if value is not None else "null"
            self._browser.execute_script(f"window['setSelectValue {self.id}']({value});")
        elif self.select_type == SelectType.SELECT2:
            element = self.element.parent.find_element(By.XPATH, f"//*[@id='{self.id}']/following-sibling::*[1]")
            element.click()

            if not isinstance(value, (list, tuple)):
                value = [value]

            for val in value:
                if val:
                    select = SeleniumSelect(self.element)
                    for option in select.options:
                        if option.get_attribute("value").strip() == val:
                            val = option.text.strip()
                            break

                    element = element.parent.switch_to.active_element
                    element.send_keys(val)

                try:
                    element.send_keys(Keys.ENTER)
                except ElementNotInteractableException:
                    actions = ActionChains(self.element.parent)
                    a = actions.move_to_element_with_offset(element, 50, 30)
                    a.send_keys(Keys.ENTER)
                    a.perform()
        else:
            select = SeleniumSelect(self.element)
            select.select_by_value(value)
        # select_by_value

    def select_by_index(self, idx):
        return self.select_by_value(list(self.options.keys())[idx])

    def send_keys(self, txt, send_enter: bool = False):
        if self.select_type == SelectType.SELECT2:
            element = self.element.parent.find_element(By.XPATH, f"//*[@id='{self.id}']/following-sibling::*[1]")
            element.click()
            element = element.parent.switch_to.active_element
            element.send_keys(txt)

            if send_enter:
                try:
                    element.send_keys(Keys.ENTER)
                except ElementNotInteractableException:
                    actions = ActionChains(self.element.parent)
                    a = actions.move_to_element_with_offset(element, 50, 30)
                    a.send_keys(Keys.ENTER)
                    a.perform()
        elif self.select_type == SelectType.COMPONENT:
            self.element.click()  # get it into input mode
            inp = self.element.find_element(By.TAG_NAME, "input")
            inp.send_keys(txt)
            if send_enter:
                inp.send_keys(Keys.ENTER)
        else:
            self.element.send_keys(txt)
            if send_enter:
                self.element.send_keys(Keys.ENTER)

    def value_from_text(self, txt):
        for k, v in self.options.items():
            if v == txt:
                return k
        return None

    def is_displayed(self):
        return self.element.is_displayed()
