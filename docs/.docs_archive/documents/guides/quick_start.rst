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


   class PageLoadSerializer(serializers.ModelSerializer):
       form_titles = {
           'table': 'Dynamic page loader list',
           'new': 'New object',
           'edit': 'Editing object',
       }

       class Meta:
           model = PageLoad
           exclude = ()


   class PageLoadViewSet(viewsets.ModelViewSet):
       template_context = dict(url_reverse='page-load')
       pagination_class = viewsets.ModelViewSet.generate_paged_loader(30)  # enables pagination

       queryset = PageLoad.objects.all()
       serializer_class = PageLoadSerializer


.. code-block:: python
   :caption: examples/models.py  (excerpt)
   :name: examples/models.py

   from django.db import models

   class PageLoad(models.Model):
       """
       Shows how DynamicForms handles dynamic loading of many records in ViewSet result
       """
       description = models.CharField(max_length=20, help_text='Item description')


Filter will be applied if user press enter in filter field. If you want to have filter button in list header,
call Actions with add_default_filter = True.

.. code-block:: python
   :caption: examples/filter.py
   :name: examples/filter.py

   from dynamicforms import serializers, viewsets
   from dynamicforms.action import Actions
   from ..models import Filter


   class FilterSerializer(serializers.ModelSerializer):
       form_titles = {
           'table': 'Dynamic filter list',
           'new': 'New object',
           'edit': 'Editing object',
       }
       actions = Actions(add_default_crud=True, add_default_filter=True)

       class Meta:
           model = Filter
           exclude = ()


   class FilterViewSet(viewsets.ModelViewSet):
       template_context = dict(url_reverse='filter')
       pagination_class = viewsets.ModelViewSet.generate_paged_loader(30)  # enables pagination

       queryset = Filter.objects.all()
       serializer_class = FilterSerializer


Custom page template
--------------------

Following is an example page template to render straight router URLs. Customise this to match your site's look & feel.
The emphasized lines show the lines that obtain and render the actual data, be it table or form.
See :py:data:`DYNAMICFORMS_PAGE_TEMPLATE`.

.. code-block:: django
   :caption: examples/templates/examples/page.html
   :name: examples/templates/examples/page.html
   :emphasize-lines: 12, 17, 20

   {% extends 'examples/base.html' %}
   {% load dynamicforms %}
   {% block title %}
     {{ serializer.page_title }}
   {% endblock %}
   {% block body %}
     {% get_data_template as data_template %}

   <div class="{{ DYNAMICFORMS.bs_card_class }}">
     <div class="{{ DYNAMICFORMS.bs_card_header }}">
       {{ serializer.page_title }}
       {% if serializer.render_type == 'table' %}{% render_table_commands serializer 'header' %}{% endif %}
     </div>
     <div class="{{ DYNAMICFORMS.bs_card_body }}">
       {% include data_template with serializer=serializer data=data %}
     </div>
   </div>
   {% endblock %}


Done. Point your DRF router to the ViewSet you just created and your browser to its URL - make sure you add ".html" to
the URL to specify the renderer. If you forget that, you will get DRF's API renderer.
