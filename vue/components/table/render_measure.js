/**
 * This mixin reports measured dimensions of rendered DOM
 * It works in tandem with TableColumnSizer mixin that actually generates the resulting styles
 */
export default {
  emits: ['render-measured'],
  mounted() { this.measureRenderedDimensions(); },
  updated() { this.measureRenderedDimensions(); },
  methods: {
    measureRenderedDimensions() {
      this.$nextTick(() => {
        Object.keys(this.$refs).reduce((res, colName) => {
          const tmp = this.$refs[colName]; // get the ref
          const elements = Array.isArray(tmp) ? tmp : [tmp]; // make sure the ref is an array
          if (!elements.length) return res; // as column defs change, columns are reset, but refs from before stay
          if (colName.substr(0, 4) === 'col-') {
            const col = this.renderedColumns.getColByName[colName.substr(4)];
            col.maxWidth = Math.max.apply(null, elements.map((el) => el.clientWidth));
          } else if (colName.substr(0, 3) === 'row') {
            const cs = this.rowData.dfControlStructure;
            cs.measuredHeight = Math.max.apply(null, elements.map((el) => el.clientHeight));
          }
          return res;
        }, []);
      });
    },
  },
};
