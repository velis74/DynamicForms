<template>
  <component :is="getThemedComponentName('Table')" v-bind="$props"/>
</template>
<script>
import Table from '../table/table';
import ThemeMixin from '../util/theme_mixin';

export default {
  name: 'DfTable',
  mixins: [ThemeMixin],
  props: Table.props, // the same props as in tables
};
</script>
