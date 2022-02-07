import ColumnOrdering from './column_ordering';
import ColumnDisplay from './display_mode';

export default class TableColumn {
  constructor(initialData, orderingArray) {
    this._maxWidth = 0;
    this.ordering = new ColumnOrdering(initialData.ordering, orderingArray, this);

    // Below we circumvent having to declare an internal variable which property getters would be reading from
    Object.defineProperties(this, {
      name: { get() { return initialData.name; }, enumerable: true },
      label: { get() { return initialData.label; }, enumerable: true },
      align: {
        get() {
          if (initialData.alignment === 'decimal') return 'right';
          return initialData.alignment;
        },
        enumerable: true,
      },
      visibility: { get() { return ColumnDisplay.get(initialData.visibility.table); }, enumerable: true },
      CSSClass: { get() { return initialData.table_classes || ''; }, enumerable: true },
      CSSClassHead: { get() { return this.isOrdered && 'ordering'; }, enumerable: true },

      /**
       * MaxWidth - computed maximum width of table column
       *
       * This property is currently used such that it violates one way data flow (data down, events up principle).
       *
       * TL;DR - this approach is chosen for performance reasons (and to reduce clutter when debugging events)
       *
       * I would argue that in this case, the standard reasons against this do not apply:
       *   The setter ensures that my rows and columns do not *accidentally* mutate the prop value
       *   It is also intended that the change here gets propagated back down: we need to create new styles
       *     OTOH the one undesired side-effect is re-rendering of everything, not just the style. Perhaps
       *     optimisation will once be done do address this particular issue, though right now only the style mixin
       *     deep-watches this prop, so in reality it is the only subcomponent re-rendering
       *   This particular solution does not belong to the two usual cases why one would like to modify props
       *
       * It would also be easy to implement this via an
       *   EventBus (https://v3.vuejs.org/guide/migration/events-api.html) or
       *   shared State (https://vuejs.org/v2/guide/state-management.html) or
       *   doing everything from the master table component, locating the cells in mounted & updated hooks.
       * The first two patterns, but both of those would result in a lot of unnecessary processing overhead for no
       * gain but declaratory compliance with accepted patterns. I would argue that this setter might already comply
       * because it has a shared state and an action to mutate it.
       */
      maxWidth: {
        get() { return this._maxWidth; },
        set(value) { if (value > this._maxWidth) this._maxWidth = value; },
        enumerable: true,
      },
    });
  }
}

/*
class TableColumn {

  get ascDescChar() {
    if (!this.isOrdered) return '';
    if (this.isAscending) return '\u25b2';
    if (this.isDescending) return '\u25bc';
    if (this.isUnsorted) return '\u2195';
    return '';
  }

  get orderIndexChar() {
    return this.orderIndex > 0 ? String.fromCharCode(0x2460 + this.orderIndex - 1) : '';
  }

  // eslint-disable-next-line camelcase
  get render_params() {
    return this._columnDef.render_params || {};
  }

  get renderDecoratorComponentName() {
    if (this.render_params.table) {
      const tableDecorator = this.render_params.table;
      return tableDecorator.substr(0, 1) === '#' ? tableDecorator.substr(1) : '';
    }
    return null;
  }

  get renderDecoratorFunction() {
    if (this.render_params && this.render_params.table) {
      const tableDecorator = this.render_params.table;
      if (tableDecorator.substr(0, 13) === 'df-tablecell-') {
        // built-in decorator functions
        const decoratorFunction = tableDecorator.substr(13);
        // eslint-disable-next-line default-case
        switch (decoratorFunction) {
        case 'bool':
          return (row, column, value) => `<code>${value}</code>`;
        case 'link':
          return (row, column, value) => `<a href="${value}">${value}</a>`;
        case 'email':
          return (row, column, value) => {
            const nameOnly = value.includes('<') ? value.substr(0, value.indexOf('<')).trim() : value;
            return `<a href="mailto:${value}">${nameOnly}</a>`;
          };
        case 'file':
          return (row, column, value) => {
            if (value) {
              // eslint-disable-next-line max-len
              return `<a href="#" onclick='event.stopPropagation();
                 window.open("${value}", "_blank")'>${helperFunctions.getFileNameFromPath(value)}</a>`;
 *-/
            }
            return null;
          };
        case 'ipaddr':
          return (row, column, value) => {
            const segments = value.split('.');
            if (segments.length === 4) {
              // eslint-disable-next-line no-param-reassign
              value = segments.map((x) => {
                const padding = x.length < 3 ? `<span style="opacity: .5">${'000'.slice(x.length - 3)}</span>` : '';
                return padding + x;
              }).join('.');
            }
            return `<code class="text-nowrap">${value}</code>`;
          };
          // DRF also formats simple lists, complex dicts / lists
          // DRF also parses ordinary strings to check if they are valid URLs(link), emails(email) or
          //   contain \n (pre)
        }
      } else {
        // Here we're expecting the decorator to either suggest we use a component or a globally accessible function
        // When component, name will start with #, e.g. #df-tablecell-float. This will instruct table body to render
        //   a component with this name
        // When a function, name will be in format module.submodule.submodule_n.function, e.g. myModule.formatEmail
        //   The above example will look for function in window['myModule']['formatEmail'] and call it.
        return tableDecorator.split('.').reduce((res, val) => res[val], window);
      }
    }
    // if special JS function for formatting data is not provided, we just format the data as plain text
    return (row, column, value) => value;
  }
}
 */
