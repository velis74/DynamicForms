import ColumnDisplay from '../../classes/display-mode';
import getObjectFromPath from '../../util/get-object-from-path';

import ColumnOrdering from './column-ordering';

type RenderDecorator = (data: any, thead: boolean) => string;

export default class TableColumn {
  name!: string;

  label!: string;

  align!: 'left' | 'right' | 'center';

  visibility!: number; // ColumnDisplay

  maxWidth!: number;

  private _maxWidth: number;

  constructor(initialData, orderingArray) {
    this._maxWidth = 0;
    initialData.ordering = initialData.ordering || '';
    this.ordering = new ColumnOrdering(initialData.ordering, orderingArray, this);
    this.layout = null;

    // Determine what is to be used for render decorator for this column
    const renderDecorator = initialData.render_params ? initialData.render_params.table : '';
    let returnFunc: RenderDecorator = this.renderDecoratorPlain;
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
        get(): RenderDecorator { return (rowData, thead) => returnFunc.apply(this, [rowData, thead]); },
        enumerable: true,
      },

      maxWidth: { get() { return this._maxWidth; }, enumerable: true },
    });
  }

  setLayout(layout) {
    this.layout = layout;
  }

  setMaxWidth(value: number) {
    if (value > this._maxWidth) {
      this._maxWidth = value;
    }
  }

  /* eslint-disable-next-line @typescript-eslint/no-unused-vars */
  renderDecoratorPlain(rowData: any, thead: boolean) {
    return rowData[this.name];
  }

  renderDecoratorBool(rowData: any, thead: boolean) {
    if (thead) return this.renderDecoratorPlain(rowData, thead);
    return `<code>${rowData[this.name]}</code>`;
  }

  renderDecoratorLink(rowData: any, thead: boolean) {
    if (thead) return this.renderDecoratorPlain(rowData, thead);
    return `<a href="${rowData[this.name]}">${rowData[this.name]}</a>`;
  }

  renderDecoratorEmail(rowData: any, thead: boolean) {
    if (thead) return this.renderDecoratorPlain(rowData, thead);
    const value = rowData[this.name];
    const nameOnly = value.includes('<') ? value.substring(0, value.indexOf('<')).trim() : value;
    return `<a href="mailto:${value}">${nameOnly}</a>`;
  }

  renderDecoratorFile(rowData: any, thead: boolean) {
    if (thead) return this.renderDecoratorPlain(rowData, thead);
    const value = rowData[this.name];
    if (value) {
      const downloadContent = `event.stopPropagation(); window.open("${value}", "_blank")`;
      const fileName = value.replace(/^.*[\\/]/, '');
      return `<a href="#" onclick='${downloadContent}'>${fileName}</a>`;
    }
    return null;
  }

  renderDecoratorIP(rowData: any, thead: boolean) {
    if (thead) return this.renderDecoratorPlain(rowData, thead);
    let value = rowData[this.name];
    const segments = value.split('.');
    if (segments.length === 4) {
      // eslint-disable-next-line no-param-reassign
      value = segments.map((x: string) => {
        const padding = x.length < 3 ? `<span style="opacity: .5">${'000'.slice(x.length - 3)}</span>` : '';
        return `${padding}<span>${x}</span>`;
      }).join('.');
    }
    return `<code>${value}</code>`;
  }
}
