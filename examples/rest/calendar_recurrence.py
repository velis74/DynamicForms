from dynamicforms import serializers
from examples.enum_field import EnumField
from examples.models import CalendarRecurrence


class RecurrenceSerializer(serializers.ModelSerializer):
    pattern = EnumField(CalendarRecurrence.Pattern)

    def __init__(self, *args, **kwds):
        super().__init__(*args, **kwds)
        self.fields['id'].read_only = False  # https://stackoverflow.com/a/46525126/1760858

    class Meta:
        model = CalendarRecurrence
        exclude = ()
