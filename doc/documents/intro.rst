What is DynamicForms?
=====================

DynamicForms performs all the visualisation & data entry of your DRF Serializers & ViewSets and adds some candy of its
own: It is a `django <https://www.djangoproject.com/>`_ library that gives you the power of dynamically-shown form
fields, auto-filled default values, dynamic record loading and similar candy with little effort. To put it differently:
once defined, a particular ViewSet / Serializer can be rendered in multiple ways allowing you to perform viewing and
authoring operations on the data in question.

It is based on `django-rest-framework <http://www.django-rest-framework.org/>`_

Why DynamicForms
----------------

* Turn your rest-framework ViewSets into HTML forms
* Powerful HTML based CRUD

   * Support for fetching “new” records, both in JSON or in HTML
   * Render to HTML, dialog html or from your own template
   * Render form (embedded or dialog) or table, depending on situation
   * Easily add actions and place the buttons to execute them anywhere you like

* Clear separation of list & dialog templates
* Dynamic loading of additional records for table views
* Easy implementation of simple filtering
* Action items, declared globally, placed where you need them
* Custom templates whenever & wherever you want them
* Render to full html or work with dialogs within same page or both at the same time
* Each form and field have a unique HTML id for easy finding & manipulation
* Bootstrap 3 & 4 templates, jQuery UI coming soon, easy to make your own or enhance existing
* Support for form validation, will show errors even if they are not tied to a field
* Convenient JS functions for easier action scripting
* Progress dialog for long lasting ajax operations
