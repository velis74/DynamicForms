from typing import List, Optional

from django.db import transaction
from django.forms.models import model_to_dict

from dynamicforms import fields, serializers, viewsets
from examples.models import CalendarEvent, CalendarRecurrence, CalendarReminder

from .calendar_recurrence import RecurrenceSerializer


class RecurrenceEventSerializer(serializers.ModelSerializer):
    change_this_record_only = fields.BooleanField(write_only=True, required=False, default=False)

    def __init__(self, *args, **kwds):
        super().__init__(*args, **kwds)
        self.fields["recurrence"].display_table = fields.DisplayMode.SUPPRESS
        self.old_recurrence = None

    # def to_internal_value(self, data):
    #     if isinstance(data, QueryDict):
    #         data = data.copy()
    #     if data['recur'] not in RecurField.TRUE_VALUES:
    #         for key in [k for k in data.keys() if k.startswith('recurrence.')]:
    #             data.pop(key)
    #         data['recurrence'] = None
    #     data.pop('recur')
    #     return super().to_internal_value(data)

    def save_dependencies(self, validated_data, instance: CalendarEvent = None, reminders: Optional[List[dict]] = None):
        def save_recurrence(data):
            recurrence = CalendarRecurrence.objects.filter(pk=int(data.get("id", 0))).first()
            res = RecurrenceSerializer(instance=recurrence)
            if recurrence:
                return res.update(recurrence, data)
            return res.create(data)

        if isinstance(validated_data.get("recurrence", None), CalendarRecurrence):
            pass  # we already saved recurrence, so let's not do anything about it now
        elif validated_data.get("recurrence", None):
            validated_data["recurrence"] = save_recurrence(validated_data["recurrence"])
        elif instance:
            instance.recurrence = None

        if reminders is not None:
            from .calendar_reminders import RemindersSerializer

            r_ids = set()
            for reminder in reminders:
                reminder["event"] = instance.id
                ser = RemindersSerializer(
                    instance=CalendarReminder.objects.filter(pk=reminder.get("id", 0)).first(), data=reminder
                )
                ser.is_valid(raise_exception=True)
                r_ids.add(ser.save().id)
            CalendarReminder.objects.filter(event=instance).exclude(id__in=r_ids).delete()

    def create(self, validated_data):
        change_this_record_only = validated_data.pop("change_this_record_only", False)
        reminders = validated_data.pop("reminders", None)
        self.save_dependencies(validated_data)
        instance = super().create(validated_data)
        self.save_dependencies(validated_data, instance, reminders)
        return self.handle_recurrence(instance, None, change_this_record_only)

    @transaction.atomic
    def update(self, instance, validated_data):
        change_this_record_only = validated_data.pop("change_this_record_only", False)
        reminders = validated_data.pop("reminders", None)
        self.save_dependencies(validated_data, instance, reminders)
        return self.handle_recurrence(
            super().update(instance, validated_data), self.old_recurrence, change_this_record_only
        )

    def handle_recurrence(
        self, instance: CalendarEvent, old_recurrence: Optional[CalendarRecurrence], change_this_record_only: bool
    ):
        cutoff_date = instance.start_at  # date before which we will not delete / modify event instances
        if not instance.recurrence and old_recurrence:
            # recurrence was cancelled: delete all instances but this one
            CalendarEvent.objects.filter(recurrence_id=old_recurrence.id).exclude(id=instance.id).exclude(
                start_at__lte=cutoff_date
            ).delete()
            if not old_recurrence.events.exists():
                old_recurrence.delete()
            else:
                instance.recurrence = old_recurrence
                instance.save(update_fields=("recurrence",))
        elif instance.recurrence:
            # Recurrence remains or is changed. Update / create any items after right now
            recur: CalendarRecurrence = instance.recurrence
            # recurrence remains the same or it has changed. Iterate & update instances
            existing = iter(
                CalendarEvent.objects.filter(recurrence_id=instance.recurrence_id).order_by("start_at").all()
            )
            instance_data = model_to_dict(instance)
            instance_reminders = list(instance.reminders.all())
            del instance_data["id"]
            instance_data["recurrence_id"] = instance_data.pop("recurrence", None)
            cur_task = next(existing, None)
            for dtm in recur.date_range(cutoff_date):
                while cur_task and cur_task.start_at < dtm:
                    if cur_task.start_at > instance.start_at:
                        cur_task.delete()
                    # advance existing recurring tasks to this date at least
                    cur_task = next(existing, None)
                instance_data["start_at"] = dtm
                instance_data["end_at"] = dtm + (instance.end_at - instance.start_at)
                if cur_task and cur_task.start_at == dtm:
                    dtm_task = cur_task
                    cur_task = next(existing, None)
                    if dtm_task.start_at > instance.start_at and not change_this_record_only:
                        for k, v in instance_data.items():
                            setattr(dtm_task, k, v)
                else:
                    dtm_task = CalendarEvent(**instance_data)
                dtm_task.save()
                if dtm_task.start_at > instance.start_at and not change_this_record_only:
                    # update also reminders
                    dtm_task.reminders.all().delete()
                    for reminder in instance_reminders:
                        CalendarReminder.objects.create(
                            event=dtm_task, type=reminder.type, quantity=reminder.quantity, unit=reminder.unit
                        )

            # finish up with deleting any tasks that exceed the shortened date_to
            if cur_task and cur_task.start_at <= recur.end_at:
                cur_task = next(existing, None)
            while cur_task:
                cur_task.delete()
                cur_task = next(existing, None)

        # end handle_recurrence
        return instance


class RecurrenceEventViewSet(viewsets.ModelViewSet):
    def __init__(self, *args, **kwds):
        super().__init__(*args, **kwds)
        self.old_recurrence = None

    def update(self, request, *args, **kwargs):
        self.old_recurrence = self.get_object().recurrence
        res = super().update(request, *args, **kwargs)
        return res

    def perform_update(self, serializer):
        serializer.old_recurrence = self.old_recurrence
        return super().perform_update(serializer)
