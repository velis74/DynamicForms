import { reactive, watch } from 'vue';
import { DisplayInstance, useDisplay } from 'vuetify';

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

function watcher(newValue: DisplayInstance) {
  const width = newValue.width.value;

  state.xsAndUp = width >= state.xs;
  state.xsOnly = width >= state.xs && width < state.sm;

  state.smAndUp = width >= state.sm;
  state.smAndDown = width < state.md;
  state.smOnly = width >= state.sm && width < state.md;

  state.mdAndUp = width >= state.md;
  state.mdAndDown = width < state.lg;
  state.mdOnly = width >= state.md && width < state.lg;

  state.lgAndUp = width >= state.lg;
  state.lgAndDown = width < state.xl;
  state.lgOnly = width >= state.lg && width < state.xl;

  state.xlOnly = width >= state.xl;

  state.width = width;
  state.height = newValue.height.value;
  state.xs = newValue.thresholds.value.xs;
  state.sm = newValue.thresholds.value.sm;
  state.md = newValue.thresholds.value.md;
  state.lg = newValue.thresholds.value.lg;
  state.xl = newValue.thresholds.value.xl;
}

function displayBreakpoints(): BreakpointsInterface {
  watch(useDisplay(), watcher, { deep: true });
  watcher(useDisplay());
  return reactive(state);
}

export default displayBreakpoints;
