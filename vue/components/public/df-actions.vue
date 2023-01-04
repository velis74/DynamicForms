<template>
  <component :is="getThemedComponentName('Actions')" v-bind="$props"/>
</template>

<script lang="ts">
import { defineComponent } from 'vue';

import ActionsMixin from '../actions/actions-mixin';
import ThemeMixin from '../util/theme-mixin';

export default /* #__PURE__ */ defineComponent({
  name: 'DfActions',
  mixins: [ThemeMixin],
  props: ActionsMixin.props, // the same props as in tables
});
</script>
