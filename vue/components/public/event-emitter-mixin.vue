<script>
import _ from 'lodash';

export default {
  name: 'EventEmitterMixin',
  emits: ['value-changed'],
  data() {
    return { dfEventHandler: false };
  },
  computed: {
    parentEmitter() {
      return this.getParentEmitter();
    },
  },
  methods: {
    getParentEmitter(getPayload = false) {
      let parent = this.$parent;
      let payload = null;
      while (parent && parent.dfEventHandler !== true) {
        parent = parent.$parent;
        if (parent.payload && !payload) {
          payload = parent.payload;
        }
      }
      if (getPayload) {
        return payload;
      }
      return parent;
    },
    emit(eventName, eventData) {
      if (this.parentEmitter && this.parentEmitter.handleEvent(
        eventName,
        {
          eventData: _.cloneDeep(eventData),
          payload: _.cloneDeep(this.getParentEmitter(true)),
          consumer: this.parentEmitter.consumer,
        },
      )) {
        return;
      }
      console.log(535353);
      if (this.handleEvent) {
        this.handleEvent(eventName, eventData);
      }
    },
  },
};
</script>
