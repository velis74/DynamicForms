import ColumnDisplay from './definitions/display_mode';

/**
 * This mixin takes care of column sizing and generating appropriate styles for our table component.
 * It works in tandem with MeasureRender mixin that actually triggers the measuring events
 *
 * TODO: adapt styles to bootstrap / vuetify. check paddings, margins, etc
 * TODO: support striped, dark / light, dense
 */
function generateStyle(wrap, uniqueId, renderedColumns) {
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
  style += `.${uniqueId} > .df-thead > .df-row > .df-col { white-space: nowrap; } `;
  style += `.${uniqueId} > .df-thead > .df-row > .df-col.ordering { cursor: pointer; user-select: none; } `;
  style += `.${uniqueId} > * > .df-row > .df-col { display: inline-block; vertical-align: top; margin: .5em .25em; } `;

  // console.log(this.maxColWidth);
  if (renderedColumns) {
    renderedColumns.items.forEach((column, index) => {
      style += (
        `.${uniqueId} > * > .df-row > .df-col:nth-of-type(${index + 1}) { ` +
        `min-width: ${column.maxWidth}px; }`
      );
    });
  }
  return style;
}

let uniqueIdGenerator = 0;

export default {
  data() {
    const uniqueId = `table-${uniqueIdGenerator++}`;
    return {
      uniqueId,
      tableStyle: generateStyle(this.wrap, uniqueId, null),
    };
  },
  computed: {
    renderedColumns() {
      return this.columns.reduce((result, column) => {
        if (column.visibility === ColumnDisplay.FULL || column.visibility === ColumnDisplay.INVISIBLE) {
          result.items.push(column);
          result.getColIndexByName[column.name] = result.length - 1;
          result.getColByName[column.name] = column;
        }
        return result;
      }, {
        items: [],
        getColByName: {},
        getColIndexByName: {},
      });
    },
    dataColumns() { return this.columns.filter((column) => column.visibility === ColumnDisplay.HIDDEN); },
  },
  mounted() { this.regenerateStyle(); },
  updated() { this.regenerateStyle(); },
  methods: {
    resetStyle() {
      // column definitions got changed, so this is probably a new table, so let's restart measurements and styles
      this.uniqueId = `table-${uniqueIdGenerator++}`;
      this.regenerateStyle();
    },
    regenerateStyle() {
      this.tableStyle = generateStyle(this.wrap, this.uniqueId, this.renderedColumns);
    },
    measureRenders(data) {
      data.forEach(({ name, maxWidth }) => {
        if (name.substring(0, 4) !== 'col-') return;
        const colName = name.substr(4);
        const col = this.renderedColumns.getColByName[colName];
        if (col) col.maxWidth = maxWidth; // modifying prop's member here. being lazy right now
      });
      this.regenerateStyle();
    },
  },
  watch: {
    columns: { handler() { this.resetStyle(); }, deep: true },
    wrap() { this.regenerateStyle(); },
  },
};
