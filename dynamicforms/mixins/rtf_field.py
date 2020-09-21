class RTFFieldMixin:
    def __init__(self, **kw):
        kwargs = dict(
            max_length=None,
            min_length=None,
        )
        for k, v in filter(lambda t: next(iter(t), None) and not t[0].startswith(('__', 'self', 'kw')),
                           locals().items()):
            kwargs[k] = v
        kwargs.update(kw)
        if kwargs.get('style', None) is None:
            kwargs['style'] = dict(
                base_template='rtf_field.html',
            )
        super().__init__(**kwargs)
