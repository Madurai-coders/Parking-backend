# Generated by Django 3.2.8 on 2022-05-22 14:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0014_carinfo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='carinfo',
            name='color',
            field=models.CharField(max_length=120),
        ),
    ]
