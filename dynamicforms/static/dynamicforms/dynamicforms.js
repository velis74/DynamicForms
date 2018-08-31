$.fn.serializeForm = function (fieldNamePrefix, handlers, returnDict) {
  /**
   * serializes the given form into a JS object. Tries to keep all input fields, including unselected checkboxes
   * and disabled fields
   * @param fieldNamePrefix: fields in the form have a prefix in their name we don't want in the object
   * @param handlers: dict of transformation functions in the form field_name: function to transform the value
   * @param returnDict: true if you want the function to return a dictionary of form.id: serialized form
   * @return: JS object with form data
   */
  fieldNamePrefix = fieldNamePrefix == undefined ? '' : fieldNamePrefix;
  handlers   = handlers == undefined ? {} : handlers;
  returnDict = returnDict == undefined ? false : returnDict;

  var res_d = {}
  var res   = $.map(this, function (item) {
    var o          = {},
        $form      = $(item),
        storeValue = function (name, value) {
          var handler = handlers[name.substring(fieldNamePrefix.length)] || {};

          if (handler.value != undefined)
            value = handler.value(name, value);
          value = value == undefined ? '' : value;

          if (o[name] !== undefined) {
            if (!o[name].push)
              o[name] = [o[name]];
            o[name].push(value);
          } else
            o[name] = value;
        },
        disabled   = $(this).find(':input:disabled').removeAttr('disabled');

    $.each($form.serializeArray(), function () {
      var name  = this.name.replace(fieldNamePrefix, ''),
          value = this.value;
      storeValue(name, value);
    });
    disabled.attr('disabled', true);
    $form.find('input:checkbox').each(function () {
      var name = this.name.replace(fieldNamePrefix, '');
      if (name in o) delete o[name];
    });
    $form.find('input:checkbox').each(function () {
      var name  = this.name.replace(fieldNamePrefix, ''),
          value = $(this).is(':checked'); // ? this.value || true : false;
      if (value && 'value' in this.attributes)
        value = this.value;
      storeValue(name, value);
    });
    res_d[item.id] = o;
    return o;
  });
  if (returnDict === true) return res_d;
  return res.length == 1 ? res[0] : res;
};

$.fn.deserializeForm = function (data, fieldNamePrefix, handlers) {
  fieldNamePrefix = fieldNamePrefix == undefined ? '' : fieldNamePrefix;
  handlers        = handlers == undefined ? {} : handlers;

  var setValue = function ($inp, value) {
    if ($inp.length > 0) {
      var handler = handlers[$inp[0].name.substring(fieldNamePrefix.length)] || {};
      if (handler.value != undefined)
        value = handler.value($inp, value);

      if ($inp.is(":checkbox"))
        $inp.prop("checked", value);
      else
        $inp.val(value);

      if ($inp.is(':ui-selectmenu')) {
        // noinspection JSUnresolvedFunction
        $inp.selectmenu("refresh");
        // noinspection JSUnresolvedFunction
        if ($inp.selectmenu("option", "change") != undefined)
        // noinspection JSUnresolvedFunction
          $inp.selectmenu("option", "change")();
      }
      if ($inp.data("select2") != undefined)
        $inp.trigger("change");

      if (handler.copy != undefined)
        setValue(handler.copy, value);
    }
  };

  this.each(function () {
    var $form = $(this);
    $.each(data, function (key, value) {
      setValue($form.find("[name='%s']".replace(/%s/, fieldNamePrefix + key)), value);
    });
  });
};

/**
 * Two level dictionary
 */
function TLD() {
  this.storage = {};
};

TLD.prototype = {
  get: function get(key1, key2) {
    if (this.storage[key1] == undefined)
      return undefined;
    return this.storage[key1][key2];
  },

  set: function set(key1, key2, value) {
    if (this.storage[key1] == undefined)
      this.storage[key1] = {};
    this.storage[key1][key2] = value;
  },

  del: function del(key) {
    delete this.storage[key];
  }
};

dynamicforms = {
  // DF is an object containing all dynamicforms settings as specified by defaults and in settings.py
  DF: {
    // This is only necessary so that IDE doesn't complain about members not found when you use any of the settings
    // in code
    "MODULE_PREFIX":        "DYNAMICFORMS_",
    "TEMPLATE":             "dynamicforms/bootstrap/",
    "TEMPLATE_OPTIONS":     {
      "BOOTSTRAP_VERSION": "v4",
      "EDIT_IN_DIALOG":    true
    },
    "MODAL_DIALOG":         "modal_dialog",
    "BSVER_INCLUDES":       "dynamicforms/bootstrap/base_includes_v4.html",
    "BSVER_FIELD_TEMPLATE": "dynamicforms/bootstrap/field/base_field_v4.html",
    "BSVER_MODAL":          "dynamicforms/bootstrap/modal_dialog_v4.html"
  },

  /**
   * Presents the error in data exchange with the server in a user understandable way
   * @param xhr
   * @param status
   * @param error
   */
  showAjaxError: function showAjaxError(xhr, status, error) {
    //TODO: make proper error display message. You will probably also need some text about what you were trying to do
    console.log(xhr, status, error);
  },

  /**
   * Handles what happens when user says "Save data". Basically serialization, send to server, response to returned
   * status and values
   * @param $dlg: current dialog which will be updated with call results or closed on successful data store
   * @param $form: the edited form containing the data
   */
  submitForm: function submitForm($dlg, $form) {
    // TODO: this will not be required once all the fields have their onChange events in place
    dynamicforms.serializeForm($form, 'final');

    var data = dynamicforms.getSerializedForm($form, 'final');

    var method = data['data-dynamicforms-method'] || 'POST';

    $.ajax({
             type:     method,
             url:      $form.attr("action"),
             data:     data,
             dataType: 'html',
             headers:  {'X-DF-DIALOG': 'true'}
           })
      .done(function () {
        // TODO: refresh list of items. Dialogjust closes, but whatever we changed doesn't get updated in the list
        dynamicforms.closeDialog($dlg);
      })
      .fail(function (xhr, status, error) {
        // TODO: this doesn't handle errors correctly: if return status is 400 something, it *might* be OK
        // but if it's 500 something, dialog will be replaced by non-dialog code and displaying it will fail
        // also for any authorization errors, CSRF, etc, it will again fail
        // Try finding a <div class="dynamicforms-dialog"/> in there to see if you actually got a dialog
        dynamicforms.replaceDialog($dlg, $(xhr.responseText));
      });
  },

  /**
   * Shows a dialog, attaches appropriate event handlers to buttons and gets initial data values
   * @param $dlg
   */
  showDialog: function showDialog($dlg) {
    //TODO: adjust hashURL
    $(document.body).append($dlg);
    var $form = $dlg.find('.dynamicforms-form');
    $($dlg).on('hidden.bs.modal', function () {
      // dialog removes itself from DOM hierarchy
      $dlg.remove();

      dynamicforms.removeFormDeclarations($form);
    });

    // Let's get initial field values from the form
    dynamicforms.serializeForm($form, 'final');

    var saveId = '#save-' + $form.attr('id');
    $(saveId).on('click', function () { dynamicforms.submitForm($dlg, $form); });
    // And show the dialog
    $dlg.modal();
  },

  /**
   * Replaces the current dialog with a new one. Different than close + open in animation
   * TODO: change animation
   * @param $dlg: dialog to close
   * @param $newDlg: newdialog to show
   */
  replaceDialog: function replaceDialog($dlg, $newDlg) {
    dynamicforms.closeDialog($dlg);
    dynamicforms.showDialog($newDlg);
  },

  /**
   * Closes the current dialog
   * TODO: adjust hashURL
   * @param $dlg: dialog to close
   */
  closeDialog: function closeDialog($dlg) {
    $dlg.modal('hide');
  },

  /**
   * Handles what should happen when user clicks to edit a record
   * @param recordURL: url to call to get data / html for the record / dialog
   */
  editRow: function editRow(recordURL) {
    if (dynamicforms.DF.TEMPLATE_OPTIONS.EDIT_IN_DIALOG) {
      recordURL += '?df_dialog=true';
      $.ajax({
               url:     recordURL,
               headers: {'X-DF-DIALOG': 'true'}
             })
        .done(function (dialogHTML) { dynamicforms.showDialog($(dialogHTML)); })
        .fail(function (xhr, status, error) { dynamicforms.showAjaxError(xhr, status, error); });
    }
    else
      window.location = recordURL;
  },

  /**
   * Handles what should happen when user clicks "Add new" button
   * Right now newRow doesn't do anything distinct, so let's just call editRow
   *
   * @param recordURL: url to call to get data / html for the record / dialog
   * @returns {*|void}
   */
  newRow: function newRow(recordURL) {
    return dynamicforms.editRow(recordURL);
  },

  /**************************************************************
   * Form current values support functions
   **************************************************************/

  form_helpers: new TLD(),

  _checkFinalParam: function _checkFinalParam(final) {
    if (final != 'final' && final != 'non-final') {
      console.trace();
      throw "Final is not in the allowed values! '" + final + "'";
    }
  },

  serializeForm: function serializeForm($form, final) {
    dynamicforms._checkFinalParam(final);
    $.each($form.serializeForm(undefined, undefined, true), function (key, value) {
      dynamicforms.form_helpers.set(key, final, value);
    });
  },

  clearSerializedForm: function clearSerializedForm($form, final) {
    dynamicforms._checkFinalParam(final);
    dynamicforms.form_helpers.del($form.attr('id'), final);
  },

  getSerializedForm: function getSerializedForm($form, final) {
    dynamicforms._checkFinalParam(final);
    return dynamicforms.form_helpers.get($form.attr('id'), final);
  },

  removeFormDeclarations: function removeFormDeclarations($form) {
    dynamicforms.form_helpers.del($form.attr('id'));
  },
  /**************************************************************
   * Actions support functions
   **************************************************************/

  // A helper obj containing all getters, setters, previous onchanging values, etc.
  field_helpers:          new TLD(),

  /**
   * fieldChange function is called whenever field's value changes. Some fields support even "changing" events where
   * this function will be called for every change in the field's contents (e.g. typing a new letter into input).
   * This function will then propagate the event to all actions letting them know of the change
   * Note that "onchanging" has a separate "previous value" tracking. "onchanged" will report value before any editing
   * no matter how many times "onchanging" has been processed
   *
   * TODO does getValue require a "default" parameter? In what situations would the default value be returned?
   * TODO what does getValue return for inputs that are currently hidden or suppressed? Proposal: nothing, but we must always use PATCH, not PUT?
   * //$inputs.on('change keyup paste', function () { self.selectMenuShow(false, $(this)); });  //navaden input onchanging
   * //$inputs.on('focusout', function () { self.selectMenuShow(true, $(this)); });  // navaden input onchanged
   *
   * @param fieldID: id of the field
   * @param final: 'final' when this is "onchanged" and 'non-final' when this is "onchanging"
   */
  fieldChange: function fieldChange(fieldID, final) {
    dynamicforms._checkFinalParam(final);

    var field       = dynamicforms.field_helpers[fieldID],
        $field      = $('#' + fieldID),
        newValue    = field.getValue($field),
        oldValue,
        $form       = dynamicforms.field_helpers.get(fieldID, '$form'),
        newFormData,
        oldFormData = {};

    if (final) {
      newFormData = dynamicforms.getSerializedForm($form, final);
      dynamicforms.clearSerializedForm($form, 'non-final')
    } else {
      newFormData = dynamicforms.getSerializedForm($form, final);
      if (formData == undefined)
        newFormData = dynamicforms.getSerializedForm($form, 'final');
    }

    $.extend(true, oldFormData, newFormData);
    oldValue                         = newFormData[$field.attr('name')];
    newFormData[$field.attr('name')] = newValue;

    if (oldValue != newValue) {
      console.log('Field ' + $field.attr('name') + 'value has changed. Triggering actions');
      var actions = dynamicforms.form_helpers.get($form.attr('id'), 'actions');
      if (actions)
        $.each(actions, function (idx, action) {
          // TODO med izvajanjem actionov je verjetno bolje, če se onchange ne procesira
          // TODO na koncu funkcije je treba serializirat formo, da vidimo, če so se še katera polja spremenila
          // če so se --> onchange? verjetno ja, ker je od novih vrednosti morda odvisna kakšna vidnost ali pa še kakšen
          // dodaten onchange
          action(newFormData, oldFormData, [fieldID]);
        });
    }
  },

  /**
   * Registers the function which will get current field's value. See "standard" fieldGetValue below
   * @param formID: id of form object
   * @param fieldID: id of the field
   * @param func: function to be called for getting current field value
   */
  registerFieldGetter: function registerFieldGetter(formID, fieldID, func) {
    dynamicforms.field_helpers.set(fieldID, 'getValue', func);
    dynamicforms.field_helpers.set(fieldID, '$form', $(formID));

    var form_fields      = dynamicforms.form_helpers.get(formID, 'fields') || {};
    form_fields[fieldID] = 1;
    dynamicforms.form_helpers.set(formID, 'fields', form_fields);
  },

  /**
   * Registers the function which will set current field's value. See "standard" fieldSetValue below
   * @param formID: id of form object
   * @param fieldID: id of the field
   * @param func: function to be called for setting current field value
   */
  registerFieldSetter: function registerFieldSetter(formID, fieldID, func) {
    dynamicforms.field_helpers.set(fieldID, 'setValue', func);
    dynamicforms.field_helpers.set(fieldID, '$form', $(formID));

    var form_fields      = dynamicforms.form_helpers.get(formID, 'fields') || {};
    form_fields[fieldID] = 1;
    dynamicforms.form_helpers.set(formID, 'fields', form_fields);
  },

  /**
   * "Standard" function for getting an input's current value. Any special cases will be handled in custom functions
   * @param $field: jQuery selector of the field
   * @returns field value
   */
  fieldGetValue: function fieldGetValue($field) {
    return $field.val();
  },

  /**
   * "Standard" function for setting an input's. Any special cases will be handled in custom functions
   * @param $field: jQuery selector of the field
   * @param value: new value to set
   */
  fieldSetValue: function fieldSetValue($field, value) {
    $field.val(value);
  }
};

$(document).ready(function () {
  // Let's get initial field values from the forms that are on-page already
  // TODO: Is this jQuery-specific? Will vue.js page also contain some kind of initializer or will everything just work?
  // TODO: also might be prudent to just move this to base_form.html. we already process dialogs separately...
  $.extend(dynamicforms, $('.dynamicforms-form').serializeForm(undefined, undefined, true));
})