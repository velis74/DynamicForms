<template>
  <tbody>
  <tr v-for="row in rows" :key="row.id"
      :style="row.df_control_data.row_css_style"
      v-observe-visibility="rows.getVisibilityHandler(row.id)"
      @click="rowClick($event,'ROW_CLICK', row)" @mouseup.right="rowClick($event,'ROW_RIGHTCLICK')"
  >
    <td v-for="col in columns" :key="col.name">
      <Actions :row="row" :actions="actions.filter('FIELD_START', col.name)"></Actions>
      <component v-if="col.renderDecoratorComponentName"
                 :is="col.renderDecoratorComponentName"
                 :row="row" :column="col"
                 :value="row[col.name]" :body-id="$parent._uid"/>
      <Actions v-else-if="['#actions-row_start', '#actions-row_end'].includes(col.name)"
               :row="row"
               :actions="actions.filter(col.name.substr(9).toUpperCase())"
      >
      </Actions>
      <div v-else v-html="col.renderDecoratorFunction(row, col, row[col.name])" style="display: inline-block"/>
      <Actions :row="row" :actions="actions.filter('FIELD_END', col.name)"></Actions>
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
      //     obj[`data-${val}`] = row[val];
      //   }
      //   return obj;
      // }, {}),
    };
  },
  methods: {
    rowClick(event, position, row) {
      const actions = this.actions.filter(position);
      actions.list.forEach((action) => {
        actions.exec(event, action, row);
      });
    },
  },
  components: { Actions, dftablecellfloat },
};
</script>

<style scoped>

</style>
