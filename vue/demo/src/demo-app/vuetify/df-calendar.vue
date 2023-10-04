<template>
  <full-calendar :options="calendarOptions"/>
</template>

<script lang="ts">
import type {
  CalendarOptions,
  DateSpanApi,
  DateSelectArg,
  DatesSetArg,
  EventDropArg,
  EventInput,
  EventClickArg,
} from '@fullcalendar/core';
import dayGridPlugin from '@fullcalendar/daygrid';
import interactionPlugin, { EventResizeDoneArg } from '@fullcalendar/interaction';
import listPlugin from '@fullcalendar/list';
import momentPlugin from '@fullcalendar/moment';
import momentTimezonePlugin from '@fullcalendar/moment-timezone';
import timeGridPlugin from '@fullcalendar/timegrid';
import FullCalendar from '@fullcalendar/vue3';
import { apiClient, ConsumerLogicApi, FormConsumerOneShotApi } from 'dynamicforms';
import SunCalc from 'suncalc';
import { defineComponent } from 'vue';

export default defineComponent({
  name: 'DfCalendar',
  components: { FullCalendar },
  emits: ['title-change'],
  data() {
    return {
      uuid: 'calendar_entry',
      sunriseTime: '8:00',
      sunsetTime: '16:00',
      url: '/calendar-event',
      apiConsumer: new ConsumerLogicApi('/calendar-event'),
    };
  },
  computed: {
    defaultSubmitHeaders() {
      return { 'x-viewmode': 'FORM' };
    },
    calendarOptions(): CalendarOptions {
      return {
        plugins: [dayGridPlugin, listPlugin, momentPlugin, momentTimezonePlugin, timeGridPlugin, interactionPlugin],
        headerToolbar: {
          left: 'prev,next today',
          center: 'title',
          right: 'listWeek,timeGridDay,timeGridWeek,dayGridMonth',
        },
        dayHeaderFormat: 'ddd DD.MMM',
        titleFormat: 'ddd DD.MMM yyyy',
        height: 'auto',
        slotLabelFormat: 'HH:mm',
        eventStartEditable: true,
        eventDurationEditable: true,
        selectable: true,
        selectMirror: true,
        selectOverlap: false,
        selectAllow(selectInfo: DateSpanApi) {
          return selectInfo.start.getDate() === selectInfo.end.getDate() &&
              selectInfo.start.getHours() >= 7 &&
              (selectInfo.end.getHours() < 21 ||
                  (selectInfo.end.getHours() === 21 && selectInfo.end.getMinutes() === 0));
        },

        allDaySlot: false,
        eventResize: this.resizeReservation,
        eventDrop: this.resizeReservation,

        initialView: 'timeGridWeek',
        editable: true,
        dayMaxEvents: true, // allow "more" link when too many events
        eventOverlap: false,

        eventClick: this.editReservation,
        select: this.addReservation,

        events: `${this.url}.json`,
        eventDataTransform: this.eventDataTransform,
        eventTimeFormat: 'HH:mm',
        timeZone: 'Europe/Ljubljana',
        slotMinTime: '06:00',
        slotMaxTime: '22:00',
        businessHours: {
          daysOfWeek: [0, 1, 2, 3, 4, 5, 6],
          startTime: this.sunriseTime,
          endTime: this.sunsetTime,
        },
        firstDay: 1,
        eventConstraint: 'businessHours',

        datesSet: this.recalculateSun,
      };
    },
  },
  methods: {
    detail_url(record_id: string): string {
      return `${this.url}/${record_id}.json`;
    },
    recalculateSun(dateInfo: DatesSetArg) {
      // console.log(dateInfo);
      const suncalc = SunCalc.getTimes(dateInfo.start, 46.05, -14.50);
      const sunrise = new Date(suncalc.sunrise.valueOf() - 30 * 60 * 1000);
      const sunset = new Date(suncalc.sunset.valueOf() + 30 * 60 * 1000);
      this.sunriseTime = `${sunrise.getHours()}:${String(sunrise.getMinutes()).padStart(2, '0')}`;
      this.sunsetTime = `${sunset.getHours()}:${String(sunset.getMinutes()).padStart(2, '0')}`;
      // console.log(suncalc, this.sunriseTime, this.sunsetTime);
    },
    eventDataTransform(input: EventInput) {
      return { id: input.id, start: input.start_at, end: input.end_at, title: input.title };
    },
    async addReservation(selectionInfo: DateSelectArg) {
      await FormConsumerOneShotApi(
        {
          url: '/calendar-event',
          trailingSlash: true,
          query: {
            start_at: selectionInfo.startStr,
            end_at: selectionInfo.endStr,
          },
        },
      );
      selectionInfo.view.calendar.refetchEvents();
    },
    async editReservation(clickInfo: EventClickArg) {
      const eventId = clickInfo.event.id;
      await FormConsumerOneShotApi(
        {
          url: '/calendar-event',
          trailingSlash: true,
          pk: eventId,
        },
      );
      clickInfo.view.calendar.refetchEvents();
    },
    async resizeReservation(resizeInfo: EventResizeDoneArg | EventDropArg) {
      const url = this.detail_url(resizeInfo.event.id);
      try {
        await apiClient.patch(
          url,
          { id: resizeInfo.event.id, start_at: resizeInfo.event.startStr, end_at: resizeInfo.event.endStr },
        );
      } catch (exc) {
        resizeInfo.revert();
        // console.log(resizeInfo.event.backgroundColor);
        // window.setTimeout(() => resizeInfo.event.setProp('backgroundColor', '#F00'), 1);
      }
    },
  },
});
</script>
