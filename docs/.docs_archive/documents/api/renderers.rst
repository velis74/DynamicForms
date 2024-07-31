Renderers
=========

Contains template renderers.

To use, declare renderers in settings.py, like so:

.. code-block:: python

   REST_FRAMEWORK = {
       'DEFAULT_RENDERER_CLASSES': (
           'rest_framework.renderers.JSONRenderer',
           'rest_framework.renderers.BrowsableAPIRenderer',
           'dynamicforms.renderers.TemplateHTMLRenderer',
       )
   }


Class reference
---------------

.. automodule:: dynamicforms.renderers
   :members:
