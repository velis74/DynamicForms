import json

from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from dynamicforms.serializers import DynamicFormsSerializer


class SerializerFilter(object):
    def get_filter_serializer(self) -> Optional["DynamicFormsSerializer"]:
        return self.filter_data if not self.is_filter else None

    def filter_serializer_component_params(self) -> Optional[dict]:
        filter_serializer: Optional["DynamicFormsSerializer"] = self.get_filter_serializer()
        params: Optional[dict] = json.loads(filter_serializer.component_params()) if filter_serializer else None
        if not params:
            return None
        params["uuid"] = self.uuid
        return params
