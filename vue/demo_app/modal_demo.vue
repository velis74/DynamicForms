<template>
  <div>
    <v-row justify="center" class="my-4">
      <v-btn @click="btnClick('template')">Template</v-btn>
      <v-btn @click="btnClick('procedural')">Procedural</v-btn>
      <v-btn @click="btnClick('nested', 1)">Nested</v-btn>
    </v-row>
    <df-modal v-model="showTemplate">
      <div slot="title">Modal as template</div>
      <div slot="body">
        <p>This modal is created as a template in this demo page.</p>
        <p>
          It should be trivial to insert any markup you wish.<br>
          <b>This bold</b> is just for testing whether everything works.<br>
          This counter too: {{ counter }}<br>
        </p>
      </div>
      <div slot="actions">
        <df-actions :actions="templateDialogActions"/>
      </div>
    </df-modal>
  </div>
</template>

<script>
import Action from '../components/actions/action';
import FilteredActions from '../components/actions/filtered-actions';
import DialogSize from '../components/classes/dialog_size';
import { DfModal } from '../components/modal';
import { DfActions } from '../components/public';

export default {
  name: 'ModalDemo',
  components: { DfModal, DfActions },
  data() {
    return {
      showTemplate: false,
      templateDialogActions: new FilteredActions([Action.closeAction()]),
      counter: 1,
    };
  },
  computed: { DialogSize() { return DialogSize; } },
  methods: {
    async btnClick(which, level) {
      switch (which) {
      case 'template':
        this.showTemplate = !this.showTemplate;
        if (this.showTemplate) {
          const intervalId = window.setInterval(() => {
            this.counter++;
            if (!this.showTemplate) window.clearInterval(intervalId);
          }, 2500);
        }
        break;
      case 'procedural': {
        const res = await this.$dfModal.yesNo(
          'Procedural modal dialog',
          'This modal was shown by calling a method from your code.\nPlease click one of the buttons.\n' +
          'In the mean time, the code is waiting and will proceed execution when you decide on one of the buttons',
        );
        await this.$dfModal.message('Result', `You clicked the "${res.action.label}" button`);
        break;
      }
      case 'nested': {
        const suggestedSize = [DialogSize.SMALL, DialogSize.DEFAULT, DialogSize.LARGE][Math.floor(Math.random() * 3)];
        await this.$dfModal.message(
          'Nested dialogs example',
          `This is dialog nesting ${level}\n` +
          'Click "Nest" to generate another dialog',
          new FilteredActions([
            // this.$modal.button('close')
            new Action({
              name: 'nest',
              label: 'Nest',
              position: 'FORM_FOOTER',
              handlerWithPayload: {
                handler: () => {
                  this.btnClick('nested', level + 1);
                  return true;
                },
                payload: null,
              },
            }),
            Action.closeAction(),
          ]),
          { size: suggestedSize },
        );
        break;
      }
      default:
        break;
      }
    },
    actionClose() { // action, payload, extraData) {
      // handles the close action of the template-based dialog
      this.showTemplate = false;
      return true;
    },
  },
};
</script>
