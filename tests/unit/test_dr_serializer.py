from django.test import TestCase
from django.test.client import RequestFactory

from dynamicforms.template_render import ViewModeSerializer
from examples.rest.validated import ValidatedSerializer, ValidatedViewSet


class SerializerTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_show_filter(self):
        request = self.factory.get("/validated/")
        request.accepted_renderer = None

        viewset = ValidatedViewSet()
        viewset.request = request

        serializer = ValidatedSerializer(context={"request": request, "view": viewset})
        serializer.show_filter = True
        serializer.view_mode = ViewModeSerializer.ViewMode.TABLE_ROW
        serializer.apply_component_context(request)
        res = serializer.component_params(output_json=False)
        filter_value = res["filter"]
        self.assertIsNotNone(filter_value)

        serializer.show_filter = False
        res = serializer.component_params(output_json=False)
        filter_value = res["filter"]
        self.assertIsNone(filter_value)
