// noinspection JSUnusedGlobalSymbols
examples = {
  Fields: {note: '', unit: '', int_fld: '', qty_fld: '', cst_fld: ''},

  hide_fields_on_show: function hide_fields_on_show(formID) {
    var rec = dynamicforms.getSerializedForm($('#' + formID), 'final');
    var fields = dynamicforms.getFieldIDs(formID);  // fields: examples.Fields

    this.action_hiddenfields_note(formID, rec, rec, [fields['note']]);
    this.action_hiddenfields_unit(formID, rec, rec, [fields['unit']]);
  },

  action_hiddenfields_note: function action_note(formID, newRec, oldRec, changedFields) {
    var fields = dynamicforms.getFieldIDs(formID);  // fields: examples.Fields
    if (changedFields.includes(fields.note)) {
      dynamicforms.fieldSetVisible(fields.unit, newRec.note != 'abc');
    }
  },

  action_hiddenfields_unit: function action_hiddenfields_unit(formID, newRec, oldRec, changedFields) {
    var fields = dynamicforms.getFieldIDs(formID);  // fields: examples.Fields
    if (changedFields.includes(fields.unit)) {
      var unit_visible = dynamicforms.fieldIsVisible(fields.unit);

      //dynamicforms.fieldSetValue(amountID, 6);
      dynamicforms.fieldSetVisible(fields.int_fld, unit_visible && ['pcs', 'cst'].includes(newRec.unit));
      dynamicforms.fieldSetVisible(fields.qty_fld, unit_visible && newRec.unit == 'wt');
      dynamicforms.fieldSetVisible(fields.cst_fld, unit_visible && newRec.unit == 'cst');
    }
  },

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
    console.log(sortedColumns);
    return sortedColumns.map((o) => (o.direction === false ? '-' : '') + o.fieldName)
  }
};
