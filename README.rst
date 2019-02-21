What is DynamicForms?
=====================

DynamicForms is a library that eliminates HTML form boilerplate by providing all the relevant functionality. Instead
of having to program tables, dialog, data forms, DynamicForms already provides you with the functionality - all you have
to do is declare a few extra properties to your DRF Serializers and ViewSets.

It performs all the visualisation & data entry of your DRF Serializers & ViewSets and adds some candy of its
own: It is a `django <https://www.djangoproject.com/>`_ library that gives you the power of dynamically-shown form
fields, auto-filled default values, dynamic record loading and similar candy with little effort. To put it differently:
once defined, a particular ViewSet / Serializer can be rendered in multiple ways allowing you to perform viewing and
authoring operations on the data in question.

It is based on `django-rest-framework <http://www.django-rest-framework.org/>`_

Documentation `on readthedocs <https://dynamicforms.readthedocs.io/>`_


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

Quick start guide
=================

.. code-block:: bash

   pip install dynamicforms

Then you need to Activate DynamicForms in DRF.

Also make sure you specify a proper base page template DYNAMICFORMS_PAGE_TEMPLATE - see below for an
example).

DynamicForms has been designed to cause minimal disruption to your existing code patterns.

So instead of DRF ModelViewSet just use DynamicForms ModelViewSet, instead of ModelSerializer - DynamicForms
ModelSerializer.

Currently only the dynamicforms.viewsets.ModelViewSet is supported for ViewSets. We have others planned,
but not implemented yet.

examples/rest/page_load.py

.. code-block:: python

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


examples/models.py  (excerpt)

.. code-block:: python

   from django.db import models

   class PageLoad(models.Model):
       """
       Shows how DynamicForms handles dynamic loading of many records in ViewSet result
       """
       description = models.CharField(max_length=20, help_text='Item description')


If you want filter in list view just set serializers property show_filter value to True. Filter will be applied if user
press enter in filter field. If you want to have filter button in list header, call Actions with
add_default_filter = True.

examples/rest/filter.py

.. code-block:: python

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
       show_filter = True

       class Meta:
           model = Filter
           exclude = ()


   class FilterViewSet(viewsets.ModelViewSet):
       template_context = dict(url_reverse='filter')
       pagination_class = viewsets.ModelViewSet.generate_paged_loader(30)  # enables pagination

       queryset = Filter.objects.all()
       serializer_class = FilterSerializer



Following is an example page template to render straight router URLs. Lines 12, 17 & 20 show the lines that obtain
and render the actual data, be it table or form. See DYNAMICFORMS_PAGE_TEMPLATE.

.. code-block:: django

   {% extends 'examples/base.html' %}
   {% load dynamicforms %}
   {% block title %}
     {{ serializer.page_title }}
   {% endblock %}
   {% block body %}
     {% get_data_template as data_template %}

   <div class="{{ DYNAMICFORMS.bs_card_class }}" style="display: inline-block; margin: 1em">
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
