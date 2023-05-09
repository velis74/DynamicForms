/**
 * This mixin reports measured dimensions of rendered DOM
 * It works in tandem with TableColumnSizer mixin that actually generates the resulting styles
 */
import { nextTick, onMounted, onUpdated, Ref } from 'vue';

type OnMeasureCallback = (colName: string, maxWidth: number, maxHeight: number) => void;

// eslint-disable-next-line import/prefer-default-export
export function useRenderMeasure(
  onMeasure: OnMeasureCallback,
  refs: { [key: string]: Ref<(HTMLElement | HTMLElement[])> },
) {
  function measureRenderedDimensions() {
    nextTick(() => {
      Object.keys(refs).forEach((colName) => {
        const tmp = refs[colName].value; // get the ref
        const elements = Array.isArray(tmp) ? tmp : [tmp]; // make sure the ref is an array
        if (!elements.length) return; // as column defs change, columns are reset, but refs from before stay
        const maxWidth = Math.max.apply(null, elements.map((el) => (el ? el.clientWidth : 0)));
        const maxHeight = Math.max.apply(null, elements.map((el) => (el ? el.clientHeight : 0)));
        if (typeof onMeasure === 'function') {
          onMeasure(colName, maxWidth, maxHeight);
        }
      });
    });
  }

  function delayedMeasureRenderedDimensions() { nextTick(() => { measureRenderedDimensions(); }); }

  onMounted(delayedMeasureRenderedDimensions);
  onUpdated(delayedMeasureRenderedDimensions);
}
