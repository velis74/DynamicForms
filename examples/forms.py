from dynamicforms import Form
from dynamicforms.fields import IntegerField
from dynamicforms.js.actions import Visible
from dynamicforms.js.conditions import CFieldValue
from .models import Validated


class ValidatedForm(Form):
    base_class = Validated

    # Hm, current declarations don't allow for actually specifying the condition / action because we don't have
    # the fields instantiated and available yet (they will construct based on base_class)

    # The following line suggests replacing them temporarily with base model fields which will be matched to actual
    # form fields in the __init__ constructor

    # Also see the overridden __init__ for an example of doing exactly the same once we have the fields constructed

    # amount = IntegerField(Validated.amount, Visible(Validated.amount, condition=CFieldValue(Validated.enabled, True)))

    def __init__(self, *args, **kwargs):
        super().__init__(self, *args, **kwargs)
        self.fields['item_flags'].multiple = ''

        # dynamic setup for amount field
        self.fields['amount'].add_action(
            Visible(self.fields['amount'], condition=CFieldValue(self.fields['enabled'], True))
        )