import DisplayMode from '../../classes/display-mode';
import FormField from '../../form/definitions/field';
import getObjectFromPath from '../../util/get-object-from-path';
import { DfTable } from '../namespace';

import ColumnOrdering from './column-ordering';

type RenderDecorator = (data: any, thead: boolean) => string;

export default class TableColumn {
  name!: string;

  label!: string;

  align!: DfTable.CSSAlignment;

  visibility!: DisplayMode;

  renderParams!: {
    table_format: any,
    table_show_zeroes?: boolean,
    max_width?: string,
  };

  maxWidth!: number;

  ordering: ColumnOrdering;

  private _maxWidth: number;

  public layout: DfTable.ResponsiveLayoutInterface | null;

  CSSClass!: string;

  CSSClassHead!: string;

  renderComponentName!: string;

  renderDecoratorFunction!: (rowData: Object, thead: boolean) => any;

  formFieldInstance ?: FormField;

  constructor(initialData: DfTable.ColumnJSON, orderingArray: ColumnOrdering[]) {
    this._maxWidth = 0;
    initialData.ordering = initialData.ordering || '';
    this.ordering = new ColumnOrdering(initialData.ordering, orderingArray, this);
    this.layout = null;

    // Determine what is to be used for render decorator for this column
    const renderDecorator = initialData.render_params?.table || '';
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
      case 'color':
        returnFunc = this.renderDecoratorColor;
        break;
        // TODO: DRF also formats simple lists, complex dicts / lists
        // TODO: DRF also parses ordinary strings to check if they contain \n (pre)
      default:
        break;
      }
    } else if (renderDecorator && renderDecorator.substring(0, 1) !== '#') {
      // Here we're expecting the decorator to suggest we use a globally accessible function
      // When a function, name will be in format module.submodule.submodule_n.function,
      //   e.g. myModule.formatEmail
      //   The above example will look for function in window['myModule']['formatEmail'] and call it.
      returnFunc = getObjectFromPath(renderDecorator) as RenderDecorator;
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
      visibility: { get() { return DisplayMode.fromAny(initialData.visibility.table); }, enumerable: true },
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

  setLayout(layout: DfTable.ResponsiveLayoutInterface) {
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

  renderDecoratorColor(rowData: any, thead: boolean) {
    if (thead) {
      return this.renderDecoratorPlain(rowData, thead);
    }
    return (
      `<div style="display: inline-block; width: 1.25em; height: 1.25em; background-color: ${rowData[this.name]}"/>`
    );
  }

  renderDecoratorBool(rowData: any, thead: boolean) {
    if (thead) {
      return this.renderDecoratorPlain(rowData, thead);
    }

    const booleanValue = rowData[this.name];

    // Check for null and display "null"
    if (booleanValue === null) {
      return 'null';
    }

    // Defines Icon: Checkmark or X
    const icon = booleanValue ? '&#10004;' : '&#10008;';
    // Defines Color: green Checkmark or red X
    const color = booleanValue ? 'green' : 'red';

    return `<span style="color: ${color};">${icon}</span>`;
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
      const func = `(function(e) { 
        e.preventDefault(); 
        e.stopPropagation(); 
        window.open("${value.replace(/\/$/, '')}", "_blank");
      })`;
      const fileName = value.replace(/^.*[\\/]/, '');
      return `<a href="javascript:void(0)" onclick='${func}(event)'>${fileName}</a>`;
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
