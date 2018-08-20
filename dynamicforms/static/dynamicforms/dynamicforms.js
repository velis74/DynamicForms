$.fn.serializeForm = function(fieldNamePrefix, handlers, returnDict) {
  /**
   * serializes the given form into a JS object. Tries to keep all input fields, including unselected checkboxes
   * and disabled fields
   * @param fieldNamePrefix: fields in the form have a prefix in their name we don't want in the object
   * @param handlers: dict of transformation functions in the form field_name: function to transform the value
   * @param returnDict: true if you want the function to return a dictionary of form.id: serialized form
   * @return: JS object with form data
   */
  fieldNamePrefix = fieldNamePrefix == undefined ? '' : fieldNamePrefix;
  handlers = handlers == undefined ? {} : handlers;
  returnDict = returnDict == undefined ? false : returnDict;

  var res_d = {}
  var res = $.map(this, function(item) {
    var o = {},
        $form = $(item),
        storeValue = function(name, value) {
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
        disabled = $(this).find(':input:disabled').removeAttr('disabled');

    $.each($form.serializeArray(), function() {
      var name = this.name.replace(fieldNamePrefix, ''),
          value = this.value;
      storeValue(name, value);
    });
    disabled.attr('disabled', true);
    $form.find('input:checkbox').each(function() {
      var name = this.name.replace(fieldNamePrefix, '');
      if (name in o) delete o[name];
    });
    $form.find('input:checkbox').each(function() {
      var name = this.name.replace(fieldNamePrefix, ''),
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

$.fn.deserializeForm = function(data, fieldNamePrefix, handlers) {
  fieldNamePrefix = fieldNamePrefix == undefined ? '' : fieldNamePrefix;
  handlers = handlers == undefined ? {} : handlers;

  var setValue = function($inp, value) {
    if ($inp.length > 0) {
      var handler = handlers[$inp[0].name.substring(fieldNamePrefix.length)] || {};
      if (handler.value != undefined)
        value = handler.value($inp, value);

      if ($inp.is(":checkbox"))
        $inp.prop("checked", value);
      else
        $inp.val(value);

      if ($inp.is(':ui-selectmenu')) {
        $inp.selectmenu("refresh");
        if ($inp.selectmenu("option", "change") != undefined)
          $inp.selectmenu("option", "change")();
      }
      if ($inp.data("select2") != undefined)
        $inp.trigger("change");

      if (handler.copy != undefined)
        setValue(handler.copy, value);
    }
  };

  this.each(function() {
    var $form = $(this);
    $.each(data, function(key, value) {
      setValue($form.find("[name='%s']".replace(/%s/, fieldNamePrefix + key)), value);
    });
  });
};

dynamicforms = {
  a: 'as'
};

$(document).ready(function() {
  // Let's get initial field values from the forms that are on-page already
  // TODO: Is this jQuery-specific? Will vue.js page also contain some kind of initializer or will everything just work?
  $.extend(dynamicforms, $('.dynamicforms-form').serializeForm(undefined, undefined, true));
  //console.log(dynamicforms);
})