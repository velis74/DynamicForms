from examples.models import CalendarEvent
from .calendar_dependencies import RecurrenceEventSerializer, RecurrenceEventViewSet
from .calendar_recurrence import RecurrenceSerializer
from .calendar_reminders import RemindersSerializer


class CalendarEventSerializer(RecurrenceEventSerializer):
    template_context = dict(url_reverse='calendar-event')
    form_titles = {
        'table': 'Calendar',
        'new': 'New event',
        'edit': 'Editing event',
    }

    recurrence = RecurrenceSerializer(required=False)
    reminders = RemindersSerializer(many=True, required=False)

    class Meta:
        model = CalendarEvent
        exclude = ()


class CalendarEventViewSet(RecurrenceEventViewSet):
    serializer_class = CalendarEventSerializer
    queryset = CalendarEvent.objects.all()
