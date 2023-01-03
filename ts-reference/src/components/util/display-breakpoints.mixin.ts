import { defineComponent } from 'vue';

import BootstrapBreakpoints from '@/components/util/bootstrap-breakpoints';
import ThemeMixin from '@/components/util/theme.mixin';

export default defineComponent({
  mixins: [ThemeMixin],
  computed: {
    screen_breakpoints(): any {
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
