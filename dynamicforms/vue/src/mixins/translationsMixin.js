const translationsMixin = {
  methods: {
    gettext(str) {
      return window.gettext ? window.gettext(str) : str;
    },
  },
};

export default translationsMixin;
