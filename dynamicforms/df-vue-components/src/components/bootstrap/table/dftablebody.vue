<template>
  <tbody>
    <tr
      v-for="row in rows"
      :key="row.id"
      v-observe-visibility="rows.getVisibilityHandler(row.id)"
      :data-id="row.id"
      :style="row.df_control_data.row_css_style"
      @click="rowClick($event,'ROW_CLICK', row)"
      @mouseup.right="rowClick($event,'ROW_RIGHTCLICK')"
    >
      <td v-for="col in columns" :key="col.name" :data-name="col.name">
        <Actions :row="row" :actions="actions.filter('FIELD_START', col.name)"/>
        <component
          :is="col.renderDecoratorComponentName"
          v-if="col.renderDecoratorComponentName"
          :row="row"
          :column="col"
          :value="row[col.name]"
          :body-id="$parent._uid"
        />
        <Actions
          v-else-if="['#actions-row_start', '#actions-row_end'].includes(col.name)"
          :row="row"
          :actions="actions.filter(col.name.substr(9).toUpperCase())"
        />
        <div v-else style="display: inline-block" v-html="col.renderDecoratorFunction(row, col, row[col.name])"/>
        <Actions :row="row" :actions="actions.filter('FIELD_END', col.name)"/>
      </td>
    </tr>
  </tbody>
</template>

<script>
import Actions from '../actions.vue';
import DFTableCellFloat from '../tableCells/dftablecellfloat.vue';

export default {
  name: 'DFTableBody',
  components: { Actions, DFTableCellFloat },
  props: {
    columns: { type: Array, required: true },
    rows: { type: Array, required: true },
    loading: { type: Boolean, required: true },
    actions: { type: Object, required: true },
  },
  data() {
    return {};
  },
  methods: {
    rowClick(event, position, row) {
      const actions = this.actions.filter(position);
      actions.list.forEach((action) => {
        actions.exec(event, action, row);
      });
    },
  },
};
</script>

<style scoped>

</style>
