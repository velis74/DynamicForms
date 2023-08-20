from typing import Union

from django.db.models import Model, QuerySet
from rest_framework.utils.model_meta import get_field_info


def get_pk_name(obj: Union[Model, QuerySet]):
    if isinstance(obj, QuerySet):
        return get_field_info(obj.model).pk.name
    return get_field_info(obj).pk.name
