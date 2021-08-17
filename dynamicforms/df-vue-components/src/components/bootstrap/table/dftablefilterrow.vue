<template>
  <tr class="dynamicforms-filterrow">
    <th v-if="actionsRowStart.list.length" class="tr-th-action">
      <Actions :row="null" :actions="actionsRowStart"></Actions>
    </th>
    <th v-for="(column, idx) in columns" :key="idx">
      <!--  todo: { field: column } must be removed, unify incoming data    -->
      <dfformcolumn :key="idx" :def="{ field: column }" :data="filter" v-on:onValueConfirmed="onValueConfirmed"
                    :errors="{}" :showLabelOrHelpText="false" :cssClasses="''"/>
    </th>
    <th v-if="actionsRowEnd.list.length" class="tr-th-action">
      <Actions :row="null" :actions="actionsRowEnd"></Actions>
    </th>
  </tr>
</template>

<script>
import _ from 'lodash';
import dfformcolumn from '@/components/bootstrap/form/dfformcolumn.vue';
import DisplayMode from '@/logic/displayMode';
import Actions from '@/components/bootstrap/actions.vue';
import ActionsHandler from '@/logic/actionsHandler';

export default {
  name: 'dftablefilterrow',
  props: ['configuration'],
  data() {
    return {
      filter: {},
      actionsRowEnd: new ActionsHandler(this.configuration.actions,
        null, this.configuration.uuid).filter('FILTER_ROW_END'),
      actionsRowStart: new ActionsHandler(this.configuration.actions,
        null, this.configuration.uuid).filter('FILTER_ROW_START'),
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
  components: {
    dfformcolumn,
    Actions,
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
