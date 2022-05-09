import BootstrapBreakpoints from './bootstrap_breakpoints';
import ThemeMixin from './theme_mixin';

export default {
  mixins: [ThemeMixin],
  computed: {
    screen_breakpoints() {
      switch (this.theme.name.toLowerCase()) {
      case 'bootstrap':
        return BootstrapBreakpoints;
      case 'vuetify':
        return this.$vuetify.breakpoint;
      default:
        return {};
      }
    },
  },
};
