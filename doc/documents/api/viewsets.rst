ViewSets
========

Currently only provides ModelViewSet for model-based data manipulation.

To use, import like so:

.. code-block:: python

   from dynamicforms.viewsets import ModelViewSet

Make sure you don't import DRF's ModelViewSet over this one.

Class reference
---------------

.. autoclass:: dynamicforms.viewsets.ModelViewSet
   :members:
   :exclude-members: initialize_request, finalize_response

   .. automethod:: new_object
