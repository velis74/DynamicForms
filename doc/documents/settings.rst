DynamicForms Configuration
==========================

Like much of django-based libraries, DynamicForms is also configured from
`settings.py <https://docs.djangoproject.com/en/dev/ref/settings/>`_.


Activate DynamicForms in DRF
----------------------------

In order to activate DynamicFroms, you need to add its renderers to DRF configuration, like so:

.. code-block:: python

   REST_FRAMEWORK = {
       'DEFAULT_RENDERER_CLASSES': (
           'rest_framework.renderers.JSONRenderer',
           'rest_framework.renderers.BrowsableAPIRenderer',
           'dynamicforms.renderers.TemplateHTMLRenderer',
       )
   }

DRF will remain in control of JSON & Browseable API renderers while we activate DynamicForms for `.html` renders.

.. note:: The DRF renderers are taken from default DRF configuration. If it should change, feel free to change the
   setting as well.

List of settings
----------------

.. py:data:: DYNAMICFORMS_TEMPLATE

   Specifies the template pack that dynamicforms will use for rendering HTML forms, e.g. 'bootstrap', 'jQuery UI', etc.

.. py:data:: DYNAMICFORMS_TEMPLATE_OPTIONS

   Offers a chance to do some things in the template pack differently. It can be used for anything from choosing version
   of the underlying framework (bootstrap 3 vs 4) or rendering various subsections differently (e.g. horizontally
   aligned form labels vs vertically aligned ones or editing record in modal dialog vs editing in new page).

   Supported bootstrap versions are v3 and v4.

.. py:data:: DYNAMICFORMS_MODAL_DIALOG

   Name of template for modal dialog. It will be appended any version modifiers, i.e. bootstrap version postfix if
   bootstrap template pack.


List of generated constants
---------------------------

These are constants, generated from settings. They are shortcuts for quick use in templates and are specific to the
chosen template pack.


.. py:data:: BSVER_INCLUDES

   Path to template for :samp:`<html><head>` tag JS & CSS includes, necessary for the chosen template pack.

.. py:data:: BSVER_FIELD_TEMPLATE

   Path to base template for fields.

.. py:data:: BSVER_MODAL

   Path to template for modal dialog
