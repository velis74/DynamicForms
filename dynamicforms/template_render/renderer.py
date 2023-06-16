from typing import Any, Optional

from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
from rest_framework.utils.serializer_helpers import ReturnDict, ReturnList

from dynamicforms.settings import COMPONENT_DEF_RENDERER_FORMAT, COMPONENT_HTML_RENDERER_FORMAT, DYNAMICFORMS


def data_is_paginated(data):
    return (
        isinstance(data, dict)
        and "next" in data
        and "results" in data
        and isinstance(data["results"], (ReturnList, ReturnDict))
    )


def get_serializer(data) -> Optional[Any]:
    if data_is_paginated(data):
        return data["results"].serializer
    if isinstance(data, (ReturnList, ReturnDict)):
        return data.serializer
    return None


class ComponentDefRenderer(JSONRenderer):
    format = COMPONENT_DEF_RENDERER_FORMAT

    def render(self, data, accepted_media_type=None, renderer_context=None):
        serializer = get_serializer(data)

        if serializer is None and isinstance(data, dict) and "detail" in data:
            return super().render(data, accepted_media_type, renderer_context)

        assert serializer is not None

        serializer.apply_component_context()
        component_params = serializer.component_params(output_json=False)

        return super().render(component_params, accepted_media_type, renderer_context)


class ComponentHTMLRenderer(TemplateHTMLRenderer):
    media_type = "text/html"
    format = COMPONENT_HTML_RENDERER_FORMAT

    def render(self, data, accepted_media_type=None, renderer_context=None):
        DYNAMICFORMS.components = True
        try:
            return super().render(data, accepted_media_type, renderer_context)
        finally:
            DYNAMICFORMS.components = False

    def get_template_names(self, response, view):
        return [DYNAMICFORMS.page_template]

    def get_template_context(self, data, renderer_context):
        serializer = get_serializer(data)
        if serializer:
            return dict(serializer=serializer)
        return super().get_template_context(data, renderer_context)
