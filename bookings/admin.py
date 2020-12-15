from django.contrib import admin

from .models import Service, Reservation


class ServiceAdmin(admin.ModelAdmin):
    list_display = ["name", "duration", "price"]
    list_filter = ["name", "duration", "price"]
    search_fields = ["name", "description", "duration", "price"]


class ReservationAdmin(admin.ModelAdmin):
    list_display = [
        "code",
        "first_name",
        "last_name",
        "email",
        "phone",
        "service",
        "employee",
        "timestamp",
        "status",
    ]
    list_filter = ["service", "employee", "timestamp", "status", "duration"]
    search_fields = [
        "first_name",
        "last_name",
        "phone",
        "email",
        "service__name",
        "service__description",
        "employee__firstname",
        "employee__lastname",
        "timestamp",
        "code",
        "status",
    ]
    autocomplete_fields = ["service", "employee"]


admin.site.register(Service, ServiceAdmin)
admin.site.register(Reservation, ReservationAdmin)
