# Generated by Django 3.2.8 on 2022-05-31 06:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0015_alter_carinfo_color'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='booking',
            options={'ordering': ['date_auto']},
        ),
    ]
