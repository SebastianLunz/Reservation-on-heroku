from datetime import time

from django import forms
from django.contrib.auth.models import User
from django.forms import ValidationError

from .models import Service, Reservation


class BaseReservationForm(forms.Form):
    timestamp = forms.DateTimeField()
    service = forms.ModelChoiceField(Service.objects.all())
    employee = forms.ModelChoiceField(User.objects.all())

    def clean_timestamp(self):
        timestamp = self.cleaned_data["timestamp"]
        if (
            timestamp.minute not in (0, 30)
            or timestamp.second != 0
            or timestamp.microsecond != 0
        ):
            raise ValidationError(f"Wprowadzony przedzaił czasu {timestamp} jest nieprawidłowy")
        return timestamp

    def clean(self):
        service = self.cleaned_data.get("service")
        employee = self.cleaned_data.get("employee")
        timestamp = self.cleaned_data.get("timestamp")

        errors = {}

        if service and employee and employee not in service.staff.all():
            errors["employee"] = ValidationError(
                f"Wybrany pracownik {employee} nie może zrealizować tej usługi {service}"
            )

        # sprawdzenie czy są inne rezerwacje w tym czsie
        if timestamp and service and employee:
            if Reservation.objects.filter(
                timestamp__gte=timestamp,
                timestamp__lt=timestamp + service.duration
                # employee=employee,   # only check specific employee's calendar
            ):
                errors["timestamp"] = ValidationError(
                    "Usługa niedostępna w wybranym przedziale czasu. "
                    "Wróć do porzedniej strony i spróbój ponownie"
                )

        # czy slot czasowy poza godzinami pracy zakładu
        if timestamp and service:
            reservation_time = timestamp.time()
            reservation_time_end = (timestamp + service.duration).time()
            if (
                reservation_time < time(10, 00)
                or reservation_time_end > time(19, 00)
            ):
                errors["timestamp"] = ValidationError(
                    "Wybrany przedział czasu poza godzinami pracy - (10:00 - 19:00)"
                )

        if errors:
            raise ValidationError(errors)


class ReservationForm(forms.ModelForm):
    privacy_policy = forms.BooleanField(
        required=True,
        label="I accept the privacy policy.",
        help_text="<a href='/pages/privacy-policy'>Link</a>",
    )
    terms_of_services = forms.BooleanField(
        required=True,
        label="I accept the term of services.",
        help_text="<a href='/pages/privacy-policy'>Link</a>",
    )

    class Meta:
        model = Reservation
        fields = [
            "first_name",
            "last_name",
            "phone",
            "email",
            "privacy_policy",
            "terms_of_services",
        ]
