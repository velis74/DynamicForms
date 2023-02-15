import { defineComponent, h, RenderFunction, resolveComponent } from 'vue';

import FilteredActions from '../actions/filtered-actions';

import CustomComponentMessage = Dialogs.CustomComponentMessage;
import DialogMessage = Dialogs.DialogMessage;
import DialogOptions = Dialogs.DialogOptions;

function processSlot(
  slot: string,
  content: string | FilteredActions | CustomComponentMessage | RenderFunction,
) {
  if (content == null) return null;
  if (typeof content === 'string') {
    // The slot is a plain string so let's just create a span element
    return () => h('span', null, content);
  }
  if (content instanceof FilteredActions) {
    // the slot is FilteredActions. Need to construct a DfActions component
    return () => h(resolveComponent('DfActions'), { slot, actions: content });
  }
  if (content && 'componentName' in content && 'props' in content) {
    return () => h(resolveComponent(content.componentName), { slot, ...content.props });
  }
  // we have slots as render functions (template usage of DfDialog)
  return content;
}

export default /* #__PURE__ */ defineComponent({
  methods: {
    renderFunction(
      curDlgKey: number,
      titleSlot: string | RenderFunction,
      bodySlot: DialogMessage | RenderFunction,
      actionsSlot: FilteredActions | RenderFunction,
      options: DialogOptions,
    ) {
      return h(
        resolveComponent('DfModalDialog'),
        { show: true, options: options || {}, key: curDlgKey },
        {
          title: processSlot('title', titleSlot),
          body: processSlot('body', bodySlot),
          actions: processSlot('actions', actionsSlot),
        },
      );
    },
  },
});
