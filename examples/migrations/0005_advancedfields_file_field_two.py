# Generated by Django 3.0.10 on 2020-09-15 07:07

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("examples", "0004_basicfields_password_field"),
    ]

    operations = [
        migrations.AddField(
            model_name="advancedfields",
            name="file_field_two",
            field=models.FileField(blank=True, null=True, upload_to="examples2/"),
        ),
    ]
