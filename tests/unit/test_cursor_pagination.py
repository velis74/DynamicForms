import datetime
import inspect
import json
import random
import string
import uuid

from django.test import TestCase
from django.urls import reverse
from django.utils.timezone import make_aware
from rest_framework import status

from examples.models import BasicFields


def random_name():
    return random.choice(
        (
            "amelia",
            "olivia",
            "isla",
            "ava",
            "emily",
            "isabella",
            "mia",
            "poppy",
            "ella",
            "lily",
            "oliver",
            "harry",
            "george",
            "noah",
            "jack",
            "jacob",
            "leo",
            "oscar",
            "charlie",
            "rowan",
        )
    )


def random_last_name():
    return random.choice(
        (
            "smith",
            "jones",
            "williams",
            "taylor",
            "davies",
            "evans",
            "thomas",
            "johnson",
            "roberts",
            "walker",
        )
    )


def random_domain():
    return random.choice(
        (
            "abc.com",
            "def.org",
            "ijk.net",
            "znj.si",
        )
    )


NUM_RECORDS = 1000


def populate_simple_fields():
    result = []
    for _ in range(NUM_RECORDS):
        # noinspection PyStringFormat
        result.append(
            BasicFields.objects.create(
                boolean_field=bool(random.randint(0, 1)),
                nullboolean_field=bool(random.randint(0, 1)) if random.randint(0, 2) else None,
                char_field="".join(
                    (
                        random.choice(string.ascii_letters + string.digits + string.punctuation)
                        for _ in range(random.randint(10, 20))
                    )
                ),
                email_field=random_name() + "." + random_last_name() + "@" + random_domain(),
                slug_field="".join(
                    (random.choice(string.ascii_letters + string.digits) for _ in range(random.randint(10, 20)))
                ),
                url_field="http://"
                + random_domain()
                + "/"
                + "".join((random.choice(string.ascii_letters + string.digits) for _ in range(random.randint(10, 20)))),
                uuid_field=str(uuid.uuid4()),
                ipaddress_field="%d.%d.%d.%d" % (*[random.randint(0, 255) for _ in range(4)],),
                integer_field=random.randint(0, 9999999999),
                float_field=random.random() * 9999999999,
                decimal_field=random.random() * 999,
                datetime_field=make_aware(datetime.datetime.fromtimestamp(random.randint(1000000000, 10000000000))),
                date_field=make_aware(datetime.datetime.fromtimestamp(random.randint(1000000000, 10000000000))).date(),
                time_field=make_aware(datetime.datetime.fromtimestamp(random.randint(1000000000, 10000000000))).time(),
                duration_field=datetime.timedelta(seconds=random.randint(0, 1000000)),
            )
        )

    return result


class CursorPaginationTest(TestCase):
    def setUp(self) -> None:
        self.records = populate_simple_fields()

    def get_segments(self):
        return inspect.stack()[2][0].f_code.co_name.split("_")[1:]

    def fetch_first(self):
        segments = self.get_segments()
        url = (
            reverse("basic-fields-list", args=["json"])
            + "?ordering="
            + ",".join(map(lambda x: x + "_field" if x not in ("id", "pk") else x, segments))
        )

        def get_response(**kwargs):
            response = self.client.get(url, **kwargs)
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(response["content-type"], "application/json")
            return json.loads(response.content.decode("utf-8"))

        content_pg = get_response(HTTP_X_PAGINATION=True)  # paginated response
        self.assertEqual(len(content_pg), 3, "Response should contain three fields")
        self.assertEqual(len(content_pg["results"]), 30, "Response page data should contain 30 records")
        content_st = get_response()  # non-paginated response
        self.assertEqual(len(content_st), NUM_RECORDS, "Response should contain exactly %d records" % NUM_RECORDS)
        self.assertEqual(content_pg["results"], content_st[:30])  # BasicFieldsViewSet defines this page size

        url = content_pg["next"]
        content_pg_next = get_response(HTTP_X_PAGINATION=True)  # second page of paginated response
        self.assertEqual(len(content_pg_next), 3, "Response should contain three fields")
        self.assertEqual(len(content_pg_next["results"]), 30, "Response page data should contain 30 records")
        self.assertEqual(content_pg_next["results"], content_st[30:60])  # BasicFieldsViewSet defines this page size

        url = content_pg_next["previous"]
        content_pg_prev = get_response(HTTP_X_PAGINATION=True)  # re-fetch first page, but through the prev URL
        self.assertEqual(len(content_pg_prev), 3, "Response should contain three fields")
        self.assertEqual(len(content_pg_prev["results"]), 30, "Response page data should contain 30 records")
        self.assertEqual(content_pg_prev, content_pg)

        # now we will sort the records manually and compare result with what our sorting filter did
        def get_segment_values(x):
            res = []
            for seg in segments:
                res.append(getattr(x, seg + "_field" if seg not in ("id", "pk") else seg))
            return res

        sorted_records = sorted(self.records, key=lambda x: get_segment_values(x))
        content_st_id = [k["id"] for k in content_st]
        sorted_id = [k.id for k in sorted_records]
        self.assertEqual(content_st_id, sorted_id, "Manual sort should equal SQL sort")

    def test_char(self):
        self.fetch_first()

    def test_boolean_id(self):
        self.fetch_first()

    def test_integer_id(self):
        self.fetch_first()

    def test_float(self):
        self.fetch_first()

    def test_datetime(self):
        self.fetch_first()

    def test_date_id(self):
        self.fetch_first()

    def test_time_id(self):
        self.fetch_first()

    def test_duration_id(self):
        self.fetch_first()

    def test_boolean_char_ipaddress(self):
        self.fetch_first()

    def test_datetime_char(self):
        self.fetch_first()
