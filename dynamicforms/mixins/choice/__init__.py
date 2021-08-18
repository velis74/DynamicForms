from .allow_tags import AllowTagsMixin
from .null_choice import NullChoiceMixin
from .single_choice import SingleChoiceMixin


class ChoiceMixin(AllowTagsMixin, NullChoiceMixin, SingleChoiceMixin):

    def as_component_def(self) -> dict:
        try:
            res = super().as_component_def()  # noqa
        except AttributeError:
            res = dict()

        res.update(dict(choices=self.__to_list_of_dicts(self.choices)))  # noqa - choices is a member of DRF ChoiceField
        return res

    def __to_list_of_dicts(self, choices_dict: dict) -> list:
        for k, v in choices_dict.items():
            yield dict(id=k, text=v)