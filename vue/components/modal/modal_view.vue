<script>
import Vue from 'vue';

import ThemeMixin from '../util/theme_mixin';

import ModalViewAPI from './modal_view_api';

function deepClone(vnodes, createElement) {
  function cloneVNode(vnode) {
    const clonedChildren = vnode.children && vnode.children.map((vn) => cloneVNode(vn));
    const cloned = createElement(vnode.tag, vnode.data, clonedChildren);
    cloned.text = vnode.text;
    cloned.isComment = vnode.isComment;
    cloned.componentOptions = vnode.componentOptions;
    cloned.elm = vnode.elm;
    // cloned.context = vnode.context;
    cloned.ns = vnode.ns;
    cloned.isStatic = vnode.isStatic;
    cloned.key = vnode.key;
    return cloned;
  }

  return vnodes.map((vn) => cloneVNode(vn));
}

function processSlot(slot, content, createElement) {
  if (content == null) return null;
  if (typeof content === 'string') {
    // The slot is a plain string so let's just create a span element
    return createElement('span', { slot }, content);
  }
  // we have slots as vnodes
  return deepClone(content, createElement);
}

export default {
  name: 'ModalView',
  mixins: [ThemeMixin, ModalViewAPI],
  data() {
    return {
      isPrimary: false,
      renderSequence: 0,
    };
  },
  computed: {
    modalAPIView() { return `${this.theme.name.capitalised}Modal`; },
    slots() { return []; }, // TODO: Currently faked
  },
  created() { this.install(); },
  methods: {
    install() {
      const vue = this.$root;
      if (!vue.modalRootInstance) {
        vue.modalRootInstance = this;
        this.isPrimary = true;
      }
      if (!Vue.prototype.$dfModal) {
        Object.defineProperty(Vue.prototype, '$dfModal', { get() { return this?.$root.modalRootInstance; } });
      }
    },
  },
  render(el) {
    if (this.isPrimary && this.currentDialog) {
      return el(
        this.modalAPIView,
        { props: { show: true }, key: this.renderSequence },
        [
          processSlot('title', this.currentDialog.title, el),
          processSlot('body', this.currentDialog.body, el),
          processSlot('actions', this.currentDialog.actions, el),
        ],
      );
    }
    return null;
  },
};
</script>
