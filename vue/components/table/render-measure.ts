import { ComponentPublicInstance, defineComponent } from 'vue';

interface MeasurableComponent extends ComponentPublicInstance {
  onMeasure: (colName: string, maxWidth: number, maxHeight: number) => void;
}

/**
 * This mixin reports measured dimensions of rendered DOM
 * It works in tandem with TableColumnSizer mixin that actually generates the resulting styles
 */
export default defineComponent({
  mounted() { this.measureRenderedDimensions(); },
  updated() { this.measureRenderedDimensions(); },
  methods: {
    measureRenderedDimensions() {
      this.$nextTick(() => {
        Object.keys(this.$refs).forEach((colName) => {
          const tmp = this.$refs[colName]; // get the ref
          const elements = Array.isArray(tmp) ? tmp : [tmp]; // make sure the ref is an array
          if (!elements.length) return; // as column defs change, columns are reset, but refs from before stay
          const maxWidth = Math.max.apply(null, elements.map((el) => (el ? el.clientWidth : 0)));
          const maxHeight = Math.max.apply(null, elements.map((el) => (el ? el.clientHeight : 0)));
          const self = this as any as MeasurableComponent;
          if (typeof self.onMeasure === 'function') {
            self.onMeasure(colName, maxWidth, maxHeight);
          }
        });
      });
    },
  },
});
