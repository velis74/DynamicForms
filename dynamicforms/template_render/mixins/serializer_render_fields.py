"""
Class that contains renderable fields for the templates.
The class provides transformation functionality
"""
from django.utils.safestring import mark_safe


class SerializerRenderFields(object):
    @property
    def fields(self):
        raise NotImplementedError('You must implement the fields property in your serializer render_fields method')

    def as_json_field_def(self):
        res = [dict(name=str(field.field_name), label=str(field.label), align='left', sort='true',
                    table_classes=field.table_classes, ordering=field.ordering(), visibility=field.display_table.name,
                    )
               for field in self.fields]
        return mark_safe(str(res))

    def __aiter__(self):
        return self.fields
