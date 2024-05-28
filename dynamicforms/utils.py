import sys
import traceback

from typing import Union

from django.db.models import Model, QuerySet
from rest_framework.utils.model_meta import get_field_info


def get_pk_name(obj: Union[Model, QuerySet]):
    if isinstance(obj, QuerySet):
        return get_field_info(obj.model).pk.name
    return get_field_info(obj).pk.name

def print_field_declaration_line():
    """
    This method prints the line where the field has been declared
    Must be called from field __init__
    """
    print("WARNING: This field should be converted to AJAX.", file=sys.stderr)
    # Iterate over the stack in reverse to find the first occurrence of "Serializer"
    stack = traceback.extract_stack()
    end_index = len(stack)
    for i, frame in enumerate(stack, 0):
        if "Serializer" in frame.name or "Serializer" in frame.line:
            end_index = i
    for frame in stack[end_index:end_index + 1]:
        print(
            f'File "{frame.filename}", line {frame.lineno}, in {frame.name}\n  {frame.line.strip()}',
            file=sys.stderr
        )

