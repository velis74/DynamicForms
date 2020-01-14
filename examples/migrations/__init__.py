import random
import django.utils.timezone


def add_relation(apps, schema_editor):
    from ..models import Relation
    for i in range(1, 11):
        Relation.objects.create(name='Relation object %d' % i)


def add_filter(apps, schema_editor):
    from ..models import Filter

    date_now = django.utils.timezone.now()
    char_field = ['abc', 'def', 'ghi', 'abcdef', 'abcghi', 'defghi', 'abcdefghi']
    for i in range(1, 100 + 1):
        date_now = date_now + django.utils.timezone.timedelta(hours=3)
        Filter.objects.create(char_field='%s %d' % (char_field[(i - 1) % 7], i),
                              datetime_field=date_now,
                              int_field=((i - 1) % 10) + 1,
                              int_choice_field=((i - 1) % 4),
                              bool_field=((i - 1) % 10) > 4
                              )


def add_page_load(apps, schema_editor):
    from ..models import PageLoad
    for i in range(1, 10000 + 1):
        PageLoad.objects.create(description='Item %d' % i, choice=random.randint(1, 4))
