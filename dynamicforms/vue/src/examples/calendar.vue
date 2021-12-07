<template>
  <div>
    <p>
      This example showcases DynamicForms' capacity for handling nested serializers, both in list and form mode. Do not
      pay too much attention to the JS fullCalendar component used here, but instead focus on the dialogs for adding or
      editing events.
    </p>
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

export default {
  name: 'Calendar',
  components: { FullCalendar },
  emits: ['title-change'],
  data() {
    return {
      sunriseTime: '8:00',
      sunsetTime: '16:00',
    };
  },
  computed: {
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

        // eventResize: resizeReservation,
        // eventDrop: resizeReservation,

        initialView: 'timeGridWeek',
        editable: true,
        dayMaxEvents: true, // allow "more" link when too many events
        eventOverlap: false,

        // eventClick: editReservation,
        // select: addReservation,

        events: '/calendar-event.json',
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
      input.start = new Date(input.start_at);
      input.end = new Date(input.end_at);
      return {
        id: input.id, start: input.start_at, end: input.end_at, title: input.title,
      };
    },
  },
};
</script>

<style scoped>

</style>
