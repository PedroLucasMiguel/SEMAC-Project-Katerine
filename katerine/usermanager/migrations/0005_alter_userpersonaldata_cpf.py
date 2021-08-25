# Generated by Django 3.2.6 on 2021-08-24 23:07

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usermanager', '0004_auto_20210824_1947'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userpersonaldata',
            name='cpf',
            field=models.CharField(max_length=14, primary_key=True, serialize=False, unique=True, validators=[django.core.validators.MinLengthValidator(14)]),
        ),
    ]
