import DisplayMode from './displayMode';
import helperFunctions from './helperFunctions';

class TableColumn {
  constructor(columnDef) {
    this._columnDef = columnDef;
  }

  get name() {
    return this._columnDef.name;
  }

  get label() {
    return this._columnDef.label;
  }

  get align() {
    if (this._columnDef.alignment === 'decimal') return 'right';
    return this._columnDef.alignment;
  }

  // eslint-disable-next-line camelcase
  get table_classes() {
    return this._columnDef.table_classes;
  }

  get ordering() {
    return this._columnDef.ordering;
  }

  get visibility() {
    switch (this._columnDef.visibility) {
    case 1:
      return DisplayMode.SUPPRESS;
    case 5:
      return DisplayMode.HIDDEN;
    case 8:
      return DisplayMode.INVISIBLE;
    case 10:
      return DisplayMode.FULL;
    default:
      console.warn(`Table column came with visibility set to ${this._columnDef.visibility}, but we don't know` +
          ' that constant');
      return DisplayMode.FULL;
    }
  }

  get isOrdered() {
    return this.ordering.includes('ordering');
  }

  // eslint-disable-next-line camelcase
  get th_classes() {
    return (`${this.table_classes} ${this.isOrdered ? 'ordering' : ''}`).trim();
  }

  get isAscending() {
    return this.isOrdered && this.ordering.includes('asc');
  }

  get isDescending() {
    return this.isOrdered && this.ordering.includes('desc');
  }

  get isUnsorted() {
    return this.isOrdered && this.ordering.includes('unsorted');
  }

  /**
   * cycles field ordering 'asc' -> 'desc' -> 'unsorted'
   */
  get cycleOrdering() {
    if (this.isAscending) return 'desc';
    return this.isDescending ? 'unsorted' : 'asc';
  }

  /**
   * sets column sort sequence and direction
   * @param direction: one of "asc", "desc" or "unsorted"
   * @param sequence: integer. if none is provided, existing sequence # will be used
   * or 1 if column was unsorted
   */
  setSorted(direction, sequence) {
    // eslint-disable-next-line no-param-reassign
    if (sequence === undefined) sequence = this.orderIndex > 0 ? this.orderIndex : 1;

    if (!this.isOrdered) {
      console.warn('column $(this.name) is not orderable. Why are you trying to set its order direction?');
    } else if (direction === 'asc' || direction === 'desc' || direction === 'unsorted') {
      this._columnDef.ordering = `ordering ${direction} ${direction === 'unsorted' ? '' : `seg-${sequence}`}`;
    } else {
      console.warn(`unknown sort direction "${direction}" for the column ${this.name}. not doing anything`);
    }
  }

  get ascDescChar() {
    if (!this.isOrdered) return '';
    if (this.isAscending) return '\u25b2';
    if (this.isDescending) return '\u25bc';
    if (this.isUnsorted) return '\u2195';
    return '';
  }

  get orderIndex() {
    if (!this.isOrdered) return 0;
    const ordrIdxMatch = /(?:seg-)(\d+)/.exec(this.ordering);
    return ordrIdxMatch != null ? Number(ordrIdxMatch[1]) : 0;
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
              return `<a href="#" onclick='event.stopPropagation();window.open("${value}", "_blank")'>${helperFunctions.getFileNameFromPath(value)}</a>`;
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
          // DRF also parses ordinary strings to check if they are valid URLs(link), emails(email) or contain \n (pre)
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

export default TableColumn;
