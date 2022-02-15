import getObjectFromPath from '../../util/get_object_from_path';

import ColumnOrdering from './column_ordering';
import ColumnDisplay from './display_mode';

export default class TableColumn {
  constructor(initialData, orderingArray) {
    this._maxWidth = 0;
    this.ordering = new ColumnOrdering(initialData.ordering, orderingArray, this);

    // Determine what is to be used for render decorator for this column
    const renderDecorator = initialData.render_params ? initialData.render_params.table : '';
    let returnFunc = this.renderDecoratorPlain;
    if (renderDecorator && renderDecorator.substring(0, 13) === 'df-tablecell-') {
      switch (renderDecorator.substring(13)) {
      case 'bool':
        returnFunc = this.renderDecoratorBool;
        break;
      case 'link':
        returnFunc = this.renderDecoratorLink;
        break;
      case 'email':
        returnFunc = this.renderDecoratorEmail;
        break;
      case 'file':
        returnFunc = this.renderDecoratorFile;
        break;
      case 'ipaddr':
        returnFunc = this.renderDecoratorIP;
        break;
        // DRF also formats simple lists, complex dicts / lists
        // DRF also parses ordinary strings to check if they contain \n (pre)
      default:
        break;
      }
    } else if (renderDecorator && renderDecorator.substring(0, 1) !== '#') {
      // Here we're expecting the decorator to suggest we use a globally accessible function
      // When a function, name will be in format module.submodule.submodule_n.function,
      //   e.g. myModule.formatEmail
      //   The above example will look for function in window['myModule']['formatEmail'] and call it.
      returnFunc = getObjectFromPath(renderDecorator);
    }

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
      CSSClassHead: { get() { return (this.ordering.isOrderable && 'ordering') || ''; }, enumerable: true },
      renderParams: { get() { return initialData.render_params; }, enumerable: true },

      renderComponentName: {
        get() {
          if (renderDecorator && renderDecorator.substring(0, 1) === '#') {
            // When component, name will start with #, e.g. #TableCellFloat. This will instruct table body to
            //   render a component with this name. You need to register it correctly
            return renderDecorator.substring(1);
          }
          return '';
        },
        enumerable: true,
      },

      renderDecoratorFunction: {
        get() { return (rowData, thead) => returnFunc.apply(this, [rowData, thead]); },
        enumerable: true,
      },

      maxWidth: { get() { return this._maxWidth; }, enumerable: true },
    });
  }

  setMaxWidth(value) {
    if (value > this._maxWidth) this._maxWidth = value;
  }

  renderDecoratorPlain(rowData) {
    return rowData[this.name];
  }

  renderDecoratorBool(rowData, thead) {
    if (thead) return this.renderDecoratorPlain(rowData, thead);
    return `<code>${rowData[this.name]}</code>`;
  }

  renderDecoratorLink(rowData, thead) {
    if (thead) return this.renderDecoratorPlain(rowData, thead);
    return `<a href="${rowData[this.name]}">${rowData[this.name]}</a>`;
  }

  renderDecoratorEmail(rowData, thead) {
    if (thead) return this.renderDecoratorPlain(rowData, thead);
    const value = rowData[this.name];
    const nameOnly = value.includes('<') ? value.substring(0, value.indexOf('<')).trim() : value;
    return `<a href="mailto:${value}">${nameOnly}</a>`;
  }

  renderDecoratorFile(rowData, thead) {
    if (thead) return this.renderDecoratorPlain(rowData, thead);
    const value = rowData[this.name];
    if (value) {
      const downloadContent = `event.stopPropagation(); window.open("${value}", "_blank")`;
      const fileName = value.replace(/^.*[\\/]/, '');
      return `<a href="#" onclick='${downloadContent}'>${fileName}</a>`;
    }
    return null;
  }

  renderDecoratorIP(rowData, thead) {
    if (thead) return this.renderDecoratorPlain(rowData, thead);
    let value = rowData[this.name];
    const segments = value.split('.');
    if (segments.length === 4) {
      // eslint-disable-next-line no-param-reassign
      value = segments.map((x) => {
        const padding = x.length < 3 ? `<span style="opacity: .5">${'000'.slice(x.length - 3)}</span>` : '';
        return padding + x;
      }).join('.');
    }
    return `<code>${value}</code>`;
  }
}
