# Notice to users of this library

## This library is no longer free software.

With 0.80.0 the library has gained a development partner that will doubtless raise it to new heights.

The LICENSE has been modified to a proprietary one with restrictions, so please be mindful of conditions.

The library is thus deprecated and in maintenance mode only.

# What is DyF?

DyF wants to eliminate HTML form boilerplate for generic tables & forms. Specifying a single DRF Serializer /
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

## Why DyF

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

