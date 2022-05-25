<template>
  <div>
    ------
    {{ getThemedComponentName('Form') }}
    {{ $props }}
    <component :is="getThemedComponentName('Form')" v-bind="$props"/>
  </div>
</template>
<script>
import Form from '../form/form';
import ThemeMixin from '../util/theme_mixin';

export default {
  name: 'DfForm',
  mixins: [ThemeMixin],
  props: Form.props, // the same props as in forms
};
</script>
