<template>
  <component :is="getThemedComponentName('FormLayout')" v-bind="$props"/>
</template>

<script>
import LayoutMixin from '../form/layout.mixin';
import ThemeMixin from '../util/theme-mixin';

export default {
  name: 'FormLayout',
  mixins: [ThemeMixin],
  props: LayoutMixin.props,
};
</script>
