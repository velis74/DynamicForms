import _ from 'lodash';
import Vue from 'vue';

const state = {};

// https://stackoverflow.com/a/62675498/9625282
/* This assumes you're using default bootstrap breakpoint names */
const style = getComputedStyle(document.body);

state.xs = style.getPropertyValue('--breakpoint-xs').replace('px', '') || 0;
state.sm = style.getPropertyValue('--breakpoint-sm').replace('px', '') || 576;
state.md = style.getPropertyValue('--breakpoint-md').replace('px', '') || 768;
state.lg = style.getPropertyValue('--breakpoint-lg').replace('px', '') || 992;
state.xl = style.getPropertyValue('--breakpoint-xl').replace('px', '') || 1200;
// we're matching Vuetify, so no xxl
// state.xxl = style.getPropertyValue('--breakpoint-xxl').replace('px', '') || 1400;

function onResize() {
  const width = window.innerWidth;

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

window.onresize = _.debounce(onResize, 100);
onResize();

export default Vue.observable(state);
