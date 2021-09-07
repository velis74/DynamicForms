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
    const cfg = this.configuration;
    return {
      filter: {},
      actionsRowEnd: new ActionsHandler(cfg.actions, null, cfg.uuid).filter('FILTER_ROW_END'),
      actionsRowStart: new ActionsHandler(cfg.actions, null, cfg.uuid).filter('FILTER_ROW_START'),
    };
  },
  computed: {
    columns() {
      // todo: which columns are in filter needs to be configured in serializer......
      return _.filter(this.configuration.columns, (c) => c.visibility.table === DisplayMode.FULL &&
          c.visibility.form === DisplayMode.FULL);
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
