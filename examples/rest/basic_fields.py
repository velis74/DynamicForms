from django.utils.translation import gettext_lazy as _

from dynamicforms import fields, serializers
from dynamicforms.action import Actions, TableAction, TablePosition
from dynamicforms.template_render.layout import Group, Layout, Row
from dynamicforms.template_render.responsive_table_layout import ResponsiveTableLayout, ResponsiveTableLayouts
from dynamicforms.viewsets import ModelViewSet

from ..models import BasicFields


class BasicFieldsSerializer(serializers.ModelSerializer):
    template_context = dict(url_reverse="basic-fields")
    form_titles = {
        "table": "Basic fields list",
        "new": "New basic fields object",
        "edit": "Editing basic fields object",
    }
    form_template = "examples/form_cols.html"

    actions = Actions(
        TableAction(TablePosition.HEADER, _("Modal dialog"), title=_("Dialog test"), name="modal_dialog"),
        # TODO:     action_js="examples.testModalDialog();"),
        TableAction(
            TablePosition.FIELD_END,
            label="field_end",
            title="field_end",
            name="field_end",
            icon="search-outline",
            field_name="char_field",
            action=dict(func_name="examples.showAlertDialog", params=dict(page="Basic fields", field="char")),
        ),
        add_default_crud=True,
        add_form_buttons=True,
    )

    boolean_field = fields.BooleanField(allow_null=False)
    nullboolean_field = fields.BooleanField(allow_null=True)
    char_field = fields.CharField()
    email_field = fields.EmailField()
    slug_field = fields.SlugField()
    url_field = fields.URLField()
    uuid_field = fields.UUIDField()
    ipaddress_field = fields.IPAddressField()
    integer_field = fields.IntegerField()
    nullint_field = fields.IntegerField(allow_null=True)
    float_field = fields.FloatField()
    decimal_field = fields.DecimalField(max_digits=5, decimal_places=2)
    datetime_field = fields.DateTimeField(required=False)
    date_field = fields.DateField()
    time_field = fields.TimeField()
    duration_field = fields.DurationField()
    password_field = fields.CharField(password_field=True)

    class Meta:
        model = BasicFields
        exclude = ()
        layout = Layout(
            Row(
                Group(
                    None,
                    "Booleans",
                    Layout(Row("boolean_field"), Row("nullboolean_field"), auto_add_fields=False),
                ),
                Group(
                    None,
                    "Text fields",
                    Layout(Row("char_field"), Row("slug_field"), Row("password_field"), auto_add_fields=False),
                    colspan=2,
                ),
            ),
            columns=3,
            size="large",
        )
        responsive_columns = ResponsiveTableLayouts(
            auto_generate_single_row_layout=True,
            layouts=[
                ResponsiveTableLayout(
                    "id",
                    ["boolean_field", "nullboolean_field"],
                    ["char_field", "slug_field"],
                    ["email_field", "url_field"],
                    ["uuid_field", ["ipaddress_field", "integer_field", "nullint_field"]],
                    ["float_field", "decimal_field"],
                    [["datetime_field", "date_field"], ["time_field", "duration_field"]],
                    auto_add_non_listed_columns=True,
                ),
                ResponsiveTableLayout(
                    "id",
                    [
                        ["boolean_field", "nullboolean_field"],
                        ["ipaddress_field", "integer_field", "nullint_field"],
                        ["float_field", "decimal_field"],
                    ],
                    [["char_field", "slug_field"], ["email_field", "url_field"], "uuid_field"],
                    [["datetime_field", "date_field"], ["time_field", "duration_field"]],
                    auto_add_non_listed_columns=True,
                ),
            ],
            auto_generate_single_column_layout=False,
        )


class BasicFieldsViewset(ModelViewSet):
    pagination_class = ModelViewSet.generate_paged_loader(30)

    queryset = BasicFields.objects.all()
    serializer_class = BasicFieldsSerializer
