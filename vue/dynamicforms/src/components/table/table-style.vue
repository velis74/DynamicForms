<script setup lang="ts">
import { onUpdated } from 'vue';

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
  uniqueId: string
}>();

function generateStyle(uniqueId: string, responsiveColumns: IndexedArray<TableColumn>) {
  let style = `
  #${uniqueId} {
    position: relative; /* position ensures resize observer to work */
    overflow-x: auto;
    font-size: 1rem; /* overrides vuetify which specifies .875 for panel body */
  }
  #${uniqueId} > * { /* thead, tbody, tfoot */
    width: fit-content;
    min-width: 100%;
  }

  #${uniqueId} .df-row {
    display: block;
    white-space: nowrap;
    background-color: white;
    transition: filter 0.4s ease
  }

  #${uniqueId} .data-row:hover {
    filter: brightness(95%);
    cursor: pointer;
  }

  #${uniqueId} .data-selected {
    filter: brightness(90%);
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

let tableStyle = generateStyle(props.uniqueId, props.columns);

onUpdated(() => {
  tableStyle = generateStyle(props.uniqueId, props.columns);
});
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
