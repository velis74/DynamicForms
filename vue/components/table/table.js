import ColumnDisplay from '../api_consumer/table_column_display';

let uniqueIdGenerator = 0;

function generateStyle(wrap, uniqueId, columns, maxColWidth) {
  // Unfortunately, this would have been much nicer as a computed value, but alas it did not work properly

  let style = '';
  if (wrap) {
    style += `.${uniqueId} > * > .df-row { display: block; white-space: wrap; } `;
  } else {
    style += `.${uniqueId} { overflow-x: auto } `;
    style += `.${uniqueId} > * { width: fit-content; min-width: 100%; } `;
    style += `.${uniqueId} > * > .df-row { display: block; white-space: nowrap; } `;
  }
  style += `.${uniqueId} > .df-thead > .df-separator { height: .25em; `;
  style += 'background: linear-gradient(rgba(0,0,0,.4), rgba(0,0,0,0)); } ';
  style += `.${uniqueId} > * > .df-row > .df-col { display: inline-block; margin: .5em .25em; } `;

  // console.log(this.maxColWidth);
  columns.forEach((column, index) => {
    style += (
      `.${uniqueId} > * > .df-row > .df-col:nth-of-type(${index + 1}) { ` +
      `min-width: ${maxColWidth[column.name] || 0}px; }`
    );
  });
  return style;
}

/**
 * Base Table mixin: provides logic for table component.
 *
 * See table_bootstrap.vue & table_vuetify.vue for respective component declarations
 */
export default {
  props: {
    pkName: { type: String, required: true },
    title: { type: String, required: true },
    columns: { type: Array, required: true },
    columnDefs: { type: Object, required: true },
    rows: { type: Array, required: true },
    wrap: { type: Boolean, default: false },
  },
  data() {
    const uniqueId = `table-${uniqueIdGenerator++}`;
    return {
      uniqueId,
      maxColWidth: {},
      tableStyle: generateStyle(this.wrap, uniqueId, [], {}),
    };
  },
  computed: {
    renderedColumns() {
      return this.columns.filter(
        (column) => (
          column.visibility === ColumnDisplay.FULL ||
          column.visibility === ColumnDisplay.INVISIBLE
        ),
      );
    },
    dataColumns() { return this.columns.filter((column) => column.visibility === ColumnDisplay.HIDDEN); },
  },
  mounted() { this.regenerateStyle(); },
  updated() { this.regenerateStyle(); },
  methods: {
    resetStyle() {
      // column definitions got changed, so this is probably a new table, so let's restart measurements and styles
      this.maxColWidth = {};
      this.uniqueId = `table-${uniqueIdGenerator++}`;
      this.regenerateStyle();
    },
    regenerateStyle() {
      this.tableStyle = generateStyle(this.wrap, this.uniqueId, this.renderedColumns, this.maxColWidth);
    },
    measureRenders(data) {
      this.maxColWidth[data.name] = Math.max(this.maxColWidth[data.name] || 0, data.maxWidth || 0);
      this.regenerateStyle();
    },
  },
  watch: {
    columns() { this.resetStyle(); },
    wrap() { this.regenerateStyle(); },
  },
};
