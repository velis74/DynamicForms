export default {
  name: 'formFieldChangeMixin',
  props: { rows: {}, uuid: {}, record: { default: null } },
  data() { return { }; },
  emits: ['fieldValueChanged'],
  computed: {
    recordFields() {
      // This entire computed copy of this.record is just so that watcher works as expected.
      // For some reason it won't work properly on record itself
      return Object.keys(this.record).reduce((res, key) => { res[key] = this.record[key]; return res; }, {});
    },
  },
  beforeDestroy() {
  },
  mounted() {
  },
  watch: {
    recordFields: {
      handler: function handler(newValue, oldValue) {
        Object.keys(this.record).map((key) => {
          if (oldValue[key] !== newValue[key]) {
            this.$emit(`${key}-changed`, {
              formID: this.uuid,
              newRec: newValue,
              oldRec: oldValue,
              changedField: key,
            });
          }
          return null;
        });
      },
      deep: true,
    },
  },
};
