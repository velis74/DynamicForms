import uuid as uuid_module

from rest_framework import serializers
from django.db import models
from ..fields import *
from ..fields.mixins import UUIDMixIn


class ModelSerializer(UUIDMixIn, serializers.ModelSerializer):
    serializer_field_mapping = {
        models.AutoField: IntegerField,
        models.BigIntegerField: IntegerField,
        models.BooleanField: BooleanField,
        models.CharField: CharField,
        models.CommaSeparatedIntegerField: CharField,
        models.DateField: DateField,
        models.DateTimeField: DateTimeField,
        models.DecimalField: DecimalField,
        models.EmailField: EmailField,
        models.Field: ModelField,
        models.FileField: FileField,
        models.FloatField: FloatField,
        models.ImageField: ImageField,
        models.IntegerField: IntegerField,
        models.NullBooleanField: NullBooleanField,
        models.PositiveIntegerField: IntegerField,
        models.PositiveSmallIntegerField: IntegerField,
        models.SlugField: SlugField,
        models.SmallIntegerField: IntegerField,
        models.TextField: CharField,
        models.TimeField: TimeField,
        models.URLField: URLField,
        models.GenericIPAddressField: IPAddressField,
        models.FilePathField: FilePathField,
    }
    if models.DurationField is not None:
        serializer_field_mapping[models.DurationField] = DurationField
    # TODO: Je treba v fielde spravit tudi vse fielde iz rest_framework/relations.py
    # serializer_related_field = PrimaryKeyRelatedField
    # serializer_related_to_field = SlugRelatedField
    # serializer_url_field = HyperlinkedIdentityField
    serializer_choice_field = ChoiceField

    @property
    def has_non_field_errors(self):
        if hasattr(self, '_errors'):
            return 'non_field_errors' in self.errors
        return False
