export default {
  emits: ['render-measured'],
  mounted() { this.measureRenderedDimensions(); },
  updated() { this.measureRenderedDimensions(); },
  methods: {
    measureRenderedDimensions() {
      this.$nextTick(() => {
        this.renderedColumns.forEach((col) => {
          if (!(col.name in this.$refs)) return; // there are no rows, so nothing was drawn
          this.$emit('render-measured', {
            name: col.name,
            maxWidth: Math.max.apply(null, this.$refs[col.name].map((el) => el.getBoundingClientRect().width)),
          });
        });
      });
    },
  },
};
