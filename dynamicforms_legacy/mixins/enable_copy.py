class EnableCopyMixin(object):
    def __init__(self, *args, enable_copy=False, **kwargs):
        super().__init__(*args, **kwargs)
        self.enable_copy = enable_copy or False
