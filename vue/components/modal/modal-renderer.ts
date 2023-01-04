import { defineComponent, h, RenderFunction, resolveComponent } from 'vue';

import FilteredActions from '../actions/filtered-actions';
import ThemeMixin from '../util/theme-mixin';
import CustomComponentMessage = Dialogs.CustomComponentMessage;
import DialogMessage = Dialogs.DialogMessage;
import DialogOptions = Dialogs.DialogOptions;

function processSlot(
  slot: string,
  content: string | FilteredActions | CustomComponentMessage | RenderFunction,
  actionsView: string,
) {
  if (content == null) return null;
  if (typeof content === 'string') {
    // The slot is a plain string so let's just create a span element
    return () => h('span', null, content);
  }
  if (content instanceof FilteredActions) {
    // the slot is FilteredActions. Need to construct a DfActions component
    return () => h(resolveComponent(actionsView), { slot, actions: content });
  }
  if (content && 'componentName' in content && 'props' in content) {
    return () => h(resolveComponent(content.componentName), { slot, ...content.props });
  }
  // we have slots as render functions (template usage of DfDialog)
  return content;
}

export default /* #__PURE__ */ defineComponent({
  mixins: [ThemeMixin],
  computed: { // eslint-disable-line object-curly-newline
    modalAPIView() { return `${this.theme.name.capitalised}Modal`; },
    actionsView() { return `${this.theme.name.capitalised}Actions`; },
  },
  methods: {
    renderFunction(
      curDlgKey: number,
      titleSlot: string | RenderFunction,
      bodySlot: DialogMessage | RenderFunction,
      actionsSlot: FilteredActions | RenderFunction,
      options: DialogOptions,
    ) {
      return h(
        resolveComponent(this.modalAPIView),
        { show: true, options: options || {}, key: curDlgKey },
        {
          title: processSlot('title', titleSlot, this.actionsView),
          body: processSlot('body', bodySlot, this.actionsView),
          actions: processSlot('actions', actionsSlot, this.actionsView),
        },
      );
    },
  },
});
