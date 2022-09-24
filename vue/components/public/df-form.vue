<template>
  <component :is="getThemedComponentName('Form')" v-bind="$props"/>
</template>
<script>
import Form from '../form/form';
import ThemeMixin from '../util/theme-mixin';

export default {
  name: 'DfForm',
  mixins: [ThemeMixin],
  props: Form.props, // the same props as in forms
};
</script>
