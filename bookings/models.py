from django.db import models
from django.contrib.auth.models import User
from datetime import timedelta
import string
import random

# Create your models here.


class Service(models.Model):
    name = models.CharField(max_length=80)
    description = models.CharField(max_length=200)
    duration = models.DurationField(default=timedelta(hours=1))
    price = models.PositiveIntegerField(default=15)
    staff = models.ManyToManyField(User)

    def __str__(self):
        return self.name


class Reservation(models.Model):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=40)
    phone = models.CharField(max_length=15)
    email = models.EmailField()
    service = models.ForeignKey(Service, on_delete=models.PROTECT)
    employee = models.ForeignKey(User, on_delete=models.PROTECT)
    timestamp = models.DateTimeField()
    duration = models.DurationField(default=timedelta(hours=1))
    price = models.PositiveIntegerField(default=15)
    STATUS_CHOICES = [
        ("pending", "Oczekująca"),
        ("accepted", "Potwierdzona"),
        ("cancelled", "Anulowana"),
        ("finished", "Zakończona"),
    ]
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=STATUS_CHOICES[0][0],
    )
    privacy_policy = models.BooleanField(
        default=False,
        blank=False,
        verbose_name="I accept the <a href='/pages/privacy-policy'>privacy policy</a>",
    )
    terms_of_services = models.BooleanField(
        default=False,
        blank=False,
        verbose_name="I accept the <a href='/pages/terms-of-services'>terms of services</a>",
    )
    code = models.CharField(max_length=10, verbose_name="Reservation code", blank=True)

    def save(self, *args, **kwargs):
        if self.code.strip() == "":
            self.code = "".join(
                random.sample(string.ascii_lowercase + string.digits, 10)
            )

        return super().save(*args, **kwargs)

    def __str__(self):
        return (
            f"{self.service} {self.code} {self.status} "
            f"{self.first_name} {self.last_name}"
        )
