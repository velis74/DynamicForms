<template>
  <component :is="getThemedComponentName('FormLayout')" v-bind="$props"/>
</template>

<script>
import ThemeMixin from '../util/theme-mixin';

import LayoutMixin from './layout.mixin';

export default {
  name: 'FormLayout',
  mixins: [ThemeMixin],
  props: LayoutMixin.props,
  mounted() {
    console.log(this.getThemedComponentName('FormLayout'));
    console.log(this.$props);
  },
};
</script>
