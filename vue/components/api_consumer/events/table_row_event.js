import apiClient from '../../util/api_client';

import DfEvent from './event';
import EventType from './event_type';

class TableRowEvent extends DfEvent {
  constructor(type, payload) {
    if (type !== EventType.TABLE_ROW_ACTION) {
      throw new Error('Wrong event type');
    }
    super(type, payload);
  }

  execute() {
    super.execute();
    console.log('tr event', this);
    if (this[this.payload.eventData.name]) {
      this[this.payload.eventData.name]();
    }
  }

  delete() {
    // eslint-disable-next-line no-debugger
    debugger;
    console.log('deleting row', this.payload.payload);
    apiClient.delete(`${this.consumer.baseURL}/${this.payload.payload[this.consumer.pkName]}/`).then((res) => {
      console.log(res);
      // TODO: instead of reload just splice row from list of rows
      this.consumer.reload();
    }).catch((errRes) => {
      console.log(errRes);
    });
  }
}

export default TableRowEvent;
