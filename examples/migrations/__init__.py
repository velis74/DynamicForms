import random

import django.utils.timezone

from dynamicforms.utils import get_pk_name
from setup.settings import TESTING


def add_relation(Relation):
    if not Relation.objects.all().count():
        for i in range(1, 11):
            Relation.objects.create(name="Relation object %d" % i)


def add_filter(Filter):
    if not Filter.objects.all().count():
        date_now = django.utils.timezone.now()
        char_field = ["abc", "def", "ghi", "abcdef", "abcghi", "defghi", "abcdefghi"]
        for i in range(1, 100 + 1):
            date_now = date_now + django.utils.timezone.timedelta(hours=3)
            filter_data: dict = dict(
                char_field="%s %d" % (char_field[(i - 1) % 7], i),
                datetime_field=date_now,
                int_field=((i - 1) % 10) + 1,
                int_choice_field=((i - 1) % 4),
                bool_field=((i - 1) % 10) > 4,
            )
            if TESTING:
                filter_data[get_pk_name(Filter)] = i
            Filter.objects.create(**filter_data)


def add_page_load(PageLoad):
    if not PageLoad.objects.all().count():
        for i in range(1, 10000 + 1):
            PageLoad.objects.create(description="Item %d" % i, choice=random.randint(1, 4))
