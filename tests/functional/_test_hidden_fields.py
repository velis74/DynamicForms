from django.urls import reverse
from parameterized import parameterized
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from tests.functional.select import Select
from tests.functional.selenium_test_case import WaitingStaticLiveServerTestCase


class HiddenFieldsDialogTest(WaitingStaticLiveServerTestCase):
    @parameterized.expand(["html", "component"])
    def test_hidden_fields(self, renderer):
        def _check_shown(show_note, show_unit, show_int, show_qty, show_cst, show_add):
            unit = Select(form.find_element(By.CSS_SELECTOR, '[name="unit"]'))
            int_fld = form.find_element(By.CSS_SELECTOR, 'input[name="int_fld"]')
            qty_fld = form.find_element(By.CSS_SELECTOR, 'input[name="qty_fld"]')
            cst_fld = form.find_element(By.CSS_SELECTOR, 'input[name="cst_fld"]')
            add_text = form.find_element(By.CSS_SELECTOR, 'input[name="additional_text"]')
            add_container = form.find_element(By.ID, f'container-{add_text.get_attribute("id")}')

            self.assertEqual(note.is_displayed(), show_note)
            self.assertEqual(note_container.is_displayed(), show_note)
            self.assertEqual(unit.is_displayed(), show_unit)
            self.assertEqual(int_fld.is_displayed(), show_int)
            self.assertEqual(qty_fld.is_displayed(), show_qty)
            self.assertEqual(cst_fld.is_displayed(), show_cst)
            self.assertEqual(add_text.is_displayed(), show_add)
            self.assertEqual(add_container.is_displayed(), show_add)

        self.browser.get(self.live_server_url + reverse("hidden-fields-list", args=[renderer]))

        header = self.find_element_by_classes(("card-header", "panel-heading", "ui-accordion-header"))
        add_btn = header.find_element(By.CLASS_NAME, "btn")
        if add_btn.tag_name == "div":
            btn_text = self.get_element_text(add_btn.find_element(By.TAG_NAME, "span"))
        else:
            btn_text = self.get_element_text(add_btn)
        self.assertEqual(btn_text, "Add")

        add_btn.click()
        dialog, modal_serializer_id = self.wait_for_modal_dialog()

        form = dialog.find_element(By.ID, modal_serializer_id)
        note = form.find_element(By.CSS_SELECTOR, 'input[name="note"]')
        note_container = form.find_element(By.ID, f'container-{note.get_attribute("id")}')

        _check_shown(True, True, False, False, False, True)
        # If we enter "abc" unit field should be hidden
        note.send_keys("abc")
        note.send_keys(Keys.TAB)
        _check_shown(True, False, False, False, False, True)

        # Enter additional text... Unit should be shown again
        note.send_keys("abc")
        note.send_keys(Keys.TAB)
        _check_shown(True, True, False, False, False, True)

        # Select first option. No additional fields should be shown
        unit = Select(form.find_element(By.CSS_SELECTOR, '[name="unit"]'))
        unit.select_by_index(0)
        _check_shown(True, True, False, False, False, True)

        # Select second option. int_fld should be shown
        unit.select_by_index(1)
        _check_shown(True, True, True, False, False, True)

        # Select third option. qty_fld should be shown
        unit.select_by_index(2)
        _check_shown(True, True, False, True, False, True)

        # Select fourth option. int_fld and cst_fld should be shown
        unit.select_by_index(3)
        _check_shown(True, True, True, False, True, True)

        # Enter "abc" again. All fields regarding unit should be hidden
        note.clear()
        note.send_keys("abc")
        note.send_keys(Keys.TAB)
        _check_shown(True, False, False, False, False, True)
