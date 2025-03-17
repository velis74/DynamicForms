import typing
import uuid as uuid_module

from enum import IntEnum
from typing import Dict, Optional

from rest_framework.fields import Field as DrfField
from rest_framework.relations import PKOnlyObject

if typing.TYPE_CHECKING:
    from dynamicforms.mixins import DFField


class DisplayMode(IntEnum):
    """
    The ways a field might be rendered (or not).

    NOTE: This class has a copy in Vue component "df-table", so if you change here, the change needs to be
          implemented there as well
    """

    SUPPRESS = 1  # Field will be entirely suppressed. it will not render (not even to JSON) and will not parse for PUT
    HIDDEN = 5  # Field will render as <input type="hidden"> or <tr data-field_name>
    INVISIBLE = 8  # Field will render completely, but with display: none. Equal to setting its style = {display: none}
    FULL = 10  # Field will render completely


class FieldAlignment(IntEnum):
    """
    How field's contents should be aligned in their respective containers (table cell / input)

    NOTE: This class has a copy in Vue component "df-table", so if you change here, the change needs to be
          implemented there as well
    """

    LEFT = -1
    CENTER = 0
    RIGHT = 1
    DECIMAL = 2  # Aligned on the decimal separator


class FieldRenderMixin(object):
    """
    Is used in fields and serializers, so every field and serializer gets its unique id. Also to specify where and how
    fields should render.

    In form where serializer is used, id is serializers uuid. Table with list of records has id »list-serializer.uuid«,
    in dialog id is »dialog-{serializer.uuid}« and save button's id on dialog is »save-{serializer.uuid}«

    Similar for fields: All inputs in HTML get id from field.uuid. Div that contains all that belongs to the field has
    »container-{field.uuid}« for id, label has »label-{field.uuid}« and help text (if exists) has »help-{field.uuid}«
    for id.

    Used for rendering individual field to table view
    """

    def __init__(
        self,
        *args,
        uuid: uuid_module.UUID = None,
        display: DisplayMode = None,  # None == Leave at default
        display_table: DisplayMode = None,  # None == Leave at default
        display_form: DisplayMode = None,  # None == Leave at default
        table_classes: str = "",
        alignment: FieldAlignment = FieldAlignment.LEFT,
        render_params: Optional[Dict] = None,
        placeholder: Optional[str] = None,
        **kwargs,
    ):
        """

        :param args: passed on to inherited constructors
        :param uuid: custom specified field UUID. if not specified, it will be assigned automatically
        :param display: see DisplayMode enum. Specifies how field will render. Leave at None for default (FULL)
            display_form and display_table also accepted for better granularity
        :param table_classes: css classes to add to the table column
        :param alignment: How field's contents should be aligned in their respective containers (table cell / input)
        :param render_params: what widget to use for render and its parameters. Whatever you want that affects rendering
        :param kwargs: passed on to inherited constructors
        """
        super().__init__(*args, **kwargs)
        self.uuid = uuid or uuid_module.uuid1()
        # noinspection PyUnresolvedReferences
        self.display_table = (
            display_table
            or display
            or (DisplayMode.FULL if not getattr(self, "write_only", False) else DisplayMode.SUPPRESS)
        )
        self.display_form = display_form or display or DisplayMode.FULL
        self.table_classes = table_classes
        self.alignment = alignment
        self.placeholder = placeholder

        # render_params need not only include form renderer and table formatting function. add anything you need!
        render_params = render_params or {}
        render_params.setdefault("form_component_name", "DInput")
        render_params.setdefault("table", "df-tablecell-plaintext")
        render_params.setdefault("input_type", "text")
        render_params.setdefault("field_class", "form-control")
        render_params.setdefault("container_class", "form-group")
        self.render_params = render_params

    # noinspection PyUnresolvedReferences,PyMethodMayBeStatic
    def use_pk_only_optimization(self):
        """
        Overrides DRF RelatedField's method. If True is returned then value passed for serialisation will be PK value
        only, not entire relation object. we don't want that because then we can't resolve the value into something more
        human-readable
        :return:
        """
        return False

    # noinspection PyUnresolvedReferences
    def to_representation(self, value, row_data=None):
        """
        Overrides DRF Field's to_representation.
        Note that this is also called for the entire record as well as the serializer also is a Field descendant
        :param value: value to serialize
        :param row_data: instance with row data
        :return: serialized value
        """
        check_for_none = value.pk if isinstance(value, PKOnlyObject) else value
        if check_for_none is None:
            value = None

        if value is None:
            # TODO: DRF excepts if value is None. However, if me have a field that redeclares its
            #  to_representation, it now won't be called :(
            return None
        else:
            return super().to_representation(value)

    def set_display(self, value):
        if isinstance(value, tuple):
            self.display_form, self.display_table = value
        else:
            self.display_form = self.display_table = value

    display = property(lambda self: self.display_form, set_display)

    # noinspection PyUnusedLocal, PyUnresolvedReferences
    def render_to_table(self, value, row_data):
        """
        Renders field value for table view. override for your field

        :param value: field value
        :param row_data: data for entire row (for more complex renderers)
        :return: rendered value for table view
        """
        return value

    def validate_empty_values(self: DrfField, data):
        # noinspection PyUnresolvedReferences
        res = super().validate_empty_values(data)

        # This is to fix a problem with calculated fields which was only solved in DRF 3.10.
        # Forces validation and inclusion of the field into validated data. See comment in original function.
        if res == (True, None) and data is None and self.source == "*":
            return False, None
        return res

    def ordering(self):
        ordering = []
        if hasattr(self, "context") and "view" in getattr(self, "context"):
            ordering = getattr(self.context["view"], "ordering", None)

        if getattr(self, "field_name") not in getattr(ordering, "fields", []):
            return ""

        index = -1
        direction_asc = True
        for idx, o in enumerate(ordering):
            if o.startswith("-"):
                direction_asc = False
                o = o[1:]
            if o == getattr(self, "field_name"):
                index = idx

        if index > -1:
            direction_class = ("asc" if direction_asc else "desc") + " seg-%d" % (index + 1)
        else:
            direction_class = "unsorted"
        return "ordering " + direction_class

    def as_component_def(self: "DFField") -> dict:
        try:
            res = super().as_component_def()  # noqa
        except AttributeError:
            res = dict()
        res.update(
            dict(
                uuid=str(self.uuid),
                name=str(self.field_name),
                label=str(self.label),
                read_only=self.read_only,
                table_classes=self.table_classes,
                ordering=self.ordering(),
                alignment=self.alignment.name.lower(),
                visibility=dict(table=self.display_table.value, form=self.display_form.value),
                render_params=self.render_params,
                help_text=res.get("help_text", ""),
                allow_null=self.allow_null,
                placeholder=self.placeholder or None,
            )
        )
        if "base_template" in self.style and self.style["base_template"] == "textarea.html":
            res["render_params"]["form"] = "TextArea"
        if hasattr(self, "max_length"):
            res["render_params"]["max_length"] = self.max_length
        if hasattr(self, "min_length"):
            res["render_params"]["min_length"] = self.min_length
        return res
