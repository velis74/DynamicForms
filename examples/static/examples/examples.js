// noinspection JSUnusedGlobalSymbols
examples = {
  Fields: {note: '', unit: '', int_fld: '', qty_fld: '', cst_fld: ''},

  modalDlgGenericCallback: function modalDlgGenericCallback() {
    alert(this.text);
  },

  testModalDialog: function testModalDialog() {
    buttons = [
      {title: 'Cancel', callback: 'examples.modalDlgGenericCallback', parameters: {text: "Test"}},
      {
        title:      'OK',
        style:      'primary',
        callback:   'examples.modalDlgGenericCallback',
        parameters: {text: "Clicked OK button"},
      },
    ];

    dynamicforms.showModalDialog('Test dialog', '<p>Modal dialog content</p>', buttons);
  },

  showAlertDialog: function(payload) {
    // This is also reactive. If you do
    // payload.context.rows = {};
    // All rows will be gone for example.

    console.log('Show alert dialog', this, payload);
    alert('Page: ' + this.page + '; Field: ' + this.field);
  },

  pageLoadOrdering: function (sortedColumns) {
    // In this example function returns same as default.
    // But you could set whatever response you like.
    return sortedColumns.map((o) => (o.direction === false ? '-' : '') + o.fieldName)
  }
};
