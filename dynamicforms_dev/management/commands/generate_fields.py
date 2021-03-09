import inspect
import os
import textwrap
import typing
import uuid

from django.core.management.base import BaseCommand
from rest_framework import fields, relations


class RTFField(object):
    pass


class Command(BaseCommand):
    help = 'Generate Field classes from DRF with applied DynamicForms mixins'

    # def add_arguments(self, parser):
    #     parser.add_argument('-dest', dest='file', type=str, default='strings.xlsx', action='store',
    #                         help='filename where to store the strings')

    def handle(self, *args, **options):
        from dynamicforms.mixins import (
            RenderMixin, ActionMixin, AllowTagsMixin, NullChoiceMixin,
            RelatedFieldAJAXMixin, PasswordFieldMixin, NullValueMixin,
            SingleChoiceMixin
        )
        from dynamicforms import mixins, action

        with open(os.path.abspath(os.path.join('dynamicforms/', 'fields.py')), 'w') as output:

            field_list = []
            for obj in fields.__dict__.values():
                if obj != fields.Field and inspect.isclass(obj) and \
                        issubclass(obj, fields.Field) and not obj.__name__.startswith('_'):
                    field_list.append(obj)

            for obj in relations.__dict__.values():
                if obj != relations.RelatedField and inspect.isclass(obj) and \
                        (issubclass(obj, relations.RelatedField) or issubclass(obj, relations.ManyRelatedField)) and \
                        obj.__name__.endswith('Field'):
                    field_list.append(obj)

            field_list.append(RTFField)

            # get all the field-specific mixins
            field_mixins = [f.__name__ + 'Mixin' for f in field_list if f.__name__ + 'Mixin' in mixins.__dict__]

            print('import warnings', file=output)
            print('from typing import Optional', file=output)
            print('from uuid import UUID\n', file=output)
            print('from rest_framework import fields, relations\n', file=output)
            print('from .action import Actions', file=output)

            print('from .mixins import (', file=output, end='')
            print('\n    '.join(
                [''] +
                textwrap.wrap(
                    'ActionMixin, RenderMixin, DisplayMode, AllowTagsMixin, NullChoiceMixin, RelatedFieldAJAXMixin, ' +
                    'FieldHelpTextMixin, PasswordFieldMixin, NullValueMixin, EnableCopyMixin, ' + ', '.join(
                        field_mixins), 115)
            ), file=output)
            print(')', file=output)

            for field in field_list:
                field_class = field.__name__
                field_params, field_params_names = [], set()
                param_classes = []
                for cls in enumerate(field.__mro__):
                    param_classes.append(cls)
                    if cls[1] == fields.Field:
                        break
                if issubclass(field, fields.ChoiceField):
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
                param_classes.append((0, RenderMixin))

                skip_depth = 0
                for depth, cls in param_classes:
                    if depth > skip_depth:
                        continue
                    skip_depth = 0

                    if hasattr(cls, '__init__'):
                        had_kwds = False
                        for parm in inspect.signature(cls.__init__).parameters.values():

                            if field_class in ('BooleanField', 'NullBooleanField') and parm.name == 'allow_null':
                                # BooleanField and NullBooleanField don't like this one
                                continue

                            parm_str = parm.name
                            if parm_str == 'self' or parm.kind in (parm.VAR_KEYWORD, parm.VAR_POSITIONAL):
                                # we don't repeat all the self fields there are. Not all the *args && **kwds
                                had_kwds |= parm.kind == parm.VAR_KEYWORD
                                continue
                            if depth and len(field_params) and \
                                    (parm.kind == parm.POSITIONAL_ONLY or
                                     (parm.kind == parm.POSITIONAL_OR_KEYWORD and parm.default == inspect._empty)
                                    ):
                                # positional arguments can only be declared before any keyword ones
                                continue

                            p_an = parm.annotation
                            p_def = parm.default

                            if field_class == 'ManyRelatedField' and parm.name == 'allow_null':
                                p_def = True  # ManyRelatedField CAN of course live without any values being set

                            if p_an != inspect._empty:
                                if isinstance(p_an, (str, int, float, bool,)) or p_an is None:
                                    parm_str += ': ' + repr(p_an)
                                elif inspect.isclass(p_an) and issubclass(p_an, (str, int, float, bool,)):
                                    parm_str += ': ' + p_an.__name__
                                elif p_an in (uuid.UUID, action.Actions):
                                    parm_str += ': ' + p_an.__name__
                                elif p_an == typing.Union[str, None]:
                                    parm_str += ': Optional[str]'
                                elif p_an == typing.Union[dict, None]:
                                    parm_str += ': Optional[dict]'
                                else:
                                    # if you get this error, you need to add the type to includes at the top
                                    # of this function and then implement the actual printing just above here
                                    print(f'Error: parameter {parm.name} annotation is of unknown type '
                                          f'{parm.annotation}.')

                            if p_def != inspect._empty:
                                equals = ' = ' if ':' in parm_str else '='
                                if isinstance(p_def, (str, int, float, bool,)) or p_def is None:
                                    parm_str += equals + repr(p_def)
                                elif p_def in (fields.empty,):
                                    parm_str += equals + '.'.join((p_def.__module__.split('.')[-1], p_def.__name__))
                                else:
                                    print(f'Error: parameter {parm.name} default is of unknown type {parm.default}.')

                            if parm.name not in field_params_names:
                                field_params_names.add(parm.name)
                                field_params.append(parm_str)

                        if had_kwds:
                            skip_depth = depth + 1

                field_params.insert(0, 'self')
                field_params.append('**kw')
                field_params = textwrap.wrap((', '.join(field_params)).replace(': ', ':_').replace(' = ', '_=_'),
                                             width=102 if field_class != 'HStoreField' else 98)

                # Special case indentation for HStoreField
                if field_class != 'HStoreField':
                    field_params = textwrap.indent('\n'.join(field_params), ' ' * 17)
                else:
                    field_params = textwrap.indent('\n'.join(field_params), ' ' * 21)

                field_params = field_params.lstrip(' ').replace(':_', ': ').replace('_=_', ' = ')

                additional_inspects = ''
                if field_class in ('SerializerMethodField', 'HiddenField', 'ReadOnlyField'):
                    additional_inspects += '# noinspection PyAbstractClass' if not additional_inspects else ',PyAbstractClass'
                if 'format' in field_params_names:
                    additional_inspects += '# noinspection PyShadowingBuiltins' if not additional_inspects else ',PyShadowingBuiltins'
                field_module = 'fields.' if field_class in fields.__dict__ else 'relations.'

                # Add additional_inspects and new line
                if additional_inspects:
                    print(textwrap.dedent(f"""

                        {additional_inspects}"""), file=output)
                else:
                    print(textwrap.dedent('\n'), file=output)

                # Check if field has a dedicated mixin and add it to mixins
                additional_mixin = field_class + 'Mixin, ' if field_class + 'Mixin' in field_mixins else ''
                if issubclass(field, fields.ChoiceField):
                    additional_mixin += 'AllowTagsMixin, NullChoiceMixin, EnableCopyMixin, SingleChoiceMixin, '
                if issubclass(field, (relations.RelatedField, relations.ManyRelatedField)):
                    additional_mixin += 'RelatedFieldAJAXMixin, '
                if issubclass(field, fields.CharField):
                    additional_mixin += 'PasswordFieldMixin, '
                if issubclass(field, (fields.IntegerField, fields.DateTimeField, fields.DateField, fields.TimeField)):
                    additional_mixin += 'NullValueMixin, '

                # Check if field is HStoreField to add wrapper and adjust indentation
                hstore_field_wrapper, hstore_field_indent = '', ''
                if field_class == 'HStoreField':
                    hstore_field_wrapper = "if hasattr(fields, 'HStoreField'):\n"
                    hstore_field_indent = ' ' * 4

                drf_class = field_class
                if issubclass(field, RTFField):
                    drf_class = fields.CharField.__name__
                    field_module = "fields."

                # Print class declaration
                print(hstore_field_wrapper, file=output, end='')
                class_def = f'{hstore_field_indent}class {field_class}({additional_mixin}' + \
                            f'RenderMixin, ActionMixin, FieldHelpTextMixin, {field_module}{drf_class}):'
                class_def = textwrap.wrap(class_def, 120)
                print(class_def[0], file=output)
                class_def = textwrap.wrap(''.join(class_def[1:]),
                                          120 - len(f'{hstore_field_indent}class {field_class}('))

                print(textwrap.indent("\n".join(class_def), ' ' * len(f'{hstore_field_indent}class {field_class}(')),
                      file=output, end='')

                # Print constructor
                indt = lambda n: ' ' * (n + len(hstore_field_indent))
                print(f'', file=output)
                print(indt(4) + f'def __init__({field_params}):', file=output)

                if issubclass(field, fields.ReadOnlyField):
                    print(indt(8) + "warnings.warn('deprecated - wrong approach! Use read_only attribute "
                                    "instead.',", file=output)
                    print(indt(22) + "DeprecationWarning, stacklevel=2)", file=output)
                    print(indt(8) + "read_only = True  # NOQA", file=output)
                elif issubclass(field, fields.HiddenField):
                    print(indt(8) + "warnings.warn('deprecated - wrong approach! Use display(|_table|_form) "
                                    "attributes instead.',", file=output)
                    print(indt(22) + "DeprecationWarning, stacklevel=2)", file=output)
                    print(indt(8) + "display = DisplayMode.HIDDEN  # NOQA", file=output)
                elif issubclass(field, (fields.DateField, fields.TimeField)):
                    print(indt(8) + "self.time_step = kw.pop('time_step', None)", file=output)

                print(
                    indt(8) +
                    f"kwargs = {{k: v for k, v in locals().items() if not k.startswith(('__', 'self', 'kw'))}}",
                    file=output)
                print(indt(8) + f'kwargs.update(kw)', file=output)

                print(indt(8) + f'super().__init__(**kwargs)', file=output)

    print('fields.py successfully generated')
    # options['file']
