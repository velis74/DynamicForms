# Using Layout in Serializers

The `layout.py` module provides a flexible way to define form layouts for your serializers. This guide explains 
how to use the `Layout` class and its components to create custom form layouts.

## Basic Usage

To use a custom layout in your serializer, add a `layout` attribute to the `Meta` class:

```python
from dynamicforms.template_render.layout import Layout, Row, Column, Field
from dynamicforms import serializers


class MySerializer(serializers.ModelSerializer):
    class Meta:
        model = MyModel
        fields = ['field1', 'field2', 'field3', 'field4']
        layout = Layout(
            Row('field1', 'field2'),
            Row(Column('field3'), Column(Field('field4', 'my_component_name'))),
        )
```

# Layout Components
## Layout

The Layout class is the top-level container for your form layout.

```python
from dynamicforms.template_render.layout import Layout, Row, Column, Field

Layout(
    *rows: Row, 
    component_name: str = "df-form-layout", 
    columns: int = 1, 
    size: str = "", 
    header_classes: str = "",
    auto_add_fields: bool = True,
)
```

* rows: A list of Row objects defining the layout structure.
* component_name: The name of the Vue component to use for rendering (default: "df-form-layout"). Used for overriding 
  default rendering.
* columns: Number of columns for automatically added fields (default: 1). Also important for layout and colspan.
* size: Size of the layout ("small", "large", "", etc.). Mostly effective when this layout is going to be rendered in a 
  dialog. See [DialogSize](dialog-size) for reference on size classes. 
* header_classes: CSS classes for the header.
* auto_add_fields: allows to specify whether fields that are not manually laid out, should be auto-added to the end of 
  the layout. If no layout is specified in serializer Meta, this will generate default single-column layout

## Row

The Row class represents a horizontal group of columns.

```python
from typing import Union
from dynamicforms.template_render.layout import Layout, Row, Column, Field

Row(*columns: Union[Column, Field, str], component_name="FormRow")
```

* columns: A list of Column objects or field names.
* component_name: The name of the Vue component to use for rendering (default: "FormRow"). Change when overriding
  default rendering components.

## Column

The Column class represents a vertical section within a row.

```python
from typing import Union, Optional, Tuple
from dynamicforms.template_render.layout import Layout, Row, Column, Field
from dynamicforms.fields import DFField

Column(field: Union[Tuple[str, DFField], Field, str, None], colspan: int = 1)
```
* field: A Field object or field name.
* colspan: how many columns does this field span. See Layout.columns property 


## Group

The `Group` class allows grouping of fields or nested serializers.

```python
from typing import Union, Optional, Tuple
from dynamicforms.template_render.layout import Layout, Row, Column, Field, Group

Group(
    field: Union[str, Field, None],
    title: str = None, 
    sub_layout: Layout = None, 
    colspan: int = 1,
    footer: Optional[str] = None,
)
```

* field: A Field object, field name, or None for flat field grouping.
* title: The title of the group.
* sub_layout: A Layout object for custom layout within the group.
* colspan: how many columns does this group span in the layout.
* footer: Optional footer text for the group.

Groups can be used in two main ways:

1. For nested serializers:

   ```python
   Group('nested_serializer_field', title="Nested Data")
   ```

2. For grouping flat fields:

   ```python
   Group(
       None, 
       title="Personal Info",
       sub_layout=Layout(
           Row('first_name', 'last_name'),
           Row('email'),
       )
   )
   ```

When used with a nested serializer, the Group will use the provided `sub_layout`, nested serializer's layout if 
available, or create a default layout for its fields. When used for flat field grouping, you must provide a `sub_layout`
to define the structure of the grouped fields.
