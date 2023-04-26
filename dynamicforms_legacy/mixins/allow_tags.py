# TODO: Implementation of this mixin is wrong for ChoiceField (single choice variant):
#  The ChoiceField will return data in an array even for (Single)ChoiceField. Select2 handles this, maybe even requires
#  this, but some other component might not
import ast

from rest_framework.fields import ChoiceField, MultipleChoiceField


class DenormalisedArray(list):
    def __init__(self, lst, field):
        self.field = field
        if lst is not None and isinstance(lst, str) and isinstance(field, MultipleChoiceField):
            for itm in ast.literal_eval(lst):
                self.append(itm)

        elif lst is not None and isinstance(lst, list):
            for itm in lst:
                self.append(itm)

        elif lst is not None:
            self.append(lst)

    def __str__(self):
        choices = self.field.choices
        ret = ""
        count = 0
        for item in self:
            ret += ", " if count else ""
            if item in choices:
                ret += choices[item]
            else:
                ret += item
            count += 1
        return ret


class AllowTagsMixin(object):
    def __init__(self, *args, allow_tags=False, **kwargs):
        super().__init__(*args, **kwargs)
        self.allow_tags = allow_tags or False

    def to_internal_value(self, data):
        """
        Validator is taken directly from DRF and updated, to check for allow_tags.
        Option allow_tags enables adding value that is not on the options list.
        """
        if not self.allow_tags:
            data = super().to_internal_value(data)

        if isinstance(self, MultipleChoiceField):
            if isinstance(data, str) or not hasattr(data, "__iter__"):
                self.fail("not_a_list", input_type=type(data).__name__)
            if not self.allow_empty and len(data) == 0:
                self.fail("empty")

            return data

        elif isinstance(self, ChoiceField) and not isinstance(self, MultipleChoiceField):
            if data == "" and self.allow_blank:
                return ""

            try:
                if not self.allow_tags:
                    return self.choice_strings_to_values[str(data)]

                return data
            except KeyError:
                self.fail("invalid_choice", input=data)

    def to_representation(self, value, row_data=None):
        if isinstance(self, ChoiceField) and self.allow_tags and value:
            return DenormalisedArray(value, self)

        return super().to_representation(value, row_data)

    def iter_options_bound(self, value):
        # noinspection PyUnresolvedReferences
        if isinstance(value, list):
            for item in value:
                if item not in self.choices.keys():
                    self.grouped_choices[item] = item
        elif isinstance(value, str) and self.allow_tags and value not in self.choices.keys():
            self.grouped_choices[value] = value

        return super().iter_options_bound(value)
