import ColumnDisplay from './definitions/display_mode';

/**
 * This mixin takes care of column sizing and generating appropriate styles for our table component.
 * It works in tandem with MeasureRender mixin that actually triggers the measuring events
 *
 * TODO: adapt styles to bootstrap / vuetify. check paddings, margins, etc
 * TODO: support striped, dark / light, dense
 */
function generateStyle(uniqueId, renderedColumns) {
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
    height: .25em; 
    background: linear-gradient(rgba(0,0,0,.4), rgba(0,0,0,0)); 
  }
  
  #${uniqueId} .df-col { 
    white-space: nowrap; 
    display: inline-block; 
    vertical-align: top; 
    margin: .5em .25em; 
  }
  
  #${uniqueId} .df-col.ordering { 
    cursor: pointer; 
    user-select: none; 
  }
  
  #${uniqueId} .df-col > * { 
    display: inline-block; 
  } 
  `;

  if (renderedColumns) {
    renderedColumns.items.forEach((column, index) => {
      style += `
      #${uniqueId} .df-col:nth-of-type(${index + 1}) { 
        min-width: ${column.maxWidth}px; 
      }`;
    });
  }
  return style;
}

let uniqueIdGenerator = 0;

export default {
  data() {
    const uniqueId = `table-${uniqueIdGenerator++}`;
    return { uniqueId };
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
    tableStyle() { return generateStyle(this.uniqueId, this.renderedColumns); },
  },
  methods: {
    resetStyle() {
      // column definitions got changed, so this is probably a new table, so let's restart measurements and styles
      this.uniqueId = `table-${uniqueIdGenerator++}`;
    },
  },
  watch: { columns: { handler() { this.resetStyle(); }, deep: true } },
};
