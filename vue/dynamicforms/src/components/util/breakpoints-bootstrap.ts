import _ from 'lodash';
import { reactive } from 'vue';

import BreakpointsInterface from './breakpoints-interface';

class StateType implements BreakpointsInterface {
  xs!: number;

  sm!: number;

  md!: number;

  lg!: number;

  xl!: number;

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

  private isSet!: boolean; // when first called, <body> is nowhere to be seen since the script wat loaded in <head>

  constructor() {
    this.setFromDocument();
  }

  setFromDocument() {
    if (this.isSet) return;
    if (document.body) {
      // https://stackoverflow.com/a/62675498/9625282
      /* This assumes you're using default bootstrap breakpoint names */
      const style = getComputedStyle(document.body);

      this.xs = +style.getPropertyValue('--breakpoint-xs').replace('px', '') || 0;
      this.sm = +style.getPropertyValue('--breakpoint-sm').replace('px', '') || 576;
      this.md = +style.getPropertyValue('--breakpoint-md').replace('px', '') || 768;
      this.lg = +style.getPropertyValue('--breakpoint-lg').replace('px', '') || 992;
      this.xl = +style.getPropertyValue('--breakpoint-xl').replace('px', '') || 1200;
      this.isSet = true;
    } else {
      this.xs = 0;
      this.sm = 576;
      this.md = 768;
      this.lg = 992;
      this.xl = 1200;
      this.isSet = false;
    }
  }
}

const state = new StateType();

// we're matching Vuetify, so no xxl
// state.xxl = style.getPropertyValue('--breakpoint-xxl').replace('px', '') || 1400;

function onResize() {
  const width = window.innerWidth;

  state.setFromDocument();

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
  state.height = window.innerHeight;
}

window.addEventListener('resize', () => _.debounce(onResize));
onResize();

const displayBreakpoints = () => reactive(state) as BreakpointsInterface;
export default displayBreakpoints;
