from django.http import HttpRequest

from .settings import DYNAMICFORMS


def add_dynamicforms_settings(request: HttpRequest):
    """
    context processor that adds DynamicForms configuration variables to template context

    Example for supporting different versions of bootstrap:

    .. code-block:: python

       {% if DYNAMICFORMS.bootstrap_version == 'v3' %}
         {% set_var card_class='panel panel-default' card_header='panel-heading' card_body='panel_body' %}
       {% else %}
         {% set_var card_class='card' card_header='card-header' card_body='card-body' %}
       {% endif %}

    .. note:: Using DynamicForms renderers automatically adds this variable into the context as it is required by
       template packs.

    :param request: see `django documentation <https://docs.djangoproject.com/en/dev/ref/templates/api/
       #writing-your-own-context-processors>`_
    :return: dict with `DYNAMICFORMS` context variable set
    """
    return dict(DYNAMICFORMS=DYNAMICFORMS)
