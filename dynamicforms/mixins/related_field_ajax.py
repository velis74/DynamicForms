from typing import Optional

from django.urls import reverse
from rest_framework.relations import ManyRelatedField, RelatedField
from rest_framework.serializers import ListSerializer


class RelatedFieldAJAXMixin(object):
    def __init__(
        self,
        *args,
        url_reverse: Optional[str] = None,
        placeholder: Optional[str] = None,
        additional_parameters: Optional[dict] = None,
        query_field: str = "query",
        value_field: str = "choice_id",
        text_field: str = "choice_text",
        **kwargs
    ):
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
        self.value_field = value_field
        self.text_field = text_field

    @property
    def additional_parameters_urlencoded(self):
        from django.utils.http import urlencode

        return "?" + urlencode(self.additional_parameters)

    # noinspection PyUnresolvedReferences
    def iter_options_bound(self, value):
        if self.url_reverse:
            if value is None:
                return [dict(value="", display_text=self.placeholder)]
            try:
                if hasattr(self, "child_relation"):
                    itm = self.child_relation
                    qry = itm.get_queryset()
                    qry = qry.filter(pk__in=value)
                else:
                    itm = self
                    qry = self.get_queryset()
                    qry = qry.filter(pk=value)

                return [dict(value=rec.id, display_text=itm.display_value(rec)) for rec in qry.all()]
            except:
                return []
        return super().iter_options()

    def as_component_def(self) -> dict:
        try:
            res = super().as_component_def()  # noqa
        except AttributeError:
            res = dict()
        if self.url_reverse:
            ajax = dict(
                ajax=dict(
                    url_reverse=reverse(self.url_reverse, kwargs=dict(format="json")),
                    placeholder=self.placeholder,
                    additional_parameters=self.additional_parameters,
                    query_field=self.query_field,
                    value_field=self.value_field,
                    text_field=self.text_field,
                )
            )
            res.update(ajax)
        else:
            res.update(
                choices=map(
                    lambda option: dict(id=option.value, text=option.display_text), self.iter_options_bound(None)
                )
            )
        return res

    # noinspection PyUnusedLocal, PyUnresolvedReferences
    def render_to_table(self, value, row_data):
        """
        Renders field value for table view :if rendering to html table, let's try to resolve any lookups
        hidden fields will render to tr data-field_name attributes, so we maybe want to have ids, not text there,
          but that's up to front end to decide

        :param value: field value
        :param row_data: data for entire row (for more complex renderers)
        :return: rendered value for table view
        """
        if isinstance(self, ManyRelatedField):
            # Hm, not sure if this is the final thing to do: an example of this field is in
            # ALC plane editor (modes of takeoff). However, value is a queryset here. There seem to still be DB queries
            # However, in the example I have, the problem is solved by doing prefetch_related on the m2m relation
            cr = self.child_relation
            return ", ".join((cr.display_value(item) for item in value))
            # return ', '.join((cr.display_value(item) for item in cr.get_queryset().filter(pk__in=value)))
        elif isinstance(self, RelatedField):
            return self.display_value(value)

        return value

    # noinspection PyUnresolvedReferences
    def to_internal_value(self, data):
        """
        Reverse of to_representation: if data coming in is a tuple, use just the "id/code/key" part, not entire tuple
        """
        if (
            self.field_name not in ("df_control_data", "df_prev_id", "row_css_style")
            and not isinstance(self, ListSerializer)
            and isinstance(data, list)
        ):
            data = data[0]

        return super().to_internal_value(data)
