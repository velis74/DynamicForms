<template>
  <div>
    <component :is="renderComponent" v-bind="renderComponentData"/>
  </div>
</template>
<script>
import ThemeMixin from '../util/theme_mixin';

import APIConsumerLogic from './api_consumer_logic';
import ComponentDisplay from './component_display';

export default {
  name: 'APIConsumer',
  mixins: [ThemeMixin],
  props: {
    /**
     * Object containing the properties required to render at least one of the display components
     */
    consumer: { type: APIConsumerLogic, required: true },
    /**
     * What UX should the component render
     */
    displayComponent: { type: Object, required: true, validator(value) { return ComponentDisplay.isDefined(value); } },
  },
  data() { return { orderingCounter: this.consumer.ordering.counter.counter }; },
  computed: {
    renderComponent() {
      switch (this.displayComponent) {
      case ComponentDisplay.TABLE:
        return `${this.theme.name.capitalised}Table`;
      case ComponentDisplay.FORM:
        return `${this.theme.name.capitalised}Form`;
      case ComponentDisplay.DIALOG:
        return `${this.theme.name.capitalised}Dialog`;
      default:
        throw Error('Unknown component display type');
      }
    },
    renderComponentData() {
      switch (this.displayComponent) {
      case ComponentDisplay.TABLE:
        return this.consumer.tableDefinition;
      default:
        throw Error('Unknown component display type');
      }
    },
  },
  watch: {
    'consumer.ordering': {
      handler() {
        if (this.orderingCounter !== this.consumer.ordering.counter.counter) {
          this.consumer.reload();
        }
      },
      deep: true,
    },
  },
};
</script>
