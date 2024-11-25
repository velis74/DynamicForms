import datetime
import json

import rest_framework.pagination as drf_p

from django.db.models import DurationField, F, Q


class CursorPagination(drf_p.CursorPagination):
    ordering = "pk"
    NONE_VALUE = "{`None`}"

    # noinspection PyAttributeOutsideInit
    def paginate_queryset(self, queryset, request, view=None):
        self.page_size = self.get_page_size(request)
        if not self.page_size:
            return None

        self.base_url = request.build_absolute_uri()
        self.ordering = self.get_ordering(request, queryset, view)
        if not any(field in self.ordering for field in ('id', '-id', 'pk', '-pk')):
            ordering = list(self.ordering)
            ordering.append("id")
            self.ordering = tuple(ordering)

        self.cursor = self.decode_cursor(request)
        if self.cursor is None:
            (offset, reverse, current_position) = (0, False, None)
        else:
            (offset, reverse, current_position) = self.cursor
        try:
            if current_position:
                current_position = json.loads(current_position)
        except TypeError:
            current_position = None

        # Cursor pagination always enforces an ordering.
        ordering = drf_p._reverse_ordering(self.ordering) if reverse else self.ordering
        # Currently we force nulls_first in ascending order and nulls_last in descending order
        ordering = [
            getattr(F(fld.lstrip("-+")), "desc" if fld.startswith("-") else "asc")(
                **{"nulls_last" if fld.startswith(("-", "++")) and not fld.startswith("--") else "nulls_first": True}
            )
            for fld in ordering
        ]
        queryset = queryset.order_by(*ordering)

        # If we have a cursor with a fixed position then filter by that.
        if current_position is not None:

            def filter_segment(segment_len):
                kwargs = {}
                args = []
                for idx in range(segment_len):
                    order = self.ordering[idx]
                    is_reversed = order.startswith("-")
                    order_attr = order.lstrip("-")
                    attr_value = self.field_to_python(queryset, order_attr, current_position[order_attr])

                    # Test for: (cursor reversed) XOR (queryset reversed)
                    if idx < segment_len - 1:
                        # if this is the last field in this segment
                        if attr_value == self.NONE_VALUE:
                            kwargs[order_attr + "__isnull"] = True
                        else:
                            kwargs[order_attr] = attr_value
                    elif self.cursor.reverse != is_reversed:
                        if attr_value == self.NONE_VALUE:
                            # It is impossible to go lower than None... so we just omit this segment
                            return None
                        else:
                            args.append(Q(**{order_attr + "__lt": attr_value}) | Q(**{order_attr + "__isnull": True}))
                    else:
                        if attr_value == self.NONE_VALUE:
                            kwargs[order_attr + "__isnull"] = False
                        else:
                            kwargs[order_attr + "__gt"] = attr_value

                return Q(**kwargs) & Q(*args)

            fltr = Q()
            for seg_len in range(len(self.ordering)):
                new_segment = filter_segment(seg_len + 1)
                if new_segment:
                    fltr = fltr | new_segment
            queryset = queryset.filter(fltr)

        # If we have an offset cursor then offset the entire page by that amount.
        # We also always fetch an extra item in order to determine if there is a
        # page following on from this one.
        results = list(queryset[offset : offset + self.page_size + 1])
        self.page = list(results[: self.page_size])
        if not self.page:
            # In rest_framework/pagination.py/get_previous_link is expected that self.page is not empty
            # if cursor offset != 0
            self.cursor = drf_p.Cursor(offset=0, reverse=False, position=None)

        # DF: contrary to DRF's implementation we always provide the "prev" and "next" links as there may appear
        # new records before / after the ones we already read. Mechanism for detecting whether they actually appeared
        # is another matter altogether :)
        if current_position is None and results:
            self.cursor = drf_p.Cursor(offset=0, reverse=False, position=None)
            current_position = self._get_position_from_instance(results[0], self.ordering)
        elif isinstance(current_position, dict):
            current_position = json.dumps(current_position)

        # Determine the position of the final item following the page.
        has_following_position = bool(results)  # len(results) > len(self.page)

        # DF: contrary to DRF's implementation we always provide the "next" link as there may appear new records after
        # the last one read
        following_position = self._get_position_from_instance(results[-1], self.ordering) if results else None

        if reverse:
            # If we have a reverse queryset, then the query ordering was in reverse
            # so we need to reverse the items again before returning them to the user.
            self.page = list(reversed(self.page))

            # Determine next and previous positions for reverse cursors.
            self.has_next = (current_position is not None) or (offset > 0)
            self.has_previous = has_following_position
            if self.has_next:
                self.next_position = current_position
            if self.has_previous:
                self.previous_position = following_position
        else:
            # Determine next and previous positions for forward cursors.
            self.has_next = has_following_position
            self.has_previous = (current_position is not None) or (offset > 0)
            if self.has_next:
                self.next_position = following_position
            if self.has_previous:
                self.previous_position = current_position

        # Display page controls in the browsable API if there is more
        # than one page.
        if (self.has_previous or self.has_next) and self.template is not None:
            self.display_page_controls = True

        return self.page


    def _get_position_from_instance(self, instance, ordering):
        def process_field(idx):
            field_name = ordering[idx].lstrip("-")
            attr = None
            if isinstance(instance, dict):
                attr = instance[field_name]
            else:
                field_name_list = field_name.split("__")
                for fn in field_name_list:
                    attr = getattr(instance if attr is None else attr, fn)
            return field_name, self.field_to_representation(attr)

        return json.dumps({k: v for k, v in map(lambda idx: process_field(idx), range(len(ordering)))})


    def field_to_representation(self, value):
        """
        Converts field value to something that will be later understood by QuerySet.filter()
        Question: why does DRF not do this? is str(value) always enough?
        """
        if isinstance(value, datetime.timedelta):
            return str(value.total_seconds())
        elif value is None:
            return self.NONE_VALUE
        return str(value)


    def field_to_python(self, queryset, order_attr, value):
        if order_attr in queryset.query.annotations:
            field = queryset.query.annotations.get(order_attr).field
        else:
            # noinspection PyProtectedMember
            field = queryset.model._meta.get_field(order_attr)
        if isinstance(field, DurationField):
            return datetime.timedelta(seconds=float(value))
        return value
