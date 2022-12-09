import BootstrapBreakpoints from './bootstrap-breakpoints';
import ThemeMixin from './theme-mixin';

export default {
  mixins: [ThemeMixin],
  computed: {
    screen_breakpoints() {
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
};
