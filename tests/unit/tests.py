import json

from django.test import TestCase

from examples.models import Validated


class ValidatedPageTest(TestCase):
    base_url = "/validated/{}{}"

    def test_get_return(self):
        validate_ = Validated.objects.create(code="123", enabled=False, amount=5, item_type=2, item_flags="A")
        response = self.client.get(self.base_url.format(validate_.id, "/"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["content-type"], "application/json")
        response = self.client.get(self.base_url.format(validate_.id, ".json"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["content-type"], "application/json")

    def test_get_return_correct_record(self):
        Validated.objects.create(code="123", enabled=False, amount=5, item_type=2, item_flags="A")
        our_record = Validated.objects.create(code="12345", enabled=True, amount=5, item_type=1, item_flags="B")
        response = self.client.get(self.base_url.format(our_record.id, "/"))
        self.assertEqual(
            json.loads(response.content.decode("utf8")),
            {
                "id": our_record.id,
                "code": our_record.code,
                "enabled": our_record.enabled,
                "amount": our_record.amount,
                "item_type": 1,
                "item_type-display": "Choice 2",
                "item_flags": "B",
                "item_flags-display": "Beta",
                "comment": our_record.comment,
                "df_prev_id": "",
                "row_css_style": "",
                "df_control_data": {"actions": {"delete": {}, "edit": {}, "sort": {}}, "row_css_style": ""},
            },
        )

    def testPOSTing_a_new_record(self):
        response = self.client.post(
            "/validated.json?df_render_type=dialog",
            # self.base_url.format("new", "/"),
            {"code": "123", "enabled": True, "amount": 7, "item_type": 2, "item_flags": "A"},
        )
        self.assertEqual(response.status_code, 201)
        our_record = Validated.objects.filter(code=123, enabled=True, amount=7, item_type=2, item_flags="A").get()
        self.assertTrue(our_record is not None)

    def testPUTing_an_existing_record(self):
        Validated.objects.create(code="123", enabled=False, amount=5, item_type=2, item_flags="A")
        our_record = Validated.objects.create(code="12345", enabled=True, amount=5, item_type=1, item_flags="B")

        response = self.client.put(
            self.base_url.format(our_record.id, ".json?df_render_type=dialog"),
            '{"code": "12345", "enabled": false, "amount": 5, "item_type": 1, "item_flags": "B"}',
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        our_record = Validated.objects.filter(pk=our_record.pk).get()
        self.assertEqual(our_record.enabled, False)
