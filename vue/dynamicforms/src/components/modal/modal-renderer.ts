import _ from 'lodash';
import { defineComponent, h, resolveComponent, DefineComponent } from 'vue';

import FilteredActions from '../actions/filtered-actions';

import { Dialogs } from './namespace';

function processSlot(
  slot: string,
  content: Dialogs.DialogSectionContent | DefineComponent | FilteredActions | Dialogs.CustomComponentMessage,
) {
  // Test
  if (content == null) return null;
  // Test 2
  if (typeof content === 'string') {
    // The slot is a plain string so let's just create a span element
    return () => h('span', null, content);
  }
  if (content instanceof FilteredActions) {
    // the slot is FilteredActions. Need to construct a DfActions component
    return () => h(resolveComponent('DfActions'), { slot, actions: content });
  }
  // Test 4
  if (content && 'componentName' in content && 'props' in content) {
    const component = _.isString(content.componentName) ?
      resolveComponent(content.componentName) :
      content.componentName; // it is a component
    return () => h(component, { slot, ...content.props });
  }
  // we have slots as render functions (template usage of DfDialog)
  return content;
}

export default /* #__PURE__ */ defineComponent({
  methods: {
    renderFunction(
      curDlgKey: number,
      titleSlot: Dialogs.DialogSectionContent,
      bodySlot: Dialogs.DialogMessage,
      actionsSlot: Dialogs.DialogSectionContent | FilteredActions,
      options: Dialogs.DialogOptions,
    ) {
      return h(
        // Jure 16.3.2023 types don't match here, but the code works. Too green to be able to fix
        // @ts-ignore
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
