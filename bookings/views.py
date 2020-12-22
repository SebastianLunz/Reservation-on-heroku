from datetime import datetime, timedelta, timezone, date

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.http import Http404
from django.shortcuts import render
from django.views.generic import ListView, CreateView, DeleteView, TemplateView
from django.urls import reverse_lazy, reverse

from .forms import BaseReservationForm, ReservationForm
from .models import Service, Reservation


class MainPage(TemplateView):
    template_name = "bookings/main.html"


class IndexView(ListView):
    template_name = "bookings/index.html"
    days_ahead = 1

    def get_queryset(self):
        today = date.today()
        self.date = date(
            self.kwargs.get('year', today.year),
            self.kwargs.get('month', today.month),
            self.kwargs.get('day', today.day),
        )
        if self.date < today:
            raise Http404()

        max_date = self.date + timedelta(days=self.days_ahead)

        return Reservation.objects.filter(
            timestamp__date__gte=self.date,
            timestamp__date__lt=max_date,
            ).order_by(
                "timestamp"
            )

    def get_context_data(self, **kwargs):
        resolution = timedelta(minutes=30)
        start = datetime(
            self.date.year,
            self.date.month,
            self.date.day,
            10, 00, tzinfo=timezone.utc
        )

        dates = {}
        for k in range(0, self.days_ahead):
            base_date = start + timedelta(days=k)
            base_dates = {base_date + i * resolution: False for i in range(18)}
            dates.update(base_dates)

        today = date.today()
        kwargs["dates"] = dates
        kwargs["selected_date"] = self.date
        kwargs["today"] = today
        kwargs["week"] = [
            today + timedelta(days=i)
            for i in range(0, 7)
        ]

        for reservation in self.object_list:
            # czas trwania rezerwacji podzielony przez rozdzielczość
            deltas = int(reservation.duration / resolution)
            for i in range(deltas):
                dates[reservation.timestamp + i * resolution] = True

        # dostępne usługi, dostępni pracownicy
        kwargs["services"] = Service.objects.all()
        kwargs["employees"] = User.objects.exclude(service__isnull=True)

        return super().get_context_data(**kwargs)


class AddReservation(CreateView):
    model = Reservation
    template_name = "bookings/add.html"
    form_class = ReservationForm

    def get(self, request, *args, **kwargs):
        self.form2 = BaseReservationForm(request.GET)
        self.form2.full_clean()
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = None

        form1 = self.get_form()
        self.form2 = BaseReservationForm(request.GET)

        if form1.is_valid() and self.form2.is_valid():
            return self.form_valid(form1, self.form2)
        else:
            print("*" * 20)
            print(self.form2.errors)
            return self.form_invalid(form1)

    def form_valid(self, form1, form2):
        form1.instance.service = form2.cleaned_data['service']
        form1.instance.employee = form2.cleaned_data['employee']
        form1.instance.timestamp = form2.cleaned_data['timestamp']

        form1.instance.duration = form1.instance.service.duration
        form1.instance.price = form1.instance.service.price

        return super().form_valid(form1)

    def get_context_data(self, **kwargs):
        kwargs["form2"] = self.form2
        kwargs["timestamp"] = self.form2.cleaned_data.get('timestamp')
        kwargs["service"] = self.form2.cleaned_data.get('service')
        kwargs["employee"] = self.form2.cleaned_data.get('employee')
        return super().get_context_data(**kwargs)

    def get_success_url(self):
        return reverse("bookings:confirm", args=[self.object.code])


class ConfirmReservation(DeleteView):
    model = Reservation
    slug_url_kwarg = "code"
    slug_field = "code"
    template_name = "bookings/confirm.html"


class CalendarView(LoginRequiredMixin, ListView):
    template_name = "bookings/calendar.html"

    def get_queryset(self):
        qs = Reservation.objects.order_by("-timestamp")

        if not self.request.user.is_superuser:
            qs = qs.filter(employee=self.request.user)

        return qs
