import FilteredActions from '../actions/filtered-actions';
import ThemeMixin from '../util/theme_mixin';

function processSlot(slot, content, createElement, actionsView) {
  if (content == null) return null;
  if (typeof content === 'string') {
    // The slot is a plain string so let's just create a span element
    return createElement('span', { slot }, content);
  }
  if (content instanceof FilteredActions) {
    // the slot is FilteredActions. Need to construct a DfActions component
    return createElement(actionsView, { slot, props: { actions: content } }, []);
  }
  if (content && content.componentName && content.props) {
    return createElement(content.componentName, { slot, props: content.props }, []);
  }
  // we have slots as vnodes
  return createElement('template', { slot }, [content]);
}

export default {
  mixins: [ThemeMixin],
  computed: { // eslint-disable-line object-curly-newline
    modalAPIView() { return `${this.theme.name.capitalised}Modal`; },
    actionsView() { return `${this.theme.name.capitalised}Actions`; },
  },
  methods: {
    renderFunction(el, titleSlot, bodySlot, actionsSlot, options) {
      const renderSequence = 0;
      return el(
        this.modalAPIView,
        { props: { show: true, options: options || {} }, key: renderSequence },
        [
          processSlot('title', titleSlot, el, this.actionsView),
          processSlot('body', bodySlot, el, this.actionsView),
          processSlot('actions', actionsSlot, el, this.actionsView),
        ],
      );
    },
  },
};
