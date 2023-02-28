<script setup lang="ts">
import IndexedArray from '../classes/indexed-array';

import TableColumn from './definitions/column';
import { ColumnGroup } from './definitions/responsive-layout';

/**
 * This component generates the styles for column sizing for our table component.
 * It works in tandem with MeasureRender mixin that actually triggers the measuring events
 *
 * TODO: adapt styles to bootstrap / vuetify. check paddings, margins, etc
 * TODO: support striped, dark / light, dense
 */
const props = defineProps<{
  columns: IndexedArray<TableColumn>
  uniqueId: number
}>();

function generateStyle(uniqueId: number, responsiveColumns: IndexedArray<TableColumn>) {
  let style = `
  #${uniqueId} {
    position: relative; /* position ensures resize observer to work */
    overflow-x: auto;
  }
  #${uniqueId} > * { /* thead, tbody, tfoot */
    width: fit-content;
    min-width: 100%;
  }

  #${uniqueId} .df-row {
    display: block;
    white-space: nowrap;
  }

  #${uniqueId} > .df-thead > .df-separator {
    margin-top: -.25em;
    margin-bottom: .25em; /* these margins ensure that the separator is closer to thead than to rows in tbody */
    height: .25em;
    background: linear-gradient(rgba(0,0,0,.4), rgba(0,0,0,0));
  }

  #${uniqueId} .df-col, #${uniqueId} .column-group {
    white-space: nowrap;
    display: inline-block;
    vertical-align: top;
  }

  #${uniqueId} .df-col {
    padding: .5em .25em;
  }

  #${uniqueId} .df-col.ordering {
    cursor: pointer;
    user-select: none;
  }

  #${uniqueId} .df-col > * { /* ensures that columns themselves act like continuous text */
    display: inline-block;
  }
  `;

  if (responsiveColumns) {
    responsiveColumns.forEach((column: TableColumn) => {
      const isColumnGroup = column instanceof ColumnGroup;
      const colClass = isColumnGroup ? 'column-group' : 'df-col';
      style += `#${uniqueId} .${colClass}.${column.name} { min-width: ${column.maxWidth}px; } `;
      if (isColumnGroup) {
        column.fields.forEach((field) => {
          style += `#${uniqueId} .df-col.${field.name} { min-width: ${field.maxWidth}px; } `;
        });
      }
    });
  }
  return style;
}

const tableStyle = generateStyle(props.uniqueId, props.columns);
/*
export default {
  computed: { tableStyle() { return generateStyle(this.uniqueId, this.responsiveColumns); } },
  methods: {
    resetStyle() {
      // column definitions got changed, so this is probably a new table, so let's restart measurements and styles
      this.uniqueId = `table-${uniqueIdGenerator++}`;
    },
  },
  watch: {
    columns: { handler() { this.resetStyle(); }, deep: true },
    responsiveColumns: { handler() { this.resetStyle(); }, deep: true },
  },
}
*/
</script>
<template>
  <!-- eslint-disable-next-line vue/no-v-text-v-html-on-component-->
  <component :is="'style'" type="text/css" scoped v-html="tableStyle"/>
</template>
