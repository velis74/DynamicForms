import { defineComponent } from 'vue';

import BootstrapBreakpoints from './breakpoints-bootstrap';
import BreakpointsInterface from './breakpoints-interface';
import ThemeMixin from './theme-mixin';

export default /* #__PURE__ */ defineComponent({
  mixins: [ThemeMixin],
  computed: {
    screen_breakpoints(): BreakpointsInterface | {} {
      switch (this.theme.name.toLowerCase()) {
      case 'bootstrap':
        return BootstrapBreakpoints;
      case 'vuetify':
        return this.$vuetify.display;
      default:
        return {};
      }
    },
  },
});
