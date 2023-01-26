import datetime

from django.utils.translation import gettext_lazy as _

from dynamicforms.action import Actions, FormButtonAction, FormButtonTypes
from dynamicforms.template_render.layout import Column, Group, Layout, Row
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
    actions = Actions(
        FormButtonAction(btn_type=FormButtonTypes.CUSTOM, name='delete_dlg', label=_('Delete')),
        add_default_crud=True, add_form_buttons=True
    )

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
        from dynamicforms.serializers import Serializer
        if self.view_mode != Serializer.ViewMode.TABLE_ROW:
            # table row serializes to string, so there's nothing to do here
            res['reminders'] = list(sorted(res['reminders'], key=lambda reminder: seconds(reminder)))
        return res

    class Meta:
        model = CalendarEvent
        layout = Layout(
            Row(Column('title', 'col-10'), Column('colour', 'col-2')),
            Row('description'),
            Row('start_at', 'end_at'),
            Row('reminders'),
            Row(Group('recurrence', width_classes='col-8'), Column('change_this_record_only', 'col-4')),
            columns=2, size='large'
        )
        exclude = ()


class CalendarEventViewSet(RecurrenceEventViewSet):
    serializer_class = CalendarEventSerializer

    def get_queryset(self):
        res = CalendarEvent.objects.all()
        start_at = self.request.query_params.get('start', '')
        if start_at:
            res = res.filter(end_at__gte=datetime.datetime.fromisoformat(start_at))
        end_at = self.request.query_params.get('end', '')
        if end_at:
            res = res.filter(start_at__lte=datetime.datetime.fromisoformat(end_at))
        return res
