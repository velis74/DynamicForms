<template>
  <component :is="getThemedComponentName('Actions')" v-bind="$props"/>
</template>
<script>
import ActionsMixin from '../actions/actions-mixin';
import ThemeMixin from '../util/theme_mixin';

export default {
  name: 'DfActions',
  mixins: [ThemeMixin],
  props: ActionsMixin.props, // the same props as in tables
};
</script>
