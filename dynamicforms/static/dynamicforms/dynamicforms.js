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
  // DYNAMICFORMS is an object containing all dynamicforms settings as specified by defaults and in settings.py
  DYNAMICFORMS: {
    'template': 'dynamicforms/bootstrap/',
    'jquery_ui': false,
    'edit_in_dialog': true,
    'bootstrap_version': 'v4',
  },

  /**
   * Presents the error in data exchange with the server in a user understandable way
   * @param xhr
   * @param status
   * @param error
   */
  showAjaxError:   function showAjaxError(xhr, status, error) {
    //TODO: make proper error display message. You will probably also need some text about what you were trying to do
    console.log([xhr, status, error]);
  },
  /**
   * Shows progress dialog if operation takes longer than 0.5 seconds. Also sets z-index of progress bar and overlay
   * @param progressDlgID: ID of progress dialog element - for custom progress dialogs.
   * @param progressSettings: Progress dialog settings - for custom progress dialogs.
   */
  showProgressDlg: function showProgressDialog(progressDlgID, progressSettings) {
    var zIndexElement = null;
    var progressDlg   = $('#' + progressDlgID);
    if (dynamicforms.DYNAMICFORMS.jquery_ui) {
      if (progressSettings === undefined)
        progressSettings = {value: 25};
      $("#df-progress-bar-indeterminate").progressbar(progressSettings);
      progressSettings['value'] = 0;
      $("#df-progress-bar-determinate").progressbar(progressSettings);

      if (dynamicforms.shouldShowProgressDlg) {
        dynamicforms.progressDlgShown = true;
        progressDlg.dialog({dialogClass: 'progress-bar', closeOnEscape: false, resizable: false});
      }
      zIndexElement = progressDlg.parents().first();
    } else {
      if (progressSettings === undefined)
        progressSettings = {keyboard: false, backdrop: 'static'};
      if (dynamicforms.shouldShowProgressDlg) {
        dynamicforms.progressDlgShown = true;
        progressDlg.modal(progressSettings);
      }
      zIndexElement = progressDlg;
    }
    var zIndexOrig = zIndexElement.css('z-index');
    var zIndex     = parseInt(zIndexOrig);
    if (zIndex == NaN)
      zIndex = zIndexOrig;
    else {
      // Because all bootstrap modules have same z-index. If we want that clickable progress bar will be on top of all
      // we must raise z-index. At the same time we must set overlay z-index, so nothing else will be clickable.
      zIndex += 1;
      zIndexElement.css('z-index', zIndex + 1);
    }

    $('#df-overlay').css('z-index', zIndex);
  },


  submitFormWithConfirmation: function submitFormWithConfirmation(url, $dlg, $form) {
    var data = dynamicforms.getSerializedForm($form, 'final');
    var method = data['data-dynamicforms-method'] || 'POST';
    var headers = {'X-DF-RENDER-TYPE': 'dialog'};

    headers['X-CSRFToken'] = dynamicforms.csrf_token;

    var dataType = 'html';

    $.ajax({
      type: method,
      url: url + 'confirm_create.html', //+ 'confirm_delete.html'
      data: data,
      dataType: dataType,
      headers: headers,
      traditional: true
    }).always(function (data, status, response) {
      dynamicforms.closeDialog($dlg);
      if (data && response.status && response.status === 201) {
        window.location.reload(true);
        return;
      }
      var newDialog = data && response.status && response.status === 200 ? $(data) : $(data.responseText);
      dynamicforms.showDialog(newDialog, 'page')
    });
  },

  submitForm: function submitForm($dlg, $form, refreshType, doneFunc) {
    return dynamicforms.makeSubmitForm($dlg, $form, refreshType, doneFunc);
  },

  progressCheckInterval: null,
  /**
   * Sets continuous checking on server about operation progress. After first check shows progress dialog if necessary.
   * @param progressDlgID: ID of progress dialog element - for custom progress dialogs.
   * @param timestamp: used for generating operation progress key under which progress is stored on server.
   * @param progressSettings: Progress dialog settings - for custom progress dialogs.
   */
  progressCheck:         function progressCheck(progressDlgID, timestamp, progressSettings) {
    if (!dynamicforms.progressDlgShown && dynamicforms.progressCheckInterval != null) {
      clearInterval(dynamicforms.progressCheckInterval);
      dynamicforms.progressCheckInterval = null;
    } else {
      $.ajax({url: '/dynamicforms/progress/', headers: {'X_DF_TIMESTAMP': timestamp}})
        .done(function (data, textStatus, jqXHR) {
          var pb_indet   = $('#df-progress-bar-indeterminate');
          var pb_det     = $('#df-progress-bar-determinate');
          var percent    = data['value'];
          var show_indet = percent == null;
          if (!show_indet) {
            if (dynamicforms.DYNAMICFORMS.jquery_ui) {
              pb_det.progressbar("value", parseInt(percent));
            } else {
              pb_det.css('width', percent + '%').attr('aria-valuenow', percent)
            }
          }
          pb_indet.toggle(show_indet);
          pb_det.toggle(!show_indet);

          if (dynamicforms.shouldShowProgressDlg && !dynamicforms.progressDlgShown) {
            dynamicforms.showProgressDlg(progressDlgID, progressSettings);
          }
        })
        .fail(function (jqXHR, textStatus, errorThrown) {
          if (dynamicforms.shouldShowProgressDlg && !dynamicforms.progressDlgShown) {
            dynamicforms.showProgressDlg(progressDlgID, progressSettings);
          }
        });
    }
  },
  /**
   * Starts continuous checking on operations progress. After first check progress dialog is opened if necessary
   * @param progressDlgID: ID of progress dialog element - for custom progress dialogs.
   * @param timestamp: used for generating operation progress key under which progress is stored on server.
   * @param progressSettings: Progress dialog settings - for custom progress dialogs.
   */
  startProgressChecker:  function startProgressChecker(progressDlgID, timestamp, progressSettings) {
    dynamicforms.progressCheck(progressDlgID, timestamp, progressSettings);
    dynamicforms.progressCheckInterval = setInterval(dynamicforms.progressCheck, 500, progressDlgID, timestamp, progressSettings);
  },
  shouldShowProgressDlg: false,
  progressDlgShown:      false,
  /**
   * Sets overlay so nothing can be clicked while operation last. If it last for more than 0.5 second it starts progress checker.
   * @param progressDlgID: ID of progress dialog element - for custom progress dialogs.
   * @param timestamp: used for generating operation progress key under which progress is stored on server.
   * @param progressSettings: Progress dialog settings - for custom progress dialogs.
   */
  setProgressDlg:        function setProgressDlg(progressDlgID, timestamp, progressSettings) {
    $('#df-overlay').css('z-index', 10000).show();
    dynamicforms.shouldShowProgressDlg = true;
    window.setTimeout(function () {
      if (dynamicforms.shouldShowProgressDlg) {
        dynamicforms.startProgressChecker(progressDlgID, timestamp, progressSettings);
      }
    }, 500);
  },
  /**
   * Closes progress dialog (if it is opened) and hides overlay that prevents clicks on other elements
   * @param progressDlgID: ID of progress dialog element - for custom progress dialogs.
   */
  closeProgressDlg:      function closeProgressDlg(progressDlgID) {
    dynamicforms.shouldShowProgressDlg = false
    if (dynamicforms.progressCheckInterval != null) {
      clearInterval(dynamicforms.progressCheckInterval);
      dynamicforms.progressCheckInterval = null;
    }

    $('#df-overlay').hide();
    if (dynamicforms.progressDlgShown) {
      dynamicforms.progressDlgShown = false;
      if (dynamicforms.DYNAMICFORMS.jquery_ui) {
        $('#' + progressDlgID).dialog('close');
      } else {
        $('#' + progressDlgID).modal('hide');
      }
    }
  },
  /**
   * Calls standard jQuery.ajax. Additionally it sets overlay that prevents clicks on other elements until operation completes
   * If operation lasts for more than 0.5 seconds progress dialog is shown.
   * @param options: Dict with options for ajax call ('ajax_setts'), and custom progress dialog ('progress_id', 'progress_sets')
   * @returns ajax promise with everything set for progress dialog: X_DF_TIMESTAMP header for progress checking and
   *  callbacks for closing progress dialog after operation completes
   */
  ajaxWithProgress:      function ajaxWithProgress(options) {
    var progressDlgID = options['progress_id'] !== undefined ? options['progress_id'] : 'df-progress-bar-container';
    var timestamp     = $.now()

    dynamicforms.setProgressDlg(progressDlgID, timestamp, options['progress_setts']);
    var closeProgressDialogFunc = function () {
      dynamicforms.closeProgressDlg(progressDlgID);
    };

    var ajaxSettings          = options['ajax_setts'] !== undefined ? options['ajax_setts'] : {};
    var headers               = ajaxSettings['headers'] !== undefined ? ajaxSettings['headers'] : {};
    headers['X_DF_TIMESTAMP'] = timestamp;
    ajaxSettings['headers'] = headers;

    return $.ajax(ajaxSettings).done(closeProgressDialogFunc).fail(closeProgressDialogFunc);
  },

  /**
   * Handles what happens when user says "Save data". Basically serialization, send to server, response to returned
   * status and values
   * @param $dlg: current dialog which will be updated with call results or closed on successful data store
   * @param $form: the edited form containing the data
   * @param refreshType: how to refresh the table
   * @param doneFunc: if specified, this function will be called on successful data send
   */
  makeSubmitForm: function makeSubmitForm($dlg, $form, refreshType, doneFunc) {
    var data = dynamicforms.getSerializedForm($form, 'final');
    var method = data['data-dynamicforms-method'] || 'POST';
    var headers = {'X-DF-RENDER-TYPE': 'dialog'};

    headers['X-CSRFToken'] = dynamicforms.csrf_token;

    var recordURL = dynamicforms.getRecordURL($form.attr('id'));
    var recordID = data.id ? data.id : false;

    var listId = dynamicforms.form_helpers.get($form.attr('id'), 'listID');

    var dataType = 'html';
    if (doneFunc == undefined) {
      doneFunc = function (data) {
        //var formContent = $dlg.find("form").html();
        dynamicforms.closeDialog($dlg);
        if (!recordID) {
          try {
            recordID = $(data).find('form.dynamicforms-form').find('input[name=\'id\']').val().trim();
            if (recordID == '')
              recordID = false;
          } catch (e) {
          }
        }
        dynamicforms.refreshList(recordURL, recordID, refreshType, listId);
      }
    } else
      dataType = 'json';  // This is a brazen assumption that custom done functions will only ever work with JSON

    dynamicforms.ajaxWithProgress({
                                    ajax_setts: {
                                      type:        method,
                                      url:         $form.attr("action"),
                                      data:        data,
                                      dataType:    dataType,
                                      headers:     headers,
                                      traditional: true,
                                    }
                                  })
      .done(doneFunc)
      .fail(function (xhr, status, error) {
        // TODO: this doesn't handle errors correctly: if return status is 400 something, it *might* be OK
        //  but if it's 500 something, dialog will be replaced by non-dialog code and displaying it will fail
        //  also for any authorization errors, CSRF, etc, it will again fail
        //  Try finding a <div class="dynamicforms-dialog"/> in there to see if you actually got a dialog
        dynamicforms.updateDialog($dlg, $(xhr.responseText), refreshType, listId);
      });
  },

  /**
   * Sets record specific url
   * @param formID: id of form
   * @param url: url for record
   */
  setRecordURL: function setRecordURL(formID, url) {
    dynamicforms.form_helpers.set(formID, 'recordURL', url);
  },

  /**
   * Gets record specific url
   * @param formID: id of form
   */
  getRecordURL: function getRecordURL(formID) {
    return dynamicforms.form_helpers.get(formID, 'recordURL');
  },

  isFunction: function isFunction(passedFunction) {
    return typeof (eval(passedFunction)) == "function";
  },

  /**
   * Gets refreshed html after add or edit
   * @param url: url for retrieving html
   * @param recordID: id of the data
   * @param refreshType: how to refresh the table
   * @param formID: id of form
   * @param deletion: if present delete action happened
   */
  refreshList: function refreshList(url, recordID, refreshType, formID, deletion) {
    if (refreshType == undefined || refreshType == 'record') {
      if (recordID) {
        var trSelector = "tr[data-id='" + recordID + "']";
        $rowToRefresh = $(trSelector); // Row to refresh
      }

      // If table will not change we wont even fetch new record
      if (!dynamicforms.isLinkNext(dynamicforms.df_tbl_pagination.get(formID, undefined).link_next) ||
        ($rowToRefresh != null && $rowToRefresh.length)) {
        var data = dynamicforms.filterData(formID, true);
        if (recordID)
          data.id = recordID
        dynamicforms.ajaxWithProgress({ajax_setts: {type: 'GET', url: url, data: data, dataType: 'html'}})
          .done(function (data) {
            dynamicforms.refreshRow(data, formID, recordID);
          })
          .fail(function (xhr, status, error) {
            // TODO: this doesn't handle errors correctly
          });
      }
    } else if (refreshType == 'table') {
      dynamicforms.refreshTable(formID, recordID);
      if (deletion == true) {
        dynamicforms.wasLastRowDeleted();
      }
    } else if (refreshType == 'page') {
      window.location.reload(true);
    } else if (typeof (refreshType) == 'function') {
      refreshType();
    } else if (refreshType.indexOf('redirect:') !== -1) {
      window.location.href = refreshType.split(':').pop();
    } else if (refreshType == 'no refresh') {
      // pass
    } else if (dynamicforms.isFunction(refreshType)) {
      // Change passed string to function call
      var functionString = refreshType + "();";
      var customFunction = new Function(functionString);
      customFunction();
    }
  },

  /**
   * Insert new row after the last row or insert first row
   * @param $newRow
   * @param listId
   */
  insertRow: function insertRow($newRow, listId) {
    if (listId !== undefined) {
      var $lastRow = $('#' + listId).find("tr[data-id]").last();
    } else {
      var $lastRow = $("tr[data-id]").last(); // Last row before adding new record
    }
    // Insert new row after the last row or insert first row
    if ($lastRow.length) {
      $newRow.insertAfter($lastRow);
    } else if (listId) {
      $('#' + listId).find("tr[data-title]").replaceWith($newRow);
    } else {
      $("table").find("tr[data-title]").replaceWith($newRow);
    }
  },

  /**
   * Replaces edited row
   * @param data
   * @param recordID: id of edited data
   * @param formID: id of form
   */
  refreshRow: function refreshRow(data, formID, recordID) {
    var tbl_pagination = dynamicforms.df_tbl_pagination.get(formID, undefined);

    var $rowToRefresh = null; // Row to refresh

    if (recordID) {
      var trSelector = "tr[data-id='" + recordID + "']";
      $rowToRefresh = $(trSelector); // Row to refresh
    }

    // Case when all records are loaded or edited record is loaded
    if (!dynamicforms.isLinkNext(tbl_pagination.link_next) || ($rowToRefresh != null && $rowToRefresh.length)) {
      var $htmlObject = $(data);

      if (recordID) {
        var $editedRow = $htmlObject.find(trSelector); // Edited record from ajax returned html
        if ($editedRow.length) {
          if ($rowToRefresh.length)
            $rowToRefresh.replaceWith($editedRow);
          else
            dynamicforms.insertRow($editedRow);
        }
      } else {
        var $newRow = $htmlObject.find("table").find("tr[data-id]").last(); // Added record from ajax returned html
        dynamicforms.insertRow($newRow);
      }
    }
    // else do nothing. Paginator will take care of new record when necessary
  },

  /**
   * Replaces entire table
   * @param formID: id of form object
   * @param recordID: id of edited data
   */
  refreshTable: function refreshTable(formID, recordID) {

    //If it is set to refresh table, we also want to see all the changes, that was made by other users.
    //We can only get them by reread data.
    dynamicforms.filterData(formID);
  },

  /**
   * Shows a dialog, attaches appropriate event handlers to buttons and gets initial data values
   * @param $dlg: dialog (parsed) html to show
   * @param refreshType: how to refresh the table after the dialog is finished with editing
   * @param listId: id of table element with records
   */
  showDialog: function showDialog($dlg, refreshType, listId) {
    //TODO: adjust hashURL
    $dlg = $dlg.find('.dynamicforms-dialog').length ?
      $dlg.find('.dynamicforms-dialog') : $dlg;
    $(document.body).append($dlg);
    var $form = $dlg.find('.dynamicforms-form');
    dynamicforms.form_helpers.set($form.attr('id'), 'listID', listId);

    $($dlg).on('hidden.bs.modal', function () {
      // dialog removes itself from DOM hierarchy
      $dlg.remove();

      dynamicforms.removeFormDeclarations($form);
    });

    // Let's get initial field values from the form
    dynamicforms.serializeForm($form, 'final');

    var saveId = '#save-' + $form.attr('id');
    $(saveId).on('click', function () {
      dynamicforms.submitForm($dlg, $form, refreshType);
    });
    // And show the dialog
    if (dynamicforms.DYNAMICFORMS.jquery_ui)
      $dlg.dialog('open')
    else {
      $dlg.on('hidden.bs.modal', function () {
        $dlg.remove();
        if ($dlg.showNewAfterHide)
          dynamicforms.showDialog($dlg.showNewAfterHide, refreshType, listId);
      });
      $dlg.modal();
    }
  },

  /**
   * Updates the current dialog with errors.
   * @param $dlg: dialog to update
   * @param $newDlg: new dialog with errors in form
   */
  updateDialog: function updateDialog($dlg, $newDlg) {
    $newDlg = $newDlg.find('.dynamicforms-dialog').length ?
      $newDlg.find('.dynamicforms-dialog') : $newDlg;
    $dlg.showNewAfterHide = $newDlg;  // Old dialog will show the new one after being hidden
    dynamicforms.closeDialog($dlg);
    /*
    // Replace current form with new form containing errors
    var newForm     = $newDlg.find("form");
    var currentForm = $dlg.find("form");
    currentForm.replaceWith(newForm);

    // Set updated form's id to dialog id
    var dlgId       = $dlg.attr("id").split("-").slice(1).join("-");
    var updatedForm = $dlg.find("form");
    updatedForm.attr("id", dlgId);
    */
  },

  /**
   * Closes the current dialog
   * TODO: adjust hashURL
   * @param $dlg: dialog to close
   * @param refreshType: how to refresh the table after the dialog is finished with editing
   * @param listId: id of table element with records
   */
  closeDialog: function closeDialog($dlg, refreshType, listId) {
    if (!dynamicforms.DYNAMICFORMS.jquery_ui) {
      $dlg.modal('hide');
    } else {
      $dlg.remove();
      if ($dlg.showNewAfterHide) {
        dynamicforms.showDialog($dlg.showNewAfterHide, refreshType, listId);
      }
    }
  },

  /**
   * Handles what should happen when user clicks to edit a record
   * @param recordURL: url to call to get data / html for the record / dialog
   * @param refreshType: how to refresh the table
   * @param listId: id of table element with records
   */
  editRow: function editRow(recordURL, refreshType, listId) {
    if (dynamicforms.DYNAMICFORMS.edit_in_dialog) {
      dynamicforms.ajaxWithProgress({
                                      ajax_setts: {
                                        url:     recordURL,
                                        headers: {'X-DF-RENDER-TYPE': 'dialog'},
                                      }
                                    })
        .done(function (dialogHTML) {
          dynamicforms.showDialog($(dialogHTML), refreshType, listId);
        })
        .fail(function (xhr, status, error) {
          dynamicforms.showDialog($(xhr.responseText), 'no-refresh', listId);
        });
    } else
      window.location = recordURL;
  },

  showReadOnlyRow: function showReadOnlyRow(recordURL, listId) {
    if (dynamicforms.DYNAMICFORMS.edit_in_dialog) {
      $.ajax({
        url: recordURL,
        headers: {'X-DF-RENDER-TYPE': 'dialog'},
      })
        .done(function (dialogHTML) {
          dynamicforms.showDialog($(dialogHTML), 'no refresh', listId);
        })
        .fail(function (xhr, status, error) {
          dynamicforms.showDialog($(xhr.responseText), 'no-refresh', listId);
        });
    } else
      window.location = recordURL;
  },

  /**
   * Removes table row after deletion
   *
   * @param recordID: data-id attribute of table row
   */
  removeRow: function removeRow(recordID, listId) {
    var $trToRemove = $('[id*=' + listId + ']').find("tr[data-id='" + recordID + "']");
    $trToRemove.remove();
    dynamicforms.wasLastRowDeleted(listId);
  },

  /**
   * Checks if last row was deleted and appends "No data" element if so
   */
  wasLastRowDeleted: function wasLastRowDeleted(listId) {
    var mainSelector = $('[id*=' + listId + ']');
    var $leftTrsCount = mainSelector.find("tr[data-id]").length;
    if ($leftTrsCount == 0) {
      // Count how many lines should "No data" element span
      var colCount = mainSelector.find("th").length;
      var noDataElement = "<tr data-title='NoData'><td colspan=" + colCount + " style='text-align: center'>No data</td></tr>";
      mainSelector.find("tbody").first().append(noDataElement);
    }
  },

  deleteRowWithConfirmation: function deleteRowWithConfirmation(recordURL, recordID, refreshType, listId) {
    $.ajax({
      url: recordURL + 'confirm_delete.html',
      method: 'GET',
      data: {
        record_id: recordID,
        list_id: listId
      },
      dataType: 'html',
      headers: {'X-CSRFToken': dynamicforms.csrf_token}
    }).always(function (dialog) {
      //show dialog
      var confirmDialog = $(dialog.responseText ? dialog.responseText : dialog);
      dynamicforms.showDialog(confirmDialog);
      var confirmButton = $("button[class*='" + recordID + '_' + listId + "']");
      if (confirmButton.length) {
        confirmButton.on('click', function (e) {
          dynamicforms.makeDeleteRow(recordURL, recordID, refreshType, listId, confirmDialog);
        });
      }
    });
  },

  deleteRow: function deleteRow(recordURL, recordID, refreshType, listId) {
    dynamicforms.makeDeleteRow(recordURL, recordID, refreshType, listId);
  },

  /**
   * Handles what should happen when user clicks to delete a record
   * @param recordURL: url to call to get data / html for the record / dialog
   * @param recordID: pk of row to be deleted
   * @param refreshType: how to refresh the table
   * @param listId: id of table element with records
   * @param dialog
   */
  makeDeleteRow: function makeDeleteRow(recordURL, recordID, refreshType, listId, dialog) {
    dynamicforms.ajaxWithProgress({
                                    ajax_setts: {
                                      url:     recordURL + '?format=html',
                                      method:  'DELETE',
                                      headers: {'X-CSRFToken': dynamicforms.csrf_token},
                                    }
                                  })
      .done(function (dialogHTML) {
        console.log('Record successfully deleted.');
        if (dialog !== undefined) {
          dynamicforms.closeDialog(dialog);
        }
        //  TODO: make a proper notification
        // Remove row after deletion
        if (refreshType == undefined || refreshType == 'record') {
          dynamicforms.removeRow(recordID, listId);
        } else if (refreshType == 'table') {
          var recordURL = dynamicforms.getRecordURL(listId);
          // var formId    = $('table')[0].getAttribute('id').replace('list-', '');
          dynamicforms.refreshList(recordURL, true, refreshType, listId, true);
        } else if (refreshType == 'page') {
          window.location.reload(true);
        } else if (typeof (refreshType) == 'function') {
          refreshType();
        } else if (refreshType.indexOf('redirect') !== -1) {
          var redirectUrl = refreshType.split(':').pop();
          window.location.href = redirectUrl;
        } else if (refreshType == 'no refresh') {
          // pass
        } else if (dynamicforms.isFunction(refreshType)) {
          // Change passed string to function call
          var functionString = refreshType + "();";
          var customFunction = new Function(functionString);
          customFunction();
        }
      })
      .fail(function (xhr, status, error) {
        if (dialog !== undefined) {
          dynamicforms.updateDialog(
            dialog, $(xhr.responseText));
        } else {
          dynamicforms.showDialog($(xhr.responseText))
        }
      });
  },

  /**
   * Handles what should happen when user clicks "Add new" button
   * Right now newRow doesn't do anything distinct, so let's just call editRow
   *
   * @param recordURL: url to call to get data / html for the record / dialog
   * @param refreshType: how to refresh the table
   * @param listId: id of table element with records
   * @returns {*|void}
   */
  newRow: function newRow(recordURL, refreshType, listId) {
    return dynamicforms.editRow(recordURL, refreshType, listId);
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
    var formID = $form.attr('id');
    var form_data = dynamicforms.form_helpers.getOrCreate(formID, final, {});
    $.each(dynamicforms.form_helpers.get(formID, 'fields'), function (fieldID, field) {
      form_data[field.name] = field.getValue(field.$field);
    });
    var fld = $form.find('input[name="data-dynamicforms-method"]');
    if (fld.length == 1)
      form_data['data-dynamicforms-method'] = fld.val();
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
  field_helpers: new TLD(),

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

    var field = dynamicforms.field_helpers.get(fieldID),
      $field = field.$field,
      $form = field.$form,
      newValue = field.getValue($field),
      oldValue,
      newFormData = dynamicforms.getSerializedFormFinal($form, final),
      oldFormData = {};

    // Copy the current form values to "old" object and adjust the current values with the change
    $.extend(true, oldFormData, newFormData);
    var field_name = $field.attr('name');
    oldValue = newFormData[field_name];
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
      var field = dynamicforms.field_helpers.get(fieldID),
        $field = field.$field,
        field_name = $field.attr('name'),
        $form = field.$form,
        formID = $form.attr('id');

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
      var $form = $('#' + formID),
        // Get new field values & visibility
        oldFormData = changedHelper.get(formID, 'old'),
        newFormData = dynamicforms.getSerializedFormFinal($form, final),
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
    var field = dynamicforms.field_helpers.getOrCreate(fieldID, undefined, {});
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
    var field = dynamicforms.field_helpers.getOrCreate(fieldID, undefined, {});
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
      field.$form = $('#' + formID);
      field.name = field.$field.attr('name');
    }
    var form_fields = dynamicforms.form_helpers.getOrCreate(formID, 'fields', {});
    form_fields[fieldID] = field;
    var field_ids = dynamicforms.form_helpers.getOrCreate(formID, 'field_ids', {});
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
    if ($field.attr('type') == 'checkbox')
      return $field.is(':checked');
    return $field.val();
  },

  /**
   * "Standard" function for setting an input's value. Any special cases will be handled in custom functions
   *
   * @param field: id or jQuery object of the field
   * @param value: new value to set
   * @param select2_ajax_option_text: label of selected option to be added to select2 options list. Only use when select2 is ajax
   */
  fieldSetValue: function fieldSetValue(field, value, select2_ajax_option_text) {
    var $field = field instanceof jQuery ? field : dynamicforms.field_helpers.get(field, '$field');
    if ($field.attr('type') == 'checkbox')
      return $field.prop('checked', value);
    if ($field.data('select2')) {
      if ($field.data('select2').options.options.ajax) {
        var opt = $('<option value="' + value + '"></option>').text(select2_ajax_option_text);
        $field.append(opt);
      }
      $field.val(value);
      $field.trigger('change');
      return;
    }
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
    var $field = field instanceof jQuery ? field : dynamicforms.field_helpers.get(field, '$field');
    var fieldID = $field.attr('id');
    var $hide = $field.parents('#container-' + fieldID);
    var $hideParent = $hide.parents('[data-hide-with-field]');
    if ($hideParent.length > 0)
      $hide = $hideParent;
    $hide.toggle(visible);
  },

  /**
   * "Standard" function for checking whether an input's is visible. Any special cases will be handled in custom
   * functions
   *
   * @param field: id or jQuery object of the field
   * @return: boolean true for visible, false for hidden
   */
  fieldIsVisible: function fieldIsVisible(field) {
    var $field = field instanceof jQuery ? field : dynamicforms.field_helpers.get(field, '$field');
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

  /**
   * Pagination init for table.
   * Remembers url for loading next page and sets trigger element for start of loading next page
   * When trigger element is visible on screen loading starts
   *
   * @param formID: id of table object
   * @param link_next: url with cursor definition for loading next page
   * @param link_prev: url with cursor definition for loading previous page
   */
  paginatorInitTable: function paginatorInitTable(formID, link_next, link_prev) {
    dynamicforms.df_tbl_pagination.set(formID, 'link_next', link_next);
    if (dynamicforms.isLinkNext(link_next)) {
      var table_rows = $("#list-" + formID).find("tbody:first").find("tr");
      dynamicforms.df_tbl_pagination.set(formID, 'trigger_element', table_rows[0]);
    }
  },

  /**
   * Checks if loading of next page should start
   * If trigger element is visible on screen
   *
   * @param formID: id of table object
   */
  paginatorCheckGetNextPage: function paginatorCheckGetNextPage(formID) {
    var trigger_element = dynamicforms.df_tbl_pagination.get(formID, 'trigger_element');

    if (trigger_element != null) {
      var rect = trigger_element.getBoundingClientRect();

      if (rect.height != 0 && rect.width != 0 && rect.top <= (window.innerHeight || document.documentElement.clientHeight))
        dynamicforms.paginatorGetNextPage(formID, '');

      //TODO: Check both methods of determining whether control item is showing (unit tests for one and the other?)
      // problem with unit tests is that automated ones only run in Firefox

      //   var top_of_element    = trigger_element.offset().top;
      //   var bottom_of_element = top_of_element + trigger_element.outerHeight();
      //   var top_of_screen     = $(window).scrollTop();
      //   var bottom_of_screen  = top_of_screen + window.innerHeight;
      //
      //   if (bottom_of_screen > top_of_element) {
      //     dynamicforms.paginatorGetNextPage(formID);
      //   }
    }
  },

  /**
   * Calls server to get next page. When filter is given all current records will be deleted and only new ones will be
   * shown
   *
   * @param formID: id of table object
   * @param filter: filter params
   */
  paginatorGetNextPage: function paginatorGetNextPage(formID, filter) {
    var tbl_pagination = dynamicforms.df_tbl_pagination.get(formID, undefined);
    var link_next = '';
    if (filter.length) {
      link_next = dynamicforms.form_helpers.get(formID, 'reverseRowURL');
      if (link_next == undefined)
        link_next = window.location.origin + window.location.pathname
      if (filter != 'nofilter')
        link_next += '?' + filter;
    } else
      link_next = tbl_pagination.link_next;

    /*console.log(link_next);
    console.log(tbl_pagination.last_link_next);
    console.log(filter.length);*/

    if (dynamicforms.isLinkNext(link_next) && (link_next != tbl_pagination.last_link_next || filter.length)) {
      tbl_pagination.last_link_next = link_next;

      var table = $("#list-" + formID).find("tbody:first");
      if (filter.length) {
        dynamicforms.df_tbl_pagination.set(formID, 'trigger_element', null);
        table.find('tr').remove();
      }
      $("#loading-" + formID).show();
      //TODO: Remember sequence number... if data that comes back has other than last sequence number than just ignore it #114
      $.ajax({
        type: 'GET',
        headers: {'X-CSRFToken': dynamicforms.csrf_token, 'X-DF-RENDER-TYPE': 'table rows'},
        url: link_next,
      }).done(function (data) {

        data = $(data).filter("tr");
        tbl_pagination.link_next = data[0].getAttribute('data-next');

        if (data[0].getAttribute("data-title") != "NoData") {
          // remove elements, that are already shown - in case of new data insertion and order different than id.
          for (var i = data.length - 1; i >= 0; i--) {
            var data_id = data[i].getAttribute('data-id');
            if (data_id == null || table.find("tr[data-id='" + data_id + "']").length > 0)
              data.splice(i, 1);
          }
        } else if (table.find("tr").length > 0)
          data = [];

        //TODO: If NoData comes back - I reached the end of dataset... do I even attempt further reading?
        //  for log-type datasets where new data is frequently inserted, it might be useful.
        $("#loading-" + formID).hide();
        if (data.length > 0) {
          table.append(data);
          tbl_pagination.trigger_element = data[0];
          if (table.find("tr[data-title=NoData]").length > 0) {
            table.find("tr[data-title=NoData]").remove()
          }
        }
        dynamicforms.paginatorCheckGetNextPage(formID);
      }).fail(function (xhr, status, error) {
        $("#loading-" + formID).hide();
        console.log('Pagination failed.', xhr, status, error);
        // TODO: what if the server returns an error? Do we continue with pagination? (Task #100)
      });
    }
  },

  /**
   * Goes through all tables that uses pagination and calls paginatorCheckGetNextPage function for them
   */
  paginatorCheckGetNextPageAll: function paginatorCheckGetNextPageAll() {
    for (var formID in dynamicforms.df_tbl_pagination.storage)
      dynamicforms.paginatorCheckGetNextPage(formID);
  },

  /**
   * Registers filtering data on enter press in filter fields
   *
   * @param formID: id of table object
   * @param reverseRowURL: url for getting filtered data
   */
  registerFilterRowKeypress: function registerFilterRowKeypress(formID, reverseRowURL) {
    dynamicforms.form_helpers.set(formID, 'reverseRowURL', reverseRowURL);
    $($("#list-" + formID).find("tr.dynamicforms-filterrow")[0]).keypress(function (e) {
      if (e.which == 13) {
        dynamicforms.filterData(formID);
      }
    })
  },

  /**
   * Prepares filter string and calls server to get filtered data
   *
   * @param formID: id of table object
   * @param returnDict: set to true if only filter data should be returned
   */
  filterData: function filterData(formID, returnDict) {
    if (returnDict == undefined)
      returnDict = false;
    var filter = {};
    $("#list-" + formID).find(".dynamicforms-filterrow th").each(function (index) {

      var element = $(this).find("[name='" + $(this).attr("data-name") + "']");

      if (element.attr('type') == 'checkbox') {
        if (element.is(':checked'))
          filter[element.attr("name")] = true;
        else if (!element.is('[readonly]'))
          filter[element.attr("name")] = false;
      } else if (element.val() != null && element.val().length) {
        if (element.is('select') && element.is("[multiple]")) {
          var delimiter = element.attr('value_delimiter');
          if (delimiter == undefined)
            delimiter = ',';
          filter[element.attr("name")] = element.val().join(delimiter);
        } else
          filter[element.attr("name")] = element.val();
      }
    });
    if (returnDict)
      return filter;
    filter = jQuery.param(filter);
    if (!filter.length)
      filter = 'nofilter';
    dynamicforms.paginatorGetNextPage(formID, filter);
  },

  /**
   * "Standard" function which is called after filter button in header is clicked.
   * It finds id of table object and calls filterData function with it.
   *
   * @param event: OnClick event from which we get id of table object
   */
  defaultFilter: function defaultFilter(event) {
    // And show the dialog
    var formId = (dynamicforms.DYNAMICFORMS.jquery_ui) ?
      $(event.currentTarget).parents('div.accordion').find('div.ui-accordion-content').find('table')[0].getAttribute('id').replace('list-', '') :
      $(event.currentTarget).parents('div.card').find('div.card-body').find('table')[0].getAttribute('id').replace('list-', '');
    dynamicforms.filterData(formId);
  },

  isLinkNext: function isLinkNext(link_next) {
    return link_next != null && link_next != undefined && link_next != '' && link_next != "None";
  },

  select2Opening: function select2Opening(evt, $select2, fnc) {
    if ($select2.data('unselecting')) {
      $select2.removeData('unselecting');
      evt.preventDefault();
    } else if (fnc != null)
      fnc(evt, $select2);
  },

  select2Unselecting: function select2Unselecting($select2) {
    $select2.data('unselecting', true);
  }

};

$(document).ready(function () {
  // Let's get initial field values from the forms that are on-page already
  // TODO: Is this jQuery-specific? Will vue.js page also contain some kind of initializer or will everything just work?
  // TODO: also might be prudent to just move this to base_form.html. we already process dialogs separately...
  $('.dynamicforms-form').each(function (idx, form) {
    dynamicforms.serializeForm($(form), 'final');
  });
  window.setInterval(dynamicforms.paginatorCheckGetNextPageAll, 100);

  var $overlay = $("<div id='df-overlay' style='position: fixed; display: none; width: 100%; height: 100%; top: 0; " +
                     "left: 0; right: 0; bottom: 0; cursor: pointer; z-index: auto'></div>");
  $("body").append($overlay);
})
