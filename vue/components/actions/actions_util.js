import ThemeMixin from '../util/theme_mixin';

export default {
  mixins: [ThemeMixin],
  data() {
    return {
      actionPositionHeader: 'HEADER',
      actionPositionRowStart: 'ROW_START',
      actionPositionRowEnd: 'ROW_END',
      actionPositionFieldStart: 'FIELD_START',
      actionPositionFieldEnd: 'FIELD_END',
    };
  },
  computed: {
    actionsComponentName() {
      return `${this.theme.name.capitalised}Actions`;
    },
  },
};
