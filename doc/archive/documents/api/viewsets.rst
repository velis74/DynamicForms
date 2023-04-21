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
   :members: template_context, get_queryset, filter_queryset, filter_queryset_field, generate_paged_loader
   :exclude-members: initialize_request

   .. automethod:: new_object
