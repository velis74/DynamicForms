import datetime

from datetime import time
from enum import IntEnum

from django.core.validators import MaxValueValidator, MinValueValidator, RegexValidator
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from enumfields import EnumIntegerField

from dynamicforms import models_fields
from dynamicforms.int_choice_enum import IntChoiceEnum


class Validated(models.Model):
    """
    Shows validation capabilities
    """

    class ItemTypeChoices(IntChoiceEnum):
        Choice_1 = 0, _("Choice 1"), "airplane"
        Choice_2 = 1, _("Choice 2"), "paper-plane"
        Choice_3 = 2, _("Choice 3"), "planet"
        Choice_4 = 3, _("Choice 4")

    code = models.CharField(
        max_length=10,
        validators=[
            RegexValidator(
                r"\w\w\d+", "Please enter a string starting with two characters, followed by up to 8 numbers"
            )
        ],
    )
    enabled = models.BooleanField()
    amount = models.IntegerField(
        null=True,
        blank=True,
        validators=[
            # This one should be interesting: will a blank value pass the Min validator? It should!
            MinValueValidator(5),
            MaxValueValidator(10),
        ],
    )  # Bit mask. 1=apartment_number, ..., 32=delay
    item_type = models_fields.IntegerChoiceMigrationIgnoreField(choices=ItemTypeChoices.get_choices_tuple())
    item_flags = models.CharField(
        max_length=4,
        blank=True,
        choices=(
            # this one will be a multi-choice field so you will need to override it in form
            ("A", "Alpha"),
            ("B", "Beta"),
            ("C", "Gamma"),
            ("D", "Delta"),
        ),
        validators=[RegexValidator(r"^[ABC]*$", "Only options A-C may be chosen", "regex")],
    )
    comment = models.TextField(null=True, blank=True)


class HiddenFields(models.Model):
    """
    Shows dynamically changing field visibility
    """

    note = models.CharField(max_length=20, help_text="Enter abc to hide unit field")
    unit = models.CharField(
        max_length=10,
        choices=(
            (None, "No additional data"),
            ("pcs", "Pieces"),
            ("wt", "Weight"),
            ("cst", "Custom"),
        ),
        null=True,
        blank=True,
    )
    int_fld = models.IntegerField(verbose_name="Quantity", null=True, blank=True)
    qty_fld = models.FloatField(
        verbose_name="Weight", null=True, blank=True, help_text="Feel free to use a decimal point / comma"
    )
    cst_fld = models.CharField(
        max_length=80, verbose_name="Comment", null=True, blank=True, help_text="Enter additional info here"
    )
    additional_text = models.CharField(
        max_length=80, null=True, blank=True, help_text="Now that you have shown me, please enter something"
    )


class PageLoad(models.Model):
    """
    Shows how DynamicForms handles dynamic loading of many records in ViewSet result
    """

    description = models.CharField(max_length=20, help_text="Item description")
    choice = models.IntegerField(
        choices=(
            (1, "Choice 1"),
            (2, "Choice 2"),
            (3, "Choice 3"),
            (4, "Choice 4"),
        ),
        null=False,
        blank=False,
        default=1,
    )


class Filter(models.Model):
    """
    Shows how DynamicForms handles filers
    """

    char_field = models.CharField(max_length=20, help_text="Char field", verbose_name="Char field")
    datetime_field = models.DateTimeField(help_text="Datetime field", verbose_name="Datetime field")
    int_field = models.IntegerField(help_text="Integer field", verbose_name="Integer field")
    int_choice_field = models.IntegerField(
        choices=(
            (0, "Choice 1"),
            (1, "Choice 2"),
            (2, "Choice 3"),
            (3, "Choice 4"),
        ),
        help_text="Integer field with choices",
        verbose_name="Integer field with choices",
    )
    bool_field = models.BooleanField(help_text="Boolean field", verbose_name="Boolean field")
    name = models.CharField(max_length=20, help_text="Name field", verbose_name="Name field", null=True, blank=True)
    rtf_field = models.TextField(help_text="RTF Field", verbose_name="RTF Field", null=True, blank=True)


class BasicFields(models.Model):
    """
    Shows basic available fields in DynamicForms
    """

    boolean_field = models.BooleanField(null=False, default=False)
    nullboolean_field = models.BooleanField(null=True, blank=True)
    char_field = models.CharField(null=True, max_length=32)
    email_field = models.EmailField(null=True)
    slug_field = models.SlugField(null=True)
    url_field = models.URLField(null=True)
    uuid_field = models.UUIDField(null=True)
    ipaddress_field = models.GenericIPAddressField(null=True)
    integer_field = models.IntegerField(null=True)
    nullint_field = models.IntegerField(null=True, blank=True)
    float_field = models.FloatField(null=True)
    decimal_field = models.DecimalField(null=True, max_digits=5, decimal_places=2)
    datetime_field = models.DateTimeField(null=True)
    date_field = models.DateField(null=True)
    time_field = models.TimeField(null=True)
    duration_field = models.DurationField(null=True)
    password_field = models.CharField(null=True, max_length=32)


class Relation(models.Model):
    """
    Model related to AdvancedFields model
    """

    name = models.CharField(max_length=16)

    def __str__(self):
        return self.name


class EnumFieldChoices(IntChoiceEnum):
    Choice_1 = 0, _("Airplane"), "airplane"
    Choice_2 = 1, _("Paper plane"), "paper-plane"
    Choice_3 = 2, _("Planet"), "planet"
    Choice_4 = 3, _("Iconless")


class AdvancedFields(models.Model):
    """
    Shows advanced available fields in DynamicForms
    """

    regex_field = models.CharField(max_length=256)
    choice_field = models.CharField(null=True, max_length=8)
    single_choice_field = models.CharField(null=True, max_length=8)
    multiplechoice_field = models.CharField(null=True, max_length=8)
    filepath_field = models.FilePathField(null=True)
    file_field = models.FileField(upload_to="examples/", null=True, blank=True)
    file_field_two = models.FileField(upload_to="examples2/", null=True, blank=True)
    image_field = models.ImageField(upload_to="examples/", null=True, blank=True)
    color_field = models_fields.ColorField(null=True)
    enum_choice_field = models_fields.EnumChoiceField(EnumFieldChoices, null=True)

    # Model attribute for ReadOnlyField
    hidden_field = models.DateTimeField(default=timezone.now)

    @property
    def readonly_field(self):
        return self.hidden_field > timezone.now() - timezone.timedelta(days=1) if self.hidden_field else False

    """ListField and DictField not supported in HTML forms in DRF"""
    # list_field = models.?
    # dict_field = models.?

    """JSONField available only for PostgreSQL"""
    # json_field = models.JSONField()

    # serializer_method_field = models.?
    # model_field = models.?

    # Relations
    # string_related_field, which is always read_only is defined only in serializer
    # and primary_key_related_field is defined as its source
    primary_key_related_field = models.OneToOneField(
        Relation, on_delete=models.CASCADE, null=True, related_name="primary"
    )
    slug_related_field = models.ForeignKey(Relation, on_delete=models.CASCADE, null=True, related_name="slug")
    hyperlinked_related_field = models.ManyToManyField(Relation, related_name="hyper_related")
    hyperlinked_identity_field = models.ForeignKey(
        Relation, on_delete=models.CASCADE, null=True, related_name="hyper_identity"
    )

    def __str__(self):
        return "Advanced field {self.id}".format(**locals())


class RefreshType(models.Model):
    """
    Shows how DynamicForms handles different refresh types
    """

    description = models.CharField(max_length=20, help_text="Item description")
    rich_text_field = models.TextField(blank=True, null=True)


class Document(models.Model):
    description = models.CharField(max_length=30, help_text="Document description")
    file = models.FileField(upload_to="documents/", blank=False)


class CalendarRecurrence(models.Model):
    from .recurrence_utils import date_range as dr_func, Pattern

    start_at = models.DateTimeField(verbose_name=_("Recurrence start"), null=False, blank=False)
    end_at = models.DateTimeField(verbose_name=_("Recurrence end"), null=False, blank=False)
    pattern = EnumIntegerField(Pattern, verbose_name=_("Pattern"), null=False, blank=False)
    recur = models.JSONField(verbose_name=_("Recur parameters"), null=False, blank=False)

    def date_range(self, cutoff_at: datetime.datetime):
        recur = self.recur
        if self.pattern == CalendarRecurrence.Pattern.Weekly:
            recur = dict(self.recur)
            recur["holidays"] = self.get_holidays()
        return CalendarRecurrence.dr_func(self.start_at, self.end_at, cutoff_at, self.pattern, recur)

    def get_holidays(self):
        # not implemented yet
        return set()


class CalendarEvent(models.Model):
    title = models.CharField(max_length=80, verbose_name=_("Title"), null=False, blank=False)
    description = models.TextField(verbose_name=_("Description"), null=True, blank=True)
    colour = models.IntegerField(verbose_name="Colour", null=True, blank=True)
    start_at = models.DateTimeField(verbose_name=_("Start"), null=False, blank=False)
    end_at = models.DateTimeField(verbose_name=_("End"), null=False, blank=False)
    recurrence = models.ForeignKey(
        CalendarRecurrence,
        verbose_name=_("Recurrence"),
        on_delete=models.PROTECT,
        related_name="events",
        null=True,
        blank=True,
    )

    @property
    def all_day(self):
        return self.start_at.time() == 0 and self.end_at.time == time(23, 59, 59, 999999)

    class Meta:
        indexes = [models.Index(fields=("recurrence", "start_at"))]


class CalendarReminder(models.Model):
    class RType(IntEnum):
        Notification = 1
        Email = 2

    class Unit(IntEnum):
        Seconds = 1
        Minutes = 2
        Hours = 3
        Days = 4
        Weeks = 5

    REMINDER_TYPE_CHOICES = [(m.value, m.name) for m in RType]
    UNIT_CHOICES = [(m.value, m.name) for m in Unit]

    event = models.ForeignKey(CalendarEvent, on_delete=models.CASCADE, related_name="reminders")
    type = models.IntegerField(verbose_name=_("Type"), choices=REMINDER_TYPE_CHOICES, null=False, blank=False)
    quantity = models.IntegerField(verbose_name=_("Quantity"), null=False, blank=False)
    unit = models.IntegerField(verbose_name=_("Unit"), choices=UNIT_CHOICES, null=False, blank=False)
