Contributor's documentation
===========================

Code style guide
----------------

Python
******

* PEP 8  with the following exceptions:
   * E5 - line length: use 120 character limit
   * E722 - (bare excepts) too broad
   * E731 - do not assign a lambda expression, use a def

   While we grudgingly accept rules like E221 (multiple spaces before operator), the above two are simply going too far
   and we sometimes reluctantly, but intentionally break them. Our rationale (for breaking them):

   * E722 - sometimes you just need code that doesn't except. Better to do nothing than to break. Depending on
      importance, such except blocks might have some sort of report added so that the programmer knows something
      happened.
   * E731 - when you have tons of tiny declarations, using a lambda means 1 line of code while using def means 3 lines
      or more

JavaScript
**********

This one is a lot tougher. It is a work in progress, but I hope we (internally) sort it out before you (the would-be
contributor) ever see this.

While we would **love** to adopt one of the popular style guides, we so far haven't managed to. No time doing research
and finding a style that doesn't break what we feel is important. Suggestions based on the following welcome:

* Pure EcmaScript 5.1 or EcmaScript 6

   * No code conversion tools: the code in the repository runs straight out of the box

* Semicolons mandatory
* 2 spaces indentation
* use == instead of ===: type coercion is helpful


The above straight out eliminates:

* `standard <https://github.com/standard/standard>`_

These remain in play

* `Airbnb <https://github.com/airbnb/javascript>`_
* `Google <https://google.github.io/styleguide/jsguide.html>`_
* `Idiomatic <https://github.com/rwaldron/idiomatic.js/>`_
* `jQuery <https://contribute.jquery.org/style-guide/js/>`_

Documentation
*************

* 120 character line length limit

dynamicforms_dev package
------------------------

This package contains a helpful code generator so that we don't have to copy-paste an interface change to 35-ish
different fields every time we add a cool new feature.

Generate fields
***************

The helpful code generator. :)

This command is used for generating `fields/__init__.py`.

1. First it finds all the field types from `rest_framework/fields.py`
2. Then take care of all the imports that are needed for `fields/__init__.py`.
3. Then it finds all the parameters, that can be used to set up field and includes them in `__init__` functions for
   individual field. This we have done so that code completion might work better in your IDE. In the end it adds another
   parameter \*\*kw which makes sure that any new parameters added in newer versions of DRF don't break the
   functionality.


.. code-block:: bash

   python manage.py generate_fields


creating your own template pack
-------------------------------

Context variables referring to template packs
*********************************************

These variables will be set in a :py:class:`dynamicforms.viewsets.ModelViewSet` class declaration.

.. py:data:: crud_form: True | False

   If set, template pack is expected to render HTML that will allow user to edit the presented data.
