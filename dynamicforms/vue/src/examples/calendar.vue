<template>
  <div>
    <FullCalendar :options="calendarOptions"/>
  </div>
</template>

<script>
import '@fullcalendar/core/vdom'; // ensures proper plugin load order
import dayGridPlugin from '@fullcalendar/daygrid';
import interactionPlugin from '@fullcalendar/interaction';
import listPlugin from '@fullcalendar/list';
import momentPlugin from '@fullcalendar/moment';
import momentTimezonePlugin from '@fullcalendar/moment-timezone';
import timeGridPlugin from '@fullcalendar/timegrid';
import FullCalendar from '@fullcalendar/vue';
import SunCalc from 'suncalc';

import apiClient from '../apiClient';
import DynamicForms from '../dynamicforms';
import ActionHandlerMixin from '../mixins/actionHandlerMixin';

export default {
  name: 'Calendar',
  components: { FullCalendar },
  mixins: [ActionHandlerMixin],
  emits: ['title-change'],
  data() {
    return {
      uuid: 'calendar_entry',
      sunriseTime: '8:00',
      sunsetTime: '16:00',
      url: '/calendar-event',
    };
  },
  computed: {
    defaultSubmitHeaders() { return { 'x-viewmode': 'FORM' }; },
    detail_url() { return `${this.url}/--record_id--.json`; },
    calendarOptions() {
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
        selectAllow(selectInfo) {
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
  mounted() {
    this.$emit('title-change', window.gettext('Calendar example'));
  },
  methods: {
    recalculateSun(dateInfo) {
      // console.log(dateInfo);
      const suncalc = SunCalc.getTimes(dateInfo.start, 46.05, -14.50);
      const sunrise = new Date(suncalc.sunrise.valueOf() - 30 * 60 * 1000);
      const sunset = new Date(suncalc.sunset.valueOf() + 30 * 60 * 1000);
      this.sunriseTime = `${sunrise.getHours()}:${String(sunrise.getMinutes()).padStart(2, '0')}`;
      this.sunsetTime = `${sunset.getHours()}:${String(sunset.getMinutes()).padStart(2, '0')}`;
      // console.log(suncalc, this.sunriseTime, this.sunsetTime);
    },
    eventDataTransform(input) {
      return {
        id: input.id, start: input.start_at, end: input.end_at, title: input.title,
      };
    },
    async addReservation(selectionInfo) {
      // console.log(selectionInfo.start, selectionInfo.end, selectionInfo.allDay);
      const startAt = encodeURIComponent(selectionInfo.startStr);
      const endAt = encodeURIComponent(selectionInfo.endStr);
      const dlgRes = await DynamicForms.dialog.fromURL(
        `${this.url}/new.componentdef?start_at=${startAt}&end_at=${endAt}`, 'new', this.uuid,
      );
      const event = this.eventDataTransform(dlgRes.data);
      selectionInfo.view.calendar.addEvent(event, true);
      // selectionInfo.view.calendar.refetchEvents();
      console.log([event, event.start, dlgRes]);
    },
    async editReservation(clickInfo) {
      // console.log(clickInfo.event);
      const eventId = clickInfo.event.id;
      const dlgRes = await DynamicForms.dialog.fromURL(`${this.url}/${eventId}.componentdef`, 'edit', this.uuid);
      switch (dlgRes && dlgRes.action ? dlgRes.action.name : null) {
      case 'delete_dlg':
        clickInfo.event.remove();
        break;
      case 'submit':
        clickInfo.event.setDates(dlgRes.data.start_at, dlgRes.data.end_at);
        clickInfo.event.setProp('title', dlgRes.data.title);
        break;
      default:
        console.log(dlgRes);
      }
    },
    actionDelete_dlgExecute(action, data, modal, params, promise) {
      // will be called from actionHandlerMixin
      if (promise) promise.resolveData = { action, data, params };
      this.actionDeleteExecute(action, data, modal, params, promise);
      if (modal) modal.hide();
    },
    async resizeReservation(resizeInfo) {
      const url = this.detail_url.replace('--record_id--', resizeInfo.event.id);
      try {
        await apiClient.patch(
          url, { id: resizeInfo.event.id, start_at: resizeInfo.event.startStr, end_at: resizeInfo.event.endStr },
        );
      } catch (exc) {
        resizeInfo.revert();
        // console.log(resizeInfo.event.backgroundColor);
        // window.setTimeout(() => resizeInfo.event.setProp('backgroundColor', '#F00'), 1);
      }
    },
  },
};
</script>

<style scoped>

</style>
