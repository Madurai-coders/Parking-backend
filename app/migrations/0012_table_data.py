# Generated by Django 3.2.9 on 2022-03-28 09:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0011_wing_plandaily'),
    ]

    operations = [
        migrations.CreateModel(
            name='Table_data',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('table_name', models.CharField(max_length=120)),
                ('table_data', models.CharField(max_length=120)),
            ],
        ),
    ]
