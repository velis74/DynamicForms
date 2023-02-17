import _ from 'lodash';
import { isReactive, reactive } from 'vue';
import { useDisplay } from 'vuetify';

import BreakpointsInterface from './breakpoints-interface';

class VuetifyBreakpoints implements BreakpointsInterface {
  xs: number = 0;

  sm: number = 0;

  md: number = 0;

  lg: number = 0;

  xl: number = 0;

  xsAndUp: boolean = false;

  xsOnly: boolean = false;

  smAndUp: boolean = false;

  smAndDown: boolean = false;

  smOnly: boolean = false;

  mdAndUp: boolean = false;

  mdAndDown: boolean = false;

  mdOnly: boolean = false;

  lgAndUp: boolean = false;

  lgAndDown: boolean = false;

  lgOnly: boolean = false;

  xlOnly: boolean = false;

  width: number = 0;

  height: number = 0;
}

const state = new VuetifyBreakpoints();

function onResize() {
  const { width, height, thresholds } = useDisplay();
  const widthVal = width.value;

  state.xs = thresholds.value.xs;
  state.sm = thresholds.value.sm;
  state.md = thresholds.value.md;
  state.lg = thresholds.value.lg;
  state.xl = thresholds.value.xl;
  state.width = widthVal;
  state.height = height.value;

  state.xsAndUp = widthVal >= state.xs;
  state.xsOnly = widthVal >= state.xs && widthVal < state.sm;

  state.smAndUp = widthVal >= state.sm;
  state.smAndDown = widthVal < state.md;
  state.smOnly = widthVal >= state.sm && widthVal < state.md;

  state.mdAndUp = widthVal >= state.md;
  state.mdAndDown = widthVal < state.lg;
  state.mdOnly = widthVal >= state.md && widthVal < state.lg;

  state.lgAndUp = widthVal >= state.lg;
  state.lgAndDown = widthVal < state.xl;
  state.lgOnly = widthVal >= state.lg && widthVal < state.xl;

  state.xlOnly = widthVal >= state.xl;
}

window.onresize = _.debounce(onResize, 100);

function displayBreakpoints(): BreakpointsInterface {
  if (!state.xs) onResize();
  return isReactive(state) ? state : reactive(state);
}

export default displayBreakpoints;
