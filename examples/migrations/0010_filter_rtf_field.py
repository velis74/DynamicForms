# Generated by Django 3.1.12 on 2021-11-09 07:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('examples', '0009_auto_20210929_1136'),
    ]

    operations = [
        migrations.AddField(
            model_name='filter',
            name='rtf_field',
            field=models.TextField(blank=True, help_text='RTF Field', null=True, verbose_name='RTF Field'),
        ),
    ]
