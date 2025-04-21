from typing import Hashable, Tuple

from rest_framework.fields import MultipleChoiceField
from rest_framework.relations import ManyRelatedField, PKOnlyObject, RelatedField
from rest_framework.serializers import ListSerializer

from .allow_tags import AllowTagsMixin, DenormalisedArray
from .null_choice import NullChoiceMixin
from .single_choice import SingleChoiceMixin


def parse_choice_icon(choice: Tuple[str]):
    if len(choice) > 2:
        return choice[2]
    return getattr(choice[1], 'icon', None)  # choice.description is a IconisedString

class ChoiceMixin(AllowTagsMixin, NullChoiceMixin, SingleChoiceMixin):
    def __init__(self, *args, **kwargs):
        choices = kwargs.get("choices", [])
        kwargs["choices"] = [choice[:2] for choice in choices]
        self.choice_icons = {choice[0]: parse_choice_icon(choice) for choice in choices if parse_choice_icon(choice)}
        super().__init__(*args, **kwargs)
        if len(choices) > 100:
            from dynamicforms.utils import print_field_declaration_line
            print_field_declaration_line()


    def as_component_def(self) -> dict:
        try:
            res = super().as_component_def()  # noqa
        except AttributeError:
            res = dict()

        res.update(
            dict(
                choices=self.__to_list_of_dicts(self.choices),
                allow_tags=self.allow_tags,  # noqa
                allow_null=self.allow_null or self.allow_blank or self.allow_tags,  # noqa
            )
        )
        return res

    def __to_list_of_dicts(self, choices_dict: dict) -> list:
        return [dict(id=k, text=v, icon=self.choice_icons.get(k, None)) for k, v in choices_dict.items()]

    # noinspection PyUnusedLocal, PyUnresolvedReferences
    def render_to_table(self, value, row_data):
        """
        Renders field value for table view :if rendering to html table, let's try to resolve any lookups
        hidden fields will render to tr data-field_name attributes, so we maybe want to have ids, not text there,
          but that's up to front end to decide

        :param value: field value
        :param row_data: data for entire row (for more complex renderers)
        :return: rendered value for table view
        """
        if isinstance(self, MultipleChoiceField):
            res = DenormalisedArray(value, self)
            return str(res)

        get_queryset = getattr(self, "get_queryset", None)

        if isinstance(self, ManyRelatedField):
            # Hm, not sure if this is the final thing to do: an example of this field is in
            # ALC plane editor (modes of takeoff). However, value is a queryset here. There seem to still be DB queries
            # However, in the example I have, the problem is solved by doing prefetch_related on the m2m relation
            cr = self.child_relation
            return ", ".join((cr.display_value(item) for item in value))
            # return ', '.join((cr.display_value(item) for item in cr.get_queryset().filter(pk__in=value)))
        elif isinstance(self, RelatedField) or get_queryset:
            return self.display_value(value)
        else:
            choices = getattr(self, "choices", {})

        # Now that we got our choices for related & choice fields, let's first get the value as it would be by DRF
        check_for_none = value.pk if isinstance(value, PKOnlyObject) else value
        if check_for_none is None:
            value = None

        if isinstance(value, Hashable) and value in choices:
            # choice field: let's render display names, not values
            value = choices[value]

        return value

    # noinspection PyUnresolvedReferences
    def to_internal_value(self, data):
        """
        Reverse of to_representation: if data coming in is a tuple, use just the "id/code/key" part, not entire tuple
        """
        if (
            self.field_name not in ("df_control_data", "df_prev_id", "row_css_style")
            and not isinstance(self, (ListSerializer, MultipleChoiceField))
            and isinstance(data, list)
            and len(data)
        ):
            data = data[0]

        return super().to_internal_value(data)
