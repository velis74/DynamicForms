from rest_framework.fields import ChoiceField


class NullChoiceMixin(object):
    """
    Declaring ChoiceField's null_choice_text
      (what should be rendered for "no selection"; DRF's default is ---------)
      We also support user declaring a choice with None value and a different text (see hidden fields example)
    """

    @property
    def null_choice_text(self):
        res = "--------"
        if isinstance(self, ChoiceField) and not getattr(self, "get_queryset", None):
            # Only do this for true ChoiceFields. RelatedFields would run a query here
            # Possibly we will at some point have to enable this for relatedfields too
            for opt in self.iter_options():
                if opt.start_option_group or opt.end_option_group:
                    pass
                elif opt.value is None:
                    res = opt.display_text
        return res

    def iter_options_bound(self, value):
        # noinspection PyUnresolvedReferences
        return super().iter_options()
