# Generated by Django 2.1.4 on 2019-02-02 15:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('examples', '0006_auto_20190103_1442'),
    ]

    operations = [
        migrations.CreateModel(
            name='RefreshType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(help_text='Item description', max_length=20)),
            ],
        ),
    ]
