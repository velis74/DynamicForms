class FileFieldMixin(object):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        # noinspection PyUnresolvedReferences
        self.style.setdefault("no_filter", True)
