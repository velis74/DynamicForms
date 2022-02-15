import ColumnDisplay from './definitions/display_mode';

/**
 * This mixin takes care of column sizing and generating appropriate styles for our table component.
 * It works in tandem with MeasureRender mixin that actually triggers the measuring events
 *
 * TODO: adapt styles to bootstrap / vuetify. check paddings, margins, etc
 * TODO: support striped, dark / light, dense
 */
function generateStyle(uniqueId, renderedColumns) {
  // Unfortunately, this would have been much nicer as a computed value, but alas it did not work properly

  let style = '';
  style += `#${uniqueId} { position: relative; overflow-x: auto; } `; // position ensures resize observer to work
  style += `#${uniqueId} > * { width: fit-content; min-width: 100%; } `;
  style += `#${uniqueId} .df-row { display: block; white-space: nowrap; } `;
  const linear = 'linear-gradient(rgba(0,0,0,.4), rgba(0,0,0,0));';
  style += `#${uniqueId} > .df-thead > .df-separator { height: .25em; background: ${linear} } `;
  style += `#${uniqueId}` +
    ' .df-col { white-space: nowrap; display: inline-block; vertical-align: top; margin: .5em .25em; } ';
  style += `#${uniqueId} .df-col.ordering { cursor: pointer; user-select: none; } `;
  style += `#${uniqueId} .df-col > * { display: inline-block; } `;

  // console.log(this.maxColWidth);
  if (renderedColumns) {
    renderedColumns.items.forEach((column, index) => {
      style += (
        `#${uniqueId} .df-col:nth-of-type(${index + 1}) { ` +
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
      tableStyle: generateStyle(uniqueId, null),
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
      this.tableStyle = generateStyle(this.uniqueId, this.renderedColumns);
    },
  },
  watch: { columns: { handler() { this.resetStyle(); }, deep: true } },
};
