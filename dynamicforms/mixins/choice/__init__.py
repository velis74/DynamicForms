from .allow_tags import AllowTagsMixin
from .null_choice import NullChoiceMixin
from .single_choice import SingleChoiceMixin


class ChoiceMixin(AllowTagsMixin, NullChoiceMixin, SingleChoiceMixin):
    def __init__(self, *args, **kwargs):
        choices = kwargs.get("choices", [])
        kwargs["choices"] = [choice[:2] for choice in choices]
        self.choice_icons = {choice[0]: choice[2] for choice in choices if len(choice) > 2}
        super().__init__(*args, **kwargs)

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
        for k, v in choices_dict.items():
            yield dict(id=k, text=v, icon=self.choice_icons.get(k, None))
