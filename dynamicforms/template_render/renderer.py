from typing import Any, Optional

from rest_framework.renderers import JSONRenderer
from rest_framework.utils.serializer_helpers import ReturnDict, ReturnList


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
    format = "componentdef"

    def render(self, data, accepted_media_type=None, renderer_context=None):
        serializer = get_serializer(data)

        if serializer is None and isinstance(data, dict) and "detail" in data:
            return super().render(data, accepted_media_type, renderer_context)

        assert serializer is not None

        serializer.apply_component_context()
        component_params = serializer.component_params(output_json=False)

        return super().render(component_params, accepted_media_type, renderer_context)
