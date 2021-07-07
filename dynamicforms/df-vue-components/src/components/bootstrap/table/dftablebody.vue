<template>
  <tbody>
  <tr v-for="row in rows" :key="row.id"
      :style="row.df_control_data.row_css_style"
      v-observe-visibility="rows.getVisibilityHandler(row.id)"
      @click="rowClick('ROW_CLICK', row)" @mouseup.right="rowClick('ROW_RIGHTCLICK')"
  >
    <td v-for="col in columns" :key="col.name">
      <component v-if="col.renderDecoratorComponentName"
                 :is="col.renderDecoratorComponentName"
                 :row="row" :column="col"
                 :value="row[col.name]" :body-id="$parent._uid"/>
      <Actions v-else-if="['#actions-row_start', '#actions-row_end'].includes(col.name)"
               :row="row"
               :actions="actions.filter(col.name.substr(9).toUpperCase())"
      >
      </Actions>
      <div v-else v-html="col.renderDecoratorFunction(row, col, row[col.name])"/>
    </td>
  </tr>
  </tbody>
</template>

<script>
import dftablecellfloat from '@/components/bootstrap/tableCells/dftablecellfloat.vue';
import Actions from '@/components/bootstrap/actions.vue';

export default {
  name: 'dftablebody',
  props: ['columns', 'rowProperties', 'rows', 'loading', 'actions'],
  data() {
    return {
      // rowProps: this.rowProperties.reduce((obj, val) => {
      //   if (!['row_css_style', 'df_control_data', 'df_prev_id'].includes(val)) {
      //     // eslint-disable-next-line no-param-reassign
      //     obj[`data-${val}`] = row[val];
      //   }
      //   return obj;
      // }, {}),
    };
  },
  methods: {
    rowClick(position, row) {
      const actions = this.actions.filter(position);
      actions.list.forEach((action) => {
        actions.exec(action, row);
      });
    },
  },
  components: { Actions, dftablecellfloat },
};
</script>

<style scoped>

</style>
