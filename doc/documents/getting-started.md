Quick start guide
=================

.. code-block:: bash

   pip install dynamicforms

Then you need to add following setting to your project's settings.py
.. code-block:: python

   :caption: settings.py
   :name: settings.py

   REST_FRAMEWORK = {
       'DEFAULT_RENDERER_CLASSES': (
           'rest_framework.renderers.JSONRenderer',
           'rest_framework.renderers.BrowsableAPIRenderer',
           'dynamicforms.renderers.TemplateHTMLRenderer',
       )
   }


DynamicForms has been designed to cause minimal disruption to your existing code patterns.

So instead of DRF ModelViewSet just use DynamicForms ModelViewSet, instead of ModelSerializer - DynamicForms
ModelSerializer.

Currently only the :py:class:`~dynamicforms.viewsets.ModelViewSet` is supported for ViewSets. We have others planned,
but not implemented yet.

.. code-block:: python

   :caption: examples/rest/page_load.py
   :name: examples/rest/page_load.py

   from dynamicforms import serializers, viewsets
   from ..models import PageLoad


