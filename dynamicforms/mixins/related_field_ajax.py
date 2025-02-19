import sys

from typing import Optional

from django.db.models.manager import BaseManager
from django.urls import reverse
from django.utils.http import urlencode
from rest_framework.relations import RelatedField


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
        **kwargs,
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
        return urlencode(self.additional_parameters) if self.additional_parameters else None

    # noinspection PyUnresolvedReferences
    def iter_options_bound(self, value):
        if self.url_reverse:
            if value is None:
                return [dict(value="", display_text=self.placeholder)]
            try:
                if hasattr(self, "child_relation"):
                    itm = self.child_relation
                    qry = itm.get_queryset()
                    if value != "__all__":
                        qry = qry.filter(pk__in=value)
                else:
                    itm = self
                    qry = self.get_queryset()
                    if value != "__all__":
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
                    additional_parameters=self.additional_parameters_urlencoded,
                    query_field=self.query_field,
                    value_field=self.value_field,
                    text_field=self.text_field,
                )
            )
            res.update(ajax)
            qs_count = self.get_queryset().count()

            if qs_count and qs_count <= 10:
                res.update(
                    choices=map(
                        lambda option: dict(id=option["value"], text=option["display_text"]),
                        self.iter_options_bound("__all__"),
                    )
                )
        else:
            res.update(
                choices=list(map(
                    lambda option: dict(id=option.value, text=option.display_text), self.iter_options_bound(None)
                )
            ))
            if len(res["choices"]) > 100:
                print(
                    f"WARNING: {self.parent.__class__.__name__}.{self.field_name} has more than 100 choices and "
                    f"should be converted to AJAX.",
                    file=sys.stderr
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
        from dynamicforms.fields import ManyRelatedField

        if isinstance(self, ManyRelatedField):
            # Hm, not sure if this is the final thing to do: an example of this field is in
            # ALC plane editor (modes of takeoff). However, value is a queryset here. There seem to still be DB queries
            # However, in the example I have, the problem is solved by doing prefetch_related on the m2m relation
            cr = self.child_relation
            if isinstance(value, BaseManager):
                value = value.all()
            if value is None:
                return ""
            return ", ".join((cr.display_value(item) for item in value))
            # return ', '.join((cr.display_value(item) for item in cr.get_queryset().filter(pk__in=value)))
        elif isinstance(self, RelatedField):
            return self.display_value(value)

        return value

    @classmethod
    def many_init(cls, *args, **kwargs):
        list_kwargs = {"child_relation": cls(*args, **kwargs)}
        from dynamicforms.fields import ManyRelatedField

        return ManyRelatedField(
            display_form=kwargs.get("display_form"), display_table=kwargs.get("display_table"), **list_kwargs
        )
