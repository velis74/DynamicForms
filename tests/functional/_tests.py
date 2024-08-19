# TODO: unit tests for table_format za datetime polja. Preveriš pa, da output ni tak, kot narekuje SETTINGS.xxx_FORMAT
#   nastavitev. Pri tem pazi, ker je vse skupaj odvisno tudi od USE_L10N nastavitve: ta nastavitev pa še dodatno povozi
#   tudi SETTINGS.TIME_FORMAT (no, in ostala dva tudi)
# TODO: unit test za nested serializerje. Preveriti je tudi treba, če imajo field serializerji na voljo pravilne
#   row_data zapise
import time

from parameterized import parameterized
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from examples.models import AdvancedFields

from .select import Select
from .selenium_test_case import WaitingStaticLiveServerTestCase


class WriteOnlyAndTaggingTest(WaitingStaticLiveServerTestCase):
    @parameterized.expand(["html", "component"])
    def test_write_only_fields(self, renderer):
        af = AdvancedFields.objects.create(regex_field="abcdef", choice_field="123456")
        self.browser.get(self.live_server_url + "/write-only-fields." + renderer)
        table = self.get_table_body(whole_table=True)
        header = table.find_elements(By.CSS_SELECTOR, "thead tr th")
        self.assertEqual(len(header), 3)
        for idx, th in enumerate(header):
            if idx == 1:
                self.assertEqual(th.text.strip().replace(" ", ""), "Shown↕")
            else:
                self.assertNotEqual(th.text.strip(), "Hidden")
        body = table.find_elements(By.CSS_SELECTOR, "tbody tr td")
        self.assertEqual(len(body), 3)
        self.assertNotEqual(len(table.find_elements(By.CSS_SELECTOR, 'tbody tr td[data-name="choice_field"]')), 0)
        self.assertEqual(len(table.find_elements(By.CSS_SELECTOR, 'tbody tr td[data-name="regex_field"]')), 0)
        af.delete()

    @parameterized.expand(["html", "component"])
    def test_choice_allow_tags_fields(self, renderer):
        self.browser.get(self.live_server_url + "/choice-allow-tags-fields." + renderer)

        header = self.find_element_by_classes(("card-header", "panel-heading", "ui-accordion-header"))
        add_btn = header.find_elements(By.CLASS_NAME, "btn")
        add_btn[0].click()
        dialog, modal_serializer_id = self.wait_for_modal_dialog()

        form = dialog.find_element(By.ID, modal_serializer_id)
        containers = form.find_elements(By.TAG_NAME, "div")
        for container in containers:
            container_id = container.get_attribute("id")
            if container_id.startswith("container-"):
                field_id = container_id.split("-", 1)[1]
                label = container.find_element(By.ID, "label-" + field_id)
                field = container.find_element(By.ID, field_id)

                label_text = self.get_element_text(label)

                if label_text == "Choice":
                    select = Select(field)
                    select.send_keys("Custom text", send_enter=True)

                if label_text == "Multiple choice":
                    select = Select(field)
                    select.select_by_value(select.value_from_text("Multiple choice 1"))
                    select.send_keys("Custom text", send_enter=True)

        btn_element_id = ("save-" if renderer == "html" else "submit-") + modal_serializer_id

        WebDriverWait(driver=self.browser, timeout=10, poll_frequency=0.2).until(
            EC.element_to_be_clickable((By.ID, btn_element_id))
        )

        dialog.find_element(By.ID, btn_element_id).click()
        self.wait_for_modal_dialog_disapear(modal_serializer_id)
        time.sleep(1)
        rows = self.get_table_body(expected_rows=1)
        self.assertEqual(len(rows), 1)
        self.check_row(
            # Record ID's value doesn't matter
            rows[0],
            4,
            [None, "Custom text", "Multiple choice 1, Custom text", "Delete", None],
        )
        AdvancedFields.objects.all().delete()  # Clean up the created record so that the second pass of test may succeed
