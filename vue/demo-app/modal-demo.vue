<template>
  <div>
    <v-row justify="center" class="my-4">
      <v-btn @click="btnClick('template')">Template</v-btn>
      <v-btn @click="btnClick('procedural')">Procedural</v-btn>
      <v-btn @click="btnClick('nested', 1)">Nested</v-btn>
    </v-row>
    <df-modal v-model="showTemplate">
      <template #title>
        <div>Modal as template</div>
      </template>
      <template #body>
        <div>
          <p>This modal is created as a template in this demo page.</p>
          <p>
            It should be trivial to insert any markup you wish.<br>
            <b>This bold</b> is just for testing whether everything works.<br>
            This counter too: {{ counter }}<br>
          </p>
        </div>
      </template>
      <template #actions>
        <div>
          <df-actions :actions="templateDialogActions"/>
        </div>
      </template>
    </df-modal>
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';

import Action, { defaultActionHandler } from '../components/actions/action';
import FilteredActions from '../components/actions/filtered-actions';
import { DfModal } from '../components/modal';
import DialogSize from '../components/modal/dialog-size';
import dfModal from '../components/modal/modal-view-api';
import { DfActions } from '../components/public';

export default /* #__PURE__ */ defineComponent({
  name: 'ModalDemo',
  components: { DfModal, DfActions },
  data() {
    return {
      showTemplate: false,
      templateDialogActions: new FilteredActions([Action.closeAction({ actionClose: this.actionClose })]),
      counter: 1,
    };
  },
  methods: {
    async btnClick(which: string, level: number) {
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
        const res = await dfModal.yesNo(
          'Procedural modal dialog',
          'This modal was shown by calling a method from your code.\nPlease click one of the buttons.\n' +
          'In the mean time, the code is waiting and will proceed with execution when you decide on one of the buttons',
        );
        await dfModal.message('Result', `You clicked the "${res.action.label}" button`);
        break;
      }
      case 'nested': {
        const suggestedSize = [DialogSize.SMALL, DialogSize.DEFAULT, DialogSize.LARGE][Math.floor(Math.random() * 3)];
        await dfModal.message(
          'Nested dialogs example',
          `This is dialog nesting ${level}\n` +
          'Click "Nest" to generate another dialog',
          new FilteredActions([
            // this.$modal.button('close')
            new Action({
              name: 'nest',
              label: 'Nest',
              position: 'FORM_FOOTER',
              actionNest: () => {
                this.btnClick('nested', level + 1);
                return true;
              },
            }),
            Action.closeAction({ actionClose: defaultActionHandler }),
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
});
</script>
