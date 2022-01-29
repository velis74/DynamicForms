<template>
  <div>
    <component :is="renderComponent" v-bind="renderComponentData"/>
  </div>
</template>
<script>
import APIConsumerLogic from './api_consumer_logic';
import ComponentDisplay from './component_display';

export default {
  name: 'APIConsumer',
  props: {
    /**
     * Object containing the props required to render at least one of the display components
     */
    consumer: { type: APIConsumerLogic, required: true },
    /**
     * What UX should the component render
     */
    displayComponent: { type: ComponentDisplay, required: true },
  },
  data() {
    return { UX: new APIConsumerLogic(this.baseURL) };
  },
  computed: {
    renderComponent() {
      switch (this.displayComponent) {
      case ComponentDisplay.TABLE:
        return 'Table';
      case ComponentDisplay.FORM:
        return 'Form';
      case ComponentDisplay.DIALOG:
        return 'Dialog';
      default:
        throw Error('Unknown component display type');
      }
    },
    renderComponentData() {
      return {}; // TODO: this needs to be programmed still
    },
  },
};
</script>
