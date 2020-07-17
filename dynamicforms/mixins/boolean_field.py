from rest_framework import __version__ as drf_version
from rest_framework.exceptions import ValidationError

from dynamicforms.settings import version_check

if version_check(drf_version, '3.9'):

    class BooleanFieldMixin(object):
        pass

else:

    class BooleanFieldMixin(object):
        NULL_VALUES = {'null', 'Null', 'NULL', '', None}

        def to_internal_value(self, data):
            try:
                parent_value = super().to_internal_value(data)
                return parent_value
            except TypeError:  # Input is an unhashable type
                pass
            except ValidationError:
                if data in self.NULL_VALUES and self.allow_null:
                    return None
            self.fail('invalid', input=data)

        def to_representation(self, value):
            parent_value = super().to_representation(value)
            if value in self.NULL_VALUES and self.allow_null:
                return None
            return parent_value
