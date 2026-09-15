"""
DynamicModelSerializerMixin.__init__() used to do `self.Meta.model = model` - since `self.Meta`
resolves to the serializer CLASS's `Meta` unless shadowed, this mutated a shared class attribute
instead of an instance one. Any other instance of the same serializer class (including ones already
constructed, or ones built moments later by a concurrent/unrelated request) would see whichever
model the LAST instantiation happened to resolve, instead of its own.
"""

from django.test import TestCase
from django.test.client import RequestFactory

from dynamicforms.serializers import DynamicModelSerializerMixin, ModelSerializer
from examples.models import Filter, Validated


class _SwitchableSerializer(DynamicModelSerializerMixin, ModelSerializer):
    class Meta:
        model = Validated
        exclude = ()

    def determine_model_at_runtime(self, request):
        return getattr(request, "dynamic_model", None)


class DynamicModelMixinTest(TestCase):
    def test_instance_override_does_not_leak_into_other_instances_or_the_class(self):
        original_model = _SwitchableSerializer.Meta.model

        request_a = RequestFactory().get("/")
        request_a.dynamic_model = Filter
        serializer_a = _SwitchableSerializer(context={"request": request_a})
        self.assertIs(serializer_a.Meta.model, Filter)
        # The class itself must be untouched by instantiating serializer_a.
        self.assertIs(_SwitchableSerializer.Meta.model, original_model)

        # A second instance (simulating a later or concurrent, unrelated request) that resolves no
        # dynamic model at all must fall back to the class default, not inherit serializer_a's Filter.
        request_b = RequestFactory().get("/")
        serializer_b = _SwitchableSerializer(context={"request": request_b})
        self.assertIs(serializer_b.Meta.model, original_model)

        # serializer_a must be unaffected by serializer_b's later construction - this is the actual
        # regression: before the fix, this would now also read `original_model`, not `Filter`.
        self.assertIs(serializer_a.Meta.model, Filter)
