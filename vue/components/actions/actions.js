import ActionsHandler from './actions_handler';
import ActionsUtils from './actions_util';

export default {
  mixins: [ActionsUtils],
  props: {
    actions: { type: ActionsHandler, required: false, default: null },
    position: { type: String, required: true },
    field: { type: String, required: false, default: null },
  },
  data() {
    return { displayStyle: {} };
  },
  computed: {
    actionList() {
      if (this.actions == null) {
        return null;
      }
      return this.actions.filter(this.position, this.field).list;
    },
  },
  methods: {
    getBoolValueOrDef(value, defValue) {
      if (value == null) {
        return defValue;
      }
      return value;
    },
  },
};
