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

dynamicforms = {
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

  showAjaxError: function showAjaxError(xhr, status, error) {
    //TODO: make proper error display message. You will probably also need some text about what you were trying to do
    console.log(xhr, status, error);
  },

  submitForm: function submitForm($dlg, $form) {
    // TODO: this will not be required once all the fields have their onChange events in place
    $.extend(dynamicforms, $form.serializeForm(undefined, undefined, true));

    var data = dynamicforms[$form.attr('id')];

    var method = data['data-dynamicforms-method'] || 'POST';

    $.ajax({
             type:     method,
             url:      $form.attr("action"),
             data:     data,
             dataType: 'html',
             headers:  {'X-DF-DIALOG': 'true'}
           })
      .done(function () { dynamicforms.closeDialog($dlg); })
      .fail(function (xhr, status, error) {
        // TODO: this doesn't handle errors correctly: if return status is 400 something, it *might* be OK
        // but if it's 500 something, dialog will be replaced by non-dialog code and displaying it will fail
        // also for any authorization errors, CSRF, etc, it will again fail
        dynamicforms.replaceDialog($dlg, $(xhr.responseText));
      });
  },

  showDialog: function showDialog($dlg) {
    //TODO: adjust hashURL
    $(document.body).append($dlg);
    var $form = $dlg.find('.dynamicforms-form');
    $($dlg).on('hidden.bs.modal', function () {
      // dialog removes itself from DOM hierarchy
      $dlg.remove();

      // And from cache of current form values
      delete dynamicforms[$form.attr('id')];
    });

    // Let's get initial field values from the form
    $.extend(dynamicforms, $form.serializeForm(undefined, undefined, true));

    var saveId = '#save-' + $form.attr('id');
    $(saveId).on('click', function () { dynamicforms.submitForm($dlg, $form); });
    // And show the dialog
    $dlg.modal();
  },

  replaceDialog: function replaceDialog($dlg, $newDlg) {
    //TODO: change animation
    dynamicforms.closeDialog($dlg);
    dynamicforms.showDialog($newDlg);
  },

  closeDialog: function closeDialog($dlg) {
    //TODO: adjust hashURL
    $dlg.modal('hide');
  },

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

  newRow: function newRow(recordURL) {
    // Right now newRow doesn't do anything distinct, so let's just call editRow
    return dynamicforms.editRow(recordURL);
  }
};

$(document).ready(function () {
  // Let's get initial field values from the forms that are on-page already
  // TODO: Is this jQuery-specific? Will vue.js page also contain some kind of initializer or will everything just work?
  // TODO: also might be prudent to just move this to base_form.html. we already process dialogs separately...
  $.extend(dynamicforms, $('.dynamicforms-form').serializeForm(undefined, undefined, true));
})