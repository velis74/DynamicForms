from typing import Optional


class RelatedFieldAJAXMixin(object):

    def __init__(self, *args, url_reverse: Optional[str] = None, placeholder: Optional[str] = None,
                 additional_parameters: Optional[dict] = None, query_field: str = 'query', **kwargs):
        """
        Allows us to use AJAX to populate select2 options instead of pre-populating at render time

        :param args:
        :param url_reverse: reverse url to ViewSet providing the JSON data
        :param placeholder: select2 placeholder to display until user selects a value
        :param additional_parameters: additional parameters to be sent to ViewSet as part of the query
        :param query_field: field against which user search will be performed
        :param kwargs:
        """
        super().__init__(*args, **kwargs)
        self.url_reverse = url_reverse
        self.placeholder = placeholder
        self.additional_parameters = additional_parameters
        self.query_field = query_field

    @property
    def additional_parameters_urlencoded(self):
        from django.utils.http import urlencode
        return '?' + urlencode(self.additional_parameters)

    # noinspection PyUnresolvedReferences
    def iter_options_bound(self, value):
        if self.url_reverse:
            if value is None:
                return [dict(value="", display_text=self.placeholder)]
            qry = self.get_queryset()
            try:
                qry = qry.filter(pk=value)
                return [dict(value=value, display_text=self.display_value(qry.first()))]
            except:
                return []
        return super().iter_options()
