<template>
  <component :is="getThemedComponentName('Actions')" v-bind="$props"/>
</template>
<script>
import Actions from '../actions/actions';
import ThemeMixin from '../util/theme_mixin';

export default {
  name: 'DfActions',
  mixins: [ThemeMixin],
  props: Actions.props, // the same props as in tables
};
</script>
