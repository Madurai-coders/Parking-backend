# Generated by Django 3.2.9 on 2021-12-10 07:26

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='BusinessPartner',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uId', models.CharField(max_length=120)),
                ('accountNumber', models.CharField(max_length=120)),
                ('userName', models.CharField(max_length=120)),
                ('lastName', models.CharField(max_length=120)),
                ('email', models.EmailField(max_length=254)),
                ('BusinessPartner_created', models.DateTimeField(auto_now=True)),
                ('accountHolder', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='useraccount', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Wing',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('wingId', models.CharField(max_length=100)),
                ('wingName', models.CharField(max_length=100)),
                ('wingCount', models.IntegerField()),
                ('wingStatus', models.BooleanField()),
                ('planWeekly', models.IntegerField()),
                ('planMonthly', models.IntegerField()),
                ('planQuarterly', models.IntegerField()),
                ('planYearly', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Slots',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slotId', models.CharField(max_length=100)),
                ('slotStatus', models.BooleanField()),
                ('date_auto', models.DateTimeField(auto_now=True)),
                ('wingId', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='slots', to='app.wing')),
            ],
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('paymentId', models.CharField(max_length=120)),
                ('paymentType', models.CharField(max_length=100)),
                ('paymentDate', models.CharField(max_length=100)),
                ('amount', models.IntegerField()),
                ('paymentDateTime_auto', models.DateTimeField(auto_now=True, null=True)),
                ('userId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='payment_partner', to='app.businesspartner')),
            ],
        ),
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bookingId', models.CharField(max_length=120)),
                ('date_auto', models.DateTimeField(auto_now=True)),
                ('date', models.CharField(max_length=120)),
                ('startFrom', models.CharField(max_length=120)),
                ('endTo', models.CharField(max_length=120)),
                ('slotid', models.CharField(max_length=120)),
                ('plan', models.CharField(max_length=120)),
                ('charge', models.CharField(max_length=120)),
                ('slot_connect', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='slots', to='app.slots')),
                ('userId', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='booking_partner', to='app.businesspartner')),
            ],
        ),
    ]
