Templates
=========

Design
------

Templates are organised in template packs for different UI libraries. DynamicForms provides template packs for
bootstrap v3 / v4 with jQuery UI templates pending.

.. code-block:: python
   :name: settings.py

   DYNAMICFORMS_TEMPLATE = 'dynamicforms/bootstrap'


Main template is base.html. HTML and its head tag are defined here. There are three blocks, that can be used in deriving
templates:

*	title: For defining the title of HTML.
*	head_extra: to add additional definitions or includes in head tag.
*	body: to insert the body of HTML.

Head tag includes base_includes.html (for bootstrap we have base_includes_v3.html and base_includes_v4.html). Here
all the libraries that are needed for dynamic forms to work are included.

Base_list.html can be used for rendering Viewset in list mode. It shows all records with values or »No data« label if
there is no data. When user clicks on record (only if default CRUD functionlity is enabled), this record is shown in
form (modal dialog or separate page) and can be edited there.

Base_form.html can be used for rendering ViewSet in form mode. It shows one record, and if crud is enabled in Viewset,
it can also be edited.

Form can be shown as modal dialog. For that template which is defined in settings.py - modal_dialog_rest_template is used.
When using bootstrap v4 default template is modal_dialog_v4.html.

Template for dialog should have first div with »dynamicforms-dialog« class. JS searches for that to see if the response
from server was a dialog or other error message.

For showing fields base template the one that is defined in settings.py -field_base_template. For bootstrap v4 default
template is field/base_field_v4.html. That template makes sure that the label, input, errors and help text is correctly
shown. This template is extracted by templates that are used for rendering individual field types (e.g.: checkbox.html,
input.html, radio.html, etc.)

Some additional functionalities are not supported with jQuery templates (e.g. copy to clipboard on Select 2 fields).

.. todo:: explain how to change template to another one