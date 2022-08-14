<template>
  <div>
    <v-row justify="center" class="my-4">
      <v-btn @click="btnClick('template')">Template</v-btn>
      <v-btn @click="btnClick('procedural')">Procedural</v-btn>
      <v-btn @click="btnClick('nested', 1)">Nested</v-btn>
    </v-row>
    <ModalView/>
    <df-modal v-model="showTemplate">
      <div slot="title">Modal as template</div>
      <div slot="body">
        <p>This modal is created as a template in this demo page.</p>
        <p>
          It should be trivial to insert any markup you wish.
          <b>This bold</b> is just for testing whether everything works.
          This counter too: {{ counter }}
        </p>
      </div>
      <div slot="actions" style="flex: 1">
        <df-actions :actions="templateDialogActions"/>
      </div>
    </df-modal>
  </div>
</template>

<script>
import Action from '../components/actions/action';
import FilteredActions from '../components/actions/filtered-actions';
import DialogSize from '../components/classes/dialog_size';
import { DfModal, ModalView } from '../components/modal';
import { DfActions } from '../components/public';

export default {
  name: 'ModalDemo',
  components: { DfModal, ModalView, DfActions },
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
          'This modal was shown by calling a method from your code.\nWe\'re currently waiting for you to click one' +
          ' of the buttons',
        );
        await this.$dfModal.message('Result', `You clicked the "${res.label}" button`);
        break;
      }
      case 'nested': {
        const suggestedSize = [DialogSize.SMALL, DialogSize.DEFAULT, DialogSize.LARGE][Math.floor(Math.random() * 3)];
        console.log(suggestedSize);
        await this.$dfModal.message(
          'Nested dialogs example',
          `This is dialog nesting ${level}\n` +
          'Click "Nest" to generate another dialog',
          [
            // this.$modal.button('close')
            { name: 'nest', label: 'Nest', action: () => { this.btnClick('nested', level + 1); } },
            { name: 'close' },
          ],
          { size: suggestedSize },
        );
        break;
      }
      default:
        break;
      }
    },
    actionClose() { // action, payload, extraData) {
      this.showTemplate = false;
      return true;
    },
  },
};
</script>
