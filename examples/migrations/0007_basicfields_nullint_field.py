# Generated by Django 2.2.13 on 2020-10-27 12:06

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("examples", "0006_merge_20200921_1152"),
    ]

    operations = [
        migrations.AddField(
            model_name="basicfields",
            name="nullint_field",
            field=models.IntegerField(null=True),
        ),
    ]
