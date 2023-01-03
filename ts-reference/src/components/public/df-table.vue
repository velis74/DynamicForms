<template>
  <component :is="getThemedComponentName('Table')" v-bind="$props"/>
</template>

<script lang="ts">
import { defineComponent } from 'vue';

import Table from '../table/table';
import ThemeMixin from '../util/theme.mixin';

export default defineComponent({
  name: 'DfTable',
  mixins: [ThemeMixin],
  props: Table.props, // the same props as in tables
});
</script>
