from .filter import FilterSerializer, FilterViewSet


class CalculatedCssClassForTableRowSerializer(FilterSerializer):
    template_context = dict(url_reverse="calculated-css-class-for-table-row")
    form_titles = {
        "table": "Table with calculated css style for row",
        "new": "New object",
        "edit": "Editing object",
    }

    def get_row_css_style(self, obj):
        if obj:
            return (
                "color:gold;font-weight:bold;background-color:steelblue;"
                if obj.char_field and "abc" in obj.char_field
                else ""
            )
        return ""

    class Meta(FilterSerializer.Meta):
        pass


class CalculatedCssClassForTableRowViewSet(FilterViewSet):
    serializer_class = CalculatedCssClassForTableRowSerializer
