import Vue from 'vue';

const state = Vue.observable({ screen: {} });

// https://stackoverflow.com/a/62675498/9625282
/* This assumes you're using default bootstrap breakpoint names */
/* You need to hardcode the breakpoint values if you want to support IE11 */
const style = getComputedStyle(document.body);
const xs = style.getPropertyValue('--breakpoint-xs').replace('px', '');
const sm = style.getPropertyValue('--breakpoint-sm').replace('px', '');
const md = style.getPropertyValue('--breakpoint-md').replace('px', '');
const lg = style.getPropertyValue('--breakpoint-lg').replace('px', '');
const xl = style.getPropertyValue('--breakpoint-xl').replace('px', '');

function onResize() {
  const width = window.innerWidth;

  /* Not really sure how to properly define gt or lt */
  state.screen = {
    xsOnly: width >= xs && width < sm,
    smOnly: width >= sm && width < md,
    mdOnly: width >= md && width < lg,
    lgOnly: width >= lg && width < xl,
    xlOnly: width >= xl,
    xsAndUp: width >= xs,
    smAndUp: width >= sm,
    mdAndUp: width >= md,
    lgAndUp: width >= lg,
    smAndDown: width <= md,
    mdAndDown: width <= lg,
    lgAndDown: width <= xl,
  };
}

/* Might want to debounce the event, to limit amount of calls */
window.onresize = onResize;
onResize();

export default state;
