# Generated by Django 3.2.6 on 2021-08-24 15:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usermanager', '0002_alter_userpersonaldata_full_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userpersonaldata',
            name='full_name',
            field=models.CharField(max_length=128),
        ),
    ]
