# Generated by Django 3.1.3 on 2020-12-05 14:25

import datetime
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
            name='Service',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=80)),
                ('description', models.CharField(max_length=200)),
                ('duration', models.DurationField(default=datetime.timedelta(seconds=3600))),
                ('price', models.PositiveIntegerField(default=15)),
                ('staff', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Reservation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=20)),
                ('last_name', models.CharField(max_length=40)),
                ('phone', models.CharField(max_length=15)),
                ('email', models.EmailField(max_length=254)),
                ('timestamp', models.DateTimeField()),
                ('duration', models.DurationField(default=datetime.timedelta(seconds=3600))),
                ('price', models.PositiveIntegerField(default=15)),
                ('status', models.CharField(choices=[('pending', 'Oczekująca'), ('accepted', 'Potwierdzona'), ('cancelled', 'Anulowana'), ('finished', 'Zakończona')], max_length=20)),
                ('privacy_policy', models.BooleanField(default=False, verbose_name="I accept the <a href='/pages/privacy-policy'>privacy policy</a>")),
                ('terms_of_services', models.BooleanField(default=False, verbose_name="I accept the <a href='/pages/terms-of-services'>terms of services</a>")),
                ('code', models.CharField(max_length=10, verbose_name='Reservation code')),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
                ('service', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='bookings.service')),
            ],
        ),
    ]
