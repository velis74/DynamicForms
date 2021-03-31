"""
Class that contains renderable fields for the templates.
The class provides transformation functionality
"""
from django.utils.safestring import mark_safe

from dynamicforms.mixins import DisplayMode


class SerializerRenderFields(object):
    @property
    def fields(self):
        raise NotImplementedError('You must implement the fields property in your serializer render_fields method')

    def as_field_def(self):
        res = [dict(name=str(field.field_name), label=str(field.label), align='left',
                    table_classes=field.table_classes, ordering=field.ordering(), visibility=field.display_table.name,
                    )
               for field in self.fields]
        return res

    def as_name_value(self):
        res = [{f'data-{field.field_name}': str(getattr(field, 'bound_value', ''))}
               for field in self.fields]
        return res

    @property
    def columns(self) -> 'SerializerRenderFields':
        """
        Returns fields that need to be rendered as columns in table, either fully visible or hidden
        This is as opposed to rendering the fields into data-field_name properties for the HIDDEN fields(see properties)
        """
        this = self

        class BoundVisibleSerializerRenderFields(SerializerRenderFields):
            @property
            def fields(self):
                for fld in this.fields:
                    if fld.display_table in (DisplayMode.INVISIBLE, DisplayMode.FULL):
                        yield fld

        return BoundVisibleSerializerRenderFields()

    @property
    def properties(self) -> 'SerializerRenderFields':
        """
        Returns fields that need to be rendered as data-field_name properties in tr
        This is as opposed to rendering the table columns
        """
        this = self

        class BoundVisibleSerializerRenderFields(SerializerRenderFields):
            @property
            def fields(self):
                for fld in this.fields:
                    if fld.display_table == DisplayMode.HIDDEN:
                        yield fld

        return BoundVisibleSerializerRenderFields()

    def __aiter__(self):
        return self.fields
