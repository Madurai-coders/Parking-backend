# Generated by Django 3.2.9 on 2022-10-04 10:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0022_paymentendpoint'),
    ]

    operations = [
        migrations.AddField(
            model_name='bookingtemp',
            name='key',
            field=models.CharField(default=1, max_length=120),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='carinfotemp',
            name='key',
            field=models.CharField(default=1, max_length=120),
            preserve_default=False,
        ),
    ]
