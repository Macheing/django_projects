# Generated by Django 3.2.4 on 2021-07-16 10:02

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('autos', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auto',
            name='nickname',
            field=models.CharField(help_text='Enter Brand name of a car (e.g toyota hilux)', max_length=200, validators=[django.core.validators.MinLengthValidator(2, 'Nickname must be greater than 1 character')]),
        ),
        migrations.AlterField(
            model_name='make',
            name='name',
            field=models.CharField(help_text='Enter a Maker or Manufacturer (e.g. Dodge)', max_length=200, validators=[django.core.validators.MinLengthValidator(2, 'Make must be greater than 1 character')]),
        ),
    ]