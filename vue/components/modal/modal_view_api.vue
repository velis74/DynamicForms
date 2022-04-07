<script>
import ModalViewList from './modal_view_list';

export default {
  mixins: [ModalViewList],
  methods: {
    fromRenderFunctions(existingDialog, slots) {
      return this.pushDialog(slots, existingDialog);
    },
    message(title, message) {
      return this.pushDialog({
        title,
        body: message,
        actions: null, // TODO: Create FilteredActions object here [{ close: 'default' }]
      }, null);
    },
    yesNo(title, question, actions, options) {
      return this.pushDialog({
        title,
        body: question,
        actions, // TODO: Create FilteredActions object here [{ yes: 'default' }, { no: 'default' }]
        options,
      }, null);
    },
  },
};
</script>
