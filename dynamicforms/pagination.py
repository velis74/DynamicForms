import datetime
import json

from django.db.models import DurationField, Q
from rest_framework.pagination import _reverse_ordering, Cursor, CursorPagination as Cp


class CursorPagination(Cp):
    ordering = 'pk'

    # noinspection PyAttributeOutsideInit
    def paginate_queryset(self, queryset, request, view=None):
        self.page_size = self.get_page_size(request)
        if not self.page_size:
            return None

        self.base_url = request.build_absolute_uri()
        self.ordering = self.get_ordering(request, queryset, view)

        self.cursor = self.decode_cursor(request)
        if self.cursor is None:
            (offset, reverse, current_position) = (0, False, None)
        else:
            (offset, reverse, current_position) = self.cursor
        try:
            current_position = json.loads(current_position)
        except TypeError:
            current_position = None

        # Cursor pagination always enforces an ordering.
        if reverse:
            queryset = queryset.order_by(*_reverse_ordering(self.ordering))
        else:
            queryset = queryset.order_by(*self.ordering)

        # If we have a cursor with a fixed position then filter by that.
        if current_position is not None:

            def filter_segment(segment_len):
                kwargs = {}
                for idx in range(segment_len):
                    order = self.ordering[idx]
                    is_reversed = order.startswith('-')
                    order_attr = order.lstrip('-')
                    attr_value = self.field_to_python(queryset, order_attr, current_position[order_attr])

                    # Test for: (cursor reversed) XOR (queryset reversed)
                    if idx < segment_len - 1:
                        # if this is the last field in this segment
                        kwargs[order_attr] = attr_value
                    elif self.cursor.reverse != is_reversed:
                        kwargs[order_attr + '__lt'] = attr_value
                    else:
                        kwargs[order_attr + '__gt'] = attr_value

                return Q(**kwargs)

            fltr = Q()
            for segment_len in range(len(self.ordering)):
                fltr = fltr | filter_segment(segment_len + 1)

            queryset = queryset.filter(fltr)

        # If we have an offset cursor then offset the entire page by that amount.
        # We also always fetch an extra item in order to determine if there is a
        # page following on from this one.
        results = list(queryset[offset:offset + self.page_size + 1])
        self.page = list(results[:self.page_size])

        # DF: contrary to DRF's implementation we always provide the "prev" and "next" links as there may appear
        # new records before / after the ones we already read. Mechanism for detecting whether they actually appeared
        # is another matter altogether :)
        if current_position is None and results:
            self.cursor = Cursor(offset=0, reverse=False, position=None)
            current_position = self._get_position_from_instance(results[0], self.ordering)

        # Determine the position of the final item following the page.
        has_following_position = True  # len(results) > len(self.page)

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
            field_name = ordering[idx].lstrip('-')
            if isinstance(instance, dict):
                attr = instance[field_name]
            else:
                attr = getattr(instance, field_name)
            return field_name, self.field_to_representation(attr)

        return json.dumps({k: v for k, v in map(lambda idx: process_field(idx), range(len(ordering)))})

    def field_to_representation(self, value):
        """
        Converts field value to something that will be later understood by QuerySet.filter()
        Question: why does DRF not do this? is str(value) always enough?
        """
        if isinstance(value, datetime.timedelta):
            return str(value.total_seconds())
        return str(value)

    def field_to_python(self, queryset, order_attr, value):
        if isinstance(queryset.model._meta.get_field(order_attr), DurationField):
            return datetime.timedelta(seconds=float(value))
        return value