import { defineComponent, h, onMounted, onUnmounted } from 'vue';

import ModalRenderer from './modal-renderer';
import dialogList from './modal-view-list';

let uniqueIdCounter = 0;
const instances: number[] = [];

export default defineComponent({
  name: 'ModalView',
  mixins: [ModalRenderer],
  setup() {
    const uniqueId = ++uniqueIdCounter;
    onMounted(() => {
      instances.push(uniqueId);
      if (instances.length > 1 && instances.indexOf(uniqueId) > 0) {
        console.warn('Multiple instances of ModalView placed in VDom. there should be only one!', instances);
        // return;
      }
    });
    onUnmounted(() => {
      const index = instances.indexOf(uniqueId);
      if (index > -1) instances.splice(index, 1);
    });
    // watch(dialogList.current, (newValue, oldValue) => {
    //   console.log('watch triggered', [newValue, oldValue]);
    // });

    // return the render function
    return { uniqueId };
  },
  render() {
    const curDlg = dialogList.current.value;
    const curDlgKey = curDlg?.dialogId;
    // only render if we're the first instance of ModalView
    if (!curDlg || instances.indexOf(this.uniqueId) !== 0) return h('div', { key: curDlgKey });
    return this.renderFunction(<number>curDlgKey, curDlg.title, curDlg.body, curDlg.actions, curDlg.options);
  },
});
