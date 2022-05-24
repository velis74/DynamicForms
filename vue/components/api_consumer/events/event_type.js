import Enum from 'enum';

const EventType = new Enum({
  TABLE: 1,
  ROW: 2,
  TABLE_ROW_ACTION: 3,
  TABLE_ACTION: 4,
  ACTION: 5,
}, { freeze: true });

export default EventType;
