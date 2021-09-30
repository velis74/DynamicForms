<template>
  <tr class="dynamicforms-filterrow">
    <th v-if="actionsRowStart.list.length" class="tr-th-action">
      <Actions :row="null" :actions="actionsRowStart"/>
    </th>
    <th v-for="(column, idx) in columns" :key="idx">
      <!--  todo: { field: column } must be removed, unify incoming data    -->
      <DFFormColumn
        :key="idx"
        :def="{ field: column }"
        :data="filter"
        :errors="{}"
        :show-label-or-help-text="false"
        :css-classes="''"
        @onValueConfirmed="onValueConfirmed"
      />
    </th>
    <th v-if="actionsRowEnd.list.length" class="tr-th-action">
      <Actions :row="null" :actions="actionsRowEnd"/>
    </th>
  </tr>
</template>

<script>
import _ from 'lodash';

import ActionsHandler from '../../../logic/actionsHandler';
import DisplayMode from '../../../logic/displayMode';
import Actions from '../actions.vue';
import DFFormColumn from '../form/dfformcolumn.vue';

export default {
  name: 'DFTableFilterRow',
  components: {
    DFFormColumn, Actions,
  },
  props: {
    configuration: { type: Object, required: true },
  },
  data() {
    return {
      filter: {},
    };
  },
  computed: {
    uuid() { return this.configuration.uuid; },
    actions() { return this.configuration.actions; },
    actionsRowEnd() {
      return new ActionsHandler(this.actions, null, this.uuid).filter('FILTER_ROW_END');
    },
    actionsRowStart() {
      return new ActionsHandler(this.actions, null, this.uuid).filter('FILTER_ROW_START');
    },
    columns() {
      // todo: which columns are in filter needs to be configured in serializer......
      // we're currently matching DFTable's filtering to full visibility
      return _.filter(this.configuration.columns, (c) => c.visibility.table === DisplayMode.FULL);
    },
  },
  methods: {
    onValueConfirmed(doFilter) {
      this.$emit('setTableFilter', { filter: this.filter, doFilter });
    },
  },
};
</script>

<style scoped>
th.ordering {
  cursor: pointer;
  user-select: none;
}

th.ordering > span.ordering > div.ordering-arrow {
  font-size: 125%;
  line-height: .8em; /* increase font size for the arrow */
  display: inline-block; /* but do not allow it to affect line size */
}

.tr-th-action {
  vertical-align: top;
}
</style>
