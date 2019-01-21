Dialogs
=======

Dialogs offer more flexibility by allowing you to place them on screen when needed instead of having them pre-rendered
in the page. Their contents are always fresh and theirHTML adapts to the task at hand. For example, when user makes a
mistake entering data, the returned dialog will already contain all the warnings in the HTML.

To use, either add `?df_render_type=dialog` to URL or add a `X_DF_RENDER_TYPE=dialog` HTTP header to request.

The default dialog templates allow for some customisation of dialog rendered.

Dialog classes
--------------

.. code-block:: python

   class MyViewSet(viewsets.ModelViewSet):
       template_context = dict(url_reverse='my-item', dialog_classes='dialog-lg')

Good for specifying additional dialog classes, like how large the dialog should be.

Dialog header classes
---------------------

.. code-block:: python

   class MyViewSet(viewsets.ModelViewSet):
       template_context = dict(url_reverse='my-item', dialog_header_classes='bg-info')

Good for specifying additional dialog header classes, like typeof dialog (warning, info, primary, etc)

