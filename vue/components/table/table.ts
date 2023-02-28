import ResizeObs from 'resize-observer-polyfill';
import { computed, ComputedRef, onBeforeUpdate, onMounted, onUnmounted, onUpdated, ref } from 'vue';

import FilteredActions from '../actions/filtered-actions';
import ColumnDisplay from '../classes/display-mode';
import IndexedArray from '../classes/indexed-array';

import TableColumn from './definitions/column';
import TableFilterRow from './definitions/filterrow';
import { ResponsiveLayout, ResponsiveLayouts } from './definitions/responsive-layout';
import TableRow from './definitions/row';
import TableRows from './definitions/rows';

/**
 * Base Table (composable): provides logic for table component.
 *
 * See table-bootstrap.vue & table-vuetify.vue for respective component declarations
 */

let uniqueIdGenerator = 0;

export interface TableBasePropsInterface {
  pkName: string;
  title: string;
  columns: TableColumn[];
  responsiveTableLayouts: object | null;
  columnDefs: object;
  rows: TableRows;
  loading: boolean;
  actions: FilteredActions;
  filterDefinition: TableFilterRow | null;
}

export function useTableBase(props: TableBasePropsInterface) {
  const containerWidth = ref(0);
  const container = ref();

  const resizeObserver = new ResizeObs((entries) => {
    // while redrawing, sometimes ResizeObserver will report width for the old as well as for the new element
    const width = Math.max.apply(null, entries.map((entry) => entry.contentRect.width));
    // while redrawing, ResizeObserver will ofter report the old element being resized to zero
    if (width) containerWidth.value = entries[0].contentRect.width;
  });
  onMounted(() => { setTimeout(() => resizeObserver.observe(container.value), 1); });
  onBeforeUpdate(() => { resizeObserver.unobserve(container.value); });
  onUpdated(() => { setTimeout(() => resizeObserver.observe(container.value), 1); });
  onUnmounted(() => { resizeObserver.disconnect(); });

  const renderedColumns: ComputedRef<IndexedArray<TableColumn>> = computed(
    () => new IndexedArray<TableColumn>(
      props.columns.filter(
        (column: TableColumn) => (
          column.visibility === ColumnDisplay.FULL || column.visibility === ColumnDisplay.INVISIBLE
        ),
      ),
    ),
  );
  const responsiveLayouts: ComputedRef<ResponsiveLayouts> = computed(
    () => new ResponsiveLayouts(renderedColumns.value, props.responsiveTableLayouts),
  );
  const responsiveLayout: ComputedRef<ResponsiveLayout> = computed(
    () => responsiveLayouts.value.recalculate(containerWidth.value || 0),
  );
  const responsiveLayoutWidth: ComputedRef<number> = computed(
    () => responsiveLayout.value.totalWidth,
  );
  const responsiveColumns: ComputedRef<IndexedArray<TableColumn>> = computed(
    () => responsiveLayout.value.columns,
  );
  const dataColumns: ComputedRef<TableColumn[]> = computed(
    () => props.columns.filter((column: TableColumn) => column.visibility === ColumnDisplay.HIDDEN),
  );
  const theadRowData: ComputedRef<TableRow> = computed(
    // Creates a fake table row with column labels for data
    () => new TableRow(renderedColumns.value.reduce((result, col) => {
      result[col.name] = col.label;
      return result;
    }, {})),
  );

  return {
    uniqueId: `table-${uniqueIdGenerator++}`,
    container,
    renderedColumns,
    containerWidth,
    responsiveLayouts,
    responsiveLayout,
    responsiveLayoutWidth,
    responsiveColumns,
    dataColumns,
    theadRowData,
    onMeasure: (refName: string, maxWidth: number) => {
      if (maxWidth) containerWidth.value = maxWidth;
    },
  };
}
