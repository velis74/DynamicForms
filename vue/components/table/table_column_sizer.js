/**
 * This mixin takes care of column sizing and generating appropriate styles for our table component.
 * It works in tandem with MeasureRender mixin that actually triggers the measuring events
 *
 * TODO: adapt styles to bootstrap / vuetify. check paddings, margins, etc
 * TODO: support striped, dark / light, dense
 */
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
  style += `.${uniqueId} > * > .df-row > .df-col { display: inline-block; vertical-align: top; margin: .5em .25em; } `;

  // console.log(this.maxColWidth);
  columns.forEach((column, index) => {
    style += (
      `.${uniqueId} > * > .df-row > .df-col:nth-of-type(${index + 1}) { ` +
      `min-width: ${maxColWidth[column.name] || 0}px; }`
    );
  });
  return style;
}

let uniqueIdGenerator = 0;

export default {
  data() {
    const uniqueId = `table-${uniqueIdGenerator++}`;
    return {
      uniqueId,
      maxColWidth: {},
      tableStyle: generateStyle(this.wrap, uniqueId, [], {}),
    };
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
      data.forEach(({ name, maxWidth }) => {
        if (name.substring(0, 4) !== 'col-') return;
        const colName = name.substr(4);
        this.maxColWidth[colName] = Math.max(this.maxColWidth[colName] || 0, maxWidth || 0);
      });
      this.regenerateStyle();
    },
  },
  watch: {
    columns() { this.resetStyle(); },
    wrap() { this.regenerateStyle(); },
  },
};
