<script>
import _ from 'lodash';

export default {
  name: 'EventEmitterMixin',
  emits: ['value-changed'],
  data() { return { dfEventEmitter: false }; },
  computed: {
    parentEmitter() {
      let parent = this.$parent;
      while (parent && parent.dfEventEmitter !== true) parent = parent.$parent;
      return parent;
    },
  },
  methods: {
    emit(eventName, eventData) {
      // If this component is an event emitter, emit. Also emit if this component has no parent that is an emitter
      if (this.dfEventEmitter || !this.parentEmitter) this.$emit(eventName, eventData);
      if (this.parentEmitter) {
        // if there's yet a parent that is an emitter, have it emit the event as well
        const oldValue = _.cloneDeep(this.payload);
        oldValue[eventData.field] = eventData.oldValue;
        console.log('a', { field: eventData.field.name, oldValue, newValue: this.payload });
        this.parentEmitter.emit(
          'value-changed',
          { field: this.parentEmitter.fieldName, oldValue, newValue: this.payload },
        );
      }
    },
  },
};
</script>
