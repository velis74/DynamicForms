/**
 * Mixin that returns currently selected theme and its parameters
 *
 * Assumes that the theme-bearing component has a "theme" property that is either a Theme or a String
 *   String: it's just theme name
 *   Object: it's an object containing theme name
 *
 * Actual theme parameters not supported yet, so there's no implementation either.
 *
 * This mixin has a side effect: it will go up the parents list until it reaches a parent with a "theme" member.
 *   So, if any of the parents uses this mixin already, the theme class will be returned from that parent, not from
 *   the topmost component with actual theme-bearing properties.
 */

// eslint-disable-next-line max-classes-per-file
import { defineComponent } from 'vue';

/**
 * ThemeName adds "capitalised" getter for returning the string with first letter in uppercase.
 * We could polyfill this into String.prototype, but that seems excessive just for this one use
 */
// eslint-disable-next-line max-classes-per-file
class ThemeName extends String {
  get capitalised() { return this.charAt(0).toUpperCase() + this.slice(1); }
}

/**
 * Theme class
 *
 * Contains currently selected theme's name, parameters and other defining properties
 */
class Theme {
  name: ThemeName;

  constructor(name: string) {
    this.name = new ThemeName(name);
  }
}

export default /* #__PURE__ */ defineComponent({
  computed: {
    theme(): Theme {
      let themeOwner = this.$parent;
      // we traverse the parents until we find the DemoApp parent which actually hosts the theme selected
      while (themeOwner && themeOwner.$options.name !== 'DemoApp') {
        themeOwner = themeOwner.$parent;
      }
      // @ts-ignore: yes, theme might not exist on parent component. But if parent component is a theme mixin it will
      const theme = themeOwner?.theme;
      if (theme instanceof Theme) return theme;
      return new Theme(theme);
    },
  },
  methods: {
    getThemedComponentName(undecoratedName: string) {
      return `${this.theme.name.capitalised}${undecoratedName}`;
    },
  },
});
