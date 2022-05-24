class DfEvent {
  constructor(type, payload) {
    this.type = type;
    this.payload = payload;
    this.consumer = payload ? payload.consumer : null;
  }

  // eslint-disable-next-line class-methods-use-this
  execute() {
    console.log('super event execute');
  }
}

export default DfEvent;
