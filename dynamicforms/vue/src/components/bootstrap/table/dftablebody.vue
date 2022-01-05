<template>
  <tbody>
    <tr
      v-for="row in rows"
      :key="row.id"
      v-observe-visibility="rows.getVisibilityHandler(row.id)"
      :data-id="row.id"
      :style="row.df_control_data.row_css_style"
      @click="rowClick($event,'ROW_CLICK', row)"
      @mouseup.right="rowClick($event,'ROW_RIGHTCLICK', row)"
    >
      <td v-for="col in columns" :key="col.name" :data-name="col.name">
        <!-- first we render any field start actions -->
        <Actions :row="row" :actions="actions.filter('FIELD_START', col.name)"/>
        <!-- then the field component itself -->
        <component
          :is="col.renderDecoratorComponentName"
          v-if="col.renderDecoratorComponentName"
          :row="row"
          :column="col"
          :value="row[col.name]"
          :body-id="$parent._uid"
        />
        <!-- but maybe the field component is actually a row start / end actions field -->
        <Actions
          v-else-if="['#actions-row_start', '#actions-row_end'].includes(col.name)"
          :row="row"
          :actions="actions.filter(col.name.substr(9).toUpperCase())"
        />
        <!-- or it's just a decorated text and not a component -->
        <div v-else style="display: inline-block" v-html="col.renderDecoratorFunction(row, col, row[col.name])"/>
        <!-- we finish up with any field end actions -->
        <Actions :row="row" :actions="actions.filter('FIELD_END', col.name)"/>
      </td>
    </tr>
  </tbody>
</template>

<script>
import Actions from '../actions.vue';
import DFTableCellDatetime from '../tableCells/dftablecelldatetime.vue';
import DFTableCellFloat from '../tableCells/dftablecellfloat.vue';

export default {
  name: 'DFTableBody',
  components: { Actions, DFTableCellFloat, DFTableCellDatetime },
  props: {
    columns: { type: Array, required: true },
    rows: { type: Array, required: true },
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
