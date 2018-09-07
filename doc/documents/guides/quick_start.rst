Quick start guide
=================

.. code-block:: python

   pip install dynamicforms

First, you need to :ref:`Activate DynamicForms in DRF <Activate_DynamicForms_in_DRF>`.

DynamicForms has been designed to cause minimal disruption to your existing code patterns.

So instead of DRF ModelViewSet just use DynamicForms ModelViewSet.

.. todo:: Provide a code example showing how a simple Serializer / ViewSet configuration might look like.


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