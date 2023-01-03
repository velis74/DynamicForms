/**
 * rows visibility observer
 * determines what rows are currently visible in tbody and fires a callback when necessary
 *
 * uses IntersectionObserver to do its magic
 * falls back on (relatively cheaply made) polling when observer isn't supported
 *
 * Actually, that's incorrect: TODO: IntersectionObserver is currently not used because it was much slower than polling
 *
 * This mixin is intended to be used in tbody. it expects the root element to be the parent div with items as rows
 */
import { defineComponent } from 'vue';

function findAnyVisibleRow(parent: any) {
  const viewPortHeight = Math.max(document.documentElement.clientHeight || 0, window.innerHeight || 0);
  const children = parent ? [...parent.children].filter((n) => n.getBoundingClientRect().height > 0) : [];
  let left = 0;
  let right = children.length - 1;
  while (left <= right) {
    const middle = Math.floor((right + left) / 2);
    const node = children[middle];
    const boundingRect = node.getBoundingClientRect();
    if (boundingRect.bottom < 0) {
      left = middle + 1;
    } else if (boundingRect.top > viewPortHeight) {
      right = middle - 1;
    } else {
      return middle;
    }
  }
  // no rows are visible, do nothing
  return null;
}

function isVisible(children: any, index: number, viewPortHeight: number) {
  if (index < 0 || index >= children.length) return false;
  const cr = children[index].getBoundingClientRect();
  return cr.bottom >= 0 && cr.top <= viewPortHeight;
}

function search(children: any, startIndex: number, direction: any, viewPortHeight: number) {
  const initiallyVisible = isVisible(children, startIndex, viewPortHeight);
  const maxIndex = children.length - 1;
  let index = startIndex + direction;
  while ((index >= 0 && index <= maxIndex)) {
    if (isVisible(children, index, viewPortHeight) !== initiallyVisible) return index - direction;
    index += direction;
  }
  return initiallyVisible ? index - direction : null; // return first or last item, if visible
}

function observeElements(observer: any, children: any) {
  for (let i = children.length - 1; i >= 0; i--) {
    observer.observe(children[i]);
  }
}

export default defineComponent({
  data() { return { intersectionObserver: null as any, intervalId: null as any }; },
  created() {
    // this.intersectionObserver = new IntersectionObserver((entries) => {
    //   if (this.intervalId) {
    //     // if observer fired, then browser supports it, we can stop polling
    //     console.log('observer triggered, deleting interval', this.intervalId);
    //     clearInterval(this.intervalId);
    //     this.intervalId = null;
    //   }
    //   this.findVisibleRows(entries);
    // });
    if (!this.intervalId) {
      this.intervalId = setInterval(() => { this.findVisibleRows(); }, 100);
      // console.log('setting interval', this.intervalId);
    }
  },
  unmounted() {
    if (this.intersectionObserver) {
      this.intersectionObserver.disconnect();
      this.intersectionObserver = null;
    }
    if (this.intervalId) {
      // console.log('deleting interval', this.intervalId);
      clearInterval(this.intervalId);
    }
  },
  mounted() {
    if (this.intersectionObserver) observeElements(this.intersectionObserver, this.$el.children);
  },
  beforeUpdate() { if (this.intersectionObserver) this.intersectionObserver.disconnect(); },
  updated() {
    if (this.intersectionObserver) observeElements(this.intersectionObserver, this.$el.children);
  },
  methods: {
    findVisibleRows() {
      const parent = this.$el;
      // startWith will contain one item that is as close as possible to the browser viewport
      const startWith = findAnyVisibleRow(parent);
      if (startWith == null || startWith < 0) return;
      const viewPortHeight = Math.max(document.documentElement.clientHeight || 0, window.innerHeight || 0);
      const children = parent.children;

      let firstVisible: number = search(children, startWith, -1, viewPortHeight) ?? 0;
      if (firstVisible === null) firstVisible = search(children, startWith, 1, viewPortHeight) ?? 0;
      let lastVisible: number;

      if (isVisible(children, firstVisible - 1, viewPortHeight)) {
        // startWith was actually below the viewport
        lastVisible = firstVisible;
        firstVisible = search(children, lastVisible - 1, -1, viewPortHeight) ?? 0;
      } else {
        lastVisible = search(children, firstVisible, 1, viewPortHeight) ?? 0;
      }
      const pageSize = this.rows.data.length === 1 ? 1 : lastVisible - firstVisible;
      this.rows.data.forEach((row: any, index: number) => {
        const isShowing = index > firstVisible - pageSize && index < lastVisible + pageSize;
        if (row.dfControlStructure.isShowing !== isShowing) row.setIsShowing(isShowing);
      });
    },
  },
});
