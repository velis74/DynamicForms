# Generated by Django 2.2.13 on 2021-03-12 11:46

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("examples", "0008_auto_20210303_0904"),
    ]

    operations = [
        migrations.AddField(
            model_name="advancedfields",
            name="single_choice_field",
            field=models.CharField(max_length=8, null=True),
        ),
    ]
