from examples.models import CalendarEvent, CalendarReminder
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

    def to_representation(self, instance, row_data=None):
        """
        Ensures proper sort order for reminders
        """

        def seconds(reminder: dict):
            if reminder['unit'] == CalendarReminder.Unit.Seconds:
                return reminder['quantity']
            elif reminder['unit'] == CalendarReminder.Unit.Minutes:
                return reminder['quantity'] * 60
            elif reminder['unit'] == CalendarReminder.Unit.Hours:
                return reminder['quantity'] * 60 * 60
            elif reminder['unit'] == CalendarReminder.Unit.Days:
                return reminder['quantity'] * 86400
            elif reminder['unit'] == CalendarReminder.Unit.Weeks:
                return reminder['quantity'] * 86400 * 7
            raise ValueError(f'Unknown CalendarReminder.Unit[{reminder["unit"]}]')

        res = super().to_representation(instance, row_data)
        res['reminders'] = list(sorted(res['reminders'], key=lambda reminder: seconds(reminder)))
        return res

    class Meta:
        model = CalendarEvent
        exclude = ()


class CalendarEventViewSet(RecurrenceEventViewSet):
    serializer_class = CalendarEventSerializer
    queryset = CalendarEvent.objects.all()
