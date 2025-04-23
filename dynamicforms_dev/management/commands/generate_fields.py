import inspect
import os
import subprocess
import textwrap
import typing
import uuid

from django.core.management.base import BaseCommand
from rest_framework import fields, relations, serializers


class ClassAssemblyDict:
    """
    Takes a dictionary with classes as keys.
    Lookups against this object will traverse the object's inheritance hierarchy in method resolution order,
    and assemble response from keys as defined in this dict. Any keys not found in higher MRO levels will be populated
    from lower ones.
    See e.g. EmailField and Field mappings below: EmailField will return a dict with three members,
      two of them from Field mapping: dict(form_component_name='DInput', input_type='email', table='df-tablecell-plaintext'),
    raises a KeyError if nothing matches
    """

    def __init__(self, mapping):
        self.mapping = mapping

    def __getitem__(self, base_class):
        res = dict()
        for cls in reversed(inspect.getmro(base_class)):
            if cls in self.mapping:
                res.update(self.mapping[cls])
        if not res and base_class.__name__ != "RTFField":
            print("Class %s not found in lookup." % base_class.__name__)
        return res

    def __setitem__(self, key, value):
        self.mapping[key] = value


class RTFField(object):
    pass


class ColorField(object):
    pass


render_params = ClassAssemblyDict(
    {
        fields.Field: dict(form_component_name="DInput", input_type="text", table="df-tablecell-plaintext"),
        fields.EmailField: dict(input_type="email", table="df-tablecell-email"),
        fields.URLField: dict(input_type="url", table="df-tablecell-link", pattern="https?://.*"),
        fields.IntegerField: dict(input_type="number"),
        fields.FloatField: dict(input_type="number", table="#TableCellFloat", table_show_zeroes=True, step=0.1),
        fields.DecimalField: dict(input_type="number", table="#TableCellFloat", table_show_zeroes=True, step=0.1),
        fields.DateTimeField: dict(
            input_type="datetime",
            form_component_name="DDateTime",
            table_format="dd.MM.yyyy HH:mm",
            form_format="dd.MM.yyyy HH:mm",
            table="#TableCellDateTime",
        ),
        fields.DateField: dict(
            input_type="date",
            form_component_name="DDateTime",
            table_format="dd.MM.yyyy",
            form_format="dd.MM.yyyy",
            table="#TableCellDateTime",
        ),
        fields.TimeField: dict(
            input_type="time",
            form_component_name="DDateTime",
            table_format="HH:mm",
            form_format="HH:mm",
            table="#TableCellDateTime",
        ),
        serializers.FileField: dict(input_type="file", form_component_name="DFile", table="df-tablecell-file"),
        fields.BooleanField: dict(
            table="df-tablecell-bool",
            input_type="checkbox",
            form_component_name="DCheckbox",
            field_class="form-check-input position-checkbox-static",
            label_class="form-check-label",
            container_class="form-check form-group",
        ),
        fields.IPAddressField: dict(table="df-tablecell-ipaddr", minlength=7, maxlength=15, size=15),
        fields.ChoiceField: dict(form_component_name="DSelect", multiple=False, allow_tags="%allow_tags"),
        fields.MultipleChoiceField: dict(multiple=True),
        relations.RelatedField: dict(form_component_name="DSelect", multiple=False),
        relations.ManyRelatedField: dict(form_component_name="DSelect", multiple=True),
        # TODO: The following two aren't taken care of yet for rendering in components
        serializers.Serializer: dict(form_component_name="DFWidgetFieldset"),
        serializers.ListSerializer: dict(form_component_name="DFWidgetListFieldset"),
        fields.ListField: dict(form_component_name="DFWidgetListField"),
        fields.DictField: dict(form_component_name="DFWidgetDictField"),
        fields.FilePathField: dict(form_component_name="DSelect", multiple=False),
        fields.JSONField: dict(form_component_name="DTextArea"),
        ColorField: dict(form_component_name="DColor", table="df-tablecell-color"),
    }
)


def arepr(value):
    if isinstance(value, str) and value.startswith("%"):
        return value[1:]
    return repr(value).replace("'", '"')


class Command(BaseCommand):
    help = "Generate Field classes from DRF with applied DynamicForms mixins"

    # def add_arguments(self, parser):
    #     parser.add_argument('-dest', dest='file', type=str, default='strings.xlsx', action='store',
    #                         help='filename where to store the strings')

    def handle(self, *args, **options):
        from dynamicforms import action, mixins
        from dynamicforms.mixins import (
            ActionMixin,
            ChoiceMixin,
            ConditionalVisibilityMixin,
            FieldAlignment,
            FieldRenderMixin,
            NullValueMixin,
            PasswordFieldMixin,
            RelatedFieldAJAXMixin,
        )
        from dynamicforms.mixins.choice import AllowTagsMixin, NullChoiceMixin, SingleChoiceMixin

        with open(os.path.abspath(os.path.join("dynamicforms/", "fields.py")), "w") as output:
            output = typing.cast("SupportsWrite[str]", output)  # just so linter stops complaining
            field_list = []
            for obj in fields.__dict__.values():
                if (
                    obj != fields.Field
                    and inspect.isclass(obj)
                    and issubclass(obj, fields.Field)
                    and not obj.__name__.startswith("_")
                ):
                    field_list.append(obj)

            for obj in relations.__dict__.values():
                if (
                    obj != relations.RelatedField
                    and inspect.isclass(obj)
                    and (issubclass(obj, relations.RelatedField) or issubclass(obj, relations.ManyRelatedField))
                    and obj.__name__.endswith("Field")
                ):
                    field_list.append(obj)

            field_list += [RTFField, ColorField]

            # get all the field-specific mixins
            field_mixins = [f.__name__ + "Mixin" for f in field_list if f.__name__ + "Mixin" in mixins.__dict__]

            print("import warnings", file=output)
            print("from typing import Dict, Optional", file=output)
            print("from uuid import UUID\n", file=output)

            print("from rest_framework import __version__ as drf_version", file=output)
            print("from rest_framework import fields, relations", file=output)
            print("from versio.version import Version", file=output)
            print("from versio.version_scheme import Pep440VersionScheme\n", file=output)

            print("from .action import Actions", file=output)
            print("from .mixins import (", file=output, end="")
            print(
                "\n    ".join(
                    [""]
                    + textwrap.wrap(
                        ", ".join(
                            sorted(
                                (
                                    "DFField, ActionMixin, FieldRenderMixin, DisplayMode, ChoiceMixin, RelatedFieldAJAXMixin, "
                                    + "FieldHelpTextMixin, PasswordFieldMixin, NullValueMixin, EnableCopyMixin, FieldAlignment, "
                                    + "ConditionalVisibilityMixin, Statement, "
                                    + ", ".join(field_mixins)
                                ).split(", "),
                                key=str.casefold,
                            )
                        ),
                        116,
                    )
                ),
                file=output,
            )
            print(")", file=output)
            print("\nassert DFField  # So that the linter does not complain", file=output)

            print("\n\nclass AutoGeneratedField(dict):", file=output)
            print("    def get_serializer_field(self, name, serializer, extra_params=None):", file=output)
            print("        from rest_framework.utils import model_meta", file=output)
            print("", file=output)
            print('        if not hasattr(serializer, "_df_model"):', file=output)
            print('            serializer._df_model = getattr(serializer.Meta, "model")', file=output)
            print('        if not hasattr(serializer, "_df_info"):', file=output)
            print("            serializer._df_info = model_meta.get_field_info(serializer._df_model)", file=output)
            print('        if not hasattr(serializer, "_df_depth"):', file=output)
            print('            serializer._df_depth = getattr(serializer.Meta, "depth", 0)', file=output)
            print("", file=output)
            print("        if extra_params is None:", file=output)
            print("            extra_params = self", file=output)
            print("        field_class, field_kwargs = serializer.build_field(", file=output)
            print("            name, serializer._df_info, serializer._df_model, serializer._df_depth", file=output)
            print("        )", file=output)
            print("        field_kwargs.update(extra_params)", file=output)
            print("", file=output)
            print("        return field_class(**field_kwargs)", file=output)

            for field in field_list:
                field_class = field.__name__
                field_params, field_params_names = [], set()
                param_classes = []
                for cls in enumerate(field.__mro__):
                    param_classes.append(cls)
                    if cls[1] == fields.Field:
                        break
                if issubclass(field, fields.ChoiceField):
                    param_classes.append((0, ChoiceMixin))
                    param_classes.append((0, AllowTagsMixin))
                    param_classes.append((0, NullChoiceMixin))
                    param_classes.append((0, SingleChoiceMixin))
                if issubclass(field, relations.RelatedField):
                    param_classes.append((0, RelatedFieldAJAXMixin))
                if issubclass(field, fields.CharField):
                    param_classes.append((0, PasswordFieldMixin))
                if issubclass(field, (fields.IntegerField, fields.DateTimeField, fields.DateField, fields.TimeField)):
                    param_classes.append((0, NullValueMixin))

                param_classes.append((0, ActionMixin))
                param_classes.append((0, ConditionalVisibilityMixin))
                param_classes.append((0, FieldRenderMixin))

                skip_depth = 0
                for depth, cls in param_classes:
                    if depth > skip_depth:
                        continue
                    skip_depth = 0

                    if hasattr(cls, "__init__"):
                        had_kwds = False
                        for parm in inspect.signature(cls.__init__).parameters.values():
                            parm_str = parm.name
                            if parm_str == "self" or parm.kind in (parm.VAR_KEYWORD, parm.VAR_POSITIONAL):
                                # we don't repeat all the self fields there are. Not all the *args && **kwds
                                had_kwds |= parm.kind == parm.VAR_KEYWORD
                                continue
                            if (
                                depth
                                and len(field_params)
                                and (
                                    parm.kind == parm.POSITIONAL_ONLY
                                    or (parm.kind == parm.POSITIONAL_OR_KEYWORD and parm.default == inspect._empty)
                                )
                            ):
                                # positional arguments can only be declared before any keyword ones
                                continue

                            p_an = parm.annotation
                            p_def = parm.default

                            if field_class == "ManyRelatedField" and parm.name == "allow_null":
                                p_def = True  # ManyRelatedField CAN of course live without any values being set

                            if p_an != inspect._empty:
                                if (
                                    isinstance(
                                        p_an,
                                        (
                                            str,
                                            int,
                                            float,
                                            bool,
                                        ),
                                    )
                                    or p_an is None
                                ):
                                    parm_str += ": " + repr(p_an)
                                elif inspect.isclass(p_an) and issubclass(
                                    p_an,
                                    (
                                        str,
                                        int,
                                        float,
                                        bool,
                                    ),
                                ):
                                    parm_str += ": " + p_an.__name__
                                elif p_an in (uuid.UUID, action.Actions):
                                    parm_str += ": " + p_an.__name__
                                elif p_an == typing.Union[str, None]:
                                    parm_str += ": Optional[str]"
                                elif p_an in (typing.Union[dict, None], typing.Union[typing.Dict, None]):
                                    parm_str += ": Optional[Dict]"
                                else:
                                    # if you get this error, you need to add the type to includes at the top
                                    # of this function and then implement the actual printing just above here
                                    print(
                                        f"Error: parameter {parm.name} annotation is of unknown type "
                                        f"{parm.annotation}."
                                    )

                            if p_def != inspect._empty:
                                equals = " = " if ":" in parm_str else "="
                                if isinstance(p_def, FieldAlignment):
                                    p_def = "FieldAlignment.LEFT"
                                    if issubclass(
                                        field, (fields.IntegerField, fields.DecimalField, fields.DurationField)
                                    ):
                                        p_def = "FieldAlignment.RIGHT"
                                    if issubclass(field, fields.FloatField):
                                        p_def = "FieldAlignment.DECIMAL"
                                    parm_str += equals + str(p_def)
                                elif (
                                    isinstance(
                                        p_def,
                                        (
                                            str,
                                            int,
                                            float,
                                            bool,
                                        ),
                                    )
                                    or p_def is None
                                ):
                                    parm_str += equals + repr(p_def)
                                elif p_def in (fields.empty,):
                                    parm_str += equals + ".".join((p_def.__module__.split(".")[-1], p_def.__name__))
                                else:
                                    print(f"Error: parameter {parm.name} default is of unknown type {parm.default}.")

                            if parm.name not in field_params_names:
                                field_params_names.add(parm.name)
                                field_params.append(parm_str)

                        if had_kwds:
                            skip_depth = depth + 1

                    # Here we tackle parameter declarations that are handled in code instead of constructor prototypes
                    if cls == fields.CharField:
                        field_params.append("allow_blank: bool = False")
                        field_params.append("trim_whitespace: bool = True")
                        field_params.append("min_length: Optional[int] = None")
                        field_params.append("max_length: Optional[int] = None")
                    elif cls == fields.UUIDField:
                        field_params.append("format: str = 'hex_verbose'")
                    elif cls in (fields.IntegerField, fields.FloatField, fields.DurationField):
                        field_params.append("max_value: int = None")
                        field_params.append("min_value: int = None")
                    elif cls == fields.ChoiceField:
                        field_params.append("html_cutoff: int = fields.ChoiceField.html_cutoff")
                        field_params.append("html_cutoff_text: str = fields.ChoiceField.html_cutoff_text")
                        field_params.append("allow_blank: bool = False")
                    elif cls == fields.MultipleChoiceField:
                        field_params.append("allow_empty: bool = True")
                    elif cls == fields.FileField:
                        field_params.append("max_length: Optional[int] = None")
                        field_params.append("allow_empty_file: bool = False")
                    elif cls == fields.ListField:
                        field_params.append("child=fields.ListField.child")
                        field_params.append("allow_empty: bool = True")
                        field_params.append("max_length: Optional[int] = None")
                        field_params.append("min_length: Optional[int] = None")
                    elif cls in (fields.ListField, fields.DictField):
                        field_params.append("child=fields.DictField.child")
                        field_params.append("allow_empty: bool = True")
                    elif cls == fields.JSONField:
                        field_params.append("binary: bool = False")
                        field_params.append("encoder=None")
                        field_params.append("decoder=None")
                    elif cls == fields.ModelField:
                        field_params.append("max_length: Optional[int] = None")

                field_params.insert(0, "self")
                field_params.append("**kw")
                field_params = textwrap.wrap(
                    (", ".join(field_params)).replace(": ", ":_").replace(" = ", "_=_"),
                    width=102 if field_class != "HStoreField" else 98,
                    break_on_hyphens=False,
                )

                # Special case indentation for HStoreField
                if field_class != "HStoreField":
                    field_params = textwrap.indent("\n".join(field_params), " " * 17)
                else:
                    field_params = textwrap.indent("\n".join(field_params), " " * 21)

                field_params = field_params.lstrip(" ").replace(":_", ": ").replace("_=_", " = ")

                additional_inspects = ""
                if field_class in ("SerializerMethodField", "HiddenField", "ReadOnlyField"):
                    additional_inspects += (
                        "# noinspection PyAbstractClass" if not additional_inspects else ",PyAbstractClass"
                    )
                if "format" in field_params_names:
                    additional_inspects += (
                        "# noinspection PyShadowingBuiltins" if not additional_inspects else ",PyShadowingBuiltins"
                    )
                field_module = "fields." if field_class in fields.__dict__ else "relations."

                # Add additional_inspects and new line
                if additional_inspects:
                    print(
                        textwrap.dedent(
                            f"""
    
                            {additional_inspects}"""
                        ),
                        file=output,
                    )
                else:
                    print(textwrap.dedent("\n"), file=output)

                # Check if field has a dedicated mixin and add it to mixins
                additional_mixin = field_class + "Mixin, " if field_class + "Mixin" in field_mixins else ""
                if issubclass(field, fields.ChoiceField):
                    additional_mixin += "ChoiceMixin, EnableCopyMixin, "
                if issubclass(field, (relations.RelatedField, relations.ManyRelatedField)):
                    additional_mixin += "RelatedFieldAJAXMixin, "
                if issubclass(field, fields.CharField):
                    additional_mixin += "PasswordFieldMixin, "
                if issubclass(field, (fields.IntegerField, fields.DateTimeField, fields.DateField, fields.TimeField)):
                    additional_mixin += "NullValueMixin, "

                # Check if field is HStoreField to add wrapper and adjust indentation
                hstore_field_wrapper, hstore_field_indent = "", ""
                if field_class == "HStoreField":
                    hstore_field_wrapper = "if hasattr(fields, 'HStoreField'):\n"
                    hstore_field_indent = " " * 4

                drf_class = field_class
                if issubclass(field, RTFField) or issubclass(field, ColorField):
                    drf_class = fields.CharField.__name__  # noqa
                    field_module = "fields."  # noqa

                # Print class declaration
                print(hstore_field_wrapper, file=output, end="")
                class_def = (
                    f"{hstore_field_indent}class {field_class}({additional_mixin}"
                    + "FieldRenderMixin, ActionMixin, FieldHelpTextMixin, "
                    + f"ConditionalVisibilityMixin, {field_module}{drf_class}):"
                )
                class_def = textwrap.wrap(class_def, 120)
                print(class_def[0], file=output)
                class_def = textwrap.wrap(
                    "".join(class_def[1:]), 120 - len(f"{hstore_field_indent}class {field_class}(")
                )

                print(
                    textwrap.indent("\n".join(class_def), " " * len(f"{hstore_field_indent}class {field_class}(")),
                    file=output,
                    end="",
                )

                # Print constructor
                indt = lambda n: " " * (n + len(hstore_field_indent))
                print("", file=output)
                print(indt(4) + f"def __init__({field_params}):", file=output)

                if issubclass(field, fields.ReadOnlyField):
                    print(
                        indt(8) + "warnings.warn('deprecated - wrong approach! Use read_only attribute " "instead.',",
                        file=output,
                    )
                    print(indt(22) + "DeprecationWarning, stacklevel=2)", file=output)
                    print(indt(8) + "read_only = True  # NOQA", file=output)
                elif issubclass(field, fields.HiddenField):
                    print(
                        indt(8) + "warnings.warn('deprecated - wrong approach! Use display(|_table|_form) "
                        "attributes instead.',",
                        file=output,
                    )
                    print(indt(22) + "DeprecationWarning, stacklevel=2)", file=output)
                    print(indt(8) + "display = DisplayMode.HIDDEN  # NOQA", file=output)
                elif issubclass(field, (fields.DateField, fields.TimeField)):
                    print(indt(8) + "self.time_step = kw.pop('time_step', None)", file=output)

                print(
                    indt(8)
                    + f"kwargs = {{k: v for k, v in locals().items() if not k.startswith(('__', 'self', 'kw'))}}",  # noqa
                    file=output,
                )
                print(indt(8) + "kwargs.update(kw)", file=output)

                if issubclass(field, fields.JSONField):
                    print(
                        indt(8) + "if Version(drf_version, scheme=Pep440VersionScheme) < "
                        "Version('3.12', scheme=Pep440VersionScheme):",
                        file=output,
                    )
                    print(indt(12) + "kwargs.pop('decoder', None)", file=output)

                params = render_params[field]
                print(indt(8) + 'kwargs["render_params"] = kwargs.get("render_params", None) or {}', file=output)
                for key, value in params.items():
                    print(indt(8) + f'kwargs["render_params"].setdefault("{key}", {arepr(value)})', file=output)

                print(indt(8) + "super().__init__(**kwargs)", file=output)

    generated_file_path = os.path.abspath(os.path.join("dynamicforms/", "fields.py"))
    subprocess.run(["ruff", "check", "--fix", generated_file_path])

    print("fields.py successfully generated")
    # options['file']
