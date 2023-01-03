import ColumnDisplay from '../../classes/display-mode';
import getObjectFromPath from '@/components/util/get-object-from-path';

import ColumnOrdering from '@/components/table/definitions/column-ordering';

export default class TableColumn {
  private _maxWidth: number;
  private ordering: ColumnOrdering;
  private layout: null;
  private returnFunction: any;
  private _initialData: any;
  private readonly renderDecorator: any;
  
  constructor(initialData: any, orderingArray: any) {
    this._maxWidth = 0;
    initialData.ordering = initialData.ordering || '';
    this.ordering = new ColumnOrdering(initialData.ordering, orderingArray, this);
    this.layout = null;
    this._initialData = initialData;

    // Determine what is to be used for render decorator for this column
    this.renderDecorator = initialData.render_params ? initialData.render_params.table : '';
    let returnFunc: any = this.renderDecoratorPlain;
    if (this.renderDecorator && this.renderDecorator.substring(0, 13) === 'df-tablecell-') {
      switch (this.renderDecorator.substring(13)) {
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
    } else if (this.renderDecorator && this.renderDecorator.substring(0, 1) !== '#') {
      // Here we're expecting the decorator to suggest we use a globally accessible function
      // When a function, name will be in format module.submodule.submodule_n.function,
      //   e.g. myModule.formatEmail
      //   The above example will look for function in window['myModule']['formatEmail'] and call it.
      returnFunc = getObjectFromPath(this.renderDecorator);
    }

    this.returnFunction = returnFunc;
  }

  // Below we circumvent having to declare an internal variable which property getters would be reading from
  get name(): string { return this._initialData.name; }
  get label(): string { return this._initialData.label; }
  get align(): string {
    if (this._initialData.alignment === 'decimal') return 'right';
    return this._initialData.alignment;
  }
  get visibility(): number { return ColumnDisplay.get(this._initialData.visibility.table); }
  get CSSClass(): string { return this._initialData.table_classes || ''; }
  get CSSClassHead(): string { return (this.ordering.isOrderable && 'ordering') || ''; }
  get renderParams(): any { return this._initialData.render_params; }
  get renderComponentName(): string {
    if (this.renderDecorator && this.renderDecorator.substring(0, 1) === '#') {
      // When component, name will start with #, e.g. #TableCellFloat. This will instruct table body to
      //   render a component with this name. You need to register it correctly
      return this.renderDecorator.substring(1);
    }
    return '';
  }
  get renderDecoratorFunction(): Function {
    return (rowData: any, thead: any) => this.returnFunction.apply(this, [rowData, thead]);
  }
  get maxWidth(): number { return this._maxWidth; }

  setLayout(layout: any) {
    this.layout = layout;
  }

  setMaxWidth(value: number) {
    if (value > this._maxWidth) {
      this._maxWidth = value;
    }
  }

  // eslint-disable-next-line @typescript-eslint/no-unused-vars
  renderDecoratorPlain(rowData: any, thead?: any) {
    return rowData[this.name];
  }

  renderDecoratorBool(rowData: any, thead: any) {
    if (thead) return this.renderDecoratorPlain(rowData, thead);
    return `<code>${rowData[this.name]}</code>`;
  }

  renderDecoratorLink(rowData: any, thead: any) {
    if (thead) return this.renderDecoratorPlain(rowData, thead);
    return `<a href="${rowData[this.name]}">${rowData[this.name]}</a>`;
  }

  renderDecoratorEmail(rowData: any, thead: any) {
    if (thead) return this.renderDecoratorPlain(rowData, thead);
    const value = rowData[this.name];
    const nameOnly = value.includes('<') ? value.substring(0, value.indexOf('<')).trim() : value;
    return `<a href="mailto:${value}">${nameOnly}</a>`;
  }

  renderDecoratorFile(rowData: any, thead: any) {
    if (thead) return this.renderDecoratorPlain(rowData, thead);
    const value = rowData[this.name];
    if (value) {
      const downloadContent = `event.stopPropagation(); window.open("${value}", "_blank")`;
      const fileName = value.replace(/^.*[\\/]/, '');
      return `<a href="#" onclick='${downloadContent}'>${fileName}</a>`;
    }
    return null;
  }

  renderDecoratorIP(rowData: any, thead: any) {
    if (thead) return this.renderDecoratorPlain(rowData, thead);
    let value = rowData[this.name];
    const segments = value.split('.');
    if (segments.length === 4) {
      // eslint-disable-next-line no-param-reassign
      value = segments.map((x: Array<any>) => {
        const padding = x.length < 3 ? `<span style="opacity: .5">${'000'.slice(x.length - 3)}</span>` : '';
        return `${padding}<span>${x}</span>`;
      }).join('.');
    }
    return `<code>${value}</code>`;
  }
}
