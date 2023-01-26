install Node.js and npm
cd TO REPOSITORY ROOT
cd dynamicforms/static
git clone git@github.com:ckeditor/ckeditor5.git
cd ckeditor5
npm install
cd node_modules/@ckeditor/ckeditor5-build-classic
npm install

Change function in following files to:

*** 1 STEP ***
node_modules/@ckeditor/ckeditor5-font/src/utils.js -> renderDowncastElement:
export function renderDowncastElement( styleAttr ) {
	return ( modelAttributeValue, { writer } ) => writer.createAttributeElement( 'span', {
		class: `text-${ modelAttributeValue }`
	}, { priority: 7 } );
}

*** 2 STEP ***
node_modules/@ckeditor/ckeditor5-font/src/utils.js -> addColorTableToDropdown:
export function addColorTableToDropdown( { dropdownView, colors, columns, removeButtonLabel, documentColorsLabel, documentColorsCount } ) {
	const locale = dropdownView.locale;
	const colorTableView = new ColorTableView( locale, { colors, columns, removeButtonLabel } );

	dropdownView.colorTableView = colorTableView;
	dropdownView.panelView.children.add( colorTableView );

	colorTableView.delegate( 'execute' ).to( dropdownView, 'execute' );

	return colorTableView;
}

*** 3 STEP ***
node_modules/@ckeditor/ckeditor5-font/src/ui/colortableview.js -> _createDocumentColorsGrid:
    _createDocumentColorsGrid() {
		const bind = Template.bind( this.documentColors, this.documentColors );
		const documentColorsGrid = new ColorGridView( this.locale, {
			columns: this.columns
		} );
		documentColorsGrid.delegate( 'execute' ).to( this );
		documentColorsGrid.extendTemplate( {
			attributes: {
				class: bind.if( 'isEmpty', 'ck-hidden' )
			}
		} );
		return documentColorsGrid;
	}

*** 4 STEP ***
node_modules/@ckeditor/ckeditor5-ui/src/colorgrid/colorgridview.js -> constructor:
	constructor( locale, options ) {
		super( locale );
		const colorDefinitions = options && options.colorDefinitions || [];
		const viewStyleAttribute = {};
		if ( options && options.columns ) {
			viewStyleAttribute.gridTemplateColumns = `repeat( ${ options.columns }, 1fr)`;
		}
		this.set( 'selectedColor' );
		this.items = this.createCollection();
		this.focusTracker = new FocusTracker();
		this.keystrokes = new KeystrokeHandler();
		this._focusCycler = new FocusCycler( {
			focusables: this.items,
			focusTracker: this.focusTracker,
			keystrokeHandler: this.keystrokes,
			actions: {
				// Navigate grid items backwards using the arrowup key.
				focusPrevious: 'arrowleft',

				// Navigate grid items forwards using the arrowdown key.
				focusNext: 'arrowright'
			}
		} );
		this.items.on( 'add', ( evt, colorTile ) => {
			colorTile.isOn = colorTile.color === this.selectedColor;
		} );
		colorDefinitions.forEach( color => {
			const colorTile = new ColorTileView(null, color);
			colorTile.set( {
				color: color,
				label: color.label,
				tooltip: true,
				hasBorder: color.options.hasBorder
			} );
			colorTile.on( 'execute', () => {
				this.fire( 'execute', {
					value: color.color,
					hasBorder: color.options.hasBorder,
					label: color.label
				} );
			} );
			this.items.add( colorTile );
		} );
		this.setTemplate( {
			tag: 'div',
			children: this.items,
			attributes: {
				class: [
					'ck',
					'ck-color-grid'
				],
				style: viewStyleAttribute
			}
		} );
		this.on( 'change:selectedColor', ( evt, name, selectedColor ) => {
			for ( const item of this.items ) {
				item.isOn = item.color === selectedColor;
			}
		} );
	}

*** 5 STEP ***
node_modules/@ckeditor/ckeditor5-ui/src/colorgrid/colortileview.js -> constructor:
    constructor( locale, color = null ) {
		super( locale );
		const bind = this.bindTemplate;
		this.set( 'color' );
		this.set( 'hasBorder' );
		this.icon = checkIcon;
		this.extendTemplate( {
			attributes: {
				class: [
					'ck',
					'ck-color-grid__tile',
				  	'bg-' +  (color ? color.color : ''),
					bind.if( 'hasBorder', 'ck-color-table__color-tile_bordered' )
				]
			}
		} );
	}

*** 6 STEP ***
node_modules/@ckeditor/ckeditor5-font/src/fontcolor/fontcolorediting.js	-> set content to:

import {Plugin} from 'ckeditor5/src/core';
import FontColorCommand from './fontcolorcommand';
import {FONT_COLOR, renderDowncastElement, renderUpcastAttribute} from '../utils';

export default class FontColorEditing extends Plugin {

  static get pluginName() {
	return 'FontColorEditing';
  }

  constructor(editor) {
	super(editor);

	editor.config.define(FONT_COLOR, {
	  colors: [
		{
		  color: 'hsl(0, 0%, 0%)',
		  label: 'Black'
		},
		{
		  color: 'hsl(0, 0%, 30%)',
		  label: 'Dim grey'
		},
		{
		  color: 'hsl(0, 0%, 60%)',
		  label: 'Grey'
		},
		{
		  color: 'hsl(0, 0%, 90%)',
		  label: 'Light grey'
		},
		{
		  color: 'hsl(0, 0%, 100%)',
		  label: 'White',
		  hasBorder: true
		},
		{
		  color: 'hsl(0, 75%, 60%)',
		  label: 'Red'
		},
		{
		  color: 'hsl(30, 75%, 60%)',
		  label: 'Orange'
		},
		{
		  color: 'hsl(60, 75%, 60%)',
		  label: 'Yellow'
		},
		{
		  color: 'hsl(90, 75%, 60%)',
		  label: 'Light green'
		},
		{
		  color: 'hsl(120, 75%, 60%)',
		  label: 'Green'
		},
		{
		  color: 'hsl(150, 75%, 60%)',
		  label: 'Aquamarine'
		},
		{
		  color: 'hsl(180, 75%, 60%)',
		  label: 'Turquoise'
		},
		{
		  color: 'hsl(210, 75%, 60%)',
		  label: 'Light blue'
		},
		{
		  color: 'hsl(240, 75%, 60%)',
		  label: 'Blue'
		},
		{
		  color: 'hsl(270, 75%, 60%)',
		  label: 'Purple'
		}
	  ],
	  columns: 5
	});

	editor.conversion.for('upcast').elementToAttribute({
	  view: {
		name: 'span',
		key: 'class'
	  },
	  model: {
		key: FONT_COLOR,
		value: viewElement => viewElement.getAttribute('class') ? viewElement.getAttribute('class').replace('text-', '') : null
	  },
	  FONT_COLOR,
	  converterPriority: 'high'
	});

	editor.conversion.for('downcast').attributeToElement({
	  model: FONT_COLOR,
	  view: renderDowncastElement('color')
	});

	editor.commands.add(FONT_COLOR, new FontColorCommand(editor));

	// Allow the font color attribute on text nodes.
	editor.model.schema.extend('$text', {allowAttributes: FONT_COLOR});

	editor.model.schema.setAttributeProperties(FONT_COLOR, {
	  isFormatting: true,
	  copyOnEnter: true
	});
  }
}

*** 7 STEP ***
edit file src/ckeditor.js
add import: import Font from '@ckeditor/ckeditor5-font/src/font';
add Font to  ClassicEditor.builtinPlugins

npm run build
cp build/ckeditor.js ../../../ckeditor-df

cd TO REPOSITORY ROOT
rm -rf dynamicforms/static/ckeditor5