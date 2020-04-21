import re
from datetime import datetime
from typing import Any

from django.utils import timezone
from django.utils.formats import localize
from rest_framework.fields import DateField, TimeField
from rest_framework.serializers import ListSerializer


class NaturalDateTimeMixin(object):
    """
    Used for rendering datetime in human natural style (e.g.: 1 hour, 10 minutes ago)
    """

    def __init__(self, *args, table_format: str = '', **kwargs) -> None:
        """

        :param args:
        :param table_format: Format for datetime rendering in table (non editable). If format is %N:{precision},
            datetime will render in natural style with {precision} depth
        :param kwargs:
        """
        super().__init__(*args, **kwargs)
        self.table_format = table_format

    # noinspection PyUnresolvedReferences
    def to_representation(self, value: Any) -> Any:
        if not value:
            return None

        if isinstance(value, str):
            return value

        if isinstance(self.parent.parent, ListSerializer):
            output_format = getattr(self, 'table_format', None)
            if output_format is not None:
                if re.match(r'%N:\d+', output_format):
                    imported = False
                    try:
                        # This library (will-natural) is used because is the only one we could find that adds text
                        # saying when is this datetime ("ago" or "from now") and have the possibility to set max
                        # precision

                        # noinspection PyPackageRequirements
                        from natural.date import duration
                        imported = True
                    except:
                        print('Install library for natural presentation of date (pip install will-natural)')

                    if imported:
                        if isinstance(self, DateField):
                            now = timezone.now().date()
                        elif isinstance(self, TimeField):
                            now = datetime.now()
                            value = datetime.now().replace(hour=value.hour, minute=value.minute, second=value.second,
                                                           microsecond=value.microsecond)
                        else:
                            now = timezone.now()

                        # noinspection PyUnboundLocalVariable
                        return duration(value, now=now, precision=int(output_format.split(':')[1]))
                else:
                    global_format = getattr(self, 'format', None)
                    setattr(self, 'format', output_format)
                    value = super().to_representation(value)
                    setattr(self, 'format', global_format)
                    return value
        return super().to_representation(value)

    def render_to_table(self, value, row_data):
        if value is None:
            # noinspection PyUnresolvedReferences
            return super().render_to_table(value, row_data)
        return localize(value)


class TimeFieldMixin(NaturalDateTimeMixin):

    def __init__(self, *args, table_format: str = None, **kwargs) -> None:
        super().__init__(*args, table_format=table_format, **kwargs)


class DateFieldMixin(NaturalDateTimeMixin):

    def __init__(self, *args, table_format: str = None, **kwargs) -> None:
        super().__init__(*args, table_format=table_format, **kwargs)


class DateTimeFieldMixin(NaturalDateTimeMixin):

    def __init__(self, *args, table_format: str = None, **kwargs) -> None:
        super().__init__(*args, table_format=table_format, **kwargs)
