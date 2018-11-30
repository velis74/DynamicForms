Contributor's documentation
===========================

Code style guide
----------------

Python
******

Rules are made to be broken, so...

**PEP 8  with the following exceptions:**

* E5 - line length: use 120 character limit
* E722 - (bare excepts) too broad
* E731 - do not assign a lambda expression, use a def

Our rationale for breaking E722 & E731:

* E722 - sometimes you just need code that doesn't except. Better to do nothing than to break. Depending on
  importance, such except blocks might have some sort of report added so that the programmer knows something
  happened.
* E731 - when you have tons of tiny declarations, using a lambda means 1 line of code while using def means 3 lines
  or more

Note that E722 & E731 may not be broken at all in this project. It's just that our linters have these checks
disabled on principle. Apologies... but no regrets.

JavaScript
**********

This one is a lot tougher. It is a work in progress, but I hope we (internally) sort it out before you (the would-be
contributor) ever see this.

While we would **love** to adopt one of the popular style guides, we so far haven't managed to. No time doing research
and finding a style that doesn't break what we feel is important. Suggestions based on the following welcome:

* Pure EcmaScript 5.1

   * No code conversion tools: the code in the repository runs straight out of the box

* Semicolons mandatory
* 2 spaces indentation
* use == instead of ===: type coercion is helpful


The above straight out eliminates:

* `standard <https://github.com/standard/standard>`_

These remain in play (we found all 5 on some "most popular linters" list)

* `Airbnb <https://github.com/airbnb/javascript>`_
* `Google <https://google.github.io/styleguide/jsguide.html>`_
* `Idiomatic <https://github.com/rwaldron/idiomatic.js/>`_
* `jQuery <https://contribute.jquery.org/style-guide/js/>`_

.. note:: While we're seriously considering EcmaScript 6, so far we haven't really encountered a situation where it
   would be absolutely required to do something. We try to be as light as possible on JavaScript anyway and while
   using EcmaScript 5.1 may mean a couple of lines more code, it also keeps away transpilers &
   missing-feature-completion scripts.

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


Requirements for running tests
------------------------------

.. code-block:: python

   pip install selenium

Gecko driver
************

Geckodriver is needed for the functional tests. It is available from https://github.com/mozilla/geckodriver/releases.
You need to download and extract it and put it somewhere on your system path.

For macOS or Linux, one convenient place to put it is ~/.local/bin

For Windows, put it in your Python Scripts folder

To test that you’ve got this working, open up a Bash console and you should be able to run:

.. code-block:: bash

   geckodriver --version
   geckodriver 0.17.0

The source code of this program is available at https://github.com/mozilla/geckodriver.

This program is subject to the terms of the Mozilla Public License 2.0.

You can obtain a copy of the license at https://mozilla.org/MPL/2.0/.


creating your own template pack
-------------------------------

Context variables referring to template packs
*********************************************

These variables will be set in a :py:class:`dynamicforms.viewsets.ModelViewSet` class declaration.

.. py:data:: crud_form: True | False

   If set, template pack is expected to render HTML that will allow user to edit the presented data.

.. todo:: The above is left just to keep an example. Currently there is nothing in the code that would be used