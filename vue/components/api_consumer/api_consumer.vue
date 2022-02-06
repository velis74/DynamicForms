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
     * Object containing the properties required to render at least one of the display components
     */
    consumer: { type: APIConsumerLogic, required: true },
    /**
     * What UX should the component render
     */
    displayComponent: { type: Object, required: true, validator(value) { return ComponentDisplay.isDefined(value); } },
  },
  data() { return {}; },
  computed: {
    themeCapitalised() {
      let themeOwner = this.$parent;
      // we traverse the parents until we find the DeomApp parent which actuayll hosts the theme selected
      while (themeOwner && themeOwner.$options.name !== 'DemoApp') {
        themeOwner = themeOwner.$parent;
      }
      return themeOwner.theme.charAt(0).toUpperCase() + themeOwner.theme.slice(1);
    },
    renderComponent() {
      switch (this.displayComponent) {
      case ComponentDisplay.TABLE:
        return `${this.themeCapitalised}Table`;
      case ComponentDisplay.FORM:
        return `${this.themeCapitalised}Form`;
      case ComponentDisplay.DIALOG:
        return `${this.themeCapitalised}Dialog`;
      default:
        throw Error('Unknown component display type');
      }
    },
    renderComponentData() {
      switch (this.displayComponent) {
      case ComponentDisplay.TABLE:
        return {
          title: this.consumer.title('table'),
          pkName: this.consumer.pkName,
          columns: this.consumer.tableColumns,
          columnDefs: this.consumer.fields,
          rows: this.consumer.rows,
          loading: this.consumer.loading,
        };
      default:
        throw Error('Unknown component display type');
      }
    },
  },
};
</script>
