import TableRow from '../../table/definitions/row';

import EventType from './event_type';
import TableRowEvent from './table_row_event';

const eventGateway = {
  methods: {
    handleEvent(type, eventPayload) {
      console.log('foo', Math.random(), type, EventType.ACTION, eventPayload);
      console.log(type === EventType.ACTION, eventPayload instanceof TableRow);
      if (type === EventType.ACTION && eventPayload.payload instanceof TableRow) {
        console.log(444);
        new TableRowEvent(EventType.TABLE_ROW_ACTION, eventPayload).execute();
      }
    },
  },
};

export default eventGateway;
