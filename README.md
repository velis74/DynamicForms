# Notice to users of this library

Releases 0.50.x and 0.70.x are interim releases with which we prepare the stage for 1.x release.

0.50.x moves all "existing" code to `dynamicforms_legacy` module. If you weren't following vue
development branches, you will need to change all imports in python to this "new" module.

This is done to keep legacy code still running as existing code is transitioned to vue-based approach. Unless there is
significant interest, we will remove this module with 1.x release.

0.70.x re-introduces `dynamicforms` module, but this time refactored to only provide .componentdef OPTIONS +
payload data responses needed by the vue front-end library. This will hopefully be refactored to be more OpenAPI
compatible. The new primary branch is now `main`.

HTML renderers will no longer be supported and have been removed from the "new" dynamicforms module. It was too slow
and required too many hacks to remain viable. So we moved to Vue. The components in 0.70 will be vue3, vuetify3, vite
and typescript-compatible. We're in final stages of adapting to the new stack. Some inputs and some table functionality
isn't working yet.

We're keeping the Bootstrap stubs too, but not actively developing to support seamless selection of the two frameworks.
If there is interest to support CSS frameworks other than Vuetify, pull requests welcome. Hopefully the stubs should
point the way on how to do it.

Migration path is thus:

- Upgrade to dynamicforms \>= 0.50.3
- replace all dynamicforms imports with dynamicforms_legacy
- because of the rename, there is a bit of work required in settings.py so that Django can find the templates and
  filters:

      ``` python
      from dynamicforms_legacy import __file__ as DYNAMICFORMS_BASEDIR_FILE
      DYNAMICFORMS_BASEDIR = os.path.dirname(DYNAMICFORMS_BASEDIR_FILE)
      ...
      INSTALLED_APPS = [
        ...
        'dynamicforms_legacy'

      TEMPLATES = [
         ...
              'DIRS': [
                  os.path.join(DYNAMICFORMS_BASEDIR, 'templates'),
         ...
              'OPTIONS': {
         ...
                  'libraries': {
                      'dynamicforms': 'dynamicforms_legacy.templatetags.dynamicforms',
                  }
      STATICFILES_DIRS = [
          ...
          os.path.join(DYNAMICFORMS_BASEDIR, 'static'),
      ]
      ```
- replace any javascript dynamicforms progress calls with progress-legacy
- all other javascript code remains the same (including the dynamicforms object with support functions)
- check that everything still works
- Upgrade dynamicforms to \>= 0.70.1
- Start migration to Vue front-end and the new backend

# What is DynamicForms?

DynamicForms wants to eliminate HTML form boilerplate for generic tables & forms. Specifying a single DRF Serializer /
ViewSet and possibly desired form layout instantly provides both HTML renders and JSON renders (and anything else DRF
supports) keeping you free to implement your project.

There are two parts to DanymicForms:

- Django / DRF extensions providing the JSON definitions for on-screen objects
- HTML / Javascript component library providing the visualisation

It performs all the visualisation & data entry of your DRF Serializers & ViewSets and adds some candy of its own: It is
a [django](https://www.djangoproject.com/) library that gives you the power of dynamically-shown form fields,
autofilled default values, dynamic record loading and similar candy with little effort. To put it differently: once
defined, a particular ViewSet / Serializer can be rendered in multiple ways allowing you to perform viewing and
authoring operations on the data in question.

It is based on
[django-rest-framework](http://www.django-rest-framework.org/)

Documentation [on readthedocs](https://dynamicforms.readthedocs.io/)

## Why DynamicForms

- Turn your rest-framework ViewSets into HTML tables & forms
- Powerful HTML based CRUD
    - Support for fetching "new" records
    - Render to table, form or dialog, with plenty of customisation options
    - Full nested data support
    - Dynamically display & hide fields based on other fields' values
    - Easily add actions and place the buttons to execute them anywhere you like
- Clear separation of list & dialog templates
- Dynamic loading of additional records for table views supported by infinite scroll
- Responsive tables (multiple table layouts for various screen widths)
- Easy implementation of filtering
- Action items, declared globally, placed where you need them
- Custom templates whenever & wherever you want them
- Support for form validation, will show errors even if they are not tied to a field
- Progress dialog for long lasting ajax operations

