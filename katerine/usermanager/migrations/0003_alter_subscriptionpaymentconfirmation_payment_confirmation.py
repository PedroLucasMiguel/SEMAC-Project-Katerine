# Generated by Django 3.2.6 on 2021-08-27 19:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usermanager', '0002_alter_subscriptionpaymentconfirmation_payment_confirmation'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subscriptionpaymentconfirmation',
            name='payment_confirmation',
            field=models.ImageField(upload_to=''),
        ),
    ]
