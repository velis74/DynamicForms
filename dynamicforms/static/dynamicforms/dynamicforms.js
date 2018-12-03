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

  var res_d = {};
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
    res_d[item.attributes['id'].value] = o;
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
}

TLD.prototype = {
  get: function get(key1, key2) {
    if (this.storage[key1] == undefined)
      return undefined;
    if (key2 == undefined)
      return this.storage[key1];
    return this.storage[key1][key2];
  },

  set: function set(key1, key2, value) {
    if (this.storage[key1] == undefined)
      this.storage[key1] = {};
    if (key2 == undefined)
      this.storage[key1] = value;
    else
      this.storage[key1][key2] = value;
  },

  del: function del(key1, key2) {
    if (key2)
      delete this.storage[key1][key2];
    else
      delete this.storage[key1];
  },

  getOrCreate: function getOrCreate(key1, key2, defVal) {
    var res = this.get(key1, key2);
    if (res == undefined) {
      res = defVal;
      this.set(key1, key2, res);
    }
    return res;
  },
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
      "EDIT_IN_DIALOG":    true,
    },
    "MODAL_DIALOG":         "modal_dialog",
    "BSVER_INCLUDES":       "dynamicforms/bootstrap/base_includes_v4.html",
    "BSVER_FIELD_TEMPLATE": "dynamicforms/bootstrap/field/base_field_v4.html",
    "BSVER_MODAL":          "dynamicforms/bootstrap/modal_dialog_v4.html",
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

    var data    = dynamicforms.getSerializedForm($form, 'final');
    var method  = data['data-dynamicforms-method'] || 'POST';
    var headers = {'X-DF-RENDER-TYPE': 'dialog'};

    if ('csrfmiddlewaretoken' in data) {
      headers['X-CSRFToken'] = data.csrfmiddlewaretoken;
      delete data.csrfmiddlewaretoken;
    }

    $.ajax({
             type:     method,
             url:      $form.attr("action"),
             data:     data,
             dataType: 'html',
             headers:  headers,
           })
      .done(function () {
        // TODO: refresh list of items. Dialog just closes, but whatever we changed doesn't get updated in the list
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
    $(saveId).on('click', function () {
      dynamicforms.submitForm($dlg, $form);
    });
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
      recordURL += '?df_render_type=dialog'; // TODO: is this necessary? we already add the header
      $.ajax({
               url:     recordURL,
               headers: {'X-DF-RENDER-TYPE': 'dialog'},
             })
        .done(function (dialogHTML) {
          dynamicforms.showDialog($(dialogHTML));
        })
        .fail(function (xhr, status, error) {
          dynamicforms.showAjaxError(xhr, status, error);
        });
    }
    else
      window.location = recordURL;
  },

  /**
   * Handles what should happen when user clicks to delete a record
   * @param recordURL: url to call to get data / html for the record / dialog
   */
  deleteRow: function deleteRow(recordURL) {
    //TODO: Ask user for confirmation
    $.ajax({
             url:    recordURL,
             method: 'DELETE',
             headers: {'X-CSRFToken': dynamicforms.csrf_token },
           })
      .done(function (dialogHTML) {
        console.log('Record successfully deleted.');
        //  TODO: make a proper notification
      })
      .fail(function (xhr, status, error) {
        dynamicforms.showAjaxError(xhr, status, error);
      });
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

  df_tbl_pagination: new TLD(),

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

  getSerializedFormFinal: function getSerializedFormFinal($form, final) {
    var newFormData = dynamicforms.getSerializedForm($form, final);
    if (final == 'final')
      dynamicforms.clearSerializedForm($form, 'non-final');
    else if (newFormData == undefined)
      newFormData = dynamicforms.getSerializedForm($form, 'final');
    return newFormData;
  },

  removeFormDeclarations: function removeFormDeclarations($form) {
    var formID = $form.attr('id');
    $.each(dynamicforms.form_helpers.getOrCreate(formID, 'fields', {}),
           function (fieldID) {
             dynamicforms.field_helpers.del(fieldID);
           }
    );
    dynamicforms.form_helpers.del(formID);
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

    var field       = dynamicforms.field_helpers.get(fieldID),
        $field      = field.$field,
        $form       = field.$form,
        newValue    = field.getValue($field),
        oldValue,
        newFormData = dynamicforms.getSerializedFormFinal($form, final),
        oldFormData = {};

    // Copy the current form values to "old" object and adjust the current values with the change
    $.extend(true, oldFormData, newFormData);
    var field_name          = $field.attr('name');
    oldValue                = newFormData[field_name];
    newFormData[field_name] = newValue;

    // Process the change if there was any
    if (oldValue != newValue)
      dynamicforms.processChangedFields(final, [fieldID], oldFormData, newFormData);
  },

  /**
   * This function calls the handlers when a field has been changed. After processing the handlers it will check for
   * additional changes. If detected, it will process the handlers for the new changes as well.
   * @param final: 'final' when this is "onchanged" and 'non-final' when this is "onchanging"
   * @param fields: list[field id]
   * @param oldFormData: object
   * @param newFormData: object
   */
  processChangedFields: function processChangedFields(final, fields, oldFormData, newFormData) {
    var changedHelper = new TLD();

    //Apply field actions
    $.each(fields, function (idx, fieldID) {
      var field      = dynamicforms.field_helpers.get(fieldID),
          $field     = field.$field,
          field_name = $field.attr('name'),
          $form      = field.$form,
          formID     = $form.attr('id');

      if (changedHelper.get(formID, 'visibility') == undefined) {
        // Remember current field visibility
        changedHelper.set(formID, 'visibility', dynamicforms.getVisibleFields(formID));
        changedHelper.set(formID, 'old', newFormData);
      }
      // console.log('Field "' + field_name + '" value has changed. Triggering actions');
      var actions = dynamicforms.form_helpers.get(formID, 'actions_' + fieldID);
      if (actions) {
        $.each(actions, function (idx, action) {
          // TODO while running actions, it's probably better not to process onchange
          action($form.attr('id'), newFormData, oldFormData, [fieldID]);
        });
      }
    });

    $.each(changedHelper.storage, function (formID, ignored) {
      var $form         = $('#' + formID),
          // Get new field values & visibility
          oldFormData   = changedHelper.get(formID, 'old'),
          newFormData   = dynamicforms.getSerializedFormFinal($form, final),
          oldVisibility = changedHelper.get(formID, 'visibility'),
          newVisibility = dynamicforms.getVisibleFields(formID),
          changedFields = [];

      // get diff for visibility & union it with diff for field values
      $.each(dynamicforms.form_helpers.get(formID, 'fields'), function (fieldID, field) {
        if (
          ($.inArray(fieldID, oldVisibility) != -1) != ($.inArray(fieldID, newVisibility) != -1) ||
          (newFormData[field.name] != oldFormData[field.name])
        ) {
          changedFields.push(fieldID);
        }
      });

      // go through all fields and run their actions if either their value or their visibility is changed
      processChangedFields(final, changedFields, oldFormData, newFormData);
    });
  },

  /**
   * Registers an onchange event with action to execute when given field's value changes
   * @param formID: id of form object
   * @param fieldID: id of the field
   * @param func: function to be called for getting current field value
   */
  registerFieldAction: function registerFieldAction(formID, fieldID, func) {
    var fieldActions = dynamicforms.form_helpers.get(formID, 'actions_' + fieldID) || [];
    fieldActions.push(func);
    dynamicforms.form_helpers.set(formID, 'actions_' + fieldID, fieldActions);
  },

  /**
   * Registers the function which will get current field's value. See "standard" fieldGetValue below
   * @param formID: id of form object
   * @param fieldID: id of the field
   * @param func: function to be called for getting current field value
   */
  registerFieldGetter: function registerFieldGetter(formID, fieldID, func) {
    var field      = dynamicforms.field_helpers.getOrCreate(fieldID, undefined, {});
    field.getValue = func;
    dynamicforms.updateFieldHelpers(formID, fieldID, field);
  },

  /**
   * Registers the function which will set current field's value. See "standard" fieldSetValue below
   * @param formID: id of form object
   * @param fieldID: id of the field
   * @param func: function to be called for setting current field value
   */
  registerFieldSetter: function registerFieldSetter(formID, fieldID, func) {
    var field      = dynamicforms.field_helpers.getOrCreate(fieldID, undefined, {});
    field.setValue = func;
    dynamicforms.updateFieldHelpers(formID, fieldID, field);
  },

  /**
   * Sets some standard field helper values so that they don't have to be re-calculated every time
   * @param formID: id of form object
   * @param fieldID: id of the field
   * @param field: field data to be populated
   */
  updateFieldHelpers: function updateFieldHelpers(formID, fieldID, field) {
    if (field.$field == undefined) {
      field.$field = $('#' + fieldID);
      field.$form  = $('#' + formID);
      field.name   = field.$field.attr('name');
    }
    var form_fields       = dynamicforms.form_helpers.getOrCreate(formID, 'fields', {});
    form_fields[fieldID]  = field;
    var field_ids         = dynamicforms.form_helpers.getOrCreate(formID, 'field_ids', {});
    field_ids[field.name] = fieldID;
  },

  /**
   * Gets an object which maps field names to their IDs. This function is a helper for actions where field UUIDs
   * are not known in advance. Its result is passed to functions such as fieldSetValue.
   *
   * @param formID: id of form object
   * @return: object where obj.field_name == field control ID
   */
  getFieldIDs: function getFieldIDs(formID) {
    return dynamicforms.form_helpers.getOrCreate(formID, 'field_ids', {});
  },

  /**
   * "Standard" function for getting an input's current value. Any special cases will be handled in custom functions
   *
   * @param field: id or jQuery object of the field
   * @returns field value
   */
  fieldGetValue: function fieldGetValue(field) {
    var $field = field instanceof jQuery ? field : dynamicforms.field_helpers.get(field, '$field');
    return $field.val();
  },

  /**
   * "Standard" function for setting an input's value. Any special cases will be handled in custom functions
   *
   * @param field: id or jQuery object of the field
   * @param value: new value to set
   */
  fieldSetValue: function fieldSetValue(field, value) {
    var $field = field instanceof jQuery ? field : dynamicforms.field_helpers.get(field, '$field');
    $field.val(value);
  },

  /**
   * "Standard" function for setting an input's visibility. Any special cases will be handled in custom functions
   *
   * @param field: id or jQuery object of the field
   * @param visible: boolean specifying whether field should be visible
   */
  fieldSetVisible: function fieldSetVisible(field, visible) {
    //TODO: we need to check parent container if everything inside it is hidden. If there is, the parent container needs to hide too
    var $field  = field instanceof jQuery ? field : dynamicforms.field_helpers.get(field, '$field');
    var fieldID = $field.attr('id');
    $field.parents('#container-' + fieldID).toggle(visible);
  },

  /**
   * "Standard" function for checking whether an input's is visible. Any special cases will be handled in custom
   * functions
   *
   * @param field: id or jQuery object of the field
   * @return: boolean true for visible, false for hidden
   */
  fieldIsVisible: function fieldIsVisible(field) {
    var $field  = field instanceof jQuery ? field : dynamicforms.field_helpers.get(field, '$field');
    var fieldID = $field.attr('id');
    return $field.parents('#container-' + fieldID).is(":visible");
  },

  getVisibleFields: function getVisibleFields(formID) {
    var res = [];
    $.each(dynamicforms.form_helpers.get(formID, 'fields'), function (fieldID, field) {
      if (dynamicforms.fieldIsVisible(field.$field))
        res.push(fieldID);
    });
    return res;
  },

  paginator_init_table: function paginator_init(serializer_uuid, link_next, link_prev) {
    if (link_next != "") {
      dynamicforms.df_tbl_pagination.set(serializer_uuid, 'link_next', link_next);
      var table_rows = $("#list-" + serializer_uuid).find("tbody:first").find("tr");
      dynamicforms.df_tbl_pagination.set(serializer_uuid, 'trigger_element', table_rows[0]);
    }
  },

  paginator_check_get_next_page: function check_get_next_page(serializer_uuid) {
    var trigger_element = dynamicforms.df_tbl_pagination.get(serializer_uuid, 'trigger_element');

    if (trigger_element != null) {
      var rect = trigger_element.getBoundingClientRect();

      if (rect.top <= (window.innerHeight || document.documentElement.clientHeight))
        dynamicforms.paginator_get_next_page(serializer_uuid);

      //TODO: Check both methods of determining whether control item is showing (unit tests for one and the other?)
      // problem with unit tests is that automated ones only run in Firefox

      //   var top_of_element    = trigger_element.offset().top;
      //   var bottom_of_element = top_of_element + trigger_element.outerHeight();
      //   var top_of_screen     = $(window).scrollTop();
      //   var bottom_of_screen  = top_of_screen + window.innerHeight;
      //
      //   if (bottom_of_screen > top_of_element) {
      //     dynamicforms.paginator_get_next_page(serializer_uuid);
      //   }
    }
  },

  paginator_get_next_page: function next_page(serializer_uuid) {
    var tbl_pagination = dynamicforms.df_tbl_pagination.get(serializer_uuid, undefined);
    var link_next      = tbl_pagination.link_next;
    if (link_next != null && link_next != tbl_pagination.last_link_next) {
      tbl_pagination.last_link_next = link_next;
      $("#loading-" + serializer_uuid).show();
      $.ajax({
               type:    'GET',
               headers: {'X-CSRFToken': dynamicforms.csrf_token, 'X-DF-RENDER-TYPE': 'table rows'},
               url:     link_next,
             }).done(function (data) {
        var table                = $("#list-" + serializer_uuid).find("tbody:first");
        data                     = $(data).filter("tr");
        tbl_pagination.link_next = data[0].getAttribute('data-next');
        // remove elements, that are already shown - in case of new data insertion and order different than id.
        for (var i = data.length - 1; i >= 0; i--) {
          var data_id = data[i].getAttribute('data-id');
          if (data_id == null || table.find("tr[data-id='" + data_id + "']").length > 0)
            data.splice(i, 1);
        }
        //TODO: If NoData comes back - i reached the end of dataset... doI even attempt further reading?
        //  for log-type datasets where new data is frequently inserted, it might be useful.
        $("#loading-" + serializer_uuid).hide();
        if (data.length > 0) {
          table.append(data);
          tbl_pagination.trigger_element = data[0];
        }
        dynamicforms.paginator_check_get_next_page(serializer_uuid);
      }).fail(function (xhr, status, error) {
        $("#loading-" + serializer_uuid).hide();
        console.log('Pagination failed.', xhr, status, error);
        // TODO: what if the server returns an error? Do we continue with pagination? (Task #100)
      });
    }
  },

  paginator_check_get_next_page_all: function paginator_check_get_next_page_all() {
    for (var serializer_uuid in dynamicforms.df_tbl_pagination.storage)
      dynamicforms.paginator_check_get_next_page(serializer_uuid);
  },
};

$(document).ready(function () {
  // Let's get initial field values from the forms that are on-page already
  // TODO: Is this jQuery-specific? Will vue.js page also contain some kind of initializer or will everything just work?
  // TODO: also might be prudent to just move this to base_form.html. we already process dialogs separately...
  $.extend(dynamicforms, $('.dynamicforms-form').serializeForm(undefined, undefined, true));
  window.setInterval(dynamicforms.paginator_check_get_next_page_all, 100);
})

