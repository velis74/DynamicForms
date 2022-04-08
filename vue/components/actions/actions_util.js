import ThemeMixin from '../util/theme_mixin';

export default {
  mixins: [ThemeMixin],
  computed: {
    actionsComponentName() {
      return `${this.theme.name.capitalised}Actions`;
    },
  },
};
