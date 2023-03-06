/**
 * rows visibility observer
 * determines what rows are currently visible in tbody and fires a callback when necessary
 *
 * uses IntersectionObserver to do its magic
 * falls back on (relatively cheaply made) polling when observer isn't supported
 *
 * Actually, that's incorrect: TODO: IntersectionObserver is currently not used because it was much slower than polling
 *   See also tbody-generic which used the observer if you ever make it more performant
 *   also re-add "resize-observer-polyfill": "^1.5.1", to dependencies in package.json
 *
 * This mixin is intended to be used in tbody. it expects the root element to be the parent div with items as rows
 */
import { onBeforeUpdate, onMounted, onUnmounted, onUpdated, Ref } from 'vue';

import TableRow from './definitions/row';
import TableRows from './definitions/rows';

const USE_INTERSECTION_OBSERVER = false;

/**
 * Finds any row that is visible and returns it. Result of this function will be used to then find the topmost
 * and bottommost items visible on screen
 *
 * @param parent container to start searching its children in
 */
function findAnyVisibleRow(parent?: HTMLElement) {
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

function isVisible(children: HTMLCollection, index: number, viewPortHeight: number) {
  if (index < 0 || index >= children.length) return false;
  const cr = children[index].getBoundingClientRect();
  return cr.bottom >= 0 && cr.top <= viewPortHeight;
}

/**
 * Finds the first visible item in the direction of search, starting from startIndex
 *
 * @param children list of items to check for visibility
 * @param startIndex starting index of an item, presumably in viewport now, where we start the search
 * @param direction +1 or -1 depending on which direction we want to be searching in
 * @param viewPortHeight height available for us
 */
function search(children: HTMLCollection, startIndex: number, direction: number, viewPortHeight: number) {
  const initiallyVisible = isVisible(children, startIndex, viewPortHeight);
  if (!initiallyVisible) {
    // if starting item's top is already negative, and we're searching up, it would be a waste
    if (direction < 0 && children[startIndex].getBoundingClientRect().top < 0) return null;
    // if starting item's bottom is already larger than viewPortHeight, and we're searching up, it would be a waste
    if (direction > 0 && children[startIndex].getBoundingClientRect().bottom > viewPortHeight) return null;
  }
  const maxIndex = children.length - 1;
  let index = startIndex + direction;
  while ((index >= 0 && index <= maxIndex)) {
    if (isVisible(children, index, viewPortHeight) !== initiallyVisible) return index - direction;
    index += direction;
  }
  // we have NOT found any item that would have its visibility differ from the starting item
  return initiallyVisible ? index - direction : null; // return first or last item, if visible
}

function observeElements(observer: IntersectionObserver, children: HTMLElement[]) {
  for (let i = children.length - 1; i >= 0; i--) {
    observer.observe(children[i]);
  }
}

function useRowVisibilityObserver(element: Ref<HTMLElement>, rows: TableRows) {
  let lastLoadRequestNext: string | null = null;

  function findVisibleRows() {
    const parent = element.value;
    // startWith will contain one item that is as close as possible to the browser viewport
    const startWith = findAnyVisibleRow(parent);
    if (startWith == null || startWith < 0) return;
    const viewPortHeight = Math.max(document.documentElement.clientHeight || 0, window.innerHeight || 0);
    const children = parent.children;

    const firstVisible: number = search(children, startWith, -1, viewPortHeight) as number;
    // unnecessary: the above statement MUST find a visible row because startWith IS visible, and we know it!
    // if (firstVisible == null) firstVisible = search(children, startWith, 1, viewPortHeight);

    // unnecessary: startWith could not have been below the viewport
    // let lastVisible: number;
    // if (isVisible(children, firstVisible - 1, viewPortHeight)) {
    //   // startWith was actually below the viewport
    //   lastVisible = firstVisible;
    //   firstVisible = search(children, lastVisible - 1, -1, viewPortHeight);
    // } else {
    const lastVisible: number = search(children, firstVisible, 1, viewPortHeight) as number;
    // }
    const pageSize = rows.data.length === 1 ? 1 : lastVisible - firstVisible;
    // TODO: speed optimisation possible: we could remember previous visible rows and then run this loop only on
    //  union of prev and newly visible rows. If they were the same, the loop needn't even run
    rows.data.forEach((row: TableRow, index: number) => {
      const isShowing = index > firstVisible - pageSize && index < lastVisible + pageSize;
      if (row.dfControlStructure.isShowing !== isShowing) row.setIsShowing(isShowing);
    });
    if (!USE_INTERSECTION_OBSERVER && lastVisible + pageSize > rows.data.length) {
      // we're not using IntersectionObserver, so when we have less than one page to end of data, load more
      if (lastLoadRequestNext !== rows.next) {
        lastLoadRequestNext = rows.next;
        rows.loadMoreRows(true);
      }
    }
  }

  let intervalId: NodeJS.Timer | null = setInterval(() => { findVisibleRows(); }, 100);

  function clearIntervalId() {
    if (!intervalId) return;
    clearInterval(intervalId);
    intervalId = null;
  }

  // console.log('setting interval', this.intervalId);

  if (USE_INTERSECTION_OBSERVER) {
    const intersectionObserver = new IntersectionObserver((/* unused: entries: IntersectionObserverEntry[] */) => {
      // if observer fired, then browser supports it, we can stop polling
      if (intervalId) {
        console.log('observer triggered, deleting interval', intervalId);
        clearIntervalId();
      }
      findVisibleRows();
    });

    onUnmounted(() => {
      intersectionObserver.disconnect();
      clearIntervalId();
    });
    onMounted(() => { observeElements(intersectionObserver, [element.value]); });
    onBeforeUpdate(() => { intersectionObserver.disconnect(); });
    onUpdated(() => { observeElements(intersectionObserver, [element.value]); });
  } else {
    onUnmounted(() => { clearIntervalId(); });
  }

  return null;
}

export default useRowVisibilityObserver;
