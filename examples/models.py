from django.db import models
from django.core.validators import RegexValidator, MaxValueValidator, MinValueValidator


# Create your models here.
class Validated(models.Model):
    code = models.CharField(max_length=10, validators=[
        RegexValidator(r'\w\w\d+', 'Please enter a string starting with two characters, followed by up to 8 numbers')
    ])
    enabled = models.BooleanField()
    amount = models.IntegerField(null=True, blank=True, validators=[
        # This one should be interesting: will a blank value pass the Min validator? It should!
        MinValueValidator(5),
        MaxValueValidator(10)
    ])  # Bit mask. 1=apartment_number, ..., 32=delay
    item_type = models.IntegerField(choices=(
        (0, 'Choice 1'),
        (1, 'Choice 2'),
        (2, 'Choice 3'),
        (3, 'Choice 4'),
    ))
    item_flags = models.CharField(max_length=4, blank=True, choices=(
        # this one will be a multi-choice field so you will need to override it in form
        ('A', 'A'),
        ('B', 'B'),
        ('C', 'C'),
        ('D', 'D'),
    ), validators=[
        RegexValidator(r'[ABC]*', 'Only options A-C may be chosen')
    ])
