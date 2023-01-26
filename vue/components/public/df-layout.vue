<template>
  <component :is="getThemedComponentName('FormLayout')" v-bind="$props"/>
</template>

<script lang="ts">
import { defineComponent } from 'vue';

import LayoutMixin from '../form/layout.mixin';
import ThemeMixin from '../util/theme-mixin';

export default /* #__PURE__ */ defineComponent({
  name: 'FormLayout',
  mixins: [ThemeMixin],
  props: LayoutMixin.props,
});
</script>
