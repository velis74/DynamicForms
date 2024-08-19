import datetime
import json

import pytz

from django.forms import model_to_dict
from django.urls import reverse
from parameterized import parameterized
from rest_framework import status
from rest_framework.test import APITestCase

from dynamicforms.template_render.mixins.util import convert_to_json_if
from examples.models import CalendarEvent, CalendarRecurrence, CalendarReminder
from examples.recurrence_utils import (
    date_range_daily,
    date_range_monthly,
    date_range_weekly,
    date_range_yearly,
    locale_weekdays,
)
from examples.rest.calendar import CalendarEventSerializer


class CommonTestBase(APITestCase):
    def get_json(self, response, expected_status):
        if response.status_code == status.HTTP_400_BAD_REQUEST and response.status_code != expected_status:
            print("You did something bad!!!")
            print(response.content)
        self.assertEqual(expected_status, response.status_code)
        if expected_status == status.HTTP_204_NO_CONTENT:
            return None
        self.assertEqual("application/json", response["content-type"])
        return json.loads(response.content.decode("utf-8"))

    def encode_json(self, data):
        return convert_to_json_if(data, True).encode("utf-8")

    def retrieve_event_id(self, id: int):
        event_url = reverse("calendar-event-detail", kwargs=dict(pk=id, format="json"))
        response = self.get_json(self.client.get(event_url), status.HTTP_200_OK)
        self.assertTrue(response)
        return response

    def check_event_as_expected(self, response: dict, expected_response: dict):
        response = self.order_weekdays_choices(response)
        expected_response = self.order_weekdays_choices(expected_response)
        trimmed_response = {k: response[k] for k in expected_response.keys()}
        if "recurrence" in trimmed_response and trimmed_response["recurrence"]:
            trimmed_response["recurrence"] = {
                k: trimmed_response["recurrence"][k] for k in expected_response["recurrence"].keys()
            }
        if "reminders" in trimmed_response and trimmed_response["reminders"] and expected_response["reminders"]:
            trimmed_response["reminders"] = [
                {k: reminder[k] for k in expected_response["reminders"][0].keys()}
                for reminder in trimmed_response["reminders"]
            ]
        self.assertEqual(expected_response, trimmed_response)
        self.assertIn("id", response)
        inserted_id = response["id"]
        self.assertIsInstance(inserted_id, int)
        return inserted_id

    def dates_to_iso(self, res):
        if isinstance(res, dict):
            return {k: self.dates_to_iso(v) for k, v in res.items()}
        elif isinstance(res, list):
            return list((self.dates_to_iso(i) for i in res))
        elif isinstance(res, datetime.datetime):
            return res.isoformat().replace("+00:00", "Z")
        return res

    # noinspection PyTypedDict
    def get_event_def(
        self,
        dates_iso: bool = True,
        skip_recurrence: bool = False,
        num_reminders: int = 0,
    ):
        start_at = datetime.datetime(2020, 1, 30, 10, 0, tzinfo=pytz.utc)
        res = dict(
            title="Party time",
            colour=0x000008,
            start_at=start_at,
            end_at=start_at + datetime.timedelta(hours=1),
            recurrence=dict(
                start_at=start_at,
                end_at=start_at + datetime.timedelta(days=11),
                pattern=CalendarRecurrence.Pattern.Weekly.value,
                recur=dict(every=1, weekdays=["mo", "we", "su", "ho"]),
            ),
        )
        if num_reminders:
            r_type, unit = CalendarReminder.RType, CalendarReminder.Unit
            res["reminders"] = [
                dict(type=r_type.Notification.value, unit=unit.Hours.value, quantity=1),
                dict(type=r_type.Email.value, unit=unit.Minutes.value, quantity=90),
                dict(type=r_type.Notification.value, unit=unit.Days.value, quantity=3),
                dict(type=r_type.Email.value, unit=unit.Seconds.value, quantity=432000),
            ][:num_reminders]
        if dates_iso:
            res = self.dates_to_iso(res)
        if skip_recurrence:
            res.pop("recurrence")
        return res

    def event_to_request_def(self, event):
        recurrence = event.get("recurrence", None)
        if recurrence is not None:
            recur = recurrence.get("recur", {})
            if (val := recur.get("every", None)) is not None:
                recurrence["every"] = val
            if (val := recur.get("weekdays", None)) is not None:
                recurrence["weekdays"] = val
            if (val := recur.get("days", None)) is not None:
                recurrence["days"] = val
            if (val := recur.get("dates", None)) is not None:
                recurrence["dates"] = val
            recurrence.pop("recur")
            event["recurrence"] = recurrence

        return event

    def get_event_request_def(
        self,
        dates_iso: bool = True,
        skip_recurrence: bool = False,
        num_reminders: int = 0,
    ):
        return self.event_to_request_def(self.get_event_def(dates_iso, skip_recurrence, num_reminders))

    def order_weekdays_choices(self, event):
        recurrence = event.get("recurrence", None)
        if recurrence is not None:
            if (weekdays := recurrence.get("weekdays", None)) is not None:
                event["recurrence"]["weekdays"] = [day for day in locale_weekdays() if day in weekdays]
        return event


class CalendarEventTest(CommonTestBase):
    def test_basic_operations(self):
        # check that table is empty and the API is working
        event_url = reverse("calendar-event-list", args=["json"])
        response = self.get_json(self.client.get(event_url), status.HTTP_200_OK)
        self.assertTrue(not response)  # we are expecting that there are no records in the events table

        # Insert a new event
        event = dict(
            title="Party time",
            colour=0x000008,
            start_at=datetime.datetime(2020, 1, 30, 10, 0, tzinfo=pytz.utc),
            end_at=datetime.datetime(2020, 1, 30, 11, 0, tzinfo=pytz.utc),
        )

        response = self.get_json(
            self.client.post(event_url, data=self.encode_json(event), content_type="application/json"),
            status.HTTP_201_CREATED,
        )
        expected_response = dict(
            title="Party time",
            description=None,
            colour=0x000008,
            start_at="2020-01-30T10:00:00Z",
            end_at="2020-01-30T11:00:00Z",
        )
        trimmed_response = {k: response[k] for k in expected_response.keys()}
        self.assertEqual(expected_response, trimmed_response)
        self.assertIn("id", response)
        self.assertNotIn("recurrence", response)  # nested serializers don't get serialized when None
        inserted_id = response["id"]
        self.assertIsInstance(inserted_id, int)

        # retrieve the new event
        response = self.retrieve_event_id(inserted_id)
        self.check_event_as_expected(response, expected_response)

        # patch the event, change only description
        event_url = reverse("calendar-event-detail", kwargs=dict(pk=inserted_id, format="json"))
        event = dict(description="Let's rock this place!")
        response = self.get_json(
            self.client.patch(event_url, data=self.encode_json(event), content_type="application/json"),
            status.HTTP_200_OK,
        )
        expected_response["description"] = event["description"]
        self.check_event_as_expected(response, expected_response)

        # delete the event
        response = self.get_json(self.client.delete(event_url), status.HTTP_204_NO_CONTENT)
        self.assertIsNone(response)


class CalendarRecurrenceUtilsTest(CommonTestBase):
    @parameterized.expand([(None,), (datetime.datetime(2021, 11, 17, 0, 0),)])
    def test_recurrence_generator_daily(self, cutoff_at):
        def D(d):
            return datetime.date(2021, 11, d)

        # first, let's test a daily generator, every single day
        res = list(
            date_range_daily(
                datetime.datetime(2021, 11, 13, 16, 0), datetime.datetime(2021, 11, 23, 16, 0), cutoff_at, 1
            )
        )
        expected_res = list(
            filter(
                lambda x: cutoff_at is None or x >= cutoff_at,
                map(lambda x: datetime.datetime.combine(x, datetime.time(16, 0)), map(D, range(13, 24))),
            )
        )
        self.assertEqual(res, expected_res)

        # every three days
        res = list(
            date_range_daily(
                datetime.datetime(2021, 11, 13, 16, 0), datetime.datetime(2021, 11, 23, 16, 0), cutoff_at, 3
            )
        )
        expected_res = list(
            filter(
                lambda x: cutoff_at is None or x >= cutoff_at,
                map(lambda x: datetime.datetime.combine(x, datetime.time(16, 0)), (D(13), D(16), D(19), D(22))),
            )
        )
        self.assertEqual(res, expected_res)

    @parameterized.expand([(None,), (datetime.datetime(2021, 11, 17, 0, 0),)])
    def test_recurrence_generator_weekly(self, cutoff_at):
        def D(d):
            return datetime.date(2021, 11, d)

        # first, we test a simple, repeat on various days of the week, pattern
        res = list(
            date_range_weekly(
                datetime.datetime(2021, 11, 13, 16, 0),
                datetime.datetime(2021, 11, 23, 16, 0),
                cutoff_at,
                1,
                ["Monday", "Wednesday", "Fr", "Sun"],
                set(),
            )
        )
        expected_res = list(
            filter(
                lambda x: cutoff_at is None or x >= cutoff_at,
                map(
                    lambda x: datetime.datetime.combine(x, datetime.time(16, 0)),
                    (D(13), D(14), D(15), D(17), D(19), D(21), D(22)),
                ),
            )
        )
        self.assertEqual(res, expected_res)

        # now we also try every other week
        res = list(
            date_range_weekly(
                datetime.datetime(2021, 11, 13, 16, 0),
                datetime.datetime(2021, 11, 23, 16, 0),
                cutoff_at,
                2,
                ["Mo"],
                set(),
            )
        )
        expected_res = list(
            filter(
                lambda x: cutoff_at is None or x >= cutoff_at,
                map(lambda x: datetime.datetime.combine(x, datetime.time(16, 0)), (D(13), D(22))),
            )
        )
        self.assertEqual(res, expected_res)

        # and holidays too
        res = list(
            date_range_weekly(
                datetime.datetime(2021, 11, 13, 16, 0),
                datetime.datetime(2021, 11, 23, 16, 0),
                cutoff_at,
                2,
                ["Mo", "Ho"],
                {D(23)},
            )
        )
        expected_res = list(
            filter(
                lambda x: cutoff_at is None or x >= cutoff_at,
                map(lambda x: datetime.datetime.combine(x, datetime.time(16, 0)), (D(13), D(22), D(23))),
            )
        )
        self.assertEqual(res, expected_res)

    @parameterized.expand([(None,), (datetime.datetime(2021, 11, 28, 0, 0),)])
    def test_recurrence_generator_monthly(self, cutoff_at):
        """
        { days: List[int|Union[weekday_modifier: Enum(first, last, second, third, fourth), weekday: str]] }
        - days is a list of days in a month when this event is recurring
        - the days can be specified as integers (e.g. 1, 15, 23) or with a modifier (e.g. first we, 3rd thu, last fr)
        """

        def nov(d):
            return datetime.datetime(2021, 11, d, 16, 0)

        def dec(d):
            return datetime.datetime(2021, 12, d, 16, 0)

        # first, we test a simple, repeat on various days of the week, pattern
        res = list(
            date_range_monthly(
                datetime.datetime(2021, 11, 13, 16, 0),
                datetime.datetime(2021, 12, 31, 16, 0),
                cutoff_at,
                [5, 14, 22, "first mo", "last fr", ("2nd", "tu")],
            )
        )
        # print(res)
        expected_res = list(
            filter(
                lambda x: cutoff_at is None or x >= cutoff_at,
                map(
                    lambda x: datetime.datetime.combine(x, datetime.time(16, 0)),
                    (nov(13), nov(14), nov(22), nov(26), dec(5), dec(6), dec(14), dec(22), dec(31)),
                ),
            )
        )
        # print(expected_res)
        self.assertEqual(res, expected_res)

    @parameterized.expand([(None,), (datetime.datetime(2021, 12, 28, 0, 0),)])
    def test_recurrence_generator_yearly(self, cutoff_at):
        """
        { dates: List[Tuple[int, int]] }
        - dates is a list of (day, month). in a year when the event occurs
        """

        def D(y, m, d):
            return datetime.datetime(y, m, d, 16, 0)

        # first, we test a simple, repeat on various days of the week, pattern
        res = list(
            date_range_yearly(
                datetime.datetime(2021, 11, 13, 16, 0),
                datetime.datetime(2022, 9, 1, 16, 0),
                cutoff_at,
                [(2, 5), (15, 6), (31, 7), (1, 10), (19, 11)],
            )
        )
        expected_res = list(
            filter(
                lambda x: cutoff_at is None or x >= cutoff_at,
                map(
                    lambda x: datetime.datetime.combine(x, datetime.time(16, 0)),
                    (D(2021, 11, 13), D(2021, 11, 19), D(2022, 5, 2), D(2022, 6, 15), D(2022, 7, 31)),
                ),
            )
        )
        self.assertEqual(res, expected_res)


class CalendarRecurrenceTest(CommonTestBase):
    def test_recurrence_basic(self):
        # First we create a calendar event with a recurrence using models API
        event = self.get_event_def(dates_iso=False)
        event["recurrence"] = CalendarRecurrence.objects.create(**event["recurrence"])
        cal_evnt = CalendarEvent.objects.create(**event)

        # Get the created event from database
        event_url = reverse("calendar-event-list", args=["json"])
        response = self.get_json(self.client.get(event_url), status.HTTP_200_OK)
        self.assertTrue(response)
        self.assertIsInstance(response, list)
        self.assertEqual(1, len(response))
        response = response[0]  # Get the first record

        expected_response = self.get_event_request_def(dates_iso=True)
        self.check_event_as_expected(response, expected_response)

        # Get the created event from database, this time in form mode
        expected_response = self.get_event_request_def(dates_iso=True)
        response = self.retrieve_event_id(cal_evnt.id)
        self.check_event_as_expected(response, expected_response)

        # remove the created event from database
        cal_evnt.delete()
        cal_evnt.recurrence.delete()  # this should fail once recurrence actually creates the additional events

    def test_recurrence_post_get(self):
        # Insert a new event via API
        event = self.get_event_request_def(dates_iso=True)
        event_url = reverse("calendar-event-list", args=["json"])
        response = self.get_json(
            self.client.post(event_url, data=self.encode_json(event), content_type="application/json"),
            status.HTTP_201_CREATED,
        )
        recurrence_id = response["recurrence"]["id"]
        # First check if result of POST is as expected
        expected_response = dict(event)
        self.check_event_as_expected(response, expected_response)
        self.assertEqual(recurrence_id, response["recurrence"]["id"])

        # check if all events were created as per recurrence
        event_url = reverse("calendar-event-list", args=["json"])
        response = self.get_json(self.client.get(event_url), status.HTTP_200_OK)
        self.assertTrue(response)
        self.assertIsInstance(response, list)
        self.assertEqual(6, len(response))
        instance_ids = tuple(map(lambda x: x["id"], response))

        # check all instances to be as they need to be
        for instance_id, d in zip(instance_ids, (0, 3, 4, 6, 10, 11)):
            response = self.retrieve_event_id(instance_id)  # 3rd instance is the one on 3.2.2020
            expected_response["id"] = instance_id
            delta = datetime.timedelta(days=d)
            expected_response["start_at"] = (datetime.datetime(2020, 1, 30, 10) + delta).isoformat() + "Z"
            expected_response["end_at"] = (datetime.datetime(2020, 1, 30, 11) + delta).isoformat() + "Z"
            self.assertEqual(instance_id, self.check_event_as_expected(response, expected_response))
            self.assertEqual(recurrence_id, response["recurrence"]["id"])

        # Then retrieve the record from the API
        response = self.retrieve_event_id(instance_ids[2])  # 3rd instance is the one on 3.2.2020
        expected_response["id"] = instance_ids[2]
        expected_response["start_at"] = "2020-02-03T10:00:00Z"
        expected_response["end_at"] = "2020-02-03T11:00:00Z"
        self.assertEqual(instance_ids[2], self.check_event_as_expected(response, expected_response))
        self.assertEqual(recurrence_id, response["recurrence"]["id"])

        for change_this_record_only in (True, False):
            # change one event only or this event and all events after it
            event = dict(expected_response)
            event["description"] = "one changed event"
            event["recurrence"]["id"] = recurrence_id
            event["change_this_record_only"] = change_this_record_only
            event_url = reverse("calendar-event-detail", kwargs=dict(pk=instance_ids[2], format="json"))
            response = self.get_json(
                self.client.put(event_url, data=self.encode_json(event), content_type="application/json"),
                status.HTTP_200_OK,
            )
            expected_response["description"] = "one changed event"
            self.check_event_as_expected(response, expected_response)

            # check that events are as they're supposed to be after the one change
            event_url = reverse("calendar-event-list", args=["json"])
            response = self.get_json(self.client.get(event_url), status.HTTP_200_OK)
            self.assertTrue(response)
            self.assertIsInstance(response, list)
            self.assertEqual(6, len(response))
            instance_ids = tuple(map(lambda x: x["id"], response))
            for d in (0, 3, 4, 6, 10, 11):
                current_event = response.pop(0)
                self.assertEqual(
                    (datetime.datetime(2020, 1, 30, 10) + datetime.timedelta(days=d)).isoformat() + "Z",
                    current_event["start_at"],
                )
                # The algorithm now changes all events following the changed event
                if change_this_record_only:
                    self.assertEqual(None if d != 4 else "one changed event", current_event["description"])
                else:
                    self.assertEqual(None if d < 4 else "one changed event", current_event["description"])

    def test_recurrence_shorten(self):
        # Insert a new event via API
        event = self.get_event_request_def(dates_iso=True)
        event_url = reverse("calendar-event-list", args=["json"])
        response = self.get_json(
            self.client.post(event_url, data=self.encode_json(event), content_type="application/json"),
            status.HTTP_201_CREATED,
        )
        recurrence_id = response["recurrence"]["id"]
        # First check if result of POST is as expected
        expected_response = dict(event)
        self.check_event_as_expected(response, expected_response)
        self.assertEqual(recurrence_id, response["recurrence"]["id"])

        # check if all events were created as per recurrence
        event_url = reverse("calendar-event-list", args=["json"])
        response = self.get_json(self.client.get(event_url), status.HTTP_200_OK)
        self.assertTrue(response)
        self.assertIsInstance(response, list)
        self.assertEqual(6, len(response))
        instance_ids = tuple(map(lambda x: x["id"], response))

        # check all instances to be as they need to be
        for instance_id, d in zip(instance_ids, (0, 3, 4, 6, 10, 11)):
            response = self.retrieve_event_id(instance_id)  # 3rd instance is the one on 3.2.2020
            expected_response["id"] = instance_id
            delta = datetime.timedelta(days=d)
            expected_response["start_at"] = (datetime.datetime(2020, 1, 30, 10) + delta).isoformat() + "Z"
            expected_response["end_at"] = (datetime.datetime(2020, 1, 30, 11) + delta).isoformat() + "Z"
            self.assertEqual(instance_id, self.check_event_as_expected(response, expected_response))
            self.assertEqual(recurrence_id, response["recurrence"]["id"])

        # Then retrieve the record from the API
        response = self.retrieve_event_id(instance_ids[2])  # 3rd instance is the one on 3.2.2020
        expected_response["id"] = instance_ids[2]
        expected_response["start_at"] = "2020-02-03T10:00:00Z"
        expected_response["end_at"] = "2020-02-03T11:00:00Z"
        self.assertEqual(instance_ids[2], self.check_event_as_expected(response, expected_response))
        self.assertEqual(recurrence_id, response["recurrence"]["id"])

        # shorten recurrence
        event = dict(expected_response)
        event["recurrence"]["id"] = recurrence_id
        event["recurrence"]["end_at"] = event["end_at"]
        event_url = reverse("calendar-event-detail", kwargs=dict(pk=instance_ids[2], format="json"))
        response = self.get_json(
            self.client.put(event_url, data=self.encode_json(event), content_type="application/json"),
            status.HTTP_200_OK,
        )
        self.check_event_as_expected(response, expected_response)

        # check that events are as they're supposed to be after the one change
        event_url = reverse("calendar-event-list", args=["json"])
        response = self.get_json(self.client.get(event_url), status.HTTP_200_OK)
        self.assertTrue(response)
        self.assertIsInstance(response, list)
        self.assertEqual(3, len(response))
        instance_ids = tuple(map(lambda x: x["id"], response))
        for d in (0, 3, 4):
            current_event = response.pop(0)
            self.assertEqual(
                (datetime.datetime(2020, 1, 30, 10) + datetime.timedelta(days=d)).isoformat() + "Z",
                current_event["start_at"],
            )

    def test_recurrence_remove(self):
        # remove recurrence altogether
        event = self.get_event_request_def(dates_iso=True)
        event_url = reverse("calendar-event-list", args=["json"])
        response = self.get_json(
            self.client.post(event_url, data=self.encode_json(event), content_type="application/json"),
            status.HTTP_201_CREATED,
        )
        recurrence_id = response["recurrence"]["id"]
        # First check if result of POST is as expected
        expected_response = dict(event)
        self.check_event_as_expected(response, expected_response)
        self.assertEqual(recurrence_id, response["recurrence"]["id"])

        # check if all events were created as per recurrence
        event_url = reverse("calendar-event-list", args=["json"])
        response = self.get_json(self.client.get(event_url), status.HTTP_200_OK)
        self.assertTrue(response)
        self.assertIsInstance(response, list)
        self.assertEqual(6, len(response))
        instance_ids = tuple(map(lambda x: x["id"], response))

        # check all instances to be as they need to be
        for instance_id, d in zip(instance_ids, (0, 3, 4, 6, 10, 11)):
            response = self.retrieve_event_id(instance_id)  # 3rd instance is the one on 3.2.2020
            expected_response["id"] = instance_id
            delta = datetime.timedelta(days=d)
            expected_response["start_at"] = (datetime.datetime(2020, 1, 30, 10) + delta).isoformat() + "Z"
            expected_response["end_at"] = (datetime.datetime(2020, 1, 30, 11) + delta).isoformat() + "Z"
            self.assertEqual(instance_id, self.check_event_as_expected(response, expected_response))
            self.assertEqual(recurrence_id, response["recurrence"]["id"])

        # Then retrieve the record from the API
        response = self.retrieve_event_id(instance_ids[0])  # 3rd instance is the one on 3.2.2020
        expected_response = self.get_event_request_def(dates_iso=True)
        self.assertEqual(instance_ids[0], self.check_event_as_expected(response, expected_response))
        self.assertEqual(recurrence_id, response["recurrence"]["id"])

        # remove recurrence
        event = dict(expected_response)
        event.pop("recurrence", None)
        event_url = reverse("calendar-event-detail", kwargs=dict(pk=instance_ids[0], format="json"))
        response = self.get_json(
            self.client.put(event_url, data=self.encode_json(event), content_type="application/json"),
            status.HTTP_200_OK,
        )
        expected_response.pop("recurrence", None)
        self.check_event_as_expected(response, expected_response)
        self.assertIsNone(response.get("recurrence", None))

        # check that events are as they're supposed to be after the one change
        event_url = reverse("calendar-event-list", args=["json"])
        response = self.get_json(self.client.get(event_url), status.HTTP_200_OK)
        self.assertTrue(response)
        self.assertIsInstance(response, list)
        self.assertEqual(1, len(response))
        for d in (0,):
            current_event = response.pop(0)
            self.assertEqual(
                (datetime.datetime(2020, 1, 30, 10) + datetime.timedelta(days=d)).isoformat() + "Z",
                current_event["start_at"],
            )

    def test_recurrence_remove_middle(self):
        # remove recurrence in the middle of the recurrence
        event = self.get_event_request_def(dates_iso=True)
        event_url = reverse("calendar-event-list", args=["json"])
        response = self.get_json(
            self.client.post(event_url, data=self.encode_json(event), content_type="application/json"),
            status.HTTP_201_CREATED,
        )
        recurrence_id = response["recurrence"]["id"]
        # First check if result of POST is as expected
        expected_response = dict(event)
        self.check_event_as_expected(response, expected_response)
        self.assertEqual(recurrence_id, response["recurrence"]["id"])

        # check if all events were created as per recurrence
        event_url = reverse("calendar-event-list", args=["json"])
        response = self.get_json(self.client.get(event_url), status.HTTP_200_OK)
        self.assertTrue(response)
        self.assertIsInstance(response, list)
        self.assertEqual(6, len(response))
        instance_ids = tuple(map(lambda x: x["id"], response))

        # check all instances to be as they need to be
        for instance_id, d in zip(instance_ids, (0, 3, 4, 6, 10, 11)):
            response = self.retrieve_event_id(instance_id)  # 3rd instance is the one on 3.2.2020
            expected_response["id"] = instance_id
            delta = datetime.timedelta(days=d)
            expected_response["start_at"] = (datetime.datetime(2020, 1, 30, 10) + delta).isoformat() + "Z"
            expected_response["end_at"] = (datetime.datetime(2020, 1, 30, 11) + delta).isoformat() + "Z"
            self.assertEqual(instance_id, self.check_event_as_expected(response, expected_response))
            self.assertEqual(recurrence_id, response["recurrence"]["id"])

        # Then retrieve the record from the API
        instance_id = instance_ids[2]
        response = self.retrieve_event_id(instance_id)  # 3rd instance is the one on 3.2.2020
        expected_response = self.get_event_request_def(dates_iso=True)
        expected_response["id"] = instance_ids[2]
        expected_response["start_at"] = "2020-02-03T10:00:00Z"
        expected_response["end_at"] = "2020-02-03T11:00:00Z"
        self.assertEqual(instance_id, self.check_event_as_expected(response, expected_response))
        self.assertEqual(recurrence_id, response["recurrence"]["id"])

        # remove recurrence
        event = dict(expected_response)
        event.pop("recurrence", None)
        event_url = reverse("calendar-event-detail", kwargs=dict(pk=instance_id, format="json"))
        response = self.get_json(
            self.client.put(event_url, data=self.encode_json(event), content_type="application/json"),
            status.HTTP_200_OK,
        )
        # we expect recurrence to still be there because we only removed it from FUTURE events, but not past ones
        self.check_event_as_expected(response, expected_response)

        # check that events are as they're supposed to be after the one change
        event_url = reverse("calendar-event-list", args=["json"])
        response = self.get_json(self.client.get(event_url), status.HTTP_200_OK)
        self.assertTrue(response)
        self.assertIsInstance(response, list)
        self.assertEqual(3, len(response))
        expected_response = self.get_event_def(dates_iso=True)
        for instance_id, d in zip(instance_ids, (0, 3, 4)):
            response = self.retrieve_event_id(instance_id)  # 3rd instance is the one on 3.2.2020
            expected_response["id"] = instance_id
            delta = datetime.timedelta(days=d)
            expected_response["start_at"] = (datetime.datetime(2020, 1, 30, 10) + delta).isoformat() + "Z"
            expected_response["end_at"] = (datetime.datetime(2020, 1, 30, 11) + delta).isoformat() + "Z"
            expected_response.pop("recurrence", None)
            self.assertEqual(instance_id, self.check_event_as_expected(response, expected_response))
            self.assertEqual(recurrence_id, response["recurrence"]["id"])

    def test_days_value_transformations(self):
        start_at = datetime.datetime(2020, 1, 30, 10, 0, tzinfo=pytz.utc)
        days_string = "13, 12, 1st mo, 2nd fr, las th"
        days_value = ["13", "12", ["1st", "mo"], ["2nd", "fr"], ["las", "th"]]
        event = dict(
            title="Party time",
            colour=0x000008,
            start_at=start_at,
            end_at=start_at + datetime.timedelta(hours=1),
            recurrence=dict(
                start_at=start_at,
                end_at=start_at + datetime.timedelta(days=11),
                pattern=CalendarRecurrence.Pattern.Monthly.value,
                recur=dict(days=days_string),
            ),
        )

        # to internal value
        ser = CalendarEventSerializer()
        internal_value = ser.to_internal_value(self.event_to_request_def(event))

        self.assertEqual(internal_value["recurrence"]["recur"]["days"], days_value)

        # to representation
        event["recurrence"] = CalendarRecurrence.objects.create(**internal_value["recurrence"])
        cal_event = CalendarEvent.objects.create(**event)
        representation = ser.to_representation(cal_event)

        self.assertEqual(representation["recurrence"]["days"], days_string)

    def test_dates_value_transformations(self):
        start_at = datetime.datetime(2020, 1, 30, 10, 0, tzinfo=pytz.utc)
        dates_string = "12.2, 29.2, 11.11, 20.12"
        dates_value = [["12", "2"], ["29", "2"], ["11", "11"], ["20", "12"]]
        event = dict(
            title="Party time",
            colour=0x000008,
            start_at=start_at,
            end_at=start_at + datetime.timedelta(hours=1),
            recurrence=dict(
                start_at=start_at,
                end_at=start_at + datetime.timedelta(days=11),
                pattern=CalendarRecurrence.Pattern.Yearly.value,
                recur=dict(dates=dates_string),
            ),
        )

        # to internal value
        ser = CalendarEventSerializer()
        internal_value = ser.to_internal_value(self.event_to_request_def(event))

        self.assertEqual(internal_value["recurrence"]["recur"]["dates"], dates_value)

        # to representation
        event["recurrence"] = CalendarRecurrence.objects.create(**internal_value["recurrence"])
        cal_event = CalendarEvent.objects.create(**event)
        representation = ser.to_representation(cal_event)

        self.assertEqual(representation["recurrence"]["dates"], dates_string)


class CalendarRemindersTest(CommonTestBase):
    @parameterized.expand([(0,), (2,), (4,)])
    def test_insert_and_check_from_db(self, num_reminders):
        # test inserting event without reminders: reminders must not be in the database
        # test inserting with reminders: reminders must be in database
        event = self.get_event_request_def(num_reminders=num_reminders)
        event_url = reverse("calendar-event-list", args=["json"])
        response = self.get_json(
            self.client.post(event_url, data=self.encode_json(event), content_type="application/json"),
            status.HTTP_201_CREATED,
        )
        recurrence_id = response["recurrence"]["id"]
        event_id = response["id"]
        # First check if result of POST is as expected
        expected_response = self.get_event_request_def(num_reminders=num_reminders)
        self.check_event_as_expected(response, expected_response)
        self.assertEqual(recurrence_id, response["recurrence"]["id"])

        def strip_event(instance):
            reminder = model_to_dict(instance)
            reminder["type"] = CalendarReminder.RType(reminder["type"]).value
            reminder["unit"] = CalendarReminder.Unit(reminder["unit"]).value
            reminder.pop("event")
            return reminder

        # now also check with database
        event = CalendarEvent.objects.get(pk=event_id)
        response = model_to_dict(event)
        recur = response["recurrence"] = model_to_dict(event.recurrence)
        recur["pattern"] = recur["pattern"].value
        response["reminders"] = list((strip_event(reminder) for reminder in event.reminders.all()))
        response = self.dates_to_iso(response)
        response = self.event_to_request_def(response)
        self.check_event_as_expected(response, expected_response)

        # test that inserted reminders are also returned by the API
        event_url = reverse("calendar-event-detail", kwargs=dict(pk=event_id, format="json"))
        response = self.get_json(self.client.get(event_url), status.HTTP_200_OK)
        self.check_event_as_expected(response, expected_response)

    def test_reminder_changing(self):
        # First we insert the event
        event = self.get_event_request_def(num_reminders=2)
        event_url = reverse("calendar-event-list", args=["json"])
        response = self.get_json(
            self.client.post(event_url, data=self.encode_json(event), content_type="application/json"),
            status.HTTP_201_CREATED,
        )
        expected_response = self.get_event_request_def(num_reminders=2)
        self.check_event_as_expected(response, expected_response)
        event_id = response["id"]

        # Now, we retrieve it
        event_url = reverse("calendar-event-detail", kwargs=dict(pk=event_id, format="json"))
        response = self.get_json(self.client.get(event_url), status.HTTP_200_OK)
        self.check_event_as_expected(response, expected_response)

        # add IDs to original event definition
        event["id"] = event_id
        event["recurrence"]["id"] = response["recurrence"]["id"]
        for idx, reminder in enumerate(event["reminders"]):
            reminder["id"] = response["reminders"][idx]["id"]

        original_count = CalendarEvent.objects.count()
        # store original event definition unchanged
        response = self.get_json(
            self.client.put(event_url, data=self.encode_json(event), content_type="application/json"),
            status.HTTP_200_OK,
        )
        expected_response = self.get_event_request_def(num_reminders=2)
        self.check_event_as_expected(response, expected_response)
        self.assertEqual(CalendarEvent.objects.count(), original_count)  # check that original event was updated

        # test adding one more reminder
        event["reminders"].append(self.get_event_request_def(num_reminders=3)["reminders"][2])
        response = self.get_json(
            self.client.put(event_url, data=self.encode_json(event), content_type="application/json"),
            status.HTTP_200_OK,
        )
        expected_response = self.get_event_request_def(num_reminders=3)
        self.check_event_as_expected(response, expected_response)
        self.assertEqual(CalendarEvent.objects.count(), original_count)  # check that original event was updated
        event["reminders"][2]["id"] = response["reminders"][2]["id"]

        # test changing a reminder or two
        event["reminders"][0]["unit"] = CalendarReminder.Unit.Minutes
        event["reminders"][1]["quantity"] = 20

        response = self.get_json(
            self.client.put(event_url, data=self.encode_json(event), content_type="application/json"),
            status.HTTP_200_OK,
        )
        expected_response = self.get_event_request_def(num_reminders=3)
        expected_response["reminders"][0]["unit"] = CalendarReminder.Unit.Minutes.value
        expected_response["reminders"][1]["quantity"] = 20
        self.check_event_as_expected(response, expected_response)
        self.assertEqual(CalendarEvent.objects.count(), original_count)  # check that original event was updated

        # test removing a reminder
        event["reminders"].pop(1)
        response = self.get_json(
            self.client.put(event_url, data=self.encode_json(event), content_type="application/json"),
            status.HTTP_200_OK,
        )
        expected_response = self.get_event_request_def(num_reminders=3)
        expected_response["reminders"][0]["unit"] = CalendarReminder.Unit.Minutes.value
        expected_response["reminders"].pop(1)
        self.check_event_as_expected(response, expected_response)
        self.assertEqual(CalendarEvent.objects.count(), original_count)  # check that original event was updated

        # test reminder sort order (must be sorted by total time before event ascending)
        event["reminders"][1]["unit"] = CalendarReminder.Unit.Seconds
        response = self.get_json(
            self.client.put(event_url, data=self.encode_json(event), content_type="application/json"),
            status.HTTP_200_OK,
        )
        expected_response = self.get_event_request_def(num_reminders=3)
        expected_response["reminders"][0]["unit"] = CalendarReminder.Unit.Minutes.value
        expected_response["reminders"].pop(1)
        expected_response["reminders"][1]["unit"] = CalendarReminder.Unit.Seconds.value
        # the order changes because second reminder is now closer to the event than the first reminder
        expected_response["reminders"] = list(reversed(expected_response["reminders"]))
        self.check_event_as_expected(response, expected_response)
        self.assertEqual(CalendarEvent.objects.count(), original_count)  # check that original event was updated

    """
    test that reminders are copied to subsequent events in recurrence interval
    test that reminders are NOT copied to subsequent events in recurrence interval when change_this_record_only == True
    """

    @parameterized.expand([(False,), (True,)])
    def test_reminders_copying(self, change_this_record_only):
        # First we insert the event
        event = self.get_event_request_def(num_reminders=2)
        event_url = reverse("calendar-event-list", args=["json"])
        response = self.get_json(
            self.client.post(event_url, data=self.encode_json(event), content_type="application/json"),
            status.HTTP_201_CREATED,
        )
        expected_response = self.get_event_request_def(num_reminders=2)
        self.check_event_as_expected(response, expected_response)

        event_url = reverse("calendar-event-list", args=["json"])
        response = self.get_json(self.client.get(event_url), status.HTTP_200_OK)
        self.assertTrue(response)
        self.assertIsInstance(response, list)
        self.assertEqual(6, len(response))
        instance_ids = tuple(map(lambda x: x["id"], response))

        response = self.retrieve_event_id(instance_ids[2])  # 3rd instance is the one on 3.2.2020
        expected_response = self.get_event_request_def(num_reminders=2)
        expected_response["id"] = instance_ids[2]
        expected_response["start_at"] = "2020-02-03T10:00:00Z"
        expected_response["end_at"] = "2020-02-03T11:00:00Z"
        self.assertEqual(instance_ids[2], self.check_event_as_expected(response, expected_response))

        event["id"] = instance_ids[2]
        event["recurrence"]["id"] = response["recurrence"]["id"]
        event["start_at"] = "2020-02-03T10:00:00Z"
        event["end_at"] = "2020-02-03T11:00:00Z"
        event["change_this_record_only"] = change_this_record_only
        event["description"] = "one changed event"
        event["reminders"].append(self.get_event_def(num_reminders=3)["reminders"][2])

        event_url = reverse("calendar-event-detail", kwargs=dict(pk=instance_ids[2], format="json"))
        response = self.get_json(
            self.client.put(event_url, data=self.encode_json(event), content_type="application/json"),
            status.HTTP_200_OK,
        )
        expected_response["description"] = "one changed event"
        expected_response["reminders"].append(self.get_event_def(num_reminders=3)["reminders"][2])
        self.check_event_as_expected(response, expected_response)

        for instance_id, d in zip(instance_ids, (0, 3, 4, 6, 10, 11)):
            event_url = reverse("calendar-event-detail", kwargs=dict(pk=instance_id, format="json"))
            response = self.get_json(self.client.get(event_url), status.HTTP_200_OK)

            self.assertEqual(
                (datetime.datetime(2020, 1, 30, 10) + datetime.timedelta(days=d)).isoformat() + "Z",
                response["start_at"],
                msg=str((instance_id, d)),
            )
            condition = (d != 4) if change_this_record_only else (d < 4)
            self.assertEqual(None if condition else "one changed event", response["description"])
            self.assertEqual(2 if condition else 3, len(response["reminders"]))

    def test_change_event_with_reminders(self):
        """
        Preserve reminders on event change
        """
        # First create event with reminders
        event = self.get_event_request_def(num_reminders=2)
        event_url = reverse("calendar-event-list", args=["json"])
        response = self.get_json(
            self.client.post(event_url, data=self.encode_json(event), content_type="application/json"),
            status.HTTP_201_CREATED,
        )
        self.check_event_as_expected(response, event)
        event_id = response["id"]

        # Check if event was created correctly
        event_url = reverse("calendar-event-detail", kwargs=dict(pk=event_id, format="json"))
        response = self.get_json(self.client.get(event_url), status.HTTP_200_OK)
        self.check_event_as_expected(response, event)

        # Update events start and end times
        event_update = dict(
            start_at=datetime.datetime(2020, 1, 30, 11, 0, tzinfo=pytz.utc),
            end_at=datetime.datetime(2020, 1, 30, 12, 0, tzinfo=pytz.utc),
        )
        response = self.get_json(
            self.client.patch(event_url, data=self.encode_json(event_update), content_type="application/json"),
            status.HTTP_200_OK,
        )
        self.assertEqual(len(response["reminders"]), len(event["reminders"]))
        for event_reminder, response_reminder in zip(response["reminders"], event["reminders"]):
            self.check_event_as_expected(event_reminder, response_reminder)

        # TODO: can't compare events due to recurrence overwrite
        # event.update(event_update)
        # self.check_event_as_expected(response, event)

    def test_clear_reminders(self):
        """
        Passing in empty array of reminders should clear reminders on event
        """
        # First create event with reminders
        event = self.get_event_request_def(num_reminders=2)
        event_url = reverse("calendar-event-list", args=["json"])
        response = self.get_json(
            self.client.post(event_url, data=self.encode_json(event), content_type="application/json"),
            status.HTTP_201_CREATED,
        )
        self.check_event_as_expected(response, event)
        event_id = response["id"]

        event_url = reverse("calendar-event-detail", kwargs=dict(pk=event_id, format="json"))
        event_update = dict(reminders=[])
        response = self.get_json(
            self.client.patch(event_url, data=self.encode_json(event_update), content_type="application/json"),
            status.HTTP_200_OK,
        )
        self.assertEqual(response["reminders"], [])
