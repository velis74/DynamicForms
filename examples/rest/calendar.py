from dynamicforms import serializers, viewsets
from examples.models import CalendarEvent


class CalendarEventSerializer(serializers.ModelSerializer):
    template_context = dict(url_reverse='calendar-event')
    form_titles = {
        'table': 'Calendar',
        'new': 'New event',
        'edit': 'Editing event',
    }

    class Meta:
        model = CalendarEvent
        exclude = ()


class CalendarEventViewSet(viewsets.ModelViewSet):
    serializer_class = CalendarEventSerializer
    queryset = CalendarEvent.objects.all()
