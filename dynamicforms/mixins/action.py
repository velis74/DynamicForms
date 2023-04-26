from dynamicforms.action import Actions


class ActionMixin(object):
    """
    Used in fields allowing declaration of actions that happen when field values change
    """

    def __init__(self, *args, actions: Actions = None, **kwargs):
        super().__init__(*args, **kwargs)
        act = actions or Actions(None)
        act.actions.extend(getattr(self, "actions", Actions()).actions)
        # Obtain a personalised list of actions
        self.actions = act.get_resolved_copy(self)
